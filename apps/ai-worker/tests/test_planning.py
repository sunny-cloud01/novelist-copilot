from worker.core_store import load_phase_two_store
from worker.main import create_chapter_plan, create_section_plans, extract_knowledge, noop_task
from worker.planning import (
    CHAPTER_PLAN_ID,
    CHAPTER_PLAN_TASK_ID,
    PLANNING_STAGES,
    PROJECT_ID,
    SECTION_PLAN_TASK_ID,
    build_chapter_plan_fixture,
    build_create_chapter_plan_command,
    build_create_section_plans_command,
    build_section_plan_fixture,
    run_create_chapter_plan,
    run_create_section_plans,
)


def load_phase_two_store_module():
    return load_phase_two_store()


def dispatch_task(store, task_id: str, trace_id: str) -> str:
    task = store.mark_task_dispatched(task_id, trace_id=trace_id)
    assert task is not None
    assert task["current_dispatch_token"] is not None
    return task["current_dispatch_token"]


def test_build_chapter_plan_fixture_matches_contract_shape() -> None:
    command = build_create_chapter_plan_command()

    fixture = build_chapter_plan_fixture(command)

    assert fixture["chapter_plan"]["chapter_plan_id"] == CHAPTER_PLAN_ID
    assert fixture["chapter_plan"]["project_id"] == PROJECT_ID
    assert fixture["chapter_plan"]["status"] == "requires_review"
    assert fixture["events"][1]["payload_json"]["planning_stages"] == PLANNING_STAGES


def test_run_create_chapter_plan_returns_requires_review_result() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created = store.create_chapter_plan(
        {"project_id": PROJECT_ID, "chapter_index": 9, "target_word_count": 4200, "payload": {}},
        trace_id="trace-plan-worker",
    )
    assert created is not None
    dispatch_token = dispatch_task(store, created["task"]["task_id"], trace_id="trace-plan-worker")
    command = {
        **build_create_chapter_plan_command(
            project_id=PROJECT_ID,
            chapter_plan_id=created["chapter_plan"]["chapter_plan_id"],
            task_id=created["task"]["task_id"],
            trace_id="trace-plan-worker",
            dispatch_token=dispatch_token,
        ),
        "chapter_index": 9,
        "target_word_count": 4200,
    }

    result = run_create_chapter_plan(command)
    refreshed = load_phase_two_store_module().get_chapter_plan(created["chapter_plan"]["chapter_plan_id"])

    assert result["task_id"] == created["task"]["task_id"]
    assert result["status"] == "requires_review"
    assert result["trace_id"] == "trace-plan-worker"
    assert result["metrics"]["current_stage"] == "quality_review"
    assert refreshed["task"]["status"] == "requires_review"
    assert refreshed["chapter_plan"]["payload"]["current_stage"] == "quality_review"
    assert refreshed["events"][-1]["event_type"] == "review_required"


def test_run_create_chapter_plan_keeps_running_on_stale_dispatch_token() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created = store.create_chapter_plan(
        {"project_id": PROJECT_ID, "chapter_index": 10, "target_word_count": 3600, "payload": {}},
        trace_id="trace-plan-stale",
    )
    first_token = dispatch_task(store, created["task"]["task_id"], trace_id="trace-plan-stale")
    store.schedule_task_retry(created["task"]["task_id"], "lease_expired", trace_id="trace-plan-stale")
    fresh_token = store.mark_task_dispatched(
        created["task"]["task_id"],
        trace_id="trace-plan-stale",
    )["current_dispatch_token"]
    command = {
        **build_create_chapter_plan_command(
            project_id=PROJECT_ID,
            chapter_plan_id=created["chapter_plan"]["chapter_plan_id"],
            task_id=created["task"]["task_id"],
            trace_id="trace-plan-stale",
            dispatch_token=first_token,
        ),
        "chapter_index": 10,
        "target_word_count": 3600,
    }

    result = run_create_chapter_plan(command)
    refreshed = load_phase_two_store_module().get_chapter_plan(created["chapter_plan"]["chapter_plan_id"])

    assert first_token != fresh_token
    assert result["status"] == "running"
    assert refreshed["task"]["status"] == "running"
    assert refreshed["task"]["current_dispatch_token"] == fresh_token
    assert all(event["event_type"] not in {"review_required", "succeeded", "failed"} for event in refreshed["events"][-2:])


def test_build_section_plan_fixture_matches_contract_shape() -> None:
    command = build_create_section_plans_command()

    fixture = build_section_plan_fixture(command)

    assert fixture["chapter_plan_id"] == CHAPTER_PLAN_ID
    assert len(fixture["items"]) == 3
    assert fixture["items"][0]["planning_role"] == "setup"
    assert fixture["events"][1]["payload_json"]["planning_stages"] == PLANNING_STAGES


def test_run_create_section_plans_returns_succeeded_result() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": PROJECT_ID, "chapter_index": 3, "target_word_count": 2800, "payload": {}},
        trace_id="trace-section-worker-plan",
    )
    assert created_plan is not None
    created_sections = store.create_section_plans(
        created_plan["chapter_plan"]["chapter_plan_id"],
        section_count=3,
        trace_id="trace-section-worker",
    )
    assert created_sections is not None
    task = store.STORE.section_plan_tasks[created_plan["chapter_plan"]["chapter_plan_id"]]
    task["status"] = "queued"
    task["progress"] = 0
    task["started_at"] = None
    task["finished_at"] = None
    dispatch_token = dispatch_task(store, created_sections["task"]["task_id"], trace_id="trace-section-worker")
    command = build_create_section_plans_command(
        chapter_plan_id=created_plan["chapter_plan"]["chapter_plan_id"],
        task_id=created_sections["task"]["task_id"],
        trace_id="trace-section-worker",
        dispatch_token=dispatch_token,
    )

    result = run_create_section_plans(command)
    refreshed = load_phase_two_store_module().list_section_plans(created_plan["chapter_plan"]["chapter_plan_id"])

    assert result["task_id"] == created_sections["task"]["task_id"]
    assert result["status"] == "succeeded"
    assert result["trace_id"] == "trace-section-worker"
    assert result["metrics"]["section_count"] == 3
    assert refreshed["task"]["status"] == "succeeded"
    assert refreshed["events"][-1]["event_type"] == "succeeded"


def test_run_create_section_plans_keeps_running_on_stale_dispatch_token() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": PROJECT_ID, "chapter_index": 4, "target_word_count": 2800, "payload": {}},
        trace_id="trace-section-stale-plan",
    )
    created_sections = store.create_section_plans(
        created_plan["chapter_plan"]["chapter_plan_id"],
        section_count=3,
        trace_id="trace-section-stale",
    )
    task = store.STORE.section_plan_tasks[created_plan["chapter_plan"]["chapter_plan_id"]]
    task["status"] = "queued"
    task["progress"] = 0
    task["started_at"] = None
    task["finished_at"] = None
    first_token = dispatch_task(store, created_sections["task"]["task_id"], trace_id="trace-section-stale")
    store.schedule_task_retry(created_sections["task"]["task_id"], "lease_expired", trace_id="trace-section-stale")
    fresh_token = store.mark_task_dispatched(
        created_sections["task"]["task_id"],
        trace_id="trace-section-stale",
    )["current_dispatch_token"]
    command = build_create_section_plans_command(
        chapter_plan_id=created_plan["chapter_plan"]["chapter_plan_id"],
        task_id=created_sections["task"]["task_id"],
        trace_id="trace-section-stale",
        dispatch_token=first_token,
    )

    result = run_create_section_plans(command)
    refreshed = load_phase_two_store_module().list_section_plans(created_plan["chapter_plan"]["chapter_plan_id"])

    assert first_token != fresh_token
    assert result["status"] == "running"
    assert refreshed["task"]["status"] == "running"
    assert refreshed["task"]["current_dispatch_token"] == fresh_token
    assert all(event["event_type"] not in {"review_required", "succeeded", "failed"} for event in refreshed["events"][-2:])


def test_planning_actor_names_are_stable() -> None:
    assert create_chapter_plan.actor_name == "create_chapter_plan"
    assert create_section_plans.actor_name == "create_section_plans"


def test_planning_actors_use_planning_queue() -> None:
    assert create_chapter_plan.queue_name == "task-planning"
    assert create_section_plans.queue_name == "task-planning"


def test_existing_actor_names_remain_stable() -> None:
    assert extract_knowledge.actor_name == "extract_knowledge"
    assert noop_task.actor_name == "noop_task"
