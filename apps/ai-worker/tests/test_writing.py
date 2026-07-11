from worker.main import create_chapter_plan, create_section_plans, create_writing_run, extract_knowledge, noop_task
from worker.writing import (
    QUALITY_REPORT_ID,
    WRITING_RUN_ID,
    WRITING_STAGES,
    WRITING_TASK_ID,
    build_create_writing_run_command,
    build_writing_run_fixture,
    run_create_writing_run,
)


def test_build_writing_run_fixture_matches_contract_shape() -> None:
    command = build_create_writing_run_command()

    fixture = build_writing_run_fixture(command)

    assert fixture["writing_run"]["writing_run_id"] == WRITING_RUN_ID
    assert fixture["writing_run"]["quality_report_id"] == QUALITY_REPORT_ID
    assert fixture["writing_run"]["model_cost"]["retry_count"] == 1
    assert fixture["writing_run"]["critic_model_profile_id"] == "model_profile_structured_fallback"
    assert fixture["writing_run"]["accepted_chapter_ref"] is None
    assert fixture["provider_calls"][1]["error_code"] == "structured_output_validation_failed"
    assert fixture["provider_calls"][2]["model_profile_id"] == "model_profile_structured_fallback"
    assert fixture["quality_report"]["quality_report_id"] == QUALITY_REPORT_ID
    assert fixture["events"][1]["payload_json"]["writing_stages"] == WRITING_STAGES


def test_run_create_writing_run_returns_requires_review_result() -> None:
    command = build_create_writing_run_command(trace_id="trace-writing-worker")

    result = run_create_writing_run(command)

    assert result["task_id"] == WRITING_TASK_ID
    assert result["status"] == "requires_review"
    assert result["trace_id"] == "trace-writing-worker"
    assert result["metrics"]["current_stage"] == "humanizer_pass"
    assert result["metrics"]["section_run_count"] == 3


def test_writing_actor_name_and_queue_are_stable() -> None:
    assert create_writing_run.actor_name == "create_writing_run"
    assert create_writing_run.queue_name == "task-writing"


def test_existing_actor_names_remain_stable_after_writing_addition() -> None:
    assert create_chapter_plan.actor_name == "create_chapter_plan"
    assert create_section_plans.actor_name == "create_section_plans"
    assert extract_knowledge.actor_name == "extract_knowledge"
    assert noop_task.actor_name == "noop_task"
