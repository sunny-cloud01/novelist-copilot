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


def create_extraction_run(book_id: str, trace_id: str) -> dict[str, Any]:
    return _STORE.create_extraction_run(book_id, trace_id)


def get_extraction_run(run_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_extraction_run(run_id)


def get_extraction_report(run_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_extraction_report(run_id)


def list_knowledge_objects_for_run(run_id: str) -> list[dict[str, Any]]:
    return _STORE.list_knowledge_objects_for_run(run_id)


def apply_review_action(
    object_id: str,
    action: str,
    target_object_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    return _STORE.apply_review_action(object_id, action, target_object_id)


def commit_knowledge_package(run_id: str) -> Optional[dict[str, Any]]:
    return _STORE.commit_knowledge_package(run_id)


def get_graph_summary(book_id: Optional[str] = None) -> dict[str, Any]:
    return _STORE.get_graph_summary(book_id)


def create_novel_project(payload: dict[str, Any], trace_id: str) -> dict[str, Any]:
    return _STORE.create_novel_project(payload, trace_id)


def create_workspace(payload: dict[str, Any]) -> dict[str, Any]:
    return _STORE.create_workspace(payload)


def get_workspace(workspace_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_workspace(workspace_id)


def get_workspace_home(workspace_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_workspace_home(workspace_id)


def get_novel_project(project_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_novel_project(project_id)


def create_chapter_plan(payload: dict[str, Any], trace_id: str) -> Optional[dict[str, Any]]:
    return _STORE.create_chapter_plan(payload, trace_id)


def get_chapter_plan(chapter_plan_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_chapter_plan(chapter_plan_id)


def list_section_plans(chapter_plan_id: str) -> Optional[dict[str, Any]]:
    return _STORE.list_section_plans(chapter_plan_id)


def create_section_plans(chapter_plan_id: str, section_count: int, trace_id: str) -> Optional[dict[str, Any]]:
    return _STORE.create_section_plans(chapter_plan_id, section_count, trace_id)


def create_writing_run(payload: dict[str, Any], trace_id: str) -> Optional[dict[str, Any]]:
    return _STORE.create_writing_run(payload, trace_id)


def get_configuration_snapshot() -> dict[str, Any]:
    return _STORE.get_configuration_snapshot()


def set_model_profile_enabled(model_profile_id: str, enabled: bool) -> Optional[dict[str, Any]]:
    return _STORE.set_model_profile_enabled(model_profile_id, enabled)


def get_writing_run(writing_run_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_writing_run(writing_run_id)


def get_quality_report(quality_report_id: str) -> Optional[dict[str, Any]]:
    return _STORE.get_quality_report(quality_report_id)


def accept_chapter(writing_run_id: str, trace_id: str) -> Optional[dict[str, Any]]:
    return _STORE.accept_chapter(writing_run_id, trace_id)


def list_feedback_records(target_type: Optional[str] = None, target_id: Optional[str] = None) -> list[dict[str, Any]]:
    return _STORE.list_feedback_records(target_type, target_id)
