import pytest

from worker.core_store import load_phase_two_store
from worker.main import create_chapter_plan, create_section_plans, create_writing_run, extract_knowledge, noop_task
from worker.provider_executor import ProviderExecutionError, execute_writing_provider_pipeline
import worker.writing as writing_module
from worker.writing import (
    QUALITY_REPORT_ID,
    WRITING_RUN_ID,
    WRITING_STAGES,
    WRITING_TASK_ID,
    build_create_writing_run_command,
    build_writing_run_fixture,
    run_create_writing_run,
)


def load_phase_two_store_module():
    return load_phase_two_store()


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
    assert fixture["provider_calls"][2]["provider_model_name"] == "claude-haiku-4-5-20251001"
    assert fixture["provider_calls"][2]["output_ref"] == "object://consistency-reports/01JZCONSIST00000000000001"
    assert fixture["provider_calls"][2]["fallback_from_call_id"] == "01JZPCALL0000000000000002"
    assert fixture["quality_report"]["quality_report_id"] == QUALITY_REPORT_ID
    assert fixture["events"][1]["payload_json"]["writing_stages"] == WRITING_STAGES


def test_execute_writing_provider_pipeline_uses_persisted_profiles() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 13, "target_word_count": 4300, "payload": {}},
        trace_id="trace-writing-provider-plan",
    )
    assert created_plan is not None
    created_sections = store.create_section_plans(
        created_plan["chapter_plan"]["chapter_plan_id"],
        section_count=3,
        trace_id="trace-writing-provider-sections",
    )
    assert created_sections is not None
    created = store.create_writing_run(
        {"project_id": store.PROJECT_ID, "chapter_plan_id": created_plan["chapter_plan"]["chapter_plan_id"]},
        trace_id="trace-writing-provider",
    )
    assert created is not None

    result = execute_writing_provider_pipeline(
        store=store,
        writing_run=created["writing_run"],
        chapter_plan=store.STORE.chapter_plans[created["writing_run"]["chapter_plan_id"]],
        section_plans=store.STORE.section_plans_by_chapter[created["writing_run"]["chapter_plan_id"]],
        section_runs=store.STORE.section_runs_by_writing[created["writing_run"]["writing_run_id"]],
        prompt_package=store.STORE.prompt_packages[created["writing_run"]["prompt_package_id"]],
    )

    assert result["retry_count"] == 1
    assert len(result["provider_calls"]) == 4
    assert result["provider_calls"][2]["model_profile_id"] == "model_profile_structured_fallback"
    assert result["section_runs"][1]["status"] == "rewrite_required"
    assert result["consistency_issues"][0]["note"] == "claude-haiku-4-5-20251001"
    assert "第1节里" in result["assembled_chapter"]



def test_run_create_writing_run_returns_requires_review_result() -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 12, "target_word_count": 4100, "payload": {}},
        trace_id="trace-writing-worker-plan",
    )
    assert created_plan is not None
    created_sections = store.create_section_plans(
        created_plan["chapter_plan"]["chapter_plan_id"],
        section_count=3,
        trace_id="trace-writing-worker-sections",
    )
    assert created_sections is not None
    created = store.create_writing_run(
        {"project_id": store.PROJECT_ID, "chapter_plan_id": created_plan["chapter_plan"]["chapter_plan_id"]},
        trace_id="trace-writing-worker",
    )
    assert created is not None
    command = build_create_writing_run_command(
        project_id=created["writing_run"]["project_id"],
        chapter_plan_id=created["writing_run"]["chapter_plan_id"],
        writing_run_id=created["writing_run"]["writing_run_id"],
        task_id=created["task"]["task_id"],
        trace_id="trace-writing-worker",
    )

    result = run_create_writing_run(command)
    refreshed = load_phase_two_store_module().get_writing_run(created["writing_run"]["writing_run_id"])

    assert result["task_id"] == created["task"]["task_id"]
    assert result["status"] == "requires_review"
    assert result["trace_id"] == "trace-writing-worker"
    assert result["metrics"]["current_stage"] == "consistency_review"
    assert result["metrics"]["memory_package"]["source_refs"][0].startswith("object://story-bibles/")
    assert result["metrics"]["prompt_package"]["template_refs"] == [
        "prompt://writer/chapter-default",
        "prompt://critic/chapter-default",
        "prompt://humanizer/chapter-default",
    ]
    assert result["metrics"]["section_run_count"] == 3
    assert refreshed["task"]["status"] == "requires_review"
    assert refreshed["writing_run"]["assembled_chapter"]
    assert refreshed["quality_report"]["human_review_required"] is True
    assert refreshed["consistency_report"]["status"] == "blocked"
    assert refreshed["revision_summary"]["status"] == "requested"
    assert refreshed["events"][-1]["event_type"] == "review_required"


def test_run_create_writing_run_fails_when_provider_execution_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    store = load_phase_two_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 14, "target_word_count": 3900, "payload": {}},
        trace_id="trace-writing-missing-profile-plan",
    )
    assert created_plan is not None
    created_sections = store.create_section_plans(
        created_plan["chapter_plan"]["chapter_plan_id"],
        section_count=3,
        trace_id="trace-writing-missing-profile-sections",
    )
    assert created_sections is not None
    created = store.create_writing_run(
        {"project_id": store.PROJECT_ID, "chapter_plan_id": created_plan["chapter_plan"]["chapter_plan_id"]},
        trace_id="trace-writing-missing-profile",
    )
    assert created is not None
    command = build_create_writing_run_command(
        project_id=created["writing_run"]["project_id"],
        chapter_plan_id=created["writing_run"]["chapter_plan_id"],
        writing_run_id=created["writing_run"]["writing_run_id"],
        task_id=created["task"]["task_id"],
        trace_id="trace-writing-missing-profile",
    )

    def boom(**_: object) -> dict[str, object]:
        raise ProviderExecutionError("model_profile_missing", "model profile missing: injected")

    monkeypatch.setattr(writing_module, "execute_writing_provider_pipeline", boom)

    result = run_create_writing_run(command)
    refreshed = load_phase_two_store_module().get_writing_run(created["writing_run"]["writing_run_id"])

    assert result["status"] == "failed"
    assert result["metrics"]["error_code"] == "model_profile_missing"
    assert refreshed["task"]["status"] == "failed"
    assert refreshed["task"]["error_code"] == "model_profile_missing"
    assert refreshed["events"][-1]["event_type"] == "failed"



def test_writing_actor_name_and_queue_are_stable() -> None:
    assert create_writing_run.actor_name == "create_writing_run"
    assert create_writing_run.queue_name == "task-writing"


def test_existing_actor_names_remain_stable_after_writing_addition() -> None:
    assert create_chapter_plan.actor_name == "create_chapter_plan"
    assert create_section_plans.actor_name == "create_section_plans"
    assert extract_knowledge.actor_name == "extract_knowledge"
    assert noop_task.actor_name == "noop_task"
