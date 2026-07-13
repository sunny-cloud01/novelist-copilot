from datetime import datetime, timezone

from scheduler.core_store import load_phase_two_store
from scheduler.main import run_scheduler_tick


class StubBroker:
    def __init__(self) -> None:
        self.messages = []

    def enqueue(self, message, *, delay=None):
        self.messages.append((message, delay))
        return message


def load_phase_two_store_module():
    return load_phase_two_store()


def test_scheduler_tick_returns_expected_counters() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_book = store.create_book(
        {"title": "Scheduler Extraction Book", "author_name": "demo", "source_type": "reference_novel"},
        trace_id="trace-scheduler-book",
    )
    created_run = store.create_extraction_run(created_book["book_id"], trace_id="trace-scheduler-extraction")
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 8, "target_word_count": 3600, "payload": {}},
        trace_id="trace-scheduler-plan",
    )
    assert created_plan is not None
    created_sections = store.create_section_plans(
        created_plan["chapter_plan"]["chapter_plan_id"],
        section_count=3,
        trace_id="trace-scheduler-sections",
    )
    assert created_sections is not None
    created_writing = store.create_writing_run(
        {"project_id": store.PROJECT_ID, "chapter_plan_id": created_plan["chapter_plan"]["chapter_plan_id"]},
        trace_id="trace-scheduler-writing",
    )
    assert created_writing is not None
    broker = StubBroker()

    result = run_scheduler_tick(datetime(2026, 7, 11, tzinfo=timezone.utc), broker=broker)
    refreshed_store = load_phase_two_store_module()
    refreshed_run = refreshed_store.get_extraction_run(created_run["run_id"])
    refreshed_plan = refreshed_store.get_chapter_plan(created_plan["chapter_plan"]["chapter_plan_id"])
    refreshed_writing = refreshed_store.get_writing_run(created_writing["writing_run"]["writing_run_id"])

    assert result.requeued == 3
    assert result.expired_leases == 0
    assert result.due_retries == 0
    assert result.ran_at == "2026-07-11T00:00:00+00:00"
    assert len(broker.messages) == 3
    assert {message.actor_name for message, _ in broker.messages} == {"extract_knowledge", "create_chapter_plan", "create_writing_run"}
    extraction_message = next(message for message, _ in broker.messages if message.actor_name == "extract_knowledge")
    assert extraction_message.args[0]["input_refs"] == [
        f"object://source-books/{created_book['book_id']}",
        f"object://extraction-runs/{created_run['run_id']}",
    ]
    assert refreshed_run["task"]["status"] == "running"
    assert refreshed_run["task"]["lease_owner"] == "scheduler"
    assert refreshed_run["task"]["heartbeat_at"] == "2026-07-11T00:00:00+00:00"
    assert refreshed_plan["task"]["status"] == "running"
    assert refreshed_writing["task"]["status"] == "running"
    assert refreshed_store.list_runtime_tasks("queued") == []



def test_scheduler_tick_requeues_requested_reextract() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    store.apply_review_action("01JZOBJ0000000000000000001", "request_reextract", trace_id="trace-reextract")
    broker = StubBroker()

    result = run_scheduler_tick(datetime(2026, 7, 12, tzinfo=timezone.utc), broker=broker)
    refreshed_store = load_phase_two_store_module()
    refreshed_run = refreshed_store.get_extraction_run(store.RUN_ID)

    assert result.requeued == 1
    assert result.expired_leases == 0
    assert result.due_retries == 0
    assert len(broker.messages) == 1
    assert broker.messages[0][0].actor_name == "extract_knowledge"
    assert refreshed_run["task"]["status"] == "running"
    assert refreshed_run["task"]["lease_owner"] == "scheduler"
    assert refreshed_run["current_stage"] == "source_submission"



def test_scheduler_tick_recovers_expired_running_task_to_retrying() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 9, "target_word_count": 3600, "payload": {}},
        trace_id="trace-expired-plan",
    )
    task = store.STORE.chapter_plan_tasks[created_plan["chapter_plan"]["chapter_plan_id"]]
    task["status"] = "running"
    task["lease_owner"] = "worker-1"
    task["lease_expires_at"] = "2026-07-11T00:00:00+00:00"
    task["heartbeat_at"] = "2026-07-11T00:00:00+00:00"
    task["retry_count"] = 0
    task["max_retry_count"] = 3
    store._persist_store()
    broker = StubBroker()

    result = run_scheduler_tick(datetime(2026, 7, 12, tzinfo=timezone.utc), broker=broker)
    refreshed_task = load_phase_two_store_module().get_chapter_plan(created_plan["chapter_plan"]["chapter_plan_id"])["task"]

    assert result.expired_leases == 1
    assert result.due_retries == 1
    assert result.requeued == 1
    assert len(broker.messages) == 1
    assert refreshed_task["status"] == "running"
    assert refreshed_task["retry_count"] == 1
    assert refreshed_task["lease_owner"] == "scheduler"
    assert refreshed_task["next_retry_at"] is None





def test_scheduler_tick_skips_duplicate_dispatch_for_running_task() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 10, "target_word_count": 3600, "payload": {}},
        trace_id="trace-duplicate-dispatch",
    )
    assert created_plan is not None
    broker = StubBroker()

    first = run_scheduler_tick(datetime(2026, 7, 12, tzinfo=timezone.utc), broker=broker)
    second = run_scheduler_tick(datetime(2026, 7, 12, tzinfo=timezone.utc), broker=broker)
    refreshed = load_phase_two_store_module().get_chapter_plan(created_plan["chapter_plan"]["chapter_plan_id"])
    dispatched_events = [event for event in refreshed["events"] if event["event_type"] == "dispatched"]

    assert first.requeued == 1
    assert second.requeued == 0
    assert len(broker.messages) == 1
    assert refreshed["task"]["status"] == "running"
    assert len(dispatched_events) == 1


def test_apply_task_execution_result_rejects_stale_dispatch_token() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 11, "target_word_count": 3600, "payload": {}},
        trace_id="trace-stale-completion",
    )
    assert created_plan is not None
    task_id = created_plan["task"]["task_id"]
    first_dispatch = store.mark_task_dispatched(task_id, trace_id="trace-stale-completion", dispatched_at="2026-07-12T00:00:00+00:00")
    assert first_dispatch is not None
    stale_token = first_dispatch["current_dispatch_token"]
    store.schedule_task_retry(task_id, "lease_expired", trace_id="trace-stale-completion", retry_at="2026-07-12T00:01:00+00:00")
    second_dispatch = store.mark_task_dispatched(task_id, trace_id="trace-stale-completion", dispatched_at="2026-07-12T00:02:00+00:00")
    assert second_dispatch is not None
    fresh_token = second_dispatch["current_dispatch_token"]
    assert stale_token != fresh_token

    stale_result = store.apply_task_execution_result(
        task_id,
        "requires_review",
        [f"object://chapter-plans/{created_plan['chapter_plan']['chapter_plan_id']}"],
        {"planning_stages": [], "current_stage": "quality_review"},
        trace_id="trace-stale-completion",
        dispatch_token=stale_token,
    )
    current = store.get_chapter_plan(created_plan["chapter_plan"]["chapter_plan_id"])

    assert stale_result is not None
    assert current is not None
    assert current["task"]["status"] == "running"
    assert current["task"]["current_dispatch_token"] == fresh_token


def test_scheduler_tick_marks_retry_exhausted_chapter_plan_failed() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 12, "target_word_count": 3600, "payload": {}},
        trace_id="trace-retry-exhausted",
    )
    assert created_plan is not None
    task = store.STORE.chapter_plan_tasks[created_plan["chapter_plan"]["chapter_plan_id"]]
    task["status"] = "running"
    task["lease_owner"] = "worker-1"
    task["lease_expires_at"] = "2026-07-11T00:00:00+00:00"
    task["heartbeat_at"] = "2026-07-11T00:00:00+00:00"
    task["retry_count"] = task["max_retry_count"]
    store._persist_store()
    broker = StubBroker()

    result = run_scheduler_tick(datetime(2026, 7, 12, tzinfo=timezone.utc), broker=broker)
    refreshed_task = load_phase_two_store_module().get_chapter_plan(created_plan["chapter_plan"]["chapter_plan_id"])["task"]

    assert result.expired_leases == 1
    assert result.due_retries == 0
    assert result.requeued == 0
    assert len(broker.messages) == 0
    assert refreshed_task["status"] == "failed"
    assert refreshed_task["lease_owner"] is None

