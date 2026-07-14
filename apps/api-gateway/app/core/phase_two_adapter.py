from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Optional


def load_phase_two_store() -> ModuleType:
    module_path = Path(__file__).resolve().parents[3] / "core-service" / "app" / "core" / "phase_two_store.py"
    spec = importlib.util.spec_from_file_location("phase_two_store_gateway", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load phase two store from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_STORE = load_phase_two_store()
if not _STORE.STORE.books:
    _STORE.seed_phase_two_demo_data()
WORKSPACE_ID = _STORE.WORKSPACE_ID
BOOK_ID = _STORE.BOOK_ID
RUN_ID = _STORE.RUN_ID
PROJECT_ID = _STORE.PROJECT_ID
CHAPTER_PLAN_ID = _STORE.CHAPTER_PLAN_ID
WRITING_RUN_ID = _STORE.WRITING_RUN_ID
QUALITY_REPORT_ID = _STORE.QUALITY_REPORT_ID


def create_book(payload: dict[str, Any], trace_id: str) -> dict[str, Any]:
    return _STORE.create_book(payload, trace_id)


def get_book(book_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_book(book_id)


def list_book_chapters(book_id: str) -> list[dict[str, Any]]:
    return _STORE.list_book_chapters(book_id)


def get_book_source_content(book_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_book_source_content(book_id)


def list_evidence_for_book(book_id: str) -> list[dict[str, Any]]:
    return _STORE.list_evidence_for_book(book_id)


def get_evidence(evidence_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_evidence(evidence_id)


def get_book_analysis(book_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_book_analysis(book_id)


def create_extraction_run(
    book_id: str,
    trace_id: str,
    request_id: str = "system-extraction",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    return _STORE.create_extraction_run(book_id, trace_id, request_id, actor_id, actor_role, workspace_id)


def get_extraction_run(run_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_extraction_run(run_id)


def get_extraction_report(run_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_extraction_report(run_id)


def list_knowledge_objects_for_run(run_id: str) -> list[dict[str, Any]]:
    return _STORE.list_knowledge_objects_for_run(run_id)


def list_knowledge_sources(workspace_id: Optional[str] = None, status: str = "committed") -> list[dict[str, Any]]:
    return _STORE.list_knowledge_sources(workspace_id, status)


def apply_review_action(
    object_id: str,
    action: str,
    target_object_id: Optional[str] = None,
    request_id: str = "system-review",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.apply_review_action(object_id, action, target_object_id, request_id, trace_id, actor_id, actor_role, workspace_id)


def commit_knowledge_package(run_id: str) -> Optional[dict[str, Any]]:
    return _STORE.commit_knowledge_package(run_id)


def get_graph_summary(book_id: Optional[str] = None) -> dict[str, Any]:
    return _STORE.get_graph_summary(book_id)


def search_graph_nodes(book_id: Optional[str] = None, query: str = "", node_type: Optional[str] = None) -> dict[str, Any]:
    return _STORE.search_graph_nodes(book_id, query, node_type)


def get_graph_node(node_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_graph_node(node_id)


def list_graph_neighbors(node_id: str) -> Optional[dict[str, Any]]:
    return _STORE.list_graph_neighbors(node_id)


def create_novel_project(
    payload: dict[str, Any],
    trace_id: str,
    request_id: str = "system-project",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    return _STORE.create_novel_project(payload, trace_id, request_id, actor_id, actor_role, workspace_id)


def create_workspace(payload: dict[str, Any]) -> dict[str, Any]:
    return _STORE.create_workspace(payload)


def get_workspace(workspace_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_workspace(workspace_id)


def get_workspace_home(workspace_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_workspace_home(workspace_id)


def list_novel_projects() -> list[dict[str, Any]]:
    return _STORE.list_novel_projects()


def get_novel_project(project_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_novel_project(project_id)


def get_story_bible(story_bible_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_story_bible(story_bible_id)


def apply_story_bible_action(
    story_bible_id: str,
    action: str,
    request_id: str = "system-story-bible",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
    payload: Optional[dict[str, Any]] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.apply_story_bible_action(story_bible_id, action, request_id, trace_id, actor_id, actor_role, workspace_id, payload)


def create_chapter_plan(
    payload: dict[str, Any],
    trace_id: str,
    request_id: str = "system-plan",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.create_chapter_plan(payload, trace_id, request_id, actor_id, actor_role, workspace_id)


def get_chapter_plan(chapter_plan_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_chapter_plan(chapter_plan_id)


def list_section_plans(chapter_plan_id: str) -> Optional[dict[str, Any]]:
    return _STORE.list_section_plans(chapter_plan_id)


def create_section_plans(
    chapter_plan_id: str,
    section_count: int,
    trace_id: str,
    request_id: str = "system-plan",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.create_section_plans(chapter_plan_id, section_count, trace_id, request_id, actor_id, actor_role, workspace_id)


def create_writing_run(
    payload: dict[str, Any],
    trace_id: str,
    request_id: str = "system-writing",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.create_writing_run(payload, trace_id, request_id, actor_id, actor_role, workspace_id)


def get_configuration_snapshot() -> dict[str, Any]:
    return _STORE.get_configuration_snapshot()


def set_model_profile_enabled(
    model_profile_id: str,
    enabled: bool,
    request_id: str = "system-config",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.set_model_profile_enabled(model_profile_id, enabled, request_id, trace_id, actor_id, actor_role, workspace_id)


def update_quality_gate_profile(
    quality_gate_profile_id: str,
    ai_flavor_threshold: float,
    originality_safety_threshold: float,
    request_id: str = "system-config",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.update_quality_gate_profile(
        quality_gate_profile_id,
        ai_flavor_threshold,
        originality_safety_threshold,
        request_id,
        trace_id,
        actor_id,
        actor_role,
        workspace_id,
    )


def update_agent_model_assignment(
    assignment_id: str,
    model_profile_id: str,
    max_retry: int,
    max_cost: float,
    enabled: bool,
    request_id: str = "system-config",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
):
    return _STORE.update_agent_model_assignment(
        assignment_id,
        model_profile_id,
        max_retry,
        max_cost,
        enabled,
        request_id,
        trace_id,
        actor_id,
        actor_role,
        workspace_id,
    )


def update_prompt_version(
    agent_role: str,
    template_ref: str,
    request_id: str = "system-config",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    return _STORE.update_prompt_version(agent_role, template_ref, request_id, trace_id, actor_id, actor_role, workspace_id)


def get_writing_run(writing_run_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_writing_run(writing_run_id)


def get_quality_report(quality_report_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_quality_report(quality_report_id)


def get_consistency_report(consistency_report_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_consistency_report(consistency_report_id)


def get_revision_summary(revision_summary_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_revision_summary(revision_summary_id)


def list_rules() -> list[dict[str, Any]]:
    return _STORE.list_rules()


def list_patterns(status: Optional[str] = None, pattern_type: Optional[str] = None) -> list[dict[str, Any]]:
    return _STORE.list_patterns(status, pattern_type)


def get_pattern(pattern_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_pattern(pattern_id)


def create_pattern(
    payload: dict[str, Any],
    request_id: str = "system-pattern",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    return _STORE.create_pattern(payload, request_id, trace_id, actor_id, actor_role, workspace_id)


def list_rhythm_profiles(status: Optional[str] = None, target_id: Optional[str] = None) -> list[dict[str, Any]]:
    return _STORE.list_rhythm_profiles(status, target_id)


def get_rhythm_profile(rhythm_profile_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_rhythm_profile(rhythm_profile_id)


def create_rhythm_profile(
    payload: dict[str, Any],
    request_id: str = "system-rhythm",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    return _STORE.create_rhythm_profile(payload, request_id, trace_id, actor_id, actor_role, workspace_id)


def list_assets(status: Optional[str] = None, asset_type: Optional[str] = None) -> list[dict[str, Any]]:
    return _STORE.list_assets(status, asset_type)


def get_asset(asset_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_asset(asset_id)


def create_asset(
    payload: dict[str, Any],
    request_id: str = "system-asset",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    return _STORE.create_asset(payload, request_id, trace_id, actor_id, actor_role, workspace_id)


def get_rule(rule_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_rule(rule_id)


def accept_chapter(
    writing_run_id: str,
    trace_id: str,
    request_id: str = "system-accept",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.accept_chapter(writing_run_id, trace_id, request_id, actor_id, actor_role, workspace_id)


def apply_writing_review_action(
    writing_run_id: str,
    payload: dict[str, Any],
    request_id: str = "system-writing-review",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.apply_writing_review_action(writing_run_id, payload, request_id, trace_id, actor_id, actor_role, workspace_id)


def list_feedback_records(target_type: Optional[str] = None, target_id: Optional[str] = None) -> list[dict[str, Any]]:
    return _STORE.list_feedback_records(target_type, target_id)


def get_prompt_ranking_snapshot(target_id: Optional[str] = None) -> Optional[dict[str, Any]]:
    return _STORE.get_prompt_ranking_snapshot(target_id)


def promote_feedback_record(
    feedback_record_id: str,
    promotion_status: str,
    output_ref: Optional[str],
    request_id: str = "system-feedback",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.promote_feedback_record(
        feedback_record_id,
        promotion_status,
        output_ref,
        request_id,
        trace_id,
        actor_id,
        actor_role,
        workspace_id,
    )


def create_agent_task(
    payload: dict[str, Any],
    request_id: str = "system-task",
    trace_id: str = "system-trace",
    actor_id: str = _STORE.USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    return _STORE.create_agent_task(payload, request_id, trace_id, actor_id, actor_role, workspace_id)


def get_agent_task(task_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_agent_task(task_id)


def list_audit_events(workspace_id: Optional[str] = None) -> list[dict[str, Any]]:
    return _STORE.list_audit_events(workspace_id)
