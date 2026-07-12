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
    assert refreshed_run["task"]["status"] == "in_progress"
    assert refreshed_plan["task"]["status"] == "in_progress"
    assert refreshed_writing["task"]["status"] == "in_progress"
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
    assert len(broker.messages) == 1
    assert broker.messages[0][0].actor_name == "extract_knowledge"
    assert refreshed_run["task"]["status"] == "in_progress"
    assert refreshed_run["current_stage"] == "source_submission"
