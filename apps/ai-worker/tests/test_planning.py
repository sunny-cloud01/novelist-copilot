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


def test_build_chapter_plan_fixture_matches_contract_shape() -> None:
    command = build_create_chapter_plan_command()

    fixture = build_chapter_plan_fixture(command)

    assert fixture["chapter_plan"]["chapter_plan_id"] == CHAPTER_PLAN_ID
    assert fixture["chapter_plan"]["project_id"] == PROJECT_ID
    assert fixture["chapter_plan"]["status"] == "requires_review"
    assert fixture["events"][1]["payload_json"]["planning_stages"] == PLANNING_STAGES


def test_run_create_chapter_plan_returns_requires_review_result() -> None:
    command = build_create_chapter_plan_command(trace_id="trace-plan-worker")

    result = run_create_chapter_plan(command)

    assert result["task_id"] == CHAPTER_PLAN_TASK_ID
    assert result["status"] == "requires_review"
    assert result["trace_id"] == "trace-plan-worker"
    assert result["metrics"]["current_stage"] == "quality_review"


def test_build_section_plan_fixture_matches_contract_shape() -> None:
    command = build_create_section_plans_command()

    fixture = build_section_plan_fixture(command)

    assert fixture["chapter_plan_id"] == CHAPTER_PLAN_ID
    assert len(fixture["items"]) == 3
    assert fixture["items"][0]["planning_role"] == "setup"
    assert fixture["events"][1]["payload_json"]["planning_stages"] == PLANNING_STAGES


def test_run_create_section_plans_returns_succeeded_result() -> None:
    command = build_create_section_plans_command(trace_id="trace-section-worker")

    result = run_create_section_plans(command)

    assert result["task_id"] == SECTION_PLAN_TASK_ID
    assert result["status"] == "succeeded"
    assert result["trace_id"] == "trace-section-worker"
    assert result["metrics"]["section_count"] == 3


def test_planning_actor_names_are_stable() -> None:
    assert create_chapter_plan.actor_name == "create_chapter_plan"
    assert create_section_plans.actor_name == "create_section_plans"


def test_planning_actors_use_planning_queue() -> None:
    assert create_chapter_plan.queue_name == "task-planning"
    assert create_section_plans.queue_name == "task-planning"


def test_existing_actor_names_remain_stable() -> None:
    assert extract_knowledge.actor_name == "extract_knowledge"
    assert noop_task.actor_name == "noop_task"
