from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Optional
import ulid

try:
    from app.core.business_persistence import backfill_business_state_from_snapshot, load_business_state, save_business_state
except ModuleNotFoundError:
    spec = importlib.util.spec_from_file_location("phase_two_business_persistence", Path(__file__).with_name("business_persistence.py"))
    if spec is None or spec.loader is None:
        raise
    business_persistence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(business_persistence)
    backfill_business_state_from_snapshot = business_persistence.backfill_business_state_from_snapshot
    load_business_state = business_persistence.load_business_state
    save_business_state = business_persistence.save_business_state

try:
    from app.core.persistence import load_runtime_projection, load_snapshot, save_snapshot, sync_runtime_projection
except ModuleNotFoundError:
    spec = importlib.util.spec_from_file_location("phase_two_persistence", Path(__file__).with_name("persistence.py"))
    if spec is None or spec.loader is None:
        raise
    persistence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(persistence)
    load_snapshot = persistence.load_snapshot
    save_snapshot = persistence.save_snapshot
    load_runtime_projection = persistence.load_runtime_projection
    sync_runtime_projection = persistence.sync_runtime_projection


USER_ID = "demo-user"
WORKSPACE_ID = "demo-workspace"
WORKSPACE_MEMBER_ID = "demo-workspace-member"
BOOK_ID = "01JZBOOK000000000000000001"
RUN_ID = "01JZRUN0000000000000000001"
TASK_ID = "01JZTASK000000000000000001"
GRAPH_BOOK_ID = BOOK_ID
PROJECT_ID = "01JZPROJECT000000000000001"
STORY_BIBLE_ID = "01JZBIBLE0000000000000001"
CHAPTER_PLAN_ID = "01JZCHPLAN000000000000001"
CHAPTER_PLAN_TASK_ID = "01JZPLANTASK0000000000001"
SECTION_PLAN_TASK_ID = "01JZSECTTASK0000000000001"
QUALITY_GATE_PROFILE_ID = "01JZQUALITY00000000000001"
WRITING_RUN_ID = "01JZWRITING00000000000001"
WRITING_TASK_ID = "01JZWRITETASK0000000000001"
MEMORY_PACKAGE_ID = "01JZMEMPKG000000000000001"
PROMPT_PACKAGE_ID = "01JZPROMPTPKG000000000001"
QUALITY_REPORT_ID = "01JZQLTREP000000000000001"
CHAPTER_DRAFT_ID = "01JZDRAFT0000000000000001"
MODEL_PROFILE_DEFAULT_ID = "model_profile_default"
MODEL_PROFILE_STRUCTURED_FALLBACK_ID = "model_profile_structured_fallback"
DEFAULT_MODEL_PROFILE_ID = MODEL_PROFILE_DEFAULT_ID
MVP_AGENT_ROLES = [
    "extraction",
    "normalization",
    "planning",
    "memory",
    "style_analyzer",
    "writer",
    "critic",
    "humanizer",
    "review",
    "feedback",
]
ROLE_CALL_METRICS = {
    "writer": {"prompt_tokens": 1800, "completion_tokens": 920, "latency_ms": 1430, "cost_estimate": 0.31},
    "critic": {"prompt_tokens": 1400, "completion_tokens": 540, "latency_ms": 980, "cost_estimate": 0.22},
    "humanizer": {"prompt_tokens": 1780, "completion_tokens": 850, "latency_ms": 1210, "cost_estimate": 0.33},
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _isoformat_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _normalize_timestamp_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = value.replace(" ", "T")
    if normalized.endswith("Z"):
        return normalized
    if len(normalized) >= 3 and normalized[-3] in {"+", "-"}:
        normalized = f"{normalized}:00"
    return normalized


@dataclass
class CoreStore:
    users: dict[str, dict[str, Any]] = field(default_factory=dict)
    workspaces: dict[str, dict[str, Any]] = field(default_factory=dict)
    workspace_members: dict[str, dict[str, Any]] = field(default_factory=dict)
    books: dict[str, dict[str, Any]] = field(default_factory=dict)
    source_contents: dict[str, dict[str, Any]] = field(default_factory=dict)
    source_content_by_book: dict[str, str] = field(default_factory=dict)
    evidences: dict[str, dict[str, Any]] = field(default_factory=dict)
    evidence_by_book: dict[str, list[str]] = field(default_factory=dict)
    evidence_by_run: dict[str, list[str]] = field(default_factory=dict)
    chapters_by_book: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    source_scenes_by_chapter: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    events_by_scene: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    conflicts: dict[str, dict[str, Any]] = field(default_factory=dict)
    hooks: dict[str, dict[str, Any]] = field(default_factory=dict)
    rewards: dict[str, dict[str, Any]] = field(default_factory=dict)
    climaxes: dict[str, dict[str, Any]] = field(default_factory=dict)
    relationship_edges: dict[str, dict[str, Any]] = field(default_factory=dict)
    extraction_runs: dict[str, dict[str, Any]] = field(default_factory=dict)
    knowledge_objects: dict[str, dict[str, Any]] = field(default_factory=dict)
    knowledge_by_run: dict[str, list[str]] = field(default_factory=dict)
    graph_summaries: dict[str, dict[str, Any]] = field(default_factory=dict)
    graph_node_details: dict[str, dict[str, Any]] = field(default_factory=dict)
    graph_neighbors_by_node: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    novel_projects: dict[str, dict[str, Any]] = field(default_factory=dict)
    story_bibles: dict[str, dict[str, Any]] = field(default_factory=dict)
    chapter_plans: dict[str, dict[str, Any]] = field(default_factory=dict)
    chapter_plan_tasks: dict[str, dict[str, Any]] = field(default_factory=dict)
    section_plan_tasks: dict[str, dict[str, Any]] = field(default_factory=dict)
    section_plans_by_chapter: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    model_profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    agent_model_assignments: dict[str, dict[str, Any]] = field(default_factory=dict)
    provider_accounts: dict[str, dict[str, Any]] = field(default_factory=dict)
    quality_gate_profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    prompt_versions: list[dict[str, Any]] = field(default_factory=list)
    writing_runs: dict[str, dict[str, Any]] = field(default_factory=dict)
    writing_run_tasks: dict[str, dict[str, Any]] = field(default_factory=dict)
    provider_calls_by_writing: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    section_runs_by_writing: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    memory_packages: dict[str, dict[str, Any]] = field(default_factory=dict)
    prompt_packages: dict[str, dict[str, Any]] = field(default_factory=dict)
    quality_reports: dict[str, dict[str, Any]] = field(default_factory=dict)
    consistency_reports: dict[str, dict[str, Any]] = field(default_factory=dict)
    revision_summaries: dict[str, dict[str, Any]] = field(default_factory=dict)
    rules: dict[str, dict[str, Any]] = field(default_factory=dict)
    chapter_snapshots: dict[str, dict[str, Any]] = field(default_factory=dict)
    manuscript_states_by_project: dict[str, dict[str, Any]] = field(default_factory=dict)
    feedback_records: dict[str, dict[str, Any]] = field(default_factory=dict)
    ranking_snapshots: dict[str, dict[str, Any]] = field(default_factory=dict)
    patterns: dict[str, dict[str, Any]] = field(default_factory=dict)
    rhythm_profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    assets: dict[str, dict[str, Any]] = field(default_factory=dict)
    agent_tasks: dict[str, dict[str, Any]] = field(default_factory=dict)
    task_events_by_task: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    audit_events: list[dict[str, Any]] = field(default_factory=list)
    migration_events: list[dict[str, Any]] = field(default_factory=list)
    knowledge_packages: dict[str, dict[str, Any]] = field(default_factory=dict)


STORE = CoreStore()


_OBJECT_KIND_OVERRIDES = {
    "workspace": "workspace",
    "workspaces": "workspace",
    "workspace-member": "workspace_member",
    "workspace-members": "workspace_member",
    "source-book": "source_book",
    "source-books": "source_book",
    "source-content": "source_content",
    "source-contents": "source_content",
    "source-chapter": "source_chapter",
    "source-chapters": "source_chapter",
    "source-scene": "source_scene",
    "source-scenes": "source_scene",
    "story-event": "story_event",
    "story-events": "story_event",
    "story-conflict": "story_conflict",
    "story-conflicts": "story_conflict",
    "story-hook": "story_hook",
    "story-hooks": "story_hook",
    "story-reward": "story_reward",
    "story-rewards": "story_reward",
    "story-climax": "story_climax",
    "story-climaxes": "story_climax",
    "relationship-edge": "relationship_edge",
    "relationship-edges": "relationship_edge",
    "evidence": "evidence",
    "evidences": "evidence",
    "extraction-run": "extraction_run",
    "extraction-runs": "extraction_run",
    "knowledge-object": "knowledge_object",
    "knowledge-objects": "knowledge_object",
    "graph-node": "graph_node",
    "graph-nodes": "graph_node",
    "graph-summary": "graph_summary",
    "graph-summaries": "graph_summary",
    "novel-project": "novel_project",
    "novel-projects": "novel_project",
    "story-bible": "story_bible",
    "story-bibles": "story_bible",
    "chapter-plan": "chapter_plan",
    "chapter-plans": "chapter_plan",
    "section-plan": "section_plan",
    "section-plans": "section_plan",
    "memory-package": "memory_package",
    "memory-packages": "memory_package",
    "prompt-package": "prompt_package",
    "prompt-packages": "prompt_package",
    "writing-run": "writing_run",
    "writing-runs": "writing_run",
    "section-run": "section_run",
    "section-runs": "section_run",
    "draft": "draft",
    "drafts": "draft",
    "critic-report": "critic_report",
    "critic-reports": "critic_report",
    "humanized": "humanized_text",
    "review-note": "review_note",
    "review-notes": "review_note",
    "feedback-comment": "feedback_comment",
    "feedback-comments": "feedback_comment",
    "critic-comment": "feedback_comment",
    "critic-comments": "feedback_comment",
    "quality-comment": "quality_comment",
    "quality-comments": "quality_comment",
    "knowledge-package": "knowledge_package",
    "knowledge-packages": "knowledge_package",
    "graph-package": "graph_package",
    "graph-packages": "graph_package",
    "extraction-report": "extraction_report",
    "extraction-reports": "extraction_report",
    "quality-report": "quality_report",
    "quality-reports": "quality_report",
    "consistency-report": "consistency_report",
    "consistency-reports": "consistency_report",
    "revision-summary": "revision_summary",
    "revision-summaries": "revision_summary",
    "manuscripts": "manuscript",
    "chapter-snapshot": "chapter_snapshot",
    "chapter-snapshots": "chapter_snapshot",
    "manuscript-state": "manuscript_state",
    "manuscript-states": "manuscript_state",
    "feedback-record": "feedback_record",
    "feedback-records": "feedback_record",
    "ranking": "ranking_snapshot",
    "rankings": "ranking_snapshot",
    "pattern": "pattern",
    "patterns": "pattern",
    "rhythm-profile": "rhythm_profile",
    "rhythm-profiles": "rhythm_profile",
    "asset": "asset",
    "assets": "asset",
    "rule": "rule",
    "rules": "rule",
    "model-profile": "model_profile",
    "model-profiles": "model_profile",
    "provider-account": "provider_account",
    "provider-accounts": "provider_account",
    "quality-profile": "quality_profile",
    "quality-gate-profiles": "quality_profile",
    "prompt-version": "prompt_version",
    "prompt-versions": "prompt_version",
    "configuration": "configuration",
}


_OBJECT_REF_PREFIX_OVERRIDES = {
    "workspace": "workspaces",
    "workspace-member": "workspace-members",
    "source-book": "source-books",
    "source-content": "source-contents",
    "source-chapter": "source-chapters",
    "source-scene": "source-scenes",
    "story-event": "story-events",
    "story-conflict": "story-conflicts",
    "story-hook": "story-hooks",
    "story-reward": "story-rewards",
    "story-climax": "story-climaxes",
    "relationship-edge": "relationship-edges",
    "evidence": "evidence",
    "extraction-run": "extraction-runs",
    "knowledge-object": "knowledge-objects",
    "graph-node": "graph-nodes",
    "graph-summary": "graph-summaries",
    "novel-project": "novel-projects",
    "story-bible": "story-bibles",
    "chapter-plan": "chapter-plans",
    "section-plan": "section-plans",
    "memory-package": "memory-packages",
    "prompt-package": "prompt-packages",
    "writing-run": "writing-runs",
    "section-run": "section-runs",
    "draft": "drafts",
    "critic-report": "critic-reports",
    "review-note": "review-notes",
    "feedback-comment": "feedback-comments",
    "critic-comment": "critic-comments",
    "quality-comment": "quality-comments",
    "knowledge-package": "knowledge-packages",
    "graph-package": "graph-packages",
    "extraction-report": "extraction-reports",
    "quality-report": "quality-reports",
    "consistency-report": "consistency-reports",
    "revision-summary": "revision-summaries",
    "chapter-snapshot": "chapter-snapshots",
    "manuscript-state": "manuscript-states",
    "feedback-record": "feedback-records",
    "ranking": "rankings",
    "pattern": "patterns",
    "rhythm-profile": "rhythm-profiles",
    "asset": "assets",
    "rule": "rules",
    "model-profile": "model-profiles",
    "provider-account": "provider-accounts",
    "quality-profile": "quality-gate-profiles",
    "prompt-version": "prompt-versions",
}


def _canonical_object_ref(object_ref: str) -> str:
    if not object_ref.startswith("object://"):
        return object_ref
    prefix, *rest = object_ref.removeprefix("object://").split("/", 1)
    normalized_prefix = _OBJECT_REF_PREFIX_OVERRIDES.get(prefix, prefix)
    suffix = f"/{rest[0]}" if rest else ""
    return f"object://{normalized_prefix}{suffix}"


def _infer_object_kind(object_ref: str) -> str:
    if not object_ref.startswith("object://"):
        return "external_ref"
    prefix = _canonical_object_ref(object_ref).removeprefix("object://").split("/", 1)[0]
    return _OBJECT_KIND_OVERRIDES.get(prefix, prefix.replace("-", "_"))


def _infer_storage_bucket(object_ref: str) -> str:
    if not object_ref.startswith("object://"):
        return "external"
    return _canonical_object_ref(object_ref).removeprefix("object://").split("/", 1)[0]


def _payload_object_metadata(object_ref: str, payload: Any, mime_type: Optional[str]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    if isinstance(payload, dict):
        for key in ("bucket", "storage_bucket"):
            value = payload.get(key)
            if value:
                metadata["bucket"] = value
                break
        for key in ("storage_key", "object_key"):
            value = payload.get(key)
            if value:
                metadata["storage_key"] = value
                break
        for key in ("checksum", "content_checksum"):
            value = payload.get(key)
            if value:
                metadata["checksum"] = value
                break
        for key in ("byte_size", "content_byte_size"):
            value = payload.get(key)
            if value is not None:
                metadata["byte_size"] = value
                break
        payload_mime_type = payload.get("mime_type")
        if payload_mime_type:
            metadata["mime_type"] = payload_mime_type
        elif mime_type:
            metadata["mime_type"] = mime_type
    elif mime_type:
        metadata["mime_type"] = mime_type
    return metadata


def _text_artifact_payload(object_ref: str, text: Optional[str], **fields: Any) -> dict[str, Any]:
    content = text or ""
    encoded = content.encode("utf-8")
    return {
        **fields,
        "object_ref": object_ref,
        "content": content,
        "mime_type": "text/plain; charset=utf-8",
        "checksum": f"sha256:{hashlib.sha256(encoded).hexdigest()}",
        "byte_size": len(encoded),
    }


def _json_artifact_payload(object_ref: str, content: Any, **fields: Any) -> dict[str, Any]:
    normalized_content = deepcopy(content)
    serialized = json.dumps(normalized_content, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return {
        **fields,
        "object_ref": object_ref,
        "content": normalized_content,
        "mime_type": "application/json",
        "checksum": f"sha256:{hashlib.sha256(serialized.encode('utf-8')).hexdigest()}",
        "byte_size": len(serialized.encode("utf-8")),
    }


def _register_projection_object(rows: dict[str, dict[str, Any]], object_ref: str, workspace_id: str, owner_ref: str, payload: Any, created_at: Optional[str] = None, updated_at: Optional[str] = None, mime_type: Optional[str] = None, access_policy: str = "workspace", overwrite: bool = True) -> None:
    if not object_ref:
        return
    canonical_ref = _canonical_object_ref(object_ref)
    if canonical_ref in rows and not overwrite:
        return
    normalized_payload = deepcopy(payload)
    serialized = json.dumps(normalized_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    metadata = _payload_object_metadata(canonical_ref, normalized_payload, mime_type)
    rows[canonical_ref] = {
        "object_ref": canonical_ref,
        "workspace_id": workspace_id,
        "object_kind": _infer_object_kind(canonical_ref),
        "bucket": metadata.get("bucket") or _infer_storage_bucket(canonical_ref),
        "storage_key": metadata.get("storage_key") or (canonical_ref.removeprefix("object://") if canonical_ref.startswith("object://") else canonical_ref),
        "checksum": metadata.get("checksum") or f"sha256:{hashlib.sha256(serialized.encode('utf-8')).hexdigest()}",
        "mime_type": metadata.get("mime_type") or "application/json",
        "byte_size": metadata.get("byte_size") if metadata.get("byte_size") is not None else len(serialized.encode("utf-8")),
        "access_policy": access_policy,
        "owner_ref": owner_ref,
        "payload": normalized_payload,
        "created_at": created_at or updated_at or utc_now(),
        "updated_at": updated_at or created_at or utc_now(),
    }


def _projection_task_record(task_id: str) -> tuple[Optional[str], Optional[str]]:
    for run_id, run in STORE.extraction_runs.items():
        task = run.get("task")
        if task and task["task_id"] == task_id:
            return "extraction_run", run_id
    for chapter_plan_id, task in STORE.chapter_plan_tasks.items():
        if task["task_id"] == task_id:
            return "chapter_plan", chapter_plan_id
    for chapter_plan_id, task in STORE.section_plan_tasks.items():
        if task["task_id"] == task_id:
            return "section_plan", chapter_plan_id
    for writing_run_id, task in STORE.writing_run_tasks.items():
        if task["task_id"] == task_id:
            return "writing_run", writing_run_id
    task = STORE.agent_tasks.get(task_id)
    if task:
        return "agent_task", task_id
    return None, None



def _as_utc_datetime(value: str) -> datetime:
    normalized = _normalize_timestamp_string(value)
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)



def _clear_task_lock(task: dict[str, Any]) -> None:
    task["lease_owner"] = None
    task["lease_expires_at"] = None
    task["heartbeat_at"] = None
    task["current_dispatch_token"] = None



def _build_task_lock_row(task: dict[str, Any]) -> Optional[dict[str, Any]]:
    if not task.get("lease_owner") and not task.get("lease_expires_at") and not task.get("heartbeat_at"):
        return None
    return {
        "task_lock_id": f"task-lock:{task['task_id']}",
        "task_id": task["task_id"],
        "lock_owner": task.get("lease_owner"),
        "lease_expires_at": task.get("lease_expires_at"),
        "heartbeat_at": task.get("heartbeat_at"),
        "created_at": task.get("started_at") or task.get("created_at"),
        "updated_at": task.get("heartbeat_at") or task.get("started_at") or task.get("created_at"),
    }



def _sync_task_owner_runtime_status(task_kind: Optional[str], entity_id: Optional[str], status: str, now: str, task: dict[str, Any]) -> None:
    if task_kind == "extraction_run" and entity_id:
        run = STORE.extraction_runs.get(entity_id)
        if not run:
            return
        run["status"] = status
        run["started_at"] = task.get("started_at") or run.get("started_at")
        if status in {"queued", "running", "retrying"}:
            run["finished_at"] = None
        elif status in {"succeeded", "failed", "requires_review", "blocked"}:
            run["finished_at"] = task.get("finished_at")
        return
    if task_kind == "chapter_plan" and entity_id:
        chapter_plan = STORE.chapter_plans.get(entity_id)
        if chapter_plan:
            chapter_plan["status"] = status
            chapter_plan["updated_at"] = now
        return
    if task_kind == "writing_run" and entity_id:
        writing_run = STORE.writing_runs.get(entity_id)
        if writing_run:
            writing_run["status"] = status
            writing_run["updated_at"] = now



def _terminal_recovery_status(task: dict[str, Any]) -> str:
    if task.get("error_code") in {"structured_output_validation_failed", "provider_invalid_response", "context_too_long"}:
        return "requires_review"
    return "failed"


LEGAL_DISPATCH_STATUSES = {"queued", "retrying"}
TERMINAL_TASK_STATUSES = {"succeeded", "requires_review", "failed", "blocked"}


def _task_dispatch_token(task: dict[str, Any]) -> Optional[str]:
    return task.get("current_dispatch_token")


def _set_task_dispatch_token(task: dict[str, Any], token: str) -> None:
    task["current_dispatch_token"] = token


def _next_dispatch_attempt(task: dict[str, Any]) -> int:
    return int(task.get("dispatch_attempt") or 0) + 1


def _dispatch_token(trace_id: str, actor_id: str, request_id: str, attempt: int) -> str:
    return f"{trace_id}:{actor_id}:{request_id}:{attempt}"


def _can_dispatch_task(task: dict[str, Any]) -> bool:
    return task.get("status") in LEGAL_DISPATCH_STATUSES


def _can_schedule_retry(task: dict[str, Any]) -> bool:
    return task.get("status") == "running"


def _can_require_manual_review(task: dict[str, Any]) -> bool:
    return task.get("status") == "running"


def _completion_matches_active_dispatch(task: dict[str, Any], dispatch_token: Optional[str]) -> bool:
    if task.get("status") != "running":
        return False
    if not task.get("lease_owner"):
        return False
    token = _task_dispatch_token(task)
    if token and dispatch_token != token:
        return False
    return True


def _build_runtime_projection() -> dict[str, list[dict[str, Any]]]:
    object_rows: dict[str, dict[str, Any]] = {}
    task_rows: list[dict[str, Any]] = []
    task_lock_rows: list[dict[str, Any]] = []
    task_event_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []

    for workspace_id, workspace in STORE.workspaces.items():
        _register_projection_object(object_rows, f"object://workspace/{workspace_id}", workspace_id, f"workspace:{workspace_id}", workspace, workspace.get("created_at"), workspace.get("updated_at"))
    for member_id, member in STORE.workspace_members.items():
        _register_projection_object(object_rows, f"object://workspace-member/{member_id}", member["workspace_id"], f"workspace-member:{member_id}", member, member.get("created_at"), member.get("updated_at"))
    for book_id, book in STORE.books.items():
        _register_projection_object(object_rows, f"object://source-book/{book_id}", book["workspace_id"], f"book:{book_id}", book, book.get("created_at"), book.get("updated_at"))
    for content_id, content in STORE.source_contents.items():
        workspace_id = STORE.books.get(content["book_id"], {}).get("workspace_id", default_workspace_id())
        _register_projection_object(object_rows, f"object://source-contents/{content_id}", workspace_id, f"source-content:{content_id}", content, content.get("created_at"), content.get("updated_at"), mime_type=content.get("mime_type", "text/plain; charset=utf-8"))
    for evidence_id, evidence in STORE.evidences.items():
        workspace_id = STORE.books.get(evidence["book_id"], {}).get("workspace_id", default_workspace_id())
        _register_projection_object(object_rows, f"object://evidence/{evidence_id}", workspace_id, f"evidence:{evidence_id}", evidence, evidence.get("created_at"), evidence.get("updated_at"), mime_type="application/json")
    for book_id, chapters in STORE.chapters_by_book.items():
        workspace_id = STORE.books.get(book_id, {}).get("workspace_id", default_workspace_id())
        for chapter in chapters:
            chapter_ref = chapter.get("text_object_ref") or f"object://source-chapter/{chapter['chapter_id']}"
            _register_projection_object(object_rows, chapter_ref, workspace_id, f"chapter:{chapter['chapter_id']}", chapter, chapter.get("created_at"), chapter.get("updated_at"), mime_type="text/plain")
    for chapter_id, scenes in STORE.source_scenes_by_chapter.items():
        for scene in scenes:
            workspace_id = scene.get("workspace_id") or STORE.books.get(scene.get("book_id"), {}).get("workspace_id", default_workspace_id())
            _register_projection_object(object_rows, f"object://source-scenes/{scene['scene_id']}", workspace_id, f"source-scene:{scene['scene_id']}", scene, scene.get("created_at"), scene.get("updated_at"))
    for scene_id, events in STORE.events_by_scene.items():
        for event in events:
            workspace_id = event.get("workspace_id") or STORE.books.get(event.get("book_id"), {}).get("workspace_id", default_workspace_id())
            _register_projection_object(object_rows, f"object://story-events/{event['event_id']}", workspace_id, f"story-event:{event['event_id']}", event, event.get("created_at"), event.get("updated_at"))
    for field_name, prefix, owner_prefix in (
        ("conflicts", "story-conflicts", "story-conflict"),
        ("hooks", "story-hooks", "story-hook"),
        ("rewards", "story-rewards", "story-reward"),
        ("climaxes", "story-climaxes", "story-climax"),
        ("relationship_edges", "relationship-edges", "relationship-edge"),
    ):
        for item_id, item in getattr(STORE, field_name).items():
            workspace_id = item.get("workspace_id") or STORE.books.get(item.get("book_id"), {}).get("workspace_id", default_workspace_id())
            _register_projection_object(object_rows, f"object://{prefix}/{item_id}", workspace_id, f"{owner_prefix}:{item_id}", item, item.get("created_at"), item.get("updated_at"))
    for run_id, run in STORE.extraction_runs.items():
        _register_projection_object(object_rows, f"object://extraction-run/{run_id}", run["workspace_id"], f"extraction-run:{run_id}", run, run.get("created_at"), run.get("finished_at") or run.get("started_at") or run.get("created_at"))
        extraction_created_at = run.get("created_at")
        extraction_updated_at = run.get("finished_at") or run.get("started_at") or run.get("created_at")
        if run.get("knowledge_package_ref"):
            _register_projection_object(
                object_rows,
                run["knowledge_package_ref"],
                run["workspace_id"],
                f"extraction-run:{run_id}",
                _json_artifact_payload(
                    run["knowledge_package_ref"],
                    {
                        "run_id": run_id,
                        "book_id": run["book_id"],
                        "current_stage": run.get("current_stage"),
                        "knowledge_object_refs": [f"object://knowledge-objects/{object_id}" for object_id in STORE.knowledge_by_run.get(run_id, [])],
                    },
                    run_id=run_id,
                    book_id=run["book_id"],
                ),
                extraction_created_at,
                extraction_updated_at,
                mime_type="application/json",
                overwrite=False,
            )
        if run.get("graph_package_ref"):
            _register_projection_object(
                object_rows,
                run["graph_package_ref"],
                run["workspace_id"],
                f"extraction-run:{run_id}",
                _json_artifact_payload(
                    run["graph_package_ref"],
                    STORE.graph_summaries.get(run["book_id"], {}),
                    run_id=run_id,
                    book_id=run["book_id"],
                ),
                extraction_created_at,
                extraction_updated_at,
                mime_type="application/json",
                overwrite=False,
            )
        if run.get("extraction_report_ref"):
            _register_projection_object(
                object_rows,
                run["extraction_report_ref"],
                run["workspace_id"],
                f"extraction-run:{run_id}",
                _json_artifact_payload(
                    run["extraction_report_ref"],
                    {
                        "run_id": run_id,
                        "status": run.get("status"),
                        "current_stage": run.get("current_stage"),
                        "chapter_count": run.get("chapter_count"),
                        "scene_count": run.get("scene_count"),
                        "object_count": run.get("object_count"),
                        "evidence_count": run.get("evidence_count"),
                        "low_confidence_count": run.get("low_confidence_count"),
                        "errors": deepcopy(run.get("errors", [])),
                    },
                    run_id=run_id,
                    book_id=run["book_id"],
                ),
                extraction_created_at,
                extraction_updated_at,
                mime_type="application/json",
                overwrite=False,
            )
        if run.get("quality_report_ref"):
            low_confidence_items = [
                deepcopy(STORE.knowledge_objects[object_id])
                for object_id in STORE.knowledge_by_run.get(run_id, [])
                if object_id in STORE.knowledge_objects
                and STORE.knowledge_objects[object_id].get("confidence", 1) < 0.8
                and STORE.knowledge_objects[object_id].get("review_status") == "pending"
            ]
            _register_projection_object(
                object_rows,
                run["quality_report_ref"],
                run["workspace_id"],
                f"extraction-run:{run_id}",
                _json_artifact_payload(
                    run["quality_report_ref"],
                    {
                        "run_id": run_id,
                        "status": run.get("status"),
                        "low_confidence_count": run.get("low_confidence_count"),
                        "low_confidence_items": low_confidence_items,
                    },
                    run_id=run_id,
                    book_id=run["book_id"],
                ),
                extraction_created_at,
                extraction_updated_at,
                mime_type="application/json",
                overwrite=False,
            )
    for object_id, obj in STORE.knowledge_objects.items():
        _register_projection_object(object_rows, f"object://knowledge-object/{object_id}", obj["workspace_id"], f"knowledge-object:{object_id}", obj, obj.get("created_at"), obj.get("updated_at"))
    for node_id, node in STORE.graph_node_details.items():
        _register_projection_object(object_rows, f"object://graph-node/{node_id}", node.get("workspace_id", default_workspace_id()), f"graph-node:{node_id}", {**node, "neighbors": STORE.graph_neighbors_by_node.get(node_id, [])}, node.get("created_at"), node.get("updated_at"))
    for book_id, summary in STORE.graph_summaries.items():
        _register_projection_object(object_rows, f"object://graph-summary/{book_id}", summary.get("workspace_id", default_workspace_id()), f"graph-summary:{book_id}", summary, summary.get("created_at"), summary.get("updated_at"))
    for project_id, project in STORE.novel_projects.items():
        _register_projection_object(object_rows, f"object://novel-project/{project_id}", project["workspace_id"], f"novel-project:{project_id}", project, project.get("created_at"), project.get("updated_at"))
    for story_bible_id, story_bible in STORE.story_bibles.items():
        _register_projection_object(object_rows, f"object://story-bible/{story_bible_id}", story_bible["workspace_id"], f"story-bible:{story_bible_id}", story_bible, story_bible.get("created_at"), story_bible.get("updated_at"))
    for chapter_plan_id, chapter_plan in STORE.chapter_plans.items():
        _register_projection_object(object_rows, f"object://chapter-plan/{chapter_plan_id}", chapter_plan["workspace_id"], f"chapter-plan:{chapter_plan_id}", chapter_plan, chapter_plan.get("created_at"), chapter_plan.get("updated_at"))
    for chapter_plan_id, sections in STORE.section_plans_by_chapter.items():
        for section in sections:
            _register_projection_object(object_rows, f"object://section-plan/{section['section_plan_id']}", section["workspace_id"], f"section-plan:{section['section_plan_id']}", section, section.get("created_at"), section.get("updated_at"))
    for package_id, package in STORE.memory_packages.items():
        _register_projection_object(object_rows, f"object://memory-package/{package_id}", package["workspace_id"], f"memory-package:{package_id}", package, package.get("created_at"), package.get("updated_at"))
    for package_id, package in STORE.prompt_packages.items():
        _register_projection_object(object_rows, f"object://prompt-package/{package_id}", package["workspace_id"], f"prompt-package:{package_id}", package, package.get("created_at"), package.get("updated_at"))
    for writing_run_id, writing_run in STORE.writing_runs.items():
        _register_projection_object(object_rows, f"object://writing-run/{writing_run_id}", writing_run["workspace_id"], f"writing-run:{writing_run_id}", writing_run, writing_run.get("created_at"), writing_run.get("updated_at"))
    for writing_run_id, section_runs in STORE.section_runs_by_writing.items():
        workspace_id = STORE.writing_runs.get(writing_run_id, {}).get("workspace_id", default_workspace_id())
        for section_run in section_runs:
            draft_ref = section_run.get("draft_object_ref")
            if draft_ref:
                _register_projection_object(
                    object_rows,
                    draft_ref,
                    workspace_id,
                    f"section-run:{section_run['section_run_id']}",
                    _text_artifact_payload(
                        draft_ref,
                        section_run.get("writer_output"),
                        section_run_id=section_run["section_run_id"],
                        writing_run_id=section_run["writing_run_id"],
                        section_plan_id=section_run.get("section_plan_id"),
                    ),
                    section_run.get("created_at"),
                    section_run.get("updated_at"),
                    mime_type="text/plain; charset=utf-8",
                )
            critic_ref = section_run.get("critic_report_ref")
            if critic_ref:
                _register_projection_object(
                    object_rows,
                    critic_ref,
                    workspace_id,
                    f"section-run:{section_run['section_run_id']}",
                    _json_artifact_payload(
                        critic_ref,
                        section_run.get("critic_issues", []),
                        section_run_id=section_run["section_run_id"],
                        writing_run_id=section_run["writing_run_id"],
                        section_plan_id=section_run.get("section_plan_id"),
                        status=section_run.get("status"),
                    ),
                    section_run.get("created_at"),
                    section_run.get("updated_at"),
                    mime_type="application/json",
                )
            humanized_ref = section_run.get("humanized_object_ref")
            if humanized_ref:
                _register_projection_object(
                    object_rows,
                    humanized_ref,
                    workspace_id,
                    f"section-run:{section_run['section_run_id']}",
                    _text_artifact_payload(
                        humanized_ref,
                        section_run.get("humanized_text"),
                        section_run_id=section_run["section_run_id"],
                        writing_run_id=section_run["writing_run_id"],
                        section_plan_id=section_run.get("section_plan_id"),
                    ),
                    section_run.get("created_at"),
                    section_run.get("updated_at"),
                    mime_type="text/plain; charset=utf-8",
                )
            _register_projection_object(object_rows, f"object://section-run/{section_run['section_run_id']}", workspace_id, f"section-run:{section_run['section_run_id']}", section_run, section_run.get("created_at"), section_run.get("updated_at"))
    for report_id, report in STORE.quality_reports.items():
        _register_projection_object(object_rows, f"object://quality-report/{report_id}", report["workspace_id"], f"quality-report:{report_id}", report, report.get("created_at"), report.get("updated_at"))
    for report_id, report in STORE.consistency_reports.items():
        _register_projection_object(object_rows, f"object://consistency-report/{report_id}", report["workspace_id"], f"consistency-report:{report_id}", report, report.get("created_at"), report.get("updated_at"))
        for issue in report.get("issues", []):
            note_ref = issue.get("note") if isinstance(issue.get("note"), str) and str(issue.get("note", "")).startswith("object://") else None
            if note_ref:
                _register_projection_object(
                    object_rows,
                    note_ref,
                    report["workspace_id"],
                    f"consistency-report:{report_id}",
                    _text_artifact_payload(note_ref, issue.get("note"), consistency_report_id=report_id, issue_id=issue.get("issue_id")),
                    report.get("updated_at") or report.get("created_at"),
                    report.get("updated_at") or report.get("created_at"),
                    mime_type="text/plain; charset=utf-8",
                    overwrite=False,
                )
    for summary_id, summary in STORE.revision_summaries.items():
        _register_projection_object(object_rows, f"object://revision-summary/{summary_id}", summary["workspace_id"], f"revision-summary:{summary_id}", summary, summary.get("created_at"), summary.get("updated_at"))
        reviewer_note_ref = summary.get("reviewer_note_ref")
        if reviewer_note_ref:
            _register_projection_object(
                object_rows,
                reviewer_note_ref,
                summary["workspace_id"],
                f"revision-summary:{summary_id}",
                _text_artifact_payload(reviewer_note_ref, summary.get("change_summary"), revision_summary_id=summary_id, writing_run_id=summary.get("writing_run_id")),
                summary.get("created_at"),
                summary.get("updated_at"),
                mime_type="text/plain; charset=utf-8",
                overwrite=False,
            )
    for snapshot_id, snapshot in STORE.chapter_snapshots.items():
        workspace_id = STORE.writing_runs.get(snapshot["writing_run_id"], {}).get("workspace_id", default_workspace_id())
        chapter_text = snapshot.get("chapter_text", "")
        chapter_checksum = f"sha256:{hashlib.sha256(chapter_text.encode('utf-8')).hexdigest()}"
        _register_projection_object(
            object_rows,
            f"object://chapter-snapshot/{snapshot_id}",
            workspace_id,
            f"chapter-snapshot:{snapshot_id}",
            {
                **snapshot,
                "checksum": chapter_checksum,
                "byte_size": len(chapter_text.encode("utf-8")),
                "mime_type": "text/plain; charset=utf-8",
            },
            snapshot.get("created_at"),
            snapshot.get("created_at"),
        )
        accepted_chapter_ref = snapshot.get("accepted_chapter_ref")
        if accepted_chapter_ref:
            _register_projection_object(
                object_rows,
                accepted_chapter_ref,
                workspace_id,
                f"chapter-snapshot:{snapshot_id}",
                {
                    "accepted_chapter_ref": accepted_chapter_ref,
                    "chapter_snapshot_id": snapshot_id,
                    "chapter_text": chapter_text,
                    "mime_type": "text/plain; charset=utf-8",
                    "byte_size": len(chapter_text.encode("utf-8")),
                    "checksum": chapter_checksum,
                },
                snapshot.get("created_at"),
                snapshot.get("created_at"),
                mime_type="text/plain; charset=utf-8",
                overwrite=False,
            )
    for project_id, state in STORE.manuscript_states_by_project.items():
        _register_projection_object(object_rows, f"object://manuscript-state/{project_id}", state.get("project_id") and STORE.novel_projects.get(state["project_id"], {}).get("workspace_id", default_workspace_id()) or default_workspace_id(), f"manuscript-state:{project_id}", state, state.get("updated_at"), state.get("updated_at"))
    for feedback_id, record in STORE.feedback_records.items():
        _register_projection_object(object_rows, f"object://feedback-record/{feedback_id}", record["workspace_id"], f"feedback-record:{feedback_id}", record, record.get("created_at"), record.get("updated_at"))
        comment_ref = record.get("comment_ref")
        if comment_ref:
            _register_projection_object(
                object_rows,
                comment_ref,
                record["workspace_id"],
                f"feedback-record:{feedback_id}",
                _text_artifact_payload(
                    comment_ref,
                    (record.get("payload") or {}).get("summary"),
                    feedback_record_id=feedback_id,
                    target_type=record.get("target_type"),
                    target_id=record.get("target_id"),
                    feedback_type=record.get("feedback_type"),
                ),
                record.get("created_at"),
                record.get("updated_at"),
                mime_type="text/plain; charset=utf-8",
                overwrite=False,
            )
    for ranking_key, snapshot in STORE.ranking_snapshots.items():
        _register_projection_object(object_rows, f"object://ranking/{ranking_key}", snapshot.get("workspace_id", default_workspace_id()), f"ranking:{ranking_key}", snapshot, snapshot.get("created_at"), snapshot.get("updated_at"))
    for pattern_id, pattern in STORE.patterns.items():
        _register_projection_object(object_rows, f"object://pattern/{pattern_id}", pattern["workspace_id"], f"pattern:{pattern_id}", pattern, pattern.get("created_at"), pattern.get("updated_at"))
    for profile_id, profile in STORE.rhythm_profiles.items():
        _register_projection_object(object_rows, f"object://rhythm-profile/{profile_id}", profile["workspace_id"], f"rhythm-profile:{profile_id}", profile, profile.get("created_at"), profile.get("updated_at"))
    for asset_id, asset in STORE.assets.items():
        _register_projection_object(object_rows, f"object://asset/{asset_id}", asset["workspace_id"], f"asset:{asset_id}", asset, asset.get("created_at"), asset.get("updated_at"))
    for rule_id, rule in STORE.rules.items():
        _register_projection_object(object_rows, f"object://rule/{rule_id}", rule["workspace_id"], f"rule:{rule_id}", rule, rule.get("created_at"), rule.get("updated_at"))
    for profile_id, profile in STORE.model_profiles.items():
        _register_projection_object(object_rows, f"object://model-profile/{profile_id}", profile.get("workspace_id", default_workspace_id()), f"model-profile:{profile_id}", profile, profile.get("created_at"), profile.get("updated_at"))
    for account_id, account in STORE.provider_accounts.items():
        _register_projection_object(object_rows, f"object://provider-account/{account_id}", account.get("workspace_id", default_workspace_id()), f"provider-account:{account_id}", account, account.get("created_at"), account.get("updated_at"))
    for profile_id, profile in STORE.quality_gate_profiles.items():
        _register_projection_object(object_rows, f"object://quality-profile/{profile_id}", profile.get("workspace_id", default_workspace_id()), f"quality-profile:{profile_id}", profile, profile.get("created_at"), profile.get("updated_at"))
    for prompt_version in STORE.prompt_versions:
        prompt_ref = f"object://prompt-version/{prompt_version['agent_role']}"
        _register_projection_object(object_rows, prompt_ref, prompt_version.get("workspace_id", default_workspace_id()), f"prompt-version:{prompt_version['agent_role']}", prompt_version, prompt_version.get("created_at"), prompt_version.get("updated_at"))

    task_sources = [
        *[run["task"] for run in STORE.extraction_runs.values() if run.get("task")],
        *STORE.chapter_plan_tasks.values(),
        *STORE.section_plan_tasks.values(),
        *STORE.writing_run_tasks.values(),
        *STORE.agent_tasks.values(),
    ]
    for task in task_sources:
        status = task.get("status", "queued")
        task_kind, entity_id = _projection_task_record(task["task_id"])
        task_rows.append(
            {
                "task_id": task["task_id"],
                "workspace_id": task["workspace_id"],
                "task_type": task["task_type"],
                "owner_module": task.get("owner_module", "ai-worker"),
                "status": status,
                "progress": task.get("progress", 0),
                "idempotency_key": task["idempotency_key"],
                "request_id": task.get("request_id"),
                "trace_id": task.get("trace_id"),
                "actor_id": task.get("actor_id"),
                "retry_count": task.get("retry_count", 0),
                "max_retry_count": task.get("max_retry_count", 3),
                "latency_ms": task.get("latency_ms"),
                "error_code": task.get("error_code"),
                "lease_owner": task.get("lease_owner"),
                "lease_expires_at": task.get("lease_expires_at"),
                "heartbeat_at": task.get("heartbeat_at"),
                "next_retry_at": task.get("next_retry_at"),
                "review_required": task.get("review_required", status == "requires_review"),
                "blocked_reason": task.get("blocked_reason"),
                "input_refs": deepcopy(task.get("input_refs", [])),
                "output_refs": deepcopy(task.get("output_refs", [])),
                "created_at": task.get("created_at"),
                "started_at": task.get("started_at"),
                "finished_at": task.get("finished_at"),
                "payload": {
                    "task_kind": task_kind,
                    "entity_id": entity_id,
                    "current_dispatch_token": task.get("current_dispatch_token"),
                    "dispatch_attempt": task.get("dispatch_attempt", 0),
                },
                "updated_at": task.get("finished_at") or task.get("started_at") or task.get("created_at"),
            }
        )
        lock_row = _build_task_lock_row(task)
        if lock_row:
            task_lock_rows.append(lock_row)
        for ref in [*task.get("input_refs", []), *task.get("output_refs", [])]:
            _register_projection_object(object_rows, ref, task["workspace_id"], f"task:{task['task_id']}", {"task_id": task["task_id"], "ref": ref}, task.get("created_at"), task.get("finished_at") or task.get("started_at") or task.get("created_at"), access_policy="task", overwrite=False)

    for events in STORE.task_events_by_task.values():
        for event in events:
            task_event_rows.append({**deepcopy(event), "updated_at": event.get("updated_at") or event.get("created_at")})
    for event in STORE.audit_events:
        audit_rows.append({**deepcopy(event), "updated_at": event.get("updated_at") or event.get("created_at")})

    return {
        "objects": sorted(object_rows.values(), key=lambda item: item["object_ref"]),
        "tasks": sorted(task_rows, key=lambda item: (item.get("created_at") or "", item["task_id"])),
        "task_locks": sorted(task_lock_rows, key=lambda item: item["task_id"]),
        "task_events": sorted(task_event_rows, key=lambda item: (item.get("created_at") or "", item["task_event_id"])),
        "audit_events": sorted(audit_rows, key=lambda item: (item.get("created_at") or "", item["audit_event_id"])),
    }


def _sync_runtime_projection() -> None:
    projection = _build_runtime_projection()
    sync_runtime_projection(
        objects=projection["objects"],
        tasks=projection["tasks"],
        task_locks=projection["task_locks"],
        task_events=projection["task_events"],
        audit_events=projection["audit_events"],
    )


def _restore_runtime_projection() -> None:
    projection = load_runtime_projection()
    if not projection["tasks"] and not projection.get("task_locks") and not projection["task_events"] and not projection["audit_events"]:
        return
    events_by_task = {task_id: [] for task_id in STORE.task_events_by_task}
    for event in projection["task_events"]:
        events_by_task.setdefault(event["task_id"], []).append(deepcopy(event))
    task_locks_by_task = {item["task_id"]: item for item in projection.get("task_locks", [])}
    for task in projection["tasks"]:
        payload = task.get("payload") or {}
        task_kind = payload.get("task_kind")
        entity_id = payload.get("entity_id")
        if not task_kind:
            task_kind, entity_id = _projection_task_record(task["task_id"])
        lock = task_locks_by_task.get(task["task_id"], {})
        restored_task = {
            "schema_version": 1,
            "task_id": task["task_id"],
            "task_type": task["task_type"],
            "workspace_id": task["workspace_id"],
            "owner_module": task.get("owner_module", "ai-worker"),
            "status": task["status"],
            "progress": task.get("progress", 0),
            "idempotency_key": task["idempotency_key"],
            "request_id": task.get("request_id"),
            "trace_id": task.get("trace_id"),
            "actor_id": task.get("actor_id"),
            "retry_count": task.get("retry_count", 0),
            "max_retry_count": task.get("max_retry_count", 3),
            "latency_ms": task.get("latency_ms"),
            "error_code": task.get("error_code"),
            "lease_owner": lock.get("lock_owner", task.get("lease_owner")),
            "lease_expires_at": _normalize_timestamp_string(lock.get("lease_expires_at", task.get("lease_expires_at"))),
            "heartbeat_at": _normalize_timestamp_string(lock.get("heartbeat_at", task.get("heartbeat_at"))),
            "current_dispatch_token": payload.get("current_dispatch_token"),
            "dispatch_attempt": payload.get("dispatch_attempt", 0),
            "next_retry_at": _normalize_timestamp_string(task.get("next_retry_at")),
            "review_required": task.get("review_required", False),
            "blocked_reason": task.get("blocked_reason"),
            "input_refs": deepcopy(task.get("input_refs", [])),
            "output_refs": deepcopy(task.get("output_refs", [])),
            "created_at": _normalize_timestamp_string(task.get("created_at")),
            "started_at": _normalize_timestamp_string(task.get("started_at")),
            "finished_at": _normalize_timestamp_string(task.get("finished_at")),
        }
        if task_kind == "extraction_run" and entity_id:
            run = STORE.extraction_runs.get(entity_id)
            if not run:
                continue
            run["task"] = {**deepcopy(run.get("task", {})), **restored_task}
        elif task_kind == "chapter_plan" and entity_id:
            STORE.chapter_plan_tasks[entity_id] = {
                **deepcopy(STORE.chapter_plan_tasks.get(entity_id, {})),
                **restored_task,
            }
        elif task_kind == "section_plan" and entity_id:
            STORE.section_plan_tasks[entity_id] = {
                **deepcopy(STORE.section_plan_tasks.get(entity_id, {})),
                **restored_task,
            }
        elif task_kind == "writing_run" and entity_id:
            STORE.writing_run_tasks[entity_id] = {
                **deepcopy(STORE.writing_run_tasks.get(entity_id, {})),
                **restored_task,
            }
        elif task_kind == "agent_task":
            STORE.agent_tasks[task["task_id"]] = {
                **deepcopy(STORE.agent_tasks.get(task["task_id"], {})),
                **restored_task,
            }
    STORE.task_events_by_task = events_by_task
    STORE.audit_events = [deepcopy(event) for event in projection["audit_events"]]
    STORE.migration_events = [deepcopy(event) for event in getattr(STORE, "migration_events", [])]



def _persist_store() -> None:
    state = asdict(STORE)
    save_business_state(state)
    save_snapshot(state)
    _sync_runtime_projection()


def _persisting_mutation(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        _persist_store()
        return result

    return wrapper


def _restore_store_from_business_tables() -> bool:
    snapshot = load_business_state()
    if snapshot is None or not isinstance(snapshot, dict):
        return False
    field_names = set(CoreStore.__dataclass_fields__)
    if not set(snapshot).issubset(field_names):
        return False
    try:
        restored = CoreStore(**snapshot)
    except TypeError:
        return False
    for field_name in CoreStore.__dataclass_fields__:
        setattr(STORE, field_name, getattr(restored, field_name))
    STORE.migration_events = [deepcopy(event) for event in getattr(restored, "migration_events", [])]
    return True


def _restore_store_from_snapshot() -> bool:
    snapshot = load_snapshot()
    if snapshot is None or not isinstance(snapshot, dict):
        return False
    field_names = set(CoreStore.__dataclass_fields__)
    if not set(snapshot).issubset(field_names):
        return False
    try:
        restored = CoreStore(**snapshot)
    except TypeError:
        return False
    for field_name in CoreStore.__dataclass_fields__:
        setattr(STORE, field_name, getattr(restored, field_name))
    STORE.migration_events = [deepcopy(event) for event in getattr(restored, "migration_events", [])]
    return True


def reset_store() -> None:
    STORE.users.clear()
    STORE.workspaces.clear()
    STORE.workspace_members.clear()
    STORE.books.clear()
    STORE.source_contents.clear()
    STORE.source_content_by_book.clear()
    STORE.evidences.clear()
    STORE.evidence_by_book.clear()
    STORE.evidence_by_run.clear()
    STORE.chapters_by_book.clear()
    STORE.source_scenes_by_chapter.clear()
    STORE.events_by_scene.clear()
    STORE.conflicts.clear()
    STORE.hooks.clear()
    STORE.rewards.clear()
    STORE.climaxes.clear()
    STORE.relationship_edges.clear()
    STORE.extraction_runs.clear()
    STORE.knowledge_objects.clear()
    STORE.knowledge_by_run.clear()
    STORE.graph_summaries.clear()
    STORE.graph_node_details.clear()
    STORE.graph_neighbors_by_node.clear()
    STORE.novel_projects.clear()
    STORE.story_bibles.clear()
    STORE.chapter_plans.clear()
    STORE.chapter_plan_tasks.clear()
    STORE.section_plan_tasks.clear()
    STORE.section_plans_by_chapter.clear()
    STORE.model_profiles.clear()
    STORE.agent_model_assignments.clear()
    STORE.provider_accounts.clear()
    STORE.quality_gate_profiles.clear()
    STORE.prompt_versions.clear()
    STORE.writing_runs.clear()
    STORE.writing_run_tasks.clear()
    STORE.provider_calls_by_writing.clear()
    STORE.section_runs_by_writing.clear()
    STORE.memory_packages.clear()
    STORE.prompt_packages.clear()
    STORE.quality_reports.clear()
    STORE.consistency_reports.clear()
    STORE.revision_summaries.clear()
    STORE.rules.clear()
    STORE.chapter_snapshots.clear()
    STORE.manuscript_states_by_project.clear()
    STORE.feedback_records.clear()
    STORE.ranking_snapshots.clear()
    STORE.patterns.clear()
    STORE.rhythm_profiles.clear()
    STORE.assets.clear()
    STORE.agent_tasks.clear()
    STORE.task_events_by_task.clear()
    STORE.audit_events.clear()
    STORE.migration_events.clear()
    STORE.knowledge_packages.clear()
    _persist_store()


def seed_phase_two_demo_data() -> None:
    if STORE.books:
        return

    STORE.users[USER_ID] = {
        "schema_version": 1,
        "user_id": USER_ID,
        "display_name": "演示作者",
        "status": "active",
        "created_at": "2026-07-11T00:00:00Z",
        "updated_at": "2026-07-11T00:10:00Z",
    }
    STORE.workspaces[WORKSPACE_ID] = {
        "schema_version": 1,
        "workspace_id": _workspace_or_default(),
        "owner_user_id": USER_ID,
        "name": "默认中文工作区",
        "slug": WORKSPACE_ID,
        "default_language": "zh-CN",
        "status": "active",
        "created_at": "2026-07-11T00:00:00Z",
        "updated_at": "2026-07-11T00:10:00Z",
    }
    STORE.workspace_members[WORKSPACE_MEMBER_ID] = {
        "schema_version": 1,
        "workspace_member_id": WORKSPACE_MEMBER_ID,
        "workspace_id": _workspace_or_default(),
        "user_id": USER_ID,
        "role": "owner",
        "status": "active",
        "created_at": "2026-07-11T00:00:00Z",
        "updated_at": "2026-07-11T00:10:00Z",
    }

    book = {
        "schema_version": 1,
        "book_id": BOOK_ID,
        "workspace_id": _workspace_or_default(),
        "title": "Battle Through the Heavens",
        "author_name": "Tian Can Tu Dou",
        "source_type": "reference_novel",
        "import_status": "ready",
        "trace_id": "01JZTRC000000000000000001",
        "created_at": "2026-07-11T00:00:00Z",
        "updated_at": "2026-07-11T00:10:00Z",
    }
    STORE.books[BOOK_ID] = book
    STORE.chapters_by_book[BOOK_ID] = [
        {
            "schema_version": 1,
            "chapter_id": "01JZCHAPTER00000000000001",
            "book_id": BOOK_ID,
            "chapter_index": 1,
            "title": "Three-Year Agreement",
            "segmentation_status": "segmented",
            "text_object_ref": "object://source-chapters/01JZCHAPTER00000000000001",
        },
        {
            "schema_version": 1,
            "chapter_id": "01JZCHAPTER00000000000002",
            "book_id": BOOK_ID,
            "chapter_index": 2,
            "title": "Yao Lao Appears",
            "segmentation_status": "segmented",
            "text_object_ref": "object://source-chapters/01JZCHAPTER00000000000002",
        },
    ]
    llm_provider = os.getenv("NOVELIST_LLM_PROVIDER", "anthropic")
    llm_model = os.getenv("NOVELIST_LLM_MODEL", "claude-sonnet-5")
    llm_structured_model = os.getenv("NOVELIST_LLM_STRUCTURED_MODEL", "claude-haiku-4-5-20251001")
    provider_account_id = f"provider-account-{llm_provider}-default"
    STORE.model_profiles[MODEL_PROFILE_DEFAULT_ID] = {
        "schema_version": 1,
        "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
        "provider_name": llm_provider,
        "provider_model_name": llm_model,
        "label": "默认中文长文本模型",
        "description": "大多数 Agent role 默认使用。",
        "enabled": True,
        "supports_structured_output": False,
        "fallback_profile_ids": [MODEL_PROFILE_STRUCTURED_FALLBACK_ID],
    }
    STORE.model_profiles[MODEL_PROFILE_STRUCTURED_FALLBACK_ID] = {
        "schema_version": 1,
        "model_profile_id": MODEL_PROFILE_STRUCTURED_FALLBACK_ID,
        "provider_name": llm_provider,
        "provider_model_name": llm_structured_model,
        "label": "结构化兜底模型",
        "description": "结构化输出失败后重试使用。",
        "enabled": True,
        "supports_structured_output": True,
        "fallback_profile_ids": [],
    }
    STORE.provider_accounts[provider_account_id] = {
        "provider_account_id": provider_account_id,
        "provider_name": llm_provider,
        "account_label": f"{llm_provider} 默认账号",
        "secret_ref": f"secret://providers/{llm_provider}/default",
        "status": "active",
        "created_at": "2026-07-11T00:00:00Z",
        "updated_at": "2026-07-11T00:10:00Z",
    }
    for index, role in enumerate(MVP_AGENT_ROLES, start=1):
        output_mode = "structured" if role in {"critic", "review", "feedback"} else "text"
        STORE.agent_model_assignments[f"01JZASSIGN{index:015d}"] = {
            "schema_version": 1,
            "assignment_id": f"01JZASSIGN{index:015d}",
            "agent_role": role,
            "task_type": f"{role}_task",
            "output_mode": output_mode,
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "fallback_profile_ids": [MODEL_PROFILE_STRUCTURED_FALLBACK_ID] if output_mode == "structured" or role in {"writer", "humanizer"} else [],
            "max_retry": 2 if role == "critic" else 1,
            "max_cost": 1.5 if role == "writer" else 0.8,
            "enabled": True,
        }
    STORE.quality_gate_profiles[QUALITY_GATE_PROFILE_ID] = {
        "quality_gate_profile_id": QUALITY_GATE_PROFILE_ID,
        "workspace_id": _workspace_or_default(),
        "trace_id": "trace-config-snapshot",
        "label": "默认质量阈值",
        "ai_flavor_threshold": 0.45,
        "originality_safety_threshold": 0.85,
        "input_refs": ["object://config/default-quality-thresholds"],
        "output_refs": [f"object://quality-gate-profiles/{QUALITY_GATE_PROFILE_ID}"],
    }
    STORE.prompt_versions.extend(
        [
            {"agent_role": "writer", "template_ref": "prompt://writer/chapter-default"},
            {"agent_role": "critic", "template_ref": "prompt://critic/chapter-default"},
            {"agent_role": "humanizer", "template_ref": "prompt://humanizer/chapter-default"},
            {"agent_role": "feedback", "template_ref": "prompt://feedback/chapter-default"},
        ]
    )

    knowledge_objects = [
        {
            "schema_version": 1,
            "object_id": "01JZOBJ0000000000000000001",
            "workspace_id": _workspace_or_default(),
            "object_type": "character",
            "canonical_name": "Xiao Yan",
            "lifecycle_status": "candidate",
            "review_status": "pending",
            "confidence": 0.58,
            "evidence_refs": ["evidence://01JZEVIDENCE0000000000001"],
            "payload": {"schema_version": 1, "aliases": ["Yan"]},
        },
        {
            "schema_version": 1,
            "object_id": "01JZOBJ0000000000000000002",
            "workspace_id": _workspace_or_default(),
            "object_type": "mentor",
            "canonical_name": "Yao Lao",
            "lifecycle_status": "candidate",
            "review_status": "pending",
            "confidence": 0.44,
            "evidence_refs": ["evidence://01JZEVIDENCE0000000000002"],
            "payload": {"schema_version": 1, "aliases": ["Old Yao"]},
        },
        {
            "schema_version": 1,
            "object_id": "01JZOBJ0000000000000000003",
            "workspace_id": _workspace_or_default(),
            "object_type": "clan",
            "canonical_name": "Xiao Clan",
            "lifecycle_status": "approved",
            "review_status": "approved",
            "confidence": 0.97,
            "evidence_refs": ["evidence://01JZEVIDENCE0000000000003"],
            "payload": {"schema_version": 1, "aliases": []},
        },
    ]
    for obj in knowledge_objects:
        STORE.knowledge_objects[obj["object_id"]] = obj
    STORE.knowledge_by_run[RUN_ID] = [obj["object_id"] for obj in knowledge_objects]
    seeded_evidences = [
        {
            "schema_version": 1,
            "evidence_id": "01JZEVIDENCE0000000000001",
            "evidence_ref": "evidence://01JZEVIDENCE0000000000001",
            "book_id": BOOK_ID,
            "chapter_id": "01JZCHAPTER00000000000001",
            "chapter_index": 1,
            "text_range": "c1:p5-p8",
            "excerpt": "萧炎沉默地站在大厅中央，所有目光都落在他身上，少年把羞辱压进喉间。",
            "source_object_refs": ["object://knowledge-objects/01JZOBJ0000000000000000001"],
            "source_content_ref": f"object://source-books/{BOOK_ID}",
            "confidence": 0.58,
            "trace_id": "01JZTRC000000000000000001",
        },
        {
            "schema_version": 1,
            "evidence_id": "01JZEVIDENCE0000000000002",
            "evidence_ref": "evidence://01JZEVIDENCE0000000000002",
            "book_id": BOOK_ID,
            "chapter_id": "01JZCHAPTER00000000000002",
            "chapter_index": 2,
            "text_range": "c2:p4-p8",
            "excerpt": "戒指中传来苍老的低笑，药老第一次点破少年体内异变的根源。",
            "source_object_refs": ["object://knowledge-objects/01JZOBJ0000000000000000002"],
            "source_content_ref": f"object://source-books/{BOOK_ID}",
            "confidence": 0.91,
            "trace_id": "01JZTRC000000000000000001",
        },
        {
            "schema_version": 1,
            "evidence_id": "01JZEVIDENCE0000000000003",
            "evidence_ref": "evidence://01JZEVIDENCE0000000000003",
            "book_id": BOOK_ID,
            "chapter_id": "01JZCHAPTER00000000000001",
            "chapter_index": 1,
            "text_range": "c1:p1-p3",
            "excerpt": "乌坦城萧家议事堂内，家族压力像潮水一样一层层压向少年。",
            "source_object_refs": ["object://knowledge-objects/01JZOBJ0000000000000000003"],
            "source_content_ref": f"object://source-books/{BOOK_ID}",
            "confidence": 0.97,
            "trace_id": "01JZTRC000000000000000001",
        },
    ]
    STORE.evidence_by_run[RUN_ID] = []
    STORE.evidence_by_book[BOOK_ID] = []
    for evidence in seeded_evidences:
        evidence_id = evidence["evidence_id"]
        STORE.evidences[evidence_id] = evidence
        STORE.evidence_by_run[RUN_ID].append(evidence_id)
        STORE.evidence_by_book[BOOK_ID].append(evidence_id)

    STORE.extraction_runs[RUN_ID] = {
        "schema_version": 1,
        "run_id": RUN_ID,
        "book_id": BOOK_ID,
        "workspace_id": _workspace_or_default(),
        "task_id": TASK_ID,
        "status": "requires_review",
        "current_stage": "quality_review",
        "chapter_count": 2,
        "scene_count": 6,
        "object_count": 3,
        "evidence_count": 3,
        "low_confidence_count": 2,
        "knowledge_package_ref": f"object://knowledge-packages/{RUN_ID}",
        "graph_package_ref": f"object://graph-packages/{BOOK_ID}",
        "extraction_report_ref": f"object://extraction-reports/{RUN_ID}",
        "quality_report_ref": f"object://quality-reports/{RUN_ID}",
        "errors": [],
        "created_at": "2026-07-11T00:00:00Z",
        "started_at": "2026-07-11T00:00:05Z",
        "finished_at": None,
        "task": {
            "schema_version": 1,
            "task_id": TASK_ID,
            "task_type": "extract_knowledge",
            "workspace_id": _workspace_or_default(),
            "owner_module": "ai-worker",
            "input_refs": [f"object://source-books/{BOOK_ID}"],
            "output_refs": [
                f"object://extraction-runs/{RUN_ID}",
                f"object://knowledge-packages/{RUN_ID}",
                f"object://graph-packages/{BOOK_ID}",
                f"object://extraction-reports/{RUN_ID}",
                f"object://quality-reports/{RUN_ID}",
            ],
            "status": "requires_review",
            "progress": 88,
            "idempotency_key": f"extract-{BOOK_ID}-001",
            "retry_count": 0,
            "error_code": None,
            "heartbeat_at": None,
            "created_at": "2026-07-11T00:00:00Z",
            "started_at": "2026-07-11T00:00:05Z",
            "finished_at": None,
        },
    }
    STORE.task_events_by_task[TASK_ID] = [
        {
            "schema_version": 1,
            "task_event_id": "01JZEVT000000000000000001",
            "task_id": TASK_ID,
            "event_type": "created",
            "message": "Extraction run created.",
            "payload_ref": None,
            "payload_json": None,
            "created_at": "2026-07-11T00:00:00Z",
        },
        {
            "schema_version": 1,
            "task_event_id": "01JZEVT000000000000000002",
            "task_id": TASK_ID,
            "event_type": "progress",
            "message": "Low confidence objects require review.",
            "payload_ref": None,
            "payload_json": {"current_stage": "quality_review", "low_confidence_count": 2},
            "created_at": "2026-07-11T00:01:00Z",
        },
    ]
    STORE.graph_summaries[GRAPH_BOOK_ID] = {
        "schema_version": 1,
        "book_id": GRAPH_BOOK_ID,
        "node_count": 3,
        "edge_count": 2,
        "nodes": [
            {
                "node_id": "01JZNODE000000000000000001",
                "label": "Xiao Yan",
                "node_type": "character",
                "evidence_refs": ["evidence://01JZEVIDENCE0000000000001"],
            },
            {
                "node_id": "01JZNODE000000000000000002",
                "label": "Yao Lao",
                "node_type": "mentor",
                "evidence_refs": ["evidence://01JZEVIDENCE0000000000002"],
            },
            {
                "node_id": "01JZNODE000000000000000003",
                "label": "Xiao Clan",
                "node_type": "clan",
                "evidence_refs": ["evidence://01JZEVIDENCE0000000000003"],
            },
        ],
    }
    STORE.graph_node_details.update(
        {
            "01JZNODE000000000000000001": {
                "schema_version": 1,
                "node_id": "01JZNODE000000000000000001",
                "book_id": GRAPH_BOOK_ID,
                "label": "Xiao Yan",
                "node_type": "character",
                "canonical_object_id": "01JZOBJ0000000000000000001",
                "review_status": "pending",
                "lifecycle_status": "candidate",
                "confidence": 0.58,
                "aliases": ["Yan"],
                "summary": "乌坦城萧家少年，正处于天赋跌落后的低谷期。",
                "evidence_refs": ["evidence://01JZEVIDENCE0000000000001"],
            },
            "01JZNODE000000000000000002": {
                "schema_version": 1,
                "node_id": "01JZNODE000000000000000002",
                "book_id": GRAPH_BOOK_ID,
                "label": "Yao Lao",
                "node_type": "mentor",
                "canonical_object_id": "01JZOBJ0000000000000000002",
                "review_status": "pending",
                "lifecycle_status": "candidate",
                "confidence": 0.44,
                "aliases": ["Old Yao"],
                "summary": "寄宿戒指中的神秘导师，对主角成长线至关重要。",
                "evidence_refs": ["evidence://01JZEVIDENCE0000000000002"],
            },
            "01JZNODE000000000000000003": {
                "schema_version": 1,
                "node_id": "01JZNODE000000000000000003",
                "book_id": GRAPH_BOOK_ID,
                "label": "Xiao Clan",
                "node_type": "clan",
                "canonical_object_id": "01JZOBJ0000000000000000003",
                "review_status": "approved",
                "lifecycle_status": "approved",
                "confidence": 0.97,
                "aliases": [],
                "summary": "乌坦城本地家族势力，也是主角当前承受压力的核心环境。",
                "evidence_refs": ["evidence://01JZEVIDENCE0000000000003"],
            },
        }
    )
    STORE.graph_neighbors_by_node.update(
        {
            "01JZNODE000000000000000001": [
                {
                    "edge_id": "01JZEDGE000000000000000001",
                    "relation_type": "mentored_by",
                    "direction": "outgoing",
                    "neighbor_node_id": "01JZNODE000000000000000002",
                    "neighbor_label": "Yao Lao",
                    "neighbor_type": "mentor",
                    "confidence": 0.91,
                    "evidence_refs": ["evidence://01JZEVIDENCE0000000000002"],
                },
                {
                    "edge_id": "01JZEDGE000000000000000002",
                    "relation_type": "member_of",
                    "direction": "outgoing",
                    "neighbor_node_id": "01JZNODE000000000000000003",
                    "neighbor_label": "Xiao Clan",
                    "neighbor_type": "clan",
                    "confidence": 0.96,
                    "evidence_refs": ["evidence://01JZEVIDENCE0000000000003"],
                },
            ],
            "01JZNODE000000000000000002": [
                {
                    "edge_id": "01JZEDGE000000000000000001",
                    "relation_type": "mentors",
                    "direction": "incoming",
                    "neighbor_node_id": "01JZNODE000000000000000001",
                    "neighbor_label": "Xiao Yan",
                    "neighbor_type": "character",
                    "confidence": 0.91,
                    "evidence_refs": ["evidence://01JZEVIDENCE0000000000002"],
                },
            ],
            "01JZNODE000000000000000003": [
                {
                    "edge_id": "01JZEDGE000000000000000002",
                    "relation_type": "has_member",
                    "direction": "incoming",
                    "neighbor_node_id": "01JZNODE000000000000000001",
                    "neighbor_label": "Xiao Yan",
                    "neighbor_type": "character",
                    "confidence": 0.96,
                    "evidence_refs": ["evidence://01JZEVIDENCE0000000000003"],
                },
            ],
        }
    )

    project = {
        "schema_version": 1,
        "project_id": PROJECT_ID,
        "workspace_id": _workspace_or_default(),
        "title": "斗破苍穹衍生原创",
        "genre_scope": "玄幻升级流",
        "status": "planning",
        "story_bible_id": STORY_BIBLE_ID,
        "quality_gate_profile_id": QUALITY_GATE_PROFILE_ID,
        "allowed_knowledge_source_refs": [
            f"object://source-books/{BOOK_ID}",
            f"object://graph-summaries/{BOOK_ID}",
        ],
        "created_at": "2026-07-11T02:00:00Z",
        "updated_at": "2026-07-11T02:05:00Z",
    }
    STORE.novel_projects[PROJECT_ID] = project
    STORE.story_bibles[STORY_BIBLE_ID] = {
        "schema_version": 1,
        "story_bible_id": STORY_BIBLE_ID,
        "workspace_id": _workspace_or_default(),
        "project_id": PROJECT_ID,
        "version": 1,
        "status": "approved",
        "payload": {
            "premise": "少年背负退婚耻辱后，踏上逆袭与成长之路。",
            "protagonist": "萧炎",
            "core_conflict": "天赋跌落后的家族压力与三年之约。",
            "style_target": "克制、证据充分、节奏稳步升级。",
            "forbidden_similarities": "不直接复刻原作人物名、金手指机制和关键桥段。",
            "world_rules": ["所有突破都必须付出明确代价。", "家族与宗门冲突都要落到资源争夺上。"],
            "narrative_promises": ["前三章完成主角受辱、立誓和第一条破局线索。", "每卷都兑现一次阶段性胜利。"],
        },
        "confirmed_payload": {
            "premise": "少年背负退婚耻辱后，踏上逆袭与成长之路。",
            "protagonist": "萧炎",
            "core_conflict": "天赋跌落后的家族压力与三年之约。",
            "style_target": "克制、证据充分、节奏稳步升级。",
            "forbidden_similarities": "不直接复刻原作人物名、金手指机制和关键桥段。",
            "world_rules": ["所有突破都必须付出明确代价。", "家族与宗门冲突都要落到资源争夺上。"],
            "narrative_promises": ["前三章完成主角受辱、立誓和第一条破局线索。", "每卷都兑现一次阶段性胜利。"],
        },
        "diff": None,
        "history": [
            {
                "version": 1,
                "status": "approved",
                "change_type": "create",
                "payload": {
                    "premise": "少年背负退婚耻辱后，踏上逆袭与成长之路。",
                    "protagonist": "萧炎",
                    "core_conflict": "天赋跌落后的家族压力与三年之约。",
                    "style_target": "克制、证据充分、节奏稳步升级。",
                    "forbidden_similarities": "不直接复刻原作人物名、金手指机制和关键桥段。",
                    "world_rules": ["所有突破都必须付出明确代价。", "家族与宗门冲突都要落到资源争夺上。"],
                    "narrative_promises": ["前三章完成主角受辱、立誓和第一条破局线索。", "每卷都兑现一次阶段性胜利。"],
                },
                "changed_fields": ["premise", "protagonist", "core_conflict", "style_target", "forbidden_similarities", "world_rules", "narrative_promises"],
                "summary": "建立首版故事圣经。",
                "note": None,
                "trace_id": "01JZTRC000000000000000002",
                "actor_id": USER_ID,
                "created_at": "2026-07-11T02:00:00Z",
            }
        ],
        "trace_id": "01JZTRC000000000000000002",
        "approved_at": "2026-07-11T02:05:00Z",
        "approved_by": USER_ID,
        "created_at": "2026-07-11T02:00:00Z",
        "updated_at": "2026-07-11T02:05:00Z",
    }
    STORE.chapter_plans[CHAPTER_PLAN_ID] = {
        "schema_version": 1,
        "chapter_plan_id": CHAPTER_PLAN_ID,
        "workspace_id": _workspace_or_default(),
        "project_id": PROJECT_ID,
        "chapter_index": 1,
        "status": "requires_review",
        "target_word_count": 3200,
        "payload": {
            "title": "乌坦城风起",
            "summary": "主角在第一章完成进入主线前的势能铺垫。",
        },
        "created_at": "2026-07-11T02:10:00Z",
        "updated_at": "2026-07-11T02:12:00Z",
    }
    STORE.chapter_plan_tasks[CHAPTER_PLAN_ID] = {
        "schema_version": 1,
        "task_id": CHAPTER_PLAN_TASK_ID,
        "task_type": "create_chapter_plan",
        "workspace_id": _workspace_or_default(),
        "owner_module": "ai-worker",
        "input_refs": [f"object://novel-projects/{PROJECT_ID}"],
        "output_refs": [f"object://chapter-plans/{CHAPTER_PLAN_ID}"],
        "status": "requires_review",
        "progress": 100,
        "idempotency_key": f"plan-{PROJECT_ID}-1",
        "retry_count": 0,
        "error_code": None,
        "created_at": "2026-07-11T02:10:00Z",
        "started_at": "2026-07-11T02:10:03Z",
        "finished_at": "2026-07-11T02:12:00Z",
    }
    STORE.task_events_by_task[CHAPTER_PLAN_TASK_ID] = [
        {
            "schema_version": 1,
            "task_event_id": "01JZPLANEVT0000000000001",
            "task_id": CHAPTER_PLAN_TASK_ID,
            "event_type": "created",
            "message": "Chapter plan created.",
            "payload_ref": None,
            "payload_json": {"chapter_index": 1},
            "created_at": "2026-07-11T02:10:00Z",
        },
        {
            "schema_version": 1,
            "task_event_id": "01JZPLANEVT0000000000002",
            "task_id": CHAPTER_PLAN_TASK_ID,
            "event_type": "progress",
            "message": "Chapter plan ready for review.",
            "payload_ref": None,
            "payload_json": {"status": "requires_review"},
            "created_at": "2026-07-11T02:12:00Z",
        },
    ]
    STORE.section_plans_by_chapter[CHAPTER_PLAN_ID] = [
        {
            "schema_version": 1,
            "section_plan_id": "01JZSECT0000000000000001",
            "workspace_id": _workspace_or_default(),
            "chapter_plan_id": CHAPTER_PLAN_ID,
            "section_index": 1,
            "planning_role": "setup",
            "payload": {
                "scene_goal": "建立乌坦城压抑氛围",
                "beats": [
                    {"index": 1, "summary": "主角出场"},
                    {"index": 2, "summary": "家族压力显现"},
                ],
            },
            "created_at": "2026-07-11T02:15:00Z",
            "updated_at": "2026-07-11T02:18:00Z",
        },
        {
            "schema_version": 1,
            "section_plan_id": "01JZSECT0000000000000002",
            "workspace_id": _workspace_or_default(),
            "chapter_plan_id": CHAPTER_PLAN_ID,
            "section_index": 2,
            "planning_role": "conflict",
            "payload": {
                "scene_goal": "压强进一步落到主角身上",
                "beats": [
                    {"index": 1, "summary": "长辈对主角失望"},
                    {"index": 2, "summary": "纳兰家消息传来"},
                ],
            },
            "created_at": "2026-07-11T02:16:00Z",
            "updated_at": "2026-07-11T02:18:00Z",
        },
        {
            "schema_version": 1,
            "section_plan_id": "01JZSECT0000000000000003",
            "workspace_id": _workspace_or_default(),
            "chapter_plan_id": CHAPTER_PLAN_ID,
            "section_index": 3,
            "planning_role": "turn",
            "payload": {
                "scene_goal": "把侮辱转化为主线承诺",
                "beats": [
                    {"index": 1, "summary": "退婚现场升级"},
                    {"index": 2, "summary": "主角立下三年之约"},
                ],
            },
            "created_at": "2026-07-11T02:17:00Z",
            "updated_at": "2026-07-11T02:18:00Z",
        },
    ]
    STORE.section_plan_tasks[CHAPTER_PLAN_ID] = {
        "schema_version": 1,
        "task_id": SECTION_PLAN_TASK_ID,
        "task_type": "create_section_plans",
        "workspace_id": _workspace_or_default(),
        "owner_module": "ai-worker",
        "input_refs": [f"object://chapter-plans/{CHAPTER_PLAN_ID}"],
        "output_refs": [
            "object://section-plans/01JZSECT0000000000000001",
            "object://section-plans/01JZSECT0000000000000002",
            "object://section-plans/01JZSECT0000000000000003",
        ],
        "status": "succeeded",
        "progress": 100,
        "idempotency_key": f"section-{CHAPTER_PLAN_ID}",
        "retry_count": 0,
        "error_code": None,
        "created_at": "2026-07-11T02:15:00Z",
        "started_at": "2026-07-11T02:15:05Z",
        "finished_at": "2026-07-11T02:18:00Z",
    }
    STORE.memory_packages[MEMORY_PACKAGE_ID] = {
        "schema_version": 1,
        "memory_package_id": MEMORY_PACKAGE_ID,
        "workspace_id": _workspace_or_default(),
        "project_id": PROJECT_ID,
        "writing_run_id": WRITING_RUN_ID,
        "summary": "已汇总故事圣经、章节目标、人物状态与来源证据。",
        "source_refs": [
            f"object://story-bibles/{STORY_BIBLE_ID}",
            f"object://chapter-plans/{CHAPTER_PLAN_ID}",
            "object://section-plans/01JZSECT0000000000000001",
            "object://graph-summaries/01JZBOOK000000000000000001",
        ],
        "source_snapshot_id": f"snapshot://knowledge-state/{WRITING_RUN_ID}",
        "created_at": "2026-07-11T03:00:00Z",
        "updated_at": "2026-07-11T03:00:00Z",
    }
    STORE.prompt_packages[PROMPT_PACKAGE_ID] = {
        "schema_version": 1,
        "prompt_package_id": PROMPT_PACKAGE_ID,
        "workspace_id": _workspace_or_default(),
        "project_id": PROJECT_ID,
        "writing_run_id": WRITING_RUN_ID,
        "summary": "写手、批评者与润色器共用同一章级提示包。",
        "template_refs": [
            "prompt://writer/chapter-default",
            "prompt://critic/chapter-default",
            "prompt://humanizer/chapter-default",
        ],
        "created_at": "2026-07-11T03:01:00Z",
        "updated_at": "2026-07-11T03:01:00Z",
    }
    STORE.rules["rule-01JZPOWER000000000000001"] = {
        "schema_version": 1,
        "rule_id": "rule-01JZPOWER000000000000001",
        "workspace_id": _workspace_or_default(),
        "trace_id": "trace-rule-power",
        "rule_type": "power_system_constraint",
        "title": "境界不能倒退",
        "severity": "critical",
        "status": "approved",
        "scope_type": "project",
        "scope_ref": "project://01JZPROJECT000000000000001",
        "description": "主角已批准境界状态不能在后续章节无原因倒退。",
        "condition_summary": "若当前 draft 中能力状态低于已批准状态，则触发阻断。",
        "auto_block": True,
        "source_refs": ["object://story-bibles/01JZBIBLE000000000000001"],
        "evidence_refs": ["evidence://01JZEVIDENCE0000000000901"],
        "input_refs": ["object://knowledge-objects/01JZOBJ0000000000000000001"],
        "output_refs": ["object://rules/rule-01JZPOWER000000000000001"],
        "created_at": "2026-07-12T01:10:00Z",
        "updated_at": "2026-07-12T01:10:00Z",
    }
    STORE.writing_runs[WRITING_RUN_ID] = {
        "schema_version": 1,
        "writing_run_id": WRITING_RUN_ID,
        "workspace_id": _workspace_or_default(),
        "project_id": PROJECT_ID,
        "chapter_plan_id": CHAPTER_PLAN_ID,
        "status": "requires_review",
        "task_id": WRITING_TASK_ID,
        "memory_package_id": MEMORY_PACKAGE_ID,
        "prompt_package_id": PROMPT_PACKAGE_ID,
        "chapter_draft_id": CHAPTER_DRAFT_ID,
        "quality_report_id": QUALITY_REPORT_ID,
        "trace_id": "01JZTRC000000000000000003",
        "current_stage": "consistency_review",
        "writer_model_profile_id": MODEL_PROFILE_DEFAULT_ID,
        "critic_model_profile_id": MODEL_PROFILE_STRUCTURED_FALLBACK_ID,
        "humanizer_model_profile_id": MODEL_PROFILE_DEFAULT_ID,
        "assembled_chapter": "萧炎在家族议事厅外停步，先听见堂内压抑的议论，再踏入众人目光中心。纳兰家的退婚信像利刃一样落下，他在众目睽睽之下接住羞辱，也在心底立下三年之约。",
        "model_cost": {
            "input_tokens": 4980,
            "output_tokens": 2310,
            "estimated_total_cost": 0.86,
            "retry_count": 1,
            "writer_input_tokens": 1800,
            "writer_output_tokens": 920,
            "critic_input_tokens": 1400,
            "critic_output_tokens": 540,
            "humanizer_input_tokens": 1780,
            "humanizer_output_tokens": 850,
        },
        "provider_calls": [],
        "accepted_into_manuscript_at": None,
        "accepted_chapter_ref": None,
        "chapter_snapshot_id": None,
        "manuscript_state_id": None,
        "chapter_snapshot": None,
        "manuscript_state": None,
        "consistency_report_id": "01JZCONSIST00000000000001",
        "consistency_report": None,
        "revision_summary_id": "01JZREVISION0000000000001",
        "revision_summary": None,
        "revision_round": 1,
        "max_revision_rounds": 3,
        "created_at": "2026-07-12T01:12:00Z",
        "updated_at": "2026-07-12T01:18:00Z",
    }
    STORE.writing_run_tasks[WRITING_RUN_ID] = {
        "schema_version": 1,
        "task_id": WRITING_TASK_ID,
        "task_type": "create_writing_run",
        "workspace_id": _workspace_or_default(),
        "owner_module": "ai-worker",
        "input_refs": [
            f"object://chapter-plans/{CHAPTER_PLAN_ID}",
            f"object://memory-packages/{MEMORY_PACKAGE_ID}",
            f"object://prompt-packages/{PROMPT_PACKAGE_ID}",
        ],
        "output_refs": [f"object://writing-runs/{WRITING_RUN_ID}"],
        "status": "requires_review",
        "progress": 100,
        "idempotency_key": f"writing-{CHAPTER_PLAN_ID}",
        "retry_count": 1,
        "error_code": None,
        "created_at": "2026-07-11T03:02:00Z",
        "started_at": "2026-07-11T03:02:05Z",
        "finished_at": "2026-07-11T03:08:00Z",
    }
    STORE.provider_calls_by_writing[WRITING_RUN_ID] = [
        {
            "schema_version": 1,
            "provider_call_id": "01JZPCALL0000000000000001",
            "workspace_id": _workspace_or_default(),
            "task_id": WRITING_TASK_ID,
            "writing_run_id": WRITING_RUN_ID,
            "request_id": "req-writing-run",
            "trace_id": "01JZTRC000000000000000003",
            "agent_role": "writer",
            "task_type": "writer_task",
            "assignment_id": "01JZASSIGN000000000000006",
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "provider_name": "anthropic",
            "provider_model_name": "claude-sonnet-5",
            "provider_account_id": "provider-account-anthropic-default",
            "prompt_package_id": PROMPT_PACKAGE_ID,
            "input_refs": [
                f"object://chapter-plans/{CHAPTER_PLAN_ID}",
                f"object://memory-packages/{MEMORY_PACKAGE_ID}",
                f"object://prompt-packages/{PROMPT_PACKAGE_ID}",
            ],
            "output_ref": f"object://drafts/{CHAPTER_DRAFT_ID}",
            "prompt_tokens": 1800,
            "completion_tokens": 920,
            "latency_ms": 1430,
            "retry_count": 0,
            "cost_estimate": 0.31,
            "cost_estimate_status": "estimated",
            "status": "succeeded",
            "error_code": None,
            "fallback_from_call_id": None,
            "created_at": "2026-07-11T03:03:00Z",
        },
        {
            "schema_version": 1,
            "provider_call_id": "01JZPCALL0000000000000002",
            "workspace_id": _workspace_or_default(),
            "task_id": WRITING_TASK_ID,
            "writing_run_id": WRITING_RUN_ID,
            "request_id": "req-writing-run",
            "trace_id": "01JZTRC000000000000000003",
            "agent_role": "critic",
            "task_type": "critic_task",
            "assignment_id": "01JZASSIGN000000000000007",
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "provider_name": "anthropic",
            "provider_model_name": "claude-sonnet-5",
            "provider_account_id": "provider-account-anthropic-default",
            "prompt_package_id": PROMPT_PACKAGE_ID,
            "input_refs": [f"object://writing-runs/{WRITING_RUN_ID}"],
            "output_ref": None,
            "prompt_tokens": 1400,
            "completion_tokens": 0,
            "latency_ms": 490,
            "retry_count": 1,
            "cost_estimate": 0.11,
            "cost_estimate_status": "estimated",
            "status": "failed",
            "error_code": "structured_output_validation_failed",
            "fallback_from_call_id": None,
            "created_at": "2026-07-11T03:04:00Z",
        },
        {
            "schema_version": 1,
            "provider_call_id": "01JZPCALL0000000000000003",
            "workspace_id": _workspace_or_default(),
            "task_id": WRITING_TASK_ID,
            "writing_run_id": WRITING_RUN_ID,
            "request_id": "req-writing-run",
            "trace_id": "01JZTRC000000000000000003",
            "agent_role": "critic",
            "task_type": "critic_task",
            "assignment_id": "01JZASSIGN000000000000007",
            "model_profile_id": MODEL_PROFILE_STRUCTURED_FALLBACK_ID,
            "provider_name": "anthropic",
            "provider_model_name": "claude-haiku-4-5-20251001",
            "provider_account_id": "provider-account-anthropic-default",
            "prompt_package_id": PROMPT_PACKAGE_ID,
            "input_refs": [f"object://writing-runs/{WRITING_RUN_ID}"],
            "output_ref": "object://consistency-reports/01JZCONSIST00000000000001",
            "prompt_tokens": 1400,
            "completion_tokens": 540,
            "latency_ms": 980,
            "retry_count": 1,
            "cost_estimate": 0.22,
            "cost_estimate_status": "estimated",
            "status": "succeeded",
            "error_code": None,
            "fallback_from_call_id": "01JZPCALL0000000000000002",
            "created_at": "2026-07-11T03:05:00Z",
        },
        {
            "schema_version": 1,
            "provider_call_id": "01JZPCALL0000000000000004",
            "workspace_id": _workspace_or_default(),
            "task_id": WRITING_TASK_ID,
            "writing_run_id": WRITING_RUN_ID,
            "request_id": "req-writing-run",
            "trace_id": "01JZTRC000000000000000003",
            "agent_role": "humanizer",
            "task_type": "humanizer_task",
            "assignment_id": "01JZASSIGN000000000000008",
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "provider_name": "anthropic",
            "provider_model_name": "claude-sonnet-5",
            "provider_account_id": "provider-account-anthropic-default",
            "prompt_package_id": PROMPT_PACKAGE_ID,
            "input_refs": [f"object://writing-runs/{WRITING_RUN_ID}"],
            "output_ref": f"object://writing-runs/{WRITING_RUN_ID}",
            "prompt_tokens": 1780,
            "completion_tokens": 850,
            "latency_ms": 1210,
            "retry_count": 0,
            "cost_estimate": 0.33,
            "cost_estimate_status": "estimated",
            "status": "succeeded",
            "error_code": None,
            "fallback_from_call_id": None,
            "created_at": "2026-07-11T03:06:00Z",
        },
    ]
    STORE.section_runs_by_writing[WRITING_RUN_ID] = [
        {
            "schema_version": 1,
            "section_run_id": "01JZSECRUN00000000000001",
            "workspace_id": _workspace_or_default(),
            "writing_run_id": WRITING_RUN_ID,
            "section_plan_id": "01JZSECT0000000000000001",
            "status": "beat_approved",
            "draft_object_ref": "object://drafts/01JZSECRUN00000000000001",
            "critic_report_ref": "object://critic-reports/01JZSECRUN00000000000001",
            "humanized_object_ref": "object://humanized/01JZSECRUN00000000000001",
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "beat_status": [
                {"index": 1, "status": "beat_approved"},
                {"index": 2, "status": "beat_approved"},
            ],
            "writer_output": "乌坦城天色未亮，萧炎已经听见议事堂传来的细碎争论。",
            "critic_issues": [],
            "humanized_text": "天还没亮透，议事堂里的争论已经顺着长廊飘到萧炎耳边。",
            "created_at": "2026-07-11T03:03:00Z",
            "updated_at": "2026-07-11T03:04:00Z",
        },
        {
            "schema_version": 1,
            "section_run_id": "01JZSECRUN00000000000002",
            "workspace_id": _workspace_or_default(),
            "writing_run_id": WRITING_RUN_ID,
            "section_plan_id": "01JZSECT0000000000000002",
            "status": "rewrite_required",
            "draft_object_ref": "object://drafts/01JZSECRUN00000000000002",
            "critic_report_ref": "object://critic-reports/01JZSECRUN00000000000002",
            "humanized_object_ref": "object://humanized/01JZSECRUN00000000000002",
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "beat_status": [
                {"index": 1, "status": "critic_review"},
                {"index": 2, "status": "rewrite_required"},
            ],
            "writer_output": "纳兰家的消息在厅内炸开，所有目光都压向萧炎。",
            "critic_issues": [
                {
                    "issue_id": "01JZCRTIC000000000000001",
                    "severity": "blocking",
                    "category": "character_consistency",
                    "summary": "主角情绪转折过快，缺少被压迫感铺垫。",
                    "affected_text_ref": "object://drafts/01JZSECRUN00000000000002#p1",
                }
            ],
            "humanized_text": "纳兰家的来信一到，厅里的空气像骤然压低了一层，所有审视都落到萧炎身上。",
            "created_at": "2026-07-11T03:04:00Z",
            "updated_at": "2026-07-11T03:06:00Z",
        },
        {
            "schema_version": 1,
            "section_run_id": "01JZSECRUN00000000000003",
            "workspace_id": _workspace_or_default(),
            "writing_run_id": WRITING_RUN_ID,
            "section_plan_id": "01JZSECT0000000000000003",
            "status": "humanizer_pass",
            "draft_object_ref": "object://drafts/01JZSECRUN00000000000003",
            "critic_report_ref": "object://critic-reports/01JZSECRUN00000000000003",
            "humanized_object_ref": "object://humanized/01JZSECRUN00000000000003",
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "beat_status": [
                {"index": 1, "status": "humanizer_pass"},
                {"index": 2, "status": "humanizer_pass"},
            ],
            "writer_output": "萧炎当众抬头，把退婚羞辱化成三年之约。",
            "critic_issues": [
                {
                    "issue_id": "01JZCRTIC000000000000002",
                    "severity": "warning",
                    "category": "style",
                    "summary": "金手指暗示可再收敛，避免过早泄露。",
                    "affected_text_ref": "object://drafts/01JZSECRUN00000000000003#p1",
                }
            ],
            "humanized_text": "他在众人的嘲讽里抬起头，把那封退婚信压回桌上，只留下一句三年后再见。",
            "created_at": "2026-07-11T03:06:00Z",
            "updated_at": "2026-07-11T03:08:00Z",
        },
    ]
    STORE.quality_reports[QUALITY_REPORT_ID] = {
        "schema_version": 1,
        "quality_report_id": QUALITY_REPORT_ID,
        "workspace_id": _workspace_or_default(),
        "writing_run_id": WRITING_RUN_ID,
        "status": "blocked",
        "ai_flavor_score": 0.34,
        "mobile_readability_score": 0.82,
        "originality_safety_score": 0.91,
        "human_review_required": True,
        "blocking_issues": [
            {
                "issue_id": "01JZQLTISSUE000000000001",
                "category": "character_continuity",
                "severity": "high",
                "summary": "第二节仍需补足压迫递进。",
                "affected_text_ref": "object://drafts/01JZSECRUN00000000000002#p1",
                "rule_id": "rule-01JZPOWER000000000000001",
                "resolution_status": "open",
                "input_refs": ["object://rules/rule-01JZPOWER000000000000001"],
                "output_refs": ["object://quality-reports/01JZQLTREP000000000000001/issues/1"],
                "note": None,
            }
        ],
        "created_at": "2026-07-11T03:08:00Z",
        "updated_at": "2026-07-11T03:08:00Z",
    }
    STORE.consistency_reports["01JZCONSIST00000000000001"] = {
        "schema_version": 1,
        "consistency_report_id": "01JZCONSIST00000000000001",
        "workspace_id": _workspace_or_default(),
        "writing_run_id": WRITING_RUN_ID,
        "trace_id": "01JZTRC000000000000000003",
        "task_id": WRITING_TASK_ID,
        "status": "blocked",
        "issue_count": 1,
        "blocking_issue_count": 1,
        "checked_domains": ["character_continuity", "power_system_constraint"],
        "issues": [
            {
                "issue_id": "01JZCONSISTISSUE000000001",
                "category": "power_system_constraint",
                "severity": "critical",
                "summary": "主角境界被写回斗之气三段，与已批准状态冲突。",
                "affected_text_ref": "object://drafts/01JZSECRUN00000000000002#p2",
                "rule_id": "rule-01JZPOWER000000000000001",
                "resolution_status": "open",
                "input_refs": ["object://rules/rule-01JZPOWER000000000000001"],
                "output_refs": ["object://consistency-reports/01JZCONSIST00000000000001/issues/1"],
                "note": None,
            }
        ],
        "input_refs": [f"object://writing-runs/{WRITING_RUN_ID}"],
        "output_refs": ["object://consistency-reports/01JZCONSIST00000000000001"],
        "created_at": "2026-07-12T01:15:00Z",
        "updated_at": "2026-07-12T01:15:00Z",
    }
    STORE.revision_summaries["01JZREVISION0000000000001"] = {
        "schema_version": 1,
        "revision_summary_id": "01JZREVISION0000000000001",
        "workspace_id": _workspace_or_default(),
        "writing_run_id": WRITING_RUN_ID,
        "trace_id": "01JZTRC000000000000000003",
        "status": "requested",
        "revision_round": 1,
        "max_revision_rounds": 3,
        "source_issue_ids": ["01JZCONSISTISSUE000000001"],
        "change_summary": "要求重写第二节，恢复主角当前境界并补足冲突升级。",
        "revision_diff_ref": None,
        "reviewer_note_ref": "object://review-notes/01JZREVISION0000000000001",
        "input_refs": ["object://consistency-reports/01JZCONSIST00000000000001"],
        "output_refs": ["object://revision-summaries/01JZREVISION0000000000001"],
        "created_at": "2026-07-12T01:18:00Z",
        "updated_at": "2026-07-12T01:18:00Z",
    }
    STORE.task_events_by_task[WRITING_TASK_ID] = [
        {
            "schema_version": 1,
            "task_event_id": "01JZWRITEEVT0000000000001",
            "task_id": WRITING_TASK_ID,
            "event_type": "writing_run_created",
            "message": "Writing run created.",
            "payload_ref": None,
            "payload_json": {"writing_run_id": WRITING_RUN_ID},
            "created_at": "2026-07-11T03:02:00Z",
        },
        {
            "schema_version": 1,
            "task_event_id": "01JZWRITEEVT0000000000002",
            "task_id": WRITING_TASK_ID,
            "event_type": "progress",
            "message": "Consistency review blocked draft and requested revision.",
            "payload_ref": None,
            "payload_json": {"current_stage": "consistency_review", "retry_count": 1, "consistency_report_id": "01JZCONSIST00000000000001"},
            "created_at": "2026-07-12T01:18:00Z",
        },
    ]
    STORE.feedback_records["01JZFDBK0000000000000001"] = {
        "schema_version": 1,
        "feedback_record_id": "01JZFDBK0000000000000001",
        "workspace_id": _workspace_or_default(),
        "target_type": "writing_run",
        "target_id": WRITING_RUN_ID,
        "feedback_type": "quality",
        "score": 0.82,
        "source": "quality_gate",
        "comment_ref": "object://quality-comments/01JZFDBK0000000000000001",
        "payload": {
            "quality_report_id": QUALITY_REPORT_ID,
            "summary": "质量门禁通过后保留了节奏与可读性指标。",
        },
        "created_at": "2026-07-11T03:10:00Z",
        "updated_at": "2026-07-11T03:10:00Z",
    }
    STORE.feedback_records["01JZFDBK0000000000000002"] = {
        "schema_version": 1,
        "feedback_record_id": "01JZFDBK0000000000000002",
        "workspace_id": _workspace_or_default(),
        "target_type": "quality_report",
        "target_id": QUALITY_REPORT_ID,
        "feedback_type": "style",
        "score": 0.64,
        "source": "critic",
        "comment_ref": "object://critic-comments/01JZFDBK0000000000000002",
        "payload": {
            "affected_text_ref": "object://drafts/01JZSECRUN00000000000003#p1",
            "summary": "金手指暗示仍偏早，可继续收敛。",
        },
        "created_at": "2026-07-11T03:11:00Z",
        "updated_at": "2026-07-11T03:11:00Z",
    }
    STORE.ranking_snapshots["prompt"] = {
        "schema_version": 1,
        "ranking_snapshot_id": "01JZRANKSNAP0000000000001",
        "workspace_id": _workspace_or_default(),
        "trace_id": "trace-ranking-prompt-1",
        "ranking_type": "prompt",
        "scope_ref": f"object://writing-runs/{WRITING_RUN_ID}",
        "version": 1,
        "updated_at": "2026-07-12T01:34:00Z",
        "items": [
            {
                "rank": 1,
                "target_type": "prompt_version",
                "target_id": "prompt://writer/chapter-default",
                "label": "writer 默认提示",
                "score": 0.83,
                "status": "leading",
                "signal_ids": ["01JZRANKSIG00000000000001"],
                "summary": "质量稳定，但风格线索仍偏显性。",
            },
            {
                "rank": 2,
                "target_type": "prompt_version",
                "target_id": "prompt://writer/chapter-compact",
                "label": "writer 紧凑提示",
                "score": 0.76,
                "status": "watch",
                "signal_ids": ["01JZRANKSIG00000000000002"],
                "summary": "可作为下一轮收紧表达候选。",
            },
        ],
        "signals": [
            {
                "schema_version": 1,
                "signal_id": "01JZRANKSIG00000000000001",
                "workspace_id": _workspace_or_default(),
                "trace_id": "trace-ranking-prompt-1",
                "ranking_type": "prompt",
                "target_type": "prompt_version",
                "target_id": "prompt://writer/chapter-default",
                "signal_type": "prompt_effectiveness",
                "score": 0.87,
                "weight": 0.7,
                "source": "quality_gate",
                "source_feedback_record_id": "01JZFDBK0000000000000001",
                "summary": "默认 writer prompt 在质量门禁后保留了节奏与可读性。",
                "evidence_refs": [f"object://quality-reports/{QUALITY_REPORT_ID}"],
                "input_refs": ["object://feedback-records/01JZFDBK0000000000000001"],
                "output_refs": ["object://rankings/prompt/signals/01JZRANKSIG00000000000001"],
                "created_at": "2026-07-12T01:30:00Z",
                "updated_at": "2026-07-12T01:30:00Z",
            },
            {
                "schema_version": 1,
                "signal_id": "01JZRANKSIG00000000000002",
                "workspace_id": _workspace_or_default(),
                "trace_id": "trace-ranking-prompt-1",
                "ranking_type": "prompt",
                "target_type": "prompt_version",
                "target_id": "prompt://writer/chapter-compact",
                "signal_type": "reader_interest",
                "score": 0.72,
                "weight": 0.5,
                "source": "critic",
                "source_feedback_record_id": "01JZFDBK0000000000000002",
                "summary": "批评者认为默认 prompt 对金手指提示过早，紧凑版更适合后续回合。",
                "evidence_refs": ["object://critic-comments/01JZFDBK0000000000000002"],
                "input_refs": ["object://feedback-records/01JZFDBK0000000000000002"],
                "output_refs": ["object://rankings/prompt/signals/01JZRANKSIG00000000000002"],
                "created_at": "2026-07-12T01:31:00Z",
                "updated_at": "2026-07-12T01:31:00Z",
            },
        ],
        "suggestions": [
            {
                "schema_version": 1,
                "suggestion_id": "01JZSTRAT000000000000001",
                "workspace_id": _workspace_or_default(),
                "trace_id": "trace-ranking-prompt-1",
                "ranking_type": "prompt",
                "target_scope": "prompt",
                "status": "review_required",
                "summary": "收紧 writer 默认提示中对金手指线索的显性表达。",
                "recommended_action": "切换到 prompt://writer/chapter-compact 进行下一轮写作。",
                "source_signal_ids": ["01JZRANKSIG00000000000002"],
                "promoted_from_feedback_record_id": "01JZFDBK0000000000000002",
                "input_refs": ["object://rankings/prompt/signals/01JZRANKSIG00000000000002"],
                "output_refs": ["object://strategy-suggestions/01JZSTRAT000000000000001"],
                "created_at": "2026-07-12T01:32:00Z",
                "updated_at": "2026-07-12T01:32:00Z",
                "promoted_at": None,
            }
        ],
    }
    STORE.patterns["01JZPATTERN00000000000001"] = {
        "schema_version": 1,
        "pattern_id": "01JZPATTERN00000000000001",
        "workspace_id": _workspace_or_default(),
        "trace_id": "trace-pattern-1",
        "canonical_name": "退婚立誓",
        "pattern_type": "conflict_escalation",
        "status": "approved",
        "intent": "用公开羞辱触发主角长期目标与情绪反弹。",
        "preconditions": ["主角处于低谷", "公开场合发生身份压迫"],
        "steps": [
            {"index": 1, "summary": "先压低主角处境"},
            {"index": 2, "summary": "让压迫升级到无法退让"},
            {"index": 3, "summary": "主角公开立誓，把羞辱转为主线目标"},
        ],
        "slots": ["压迫者", "见证者", "誓约代价"],
        "expected_reader_effect": "先压后燃，形成升级流期待。",
        "compatible_rhythm_profile_id": "01JZRHYTHM00000000000001",
        "evidence_refs": ["evidence://01JZEVIDENCE0000000000101"],
        "created_at": "2026-07-12T01:00:00Z",
        "updated_at": "2026-07-12T01:02:00Z",
    }
    STORE.rhythm_profiles["01JZRHYTHM00000000000001"] = {
        "schema_version": 1,
        "rhythm_profile_id": "01JZRHYTHM00000000000001",
        "workspace_id": _workspace_or_default(),
        "trace_id": "trace-rhythm-1",
        "target_id": CHAPTER_PLAN_ID,
        "status": "approved",
        "label": "退婚压迫三段式",
        "climax_index": 0.86,
        "conflict_index": 0.78,
        "dialogue_ratio": 0.42,
        "description_ratio": 0.28,
        "battle_ratio": 0,
        "information_density": 0.65,
        "suspense_index": 0.74,
        "reward_count": 2,
        "emotion_curve": [
            {"beat": 1, "intensity": 0.35, "summary": "压抑铺垫"},
            {"beat": 2, "intensity": 0.68, "summary": "冲突加压"},
            {"beat": 3, "intensity": 0.92, "summary": "立誓爆点"},
        ],
        "created_at": "2026-07-12T01:03:00Z",
        "updated_at": "2026-07-12T01:05:00Z",
    }
    STORE.assets["01JZASSET000000000000001"] = {
        "schema_version": 1,
        "asset_id": "01JZASSET000000000000001",
        "workspace_id": _workspace_or_default(),
        "trace_id": "trace-asset-1",
        "asset_type": "expression",
        "canonical_name": "三年之约宣言模板",
        "status": "approved",
        "content_summary": "用于公开立誓场景的短句式资产。",
        "style_tags": ["克制", "燃点前压"],
        "genre_scope": "玄幻升级流",
        "usage_context": "公开羞辱后主角反击",
        "constraints": ["避免过早泄露金手指", "句式不超过两行"],
        "expression_type_refs": ["expression://oath-line"],
        "source_refs": [f"object://source-books/{BOOK_ID}"],
        "evidence_refs": ["evidence://01JZEVIDENCE0000000000201"],
        "quality_score": 0.88,
        "created_at": "2026-07-12T01:06:00Z",
        "updated_at": "2026-07-12T01:08:00Z",
    }
    STORE.section_plan_tasks[CHAPTER_PLAN_ID] = {
        "schema_version": 1,
        "task_id": SECTION_PLAN_TASK_ID,
        "task_type": "create_section_plans",
        "workspace_id": _workspace_or_default(),
        "owner_module": "ai-worker",
        "input_refs": [f"object://chapter-plans/{CHAPTER_PLAN_ID}"],
        "output_refs": [
            "object://section-plans/01JZSECT0000000000000001",
            "object://section-plans/01JZSECT0000000000000002",
            "object://section-plans/01JZSECT0000000000000003",
        ],
        "status": "succeeded",
        "progress": 100,
        "idempotency_key": f"section-{CHAPTER_PLAN_ID}",
        "retry_count": 0,
        "error_code": None,
        "created_at": "2026-07-11T02:15:00Z",
        "started_at": "2026-07-11T02:15:05Z",
        "finished_at": "2026-07-11T02:18:00Z",
    }
    STORE.task_events_by_task[SECTION_PLAN_TASK_ID] = [
        {
            "schema_version": 1,
            "task_event_id": "01JZSECTEVT0000000000001",
            "task_id": SECTION_PLAN_TASK_ID,
            "event_type": "created",
            "message": "Section plans created.",
            "payload_ref": None,
            "payload_json": {"section_count": 3},
            "created_at": "2026-07-11T02:15:00Z",
        },
        {
            "schema_version": 1,
            "task_event_id": "01JZSECTEVT0000000000002",
            "task_id": SECTION_PLAN_TASK_ID,
            "event_type": "progress",
            "message": "Section plans generated.",
            "payload_ref": None,
            "payload_json": {"section_count": 3},
            "created_at": "2026-07-11T02:18:00Z",
        },
    ]
    _normalize_seed_records()


def default_workspace_id() -> str:
    return WORKSPACE_ID if WORKSPACE_ID in STORE.workspaces else next(iter(STORE.workspaces), WORKSPACE_ID)


def default_workspace() -> Optional[dict[str, Any]]:
    return STORE.workspaces.get(default_workspace_id())


def _workspace_or_default(workspace_id: Optional[str] = None) -> str:
    if workspace_id and workspace_id in STORE.workspaces:
        return workspace_id
    return default_workspace_id()


def _member_for_actor(workspace_id: str, actor_id: str) -> Optional[dict[str, Any]]:
    for member in STORE.workspace_members.values():
        if member["workspace_id"] == workspace_id and member["user_id"] == actor_id and member["status"] == "active":
            return member
    return None


def _actor_context(
    workspace_id: Optional[str] = None,
    actor_id: Optional[str] = None,
    actor_role: Optional[str] = None,
) -> dict[str, str]:
    resolved_workspace_id = _workspace_or_default(workspace_id)
    resolved_actor_id = actor_id or USER_ID
    member = _member_for_actor(resolved_workspace_id, resolved_actor_id)
    resolved_actor_role = actor_role or (member["role"] if member else "viewer")
    return {
        "workspace_id": resolved_workspace_id,
        "actor_id": resolved_actor_id,
        "actor_role": resolved_actor_role,
    }


def _append_task_event(
    task: Optional[dict[str, Any]],
    event_type: str,
    message: str,
    status: str,
    request_id: str,
    trace_id: str,
    actor_id: str,
    agent_role: str = "system",
    payload_json: Optional[dict[str, Any]] = None,
    error_code: Optional[str] = None,
    created_at: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    if not task:
        return None
    event = {
        "schema_version": 1,
        "task_event_id": str(ulid.new()),
        "task_id": task["task_id"],
        "workspace_id": task["workspace_id"],
        "event_type": event_type,
        "status": status,
        "request_id": request_id,
        "trace_id": trace_id,
        "actor_id": actor_id,
        "agent_role": agent_role,
        "message": message,
        "payload_ref": None,
        "payload_json": payload_json,
        "error_code": error_code,
        "created_at": created_at or utc_now(),
    }
    STORE.task_events_by_task.setdefault(task["task_id"], []).append(event)
    return event


def _append_audit_event(
    action: str,
    target_type: str,
    target_id: str,
    request_id: str,
    trace_id: str,
    actor_id: str,
    actor_role: str,
    workspace_id: str,
    target_ref: Optional[str] = None,
    before_ref: Optional[str] = None,
    after_ref: Optional[str] = None,
    reason: Optional[str] = None,
    payload: Optional[dict[str, Any]] = None,
    created_at: Optional[str] = None,
) -> dict[str, Any]:
    event = {
        "schema_version": 1,
        "audit_event_id": str(ulid.new()),
        "workspace_id": workspace_id,
        "request_id": request_id,
        "trace_id": trace_id,
        "actor_id": actor_id,
        "actor_role": actor_role,
        "action": action,
        "target_type": target_type,
        "target_id": target_id,
        "target_ref": target_ref,
        "before_ref": before_ref,
        "after_ref": after_ref,
        "reason": reason,
        "payload": payload,
        "created_at": created_at or utc_now(),
    }
    STORE.audit_events.append(event)
    return event


def _require_role(actor_role: str, allowed_roles: set[str]) -> None:
    if actor_role not in allowed_roles:
        raise PermissionError("forbidden")


def _build_task(
    task_id: str,
    task_type: str,
    workspace_id: str,
    input_refs: list[str],
    output_refs: list[str],
    status: str,
    progress: int,
    idempotency_key: str,
    request_id: str,
    trace_id: str,
    actor_id: str,
    retry_count: int = 0,
    error_code: Optional[str] = None,
    created_at: Optional[str] = None,
    started_at: Optional[str] = None,
    finished_at: Optional[str] = None,
    latency_ms: Optional[int] = None,
    max_retry_count: int = 3,
    lease_owner: Optional[str] = None,
    lease_expires_at: Optional[str] = None,
    heartbeat_at: Optional[str] = None,
    next_retry_at: Optional[str] = None,
    blocked_reason: Optional[str] = None,
    current_dispatch_token: Optional[str] = None,
    dispatch_attempt: int = 0,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "task_id": task_id,
        "task_type": task_type,
        "workspace_id": workspace_id,
        "owner_module": "ai-worker",
        "input_refs": input_refs,
        "output_refs": output_refs,
        "status": status,
        "progress": progress,
        "idempotency_key": idempotency_key,
        "request_id": request_id,
        "trace_id": trace_id,
        "actor_id": actor_id,
        "retry_count": retry_count,
        "max_retry_count": max_retry_count,
        "latency_ms": latency_ms,
        "error_code": error_code,
        "lease_owner": lease_owner,
        "lease_expires_at": lease_expires_at,
        "heartbeat_at": heartbeat_at,
        "next_retry_at": next_retry_at,
        "review_required": status == "requires_review",
        "blocked_reason": blocked_reason,
        "current_dispatch_token": current_dispatch_token,
        "dispatch_attempt": dispatch_attempt,
        "created_at": created_at,
        "started_at": started_at,
        "finished_at": finished_at,
    }


def _build_feedback_record(
    feedback_record_id: str,
    workspace_id: str,
    target_type: str,
    target_id: str,
    feedback_type: str,
    score: float,
    source: str,
    request_id: str,
    trace_id: str,
    actor_id: str,
    created_at: str,
    comment_ref: Optional[str] = None,
    payload: Optional[dict[str, Any]] = None,
    promotion_status: str = "pending",
    input_refs: Optional[list[str]] = None,
    output_refs: Optional[list[str]] = None,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "feedback_record_id": feedback_record_id,
        "workspace_id": workspace_id,
        "target_type": target_type,
        "target_id": target_id,
        "feedback_type": feedback_type,
        "score": score,
        "source": source,
        "request_id": request_id,
        "trace_id": trace_id,
        "actor_id": actor_id,
        "promotion_status": promotion_status,
        "input_refs": input_refs or [],
        "output_refs": output_refs or [],
        "comment_ref": comment_ref,
        "payload": payload,
        "created_at": created_at,
        "updated_at": created_at,
    }


def list_audit_events(workspace_id: Optional[str] = None) -> list[dict[str, Any]]:
    items = STORE.audit_events
    if workspace_id:
        items = [item for item in items if item["workspace_id"] == workspace_id]
    return sorted(items, key=lambda item: item["created_at"])


@_persisting_mutation
def create_workspace(payload: dict[str, Any]) -> dict[str, Any]:
    workspace_id = payload.get("slug") or str(ulid.new())
    now = utc_now()
    workspace = {
        "schema_version": 1,
        "workspace_id": workspace_id,
        "owner_user_id": USER_ID,
        "name": payload["name"],
        "slug": payload.get("slug", workspace_id),
        "default_language": payload.get("default_language", "zh-CN"),
        "status": "active",
        "created_at": now,
        "updated_at": now,
    }
    workspace_member = {
        "schema_version": 1,
        "workspace_member_id": str(ulid.new()),
        "workspace_id": workspace_id,
        "user_id": USER_ID,
        "role": "owner",
        "status": "active",
        "created_at": now,
        "updated_at": now,
    }
    STORE.workspaces[workspace_id] = workspace
    STORE.workspace_members[workspace_member["workspace_member_id"]] = workspace_member
    return {
        "workspace": workspace,
        "workspace_member": workspace_member,
    }


def get_workspace(workspace_id: str) -> Optional[dict[str, Any]]:
    workspace = STORE.workspaces.get(workspace_id)
    if not workspace:
        return None
    members = [item for item in STORE.workspace_members.values() if item["workspace_id"] == workspace_id]
    return {
        "workspace": workspace,
        "members": members,
    }


def get_workspace_home(workspace_id: str) -> Optional[dict[str, Any]]:
    workspace = STORE.workspaces.get(workspace_id)
    if not workspace:
        return None

    recent_tasks: list[dict[str, Any]] = []
    task_sources = [
        *[run["task"] for run in STORE.extraction_runs.values() if run.get("task")],
        *STORE.chapter_plan_tasks.values(),
        *STORE.section_plan_tasks.values(),
        *STORE.writing_run_tasks.values(),
    ]
    for item in task_sources:
        target_ref = item["output_refs"][0] if item.get("output_refs") else None
        recent_tasks.append(
            {
                "task_id": item["task_id"],
                "task_type": item["task_type"],
                "status": item["status"],
                "summary": f"{item['task_type']} 当前状态：{item['status']}。",
                "updated_at": item.get("finished_at") or item.get("started_at") or item["created_at"],
                "target_ref": target_ref,
            }
        )
    recent_tasks.sort(key=lambda item: item["updated_at"], reverse=True)

    pending_reviews = []
    for item in STORE.knowledge_objects.values():
        if item["workspace_id"] == workspace_id and item["review_status"] == "pending":
            pending_reviews.append(
                {
                    "review_id": item["object_id"],
                    "review_type": "knowledge_object",
                    "status": item["review_status"],
                    "title": f"{item['canonical_name']} 待知识审核",
                    "target_ref": f"object://knowledge-objects/{item['object_id']}",
                }
            )
    for writing_run_id, section_runs in STORE.section_runs_by_writing.items():
        writing_run = STORE.writing_runs.get(writing_run_id)
        if not writing_run or writing_run["workspace_id"] != workspace_id:
            continue
        for section in section_runs:
            if section["status"] in {"rewrite_required", "critic_review", "blocked"}:
                pending_reviews.append(
                    {
                        "review_id": section["section_run_id"],
                        "review_type": "section_run",
                        "status": section["status"],
                        "title": f"章节小节 {section['section_run_id']} 需人工处理",
                        "target_ref": f"object://section-runs/{section['section_run_id']}",
                    }
                )

    quick_links = [
        {
            "label": "进入来源书库",
            "route": "/sources",
            "resource_ref": f"object://source-books/{BOOK_ID}",
        },
        {
            "label": "进入写作工作台",
            "route": "/projects/demo-project/writing/demo-run",
            "resource_ref": f"object://writing-runs/{WRITING_RUN_ID}",
        },
        {
            "label": "进入配置中心",
            "route": "/configuration",
            "resource_ref": "object://configuration/default",
        },
    ]

    return {
        "workspace": workspace,
        "recent_tasks": recent_tasks[:4],
        "pending_reviews": pending_reviews[:4],
        "quick_links": quick_links,
    }


def _normalize_seed_records() -> None:
    for object_id, obj in STORE.knowledge_objects.items():
        obj.setdefault("trace_id", STORE.extraction_runs.get(RUN_ID, {}).get("task", {}).get("trace_id", "01JZTRC000000000000000001"))
        obj.setdefault("input_refs", [f"object://extraction-runs/{RUN_ID}"])
        obj.setdefault("output_refs", [f"object://knowledge-objects/{object_id}"])

    for story_bible in STORE.story_bibles.values():
        _hydrate_story_bible(story_bible)

    for chapter_plan in STORE.chapter_plans.values():
        chapter_plan.setdefault("trace_id", "01JZTRC000000000000000002")
        chapter_plan.setdefault("input_refs", [f"object://novel-projects/{chapter_plan['project_id']}"])
        chapter_plan.setdefault("output_refs", [f"object://chapter-plans/{chapter_plan['chapter_plan_id']}"])

    for section_items in STORE.section_plans_by_chapter.values():
        for section in section_items:
            section.setdefault("trace_id", "01JZTRC000000000000000002")
            section.setdefault("input_refs", [f"object://chapter-plans/{section['chapter_plan_id']}"])
            section.setdefault("output_refs", [f"object://section-plans/{section['section_plan_id']}"])

    for task in [*STORE.chapter_plan_tasks.values(), *STORE.section_plan_tasks.values(), *STORE.writing_run_tasks.values()]:
        task.setdefault("request_id", "seed-request")
        task.setdefault("trace_id", "seed-trace")
        task.setdefault("actor_id", USER_ID)
        task.setdefault("latency_ms", 1000 if task.get("finished_at") else 0)
        task.setdefault("max_retry_count", 3)
        task.setdefault("lease_owner", None)
        task.setdefault("lease_expires_at", None)
        task.setdefault("heartbeat_at", None)
        task.setdefault("current_dispatch_token", None)
        task.setdefault("dispatch_attempt", 0)
        task.setdefault("next_retry_at", None)
        task.setdefault("review_required", task.get("status") == "requires_review")
        task.setdefault("blocked_reason", None)

    extraction_task = STORE.extraction_runs.get(RUN_ID, {}).get("task")
    if extraction_task:
        extraction_task.setdefault("request_id", "seed-request")
        extraction_task.setdefault("trace_id", "01JZTRC000000000000000001")
        extraction_task.setdefault("actor_id", USER_ID)
        extraction_task.setdefault("latency_ms", 0)
        extraction_task.setdefault("max_retry_count", 3)
        extraction_task.setdefault("lease_owner", None)
        extraction_task.setdefault("lease_expires_at", None)
        extraction_task.setdefault("heartbeat_at", None)
        extraction_task.setdefault("current_dispatch_token", None)
        extraction_task.setdefault("dispatch_attempt", 0)
        extraction_task.setdefault("next_retry_at", None)
        extraction_task.setdefault("review_required", extraction_task.get("status") == "requires_review")
        extraction_task.setdefault("blocked_reason", None)

    for writing_run_id, provider_calls in STORE.provider_calls_by_writing.items():
        task = STORE.writing_run_tasks.get(writing_run_id)
        for call in provider_calls:
            call.setdefault("workspace_id", default_workspace_id())
            call.setdefault("task_id", task["task_id"] if task else WRITING_TASK_ID)
            call.setdefault("writing_run_id", writing_run_id)
            call.setdefault("request_id", "seed-request")
            call.setdefault("trace_id", STORE.writing_runs.get(writing_run_id, {}).get("trace_id", "seed-trace"))

    for writing_run in STORE.writing_runs.values():
        consistency_report_id = writing_run.get("consistency_report_id")
        revision_summary_id = writing_run.get("revision_summary_id")
        writing_run["provider_calls"] = deepcopy(STORE.provider_calls_by_writing.get(writing_run["writing_run_id"], []))
        writing_run["chapter_snapshot"] = None
        writing_run["manuscript_state"] = None
        writing_run["consistency_report"] = deepcopy(STORE.consistency_reports.get(consistency_report_id)) if consistency_report_id else None
        writing_run["revision_summary"] = deepcopy(STORE.revision_summaries.get(revision_summary_id)) if revision_summary_id else None
        writing_run.setdefault("revision_round", 0)
        writing_run.setdefault("max_revision_rounds", 3)

    for report in STORE.consistency_reports.values():
        report.setdefault("updated_at", report["created_at"])

    for summary in STORE.revision_summaries.values():
        summary.setdefault("updated_at", summary["created_at"])

    for rule in STORE.rules.values():
        rule.setdefault("updated_at", rule["created_at"])

    for record_id, record in STORE.feedback_records.items():
        target_ref = f"object://{record['target_type'].replace('_', '-')}/{record['target_id']}"
        record.setdefault("request_id", "seed-request")
        record.setdefault("trace_id", STORE.writing_runs.get(WRITING_RUN_ID, {}).get("trace_id", "seed-trace"))
        record.setdefault("actor_id", USER_ID)
        record.setdefault("promotion_status", "pending")
        record.setdefault("input_refs", [target_ref])
        record.setdefault("output_refs", [])

    for task_id, events in STORE.task_events_by_task.items():
        task = None
        for candidate in [STORE.extraction_runs.get(RUN_ID, {}).get("task"), *STORE.chapter_plan_tasks.values(), *STORE.section_plan_tasks.values(), *STORE.writing_run_tasks.values()]:
            if candidate and candidate["task_id"] == task_id:
                task = candidate
                break
        for event in events:
            event.setdefault("workspace_id", task["workspace_id"] if task else default_workspace_id())
            event.setdefault("status", task["status"] if task else "queued")
            event.setdefault("request_id", task.get("request_id") if task else "seed-request")
            event.setdefault("trace_id", task.get("trace_id") if task else "seed-trace")
            event.setdefault("actor_id", task.get("actor_id") if task else USER_ID)
            event.setdefault("agent_role", "system")
            event.setdefault("error_code", None)
            if event.get("event_type") == "writing_run_created":
                event["event_type"] = "created"
            if event.get("event_type") == "progress" and event.get("payload_json", {}).get("status") == "requires_review":
                event["event_type"] = "review_required"

    for writing_task in STORE.writing_run_tasks.values():
        writing_task.setdefault("request_id", "seed-request")
        writing_task.setdefault("trace_id", "seed-trace")
        writing_task.setdefault("actor_id", USER_ID)
        writing_task.setdefault("latency_ms", 1000 if writing_task.get("finished_at") else 0)
        writing_task.setdefault("max_retry_count", 3)
        writing_task.setdefault("lease_owner", None)
        writing_task.setdefault("lease_expires_at", None)
        writing_task.setdefault("heartbeat_at", None)
        writing_task.setdefault("current_dispatch_token", None)
        writing_task.setdefault("next_retry_at", None)
        writing_task.setdefault("review_required", writing_task.get("status") == "requires_review")
        writing_task.setdefault("blocked_reason", None)



def _source_content_ref(source_content_id: str) -> str:
    return f"object://source-contents/{source_content_id}"


def _evidence_ref(evidence_id: str) -> str:
    return f"evidence://{evidence_id}"


def _evidence_id_from_ref(evidence_id_or_ref: str) -> str:
    return evidence_id_or_ref.removeprefix("evidence://")


def _default_story_bible_payload(title: Optional[str] = None) -> dict[str, Any]:
    project_title = title or "该项目"
    return {
        "premise": f"{project_title} 的故事设定待完善。",
        "protagonist": "待设定",
        "core_conflict": "待设定",
        "style_target": "克制、证据充分、节奏稳步升级。",
        "forbidden_similarities": "不直接复刻参考作品的人物名、金手指机制和关键桥段。",
        "world_rules": ["所有关键成长都要付出明确代价。"],
        "narrative_promises": ["前三章完成主角困境、破局线索和阶段承诺。"],
    }


def _normalize_story_bible_payload(payload: Optional[dict[str, Any]], title: Optional[str] = None) -> dict[str, Any]:
    base = _default_story_bible_payload(title)
    merged = {**base, **(payload or {})}
    normalized: dict[str, Any] = {}
    for field in ("premise", "protagonist", "core_conflict", "style_target", "forbidden_similarities"):
        value = str(merged.get(field) or base[field]).strip()
        normalized[field] = value or base[field]
    for field in ("world_rules", "narrative_promises"):
        value = merged.get(field)
        if isinstance(value, list):
            items = [str(item).strip() for item in value if str(item).strip()]
        elif value is None:
            items = []
        else:
            items = [item.strip() for item in str(value).splitlines() if item.strip()]
        normalized[field] = items or deepcopy(base[field])
    return normalized


def _story_bible_changed_fields(before_payload: Optional[dict[str, Any]], after_payload: dict[str, Any]) -> list[str]:
    if before_payload is None:
        return list(after_payload.keys())
    before = _normalize_story_bible_payload(before_payload)
    after = _normalize_story_bible_payload(after_payload)
    return [field for field in after if before.get(field) != after.get(field)]


def _story_bible_diff(
    from_version: Optional[int],
    to_version: int,
    before_payload: Optional[dict[str, Any]],
    after_payload: dict[str, Any],
    summary: str,
) -> dict[str, Any]:
    normalized_after = _normalize_story_bible_payload(after_payload)
    normalized_before = _normalize_story_bible_payload(before_payload) if before_payload is not None else None
    changed_fields = _story_bible_changed_fields(normalized_before, normalized_after)
    return {
        "from_version": from_version,
        "to_version": to_version,
        "changed_fields": changed_fields,
        "changes": [
            {
                "field": field,
                "before": normalized_before.get(field) if normalized_before is not None else None,
                "after": normalized_after.get(field),
            }
            for field in changed_fields
        ],
        "summary": summary,
    }


def _story_bible_history_entry(
    version: int,
    status: str,
    change_type: str,
    payload: dict[str, Any],
    changed_fields: list[str],
    summary: str,
    trace_id: str,
    actor_id: str,
    created_at: str,
    note: Optional[str] = None,
) -> dict[str, Any]:
    return {
        "version": version,
        "status": status,
        "change_type": change_type,
        "payload": _normalize_story_bible_payload(payload),
        "changed_fields": changed_fields,
        "summary": summary,
        "note": note,
        "trace_id": trace_id,
        "actor_id": actor_id,
        "created_at": created_at,
    }


def _hydrate_story_bible(story_bible: dict[str, Any]) -> dict[str, Any]:
    story_bible["payload"] = _normalize_story_bible_payload(story_bible.get("payload"))
    confirmed_payload = story_bible.get("confirmed_payload")
    if confirmed_payload is not None:
        story_bible["confirmed_payload"] = _normalize_story_bible_payload(confirmed_payload)
    elif story_bible.get("status") == "approved":
        story_bible["confirmed_payload"] = deepcopy(story_bible["payload"])
    else:
        story_bible["confirmed_payload"] = None
    story_bible.setdefault("approved_at", story_bible.get("updated_at") if story_bible.get("status") == "approved" else None)
    story_bible.setdefault("approved_by", USER_ID if story_bible.get("status") == "approved" else None)
    history = story_bible.setdefault("history", [])
    if not history:
        history.append(
            _story_bible_history_entry(
                version=story_bible.get("version", 1),
                status=story_bible.get("status", "draft"),
                change_type="create",
                payload=story_bible["payload"],
                changed_fields=list(story_bible["payload"].keys()),
                summary="建立首版故事圣经。",
                trace_id=story_bible.get("trace_id", "seed-trace"),
                actor_id=story_bible.get("approved_by") or USER_ID,
                created_at=story_bible.get("created_at") or utc_now(),
            )
        )
    for entry in history:
        entry["payload"] = _normalize_story_bible_payload(entry.get("payload"))
        entry.setdefault("changed_fields", list(entry["payload"].keys()) if entry.get("change_type") == "create" else [])
        entry.setdefault("summary", "故事圣经已更新。")
        entry.setdefault("note", None)
        entry.setdefault("trace_id", story_bible.get("trace_id", "seed-trace"))
        entry.setdefault("actor_id", story_bible.get("approved_by") or USER_ID)
        entry.setdefault("created_at", story_bible.get("updated_at") or story_bible.get("created_at") or utc_now())
    if story_bible.get("diff") is None and len(history) >= 2 and (
        story_bible.get("status") == "pending_review" or history[-1].get("change_type") == "regenerate"
    ):
        previous = history[-2]
        current = history[-1]
        story_bible["diff"] = _story_bible_diff(
            previous.get("version"),
            story_bible.get("version", current.get("version", 1)),
            previous.get("payload"),
            story_bible["payload"],
            current.get("summary", "故事圣经已更新。"),
        )
    story_bible.setdefault("diff", None)
    return story_bible


if _restore_store_from_business_tables():
    _normalize_seed_records()
    _restore_runtime_projection()
elif _restore_store_from_snapshot():
    _normalize_seed_records()
    backfill_business_state_from_snapshot(asdict(STORE))
    _restore_runtime_projection()
else:
    seed_phase_two_demo_data()
    _normalize_seed_records()
    _persist_store()


def _split_source_text_into_chapters(book_id: str, source_text: str, now: str) -> list[dict[str, Any]]:
    lines = [line.strip() for line in source_text.splitlines()]
    chunks: list[tuple[str, list[str]]] = []
    current_title: Optional[str] = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_title, current_lines
        text = "\n".join(line for line in current_lines if line).strip()
        if text:
            chunks.append((current_title or f"第 {len(chunks) + 1} 章", current_lines.copy()))
        current_title = None
        current_lines = []

    for line in lines:
        is_heading = bool(line) and (line.startswith("第") and "章" in line[:12] or line.lower().startswith("chapter "))
        if is_heading:
            flush()
            current_title = line
            current_lines = [line]
        else:
            current_lines.append(line)
    flush()

    if not chunks:
        chunks = [("第 1 章", [source_text])]

    chapters = []
    for index, (title, chapter_lines) in enumerate(chunks, start=1):
        chapter_id = str(ulid.new())
        raw_text = "\n".join(chapter_lines).strip()
        excerpt = raw_text[:160]
        chapters.append(
            {
                "schema_version": 1,
                "chapter_id": chapter_id,
                "book_id": book_id,
                "chapter_index": index,
                "title": title or f"第 {index} 章",
                "segmentation_status": "segmented",
                "text_object_ref": f"object://source-chapters/{chapter_id}",
                "text_range": f"c{index}:p1-p{max(1, len([line for line in chapter_lines if line]))}",
                "raw_text": raw_text,
                "text_excerpt": excerpt,
                "created_at": now,
                "updated_at": now,
            }
        )
    return chapters


@_persisting_mutation
def create_book(payload: dict[str, Any], trace_id: str) -> dict[str, Any]:
    book_id = str(ulid.new())
    now = utc_now()
    source_text = payload.get("source_text")
    source_content_id = str(ulid.new()) if source_text is not None else None
    encoded_source = source_text.encode("utf-8") if source_text is not None else b""
    book = {
        "schema_version": 1,
        "book_id": book_id,
        "workspace_id": _workspace_or_default(payload.get("workspace_id")),
        "title": payload["title"],
        "author_name": payload["author_name"],
        "source_type": payload["source_type"],
        "platform": payload.get("platform"),
        "genre": payload.get("genre"),
        "usage_boundary": payload.get("usage_boundary"),
        "source_content_ref": _source_content_ref(source_content_id) if source_content_id else None,
        "content_checksum": f"sha256:{hashlib.sha256(encoded_source).hexdigest()}" if source_text is not None else None,
        "content_byte_size": len(encoded_source) if source_text is not None else None,
        "chapter_count": 0,
        "import_status": "ready" if source_text else "uploaded",
        "trace_id": trace_id,
        "created_at": now,
        "updated_at": now,
    }
    STORE.books[book_id] = book
    STORE.chapters_by_book[book_id] = []

    if source_text is not None and source_content_id is not None:
        content = {
            "schema_version": 1,
            "source_content_id": source_content_id,
            "book_id": book_id,
            "object_ref": _source_content_ref(source_content_id),
            "mime_type": "text/plain; charset=utf-8",
            "checksum": book["content_checksum"],
            "byte_size": book["content_byte_size"],
            "content": source_text,
            "created_at": now,
            "updated_at": now,
        }
        STORE.source_contents[source_content_id] = content
        STORE.source_content_by_book[book_id] = source_content_id
        chapters = _split_source_text_into_chapters(book_id, source_text, now)
        STORE.chapters_by_book[book_id] = chapters
        book["chapter_count"] = len(chapters)

    _persist_store()
    return book


def get_book(book_id: str) -> Optional[dict[str, Any]]:
    return STORE.books.get(book_id)


def list_book_chapters(book_id: str) -> list[dict[str, Any]]:
    return STORE.chapters_by_book.get(book_id, [])


def get_book_source_content(book_id: str) -> Optional[dict[str, Any]]:
    source_content_id = STORE.source_content_by_book.get(book_id)
    if not source_content_id:
        return None
    return STORE.source_contents.get(source_content_id)


def list_evidence_for_book(book_id: str) -> list[dict[str, Any]]:
    return [STORE.evidences[evidence_id] for evidence_id in STORE.evidence_by_book.get(book_id, []) if evidence_id in STORE.evidences]


def get_evidence(evidence_id_or_ref: str) -> Optional[dict[str, Any]]:
    return STORE.evidences.get(_evidence_id_from_ref(evidence_id_or_ref))


def _latest_extraction_run_for_book(book_id: str) -> Optional[dict[str, Any]]:
    runs = [run for run in STORE.extraction_runs.values() if run.get("book_id") == book_id]
    if not runs:
        return None
    return sorted(runs, key=lambda item: item.get("created_at", ""), reverse=True)[0]


def _analysis_exceptions_for_run(run_id: Optional[str]) -> list[dict[str, Any]]:
    if not run_id:
        return []
    exceptions = []
    for obj in list_knowledge_objects_for_run(run_id):
        if obj.get("confidence", 1) < 0.8 and obj.get("review_status") == "pending":
            exceptions.append(
                {
                    "exception_id": f"analysis-exception-{obj['object_id']}",
                    "type": "low_confidence_object",
                    "severity": "warning",
                    "title": f"{obj.get('canonical_name', obj['object_id'])} 需要确认",
                    "summary": f"{obj.get('canonical_name', obj['object_id'])} 的置信度为 {obj.get('confidence')}，需要确认后再进入知识包。",
                    "target_ref": f"object://knowledge-objects/{obj['object_id']}",
                    "evidence_refs": deepcopy(obj.get("evidence_refs", [])),
                    "recommended_action": "approve_or_reextract",
                }
            )
    return exceptions


def get_book_analysis(book_id: str) -> Optional[dict[str, Any]]:
    book = get_book(book_id)
    if not book:
        return None
    run = _latest_extraction_run_for_book(book_id)
    run_id = run.get("run_id") if run else None
    knowledge_objects = list_knowledge_objects_for_run(run_id) if run_id else []
    evidence_samples = list_evidence_for_book(book_id)
    exceptions = _analysis_exceptions_for_run(run_id)
    scenes = [scene for chapter in list_book_chapters(book_id) for scene in STORE.source_scenes_by_chapter.get(chapter["chapter_id"], [])]
    scene_ids = {scene["scene_id"] for scene in scenes}
    events = [event for scene_id in scene_ids for event in STORE.events_by_scene.get(scene_id, [])]
    book_conflicts = [item for item in STORE.conflicts.values() if item.get("book_id") == book_id]
    book_hooks = [item for item in STORE.hooks.values() if item.get("book_id") == book_id]
    book_rewards = [item for item in STORE.rewards.values() if item.get("book_id") == book_id]
    book_climaxes = [item for item in STORE.climaxes.values() if item.get("book_id") == book_id]
    book_relationships = [item for item in STORE.relationship_edges.values() if item.get("book_id") == book_id]
    return {
        "schema_version": 1,
        "book": book,
        "run": run,
        "chapters": list_book_chapters(book_id),
        "summary": {
            "book_id": book_id,
            "run_id": run_id,
            "status": run.get("status") if run else book.get("import_status", "uploaded"),
            "current_stage": run.get("current_stage") if run else "source_submission",
            "chapter_count": len(list_book_chapters(book_id)),
            "scene_count": len(scenes) or (run.get("scene_count", 0) if run else 0),
            "event_count": len(events),
            "conflict_count": len(book_conflicts),
            "hook_count": len(book_hooks),
            "reward_count": len(book_rewards),
            "climax_count": len(book_climaxes),
            "relationship_count": len(book_relationships),
            "knowledge_object_count": len(knowledge_objects),
            "evidence_count": len(evidence_samples),
            "pattern_count": len(STORE.patterns),
            "rhythm_profile_count": len(STORE.rhythm_profiles),
            "asset_count": len(STORE.assets),
            "rule_count": len(STORE.rules),
            "needs_attention_count": len(exceptions),
            "can_commit_knowledge": bool(run and run.get("status") in {"requires_review", "succeeded"}),
        },
        "exceptions": exceptions,
        "evidence_samples": evidence_samples[:3],
        "knowledge_objects": knowledge_objects,
        "scenes": scenes,
        "events": events,
        "conflicts": book_conflicts,
        "hooks": book_hooks,
        "rewards": book_rewards,
        "climaxes": book_climaxes,
        "relationships": book_relationships,
        "patterns": list_patterns(status="approved"),
        "rhythm_profiles": list_rhythm_profiles(status="approved"),
        "assets": list_assets(status="approved"),
        "rules": list_rules(),
    }


def list_knowledge_sources(workspace_id: Optional[str] = None, status: str = "committed") -> list[dict[str, Any]]:
    current_workspace = _workspace_or_default(workspace_id)
    items = []
    for book_id, book in STORE.books.items():
        if book.get("workspace_id") != current_workspace:
            continue
        run = _latest_extraction_run_for_book(book_id)
        source_status = "committed" if run and run.get("status") == "succeeded" else book.get("import_status", "uploaded")
        if status != "all" and source_status != status:
            continue
        run_id = run.get("run_id") if run else None
        items.append(
            {
                "source_ref": f"object://source-books/{book_id}",
                "label": book["title"],
                "book_id": book_id,
                "run_id": run_id,
                "source_type": book["source_type"],
                "status": source_status,
                "knowledge_object_count": len(list_knowledge_objects_for_run(run_id)) if run_id else 0,
                "evidence_count": len(list_evidence_for_book(book_id)),
                "graph_summary_ref": f"object://graph-summaries/{book_id}" if book_id in STORE.graph_summaries else None,
                "updated_at": book.get("updated_at") or book.get("created_at"),
            }
        )
    return items


def build_knowledge_context(
    allowed_knowledge_source_refs: list[str],
    max_objects: int = 12,
    max_evidence: int = 6,
) -> dict[str, Any]:
    objects: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    graph_nodes: list[dict[str, Any]] = []
    source_labels: list[str] = []
    seen_books: set[str] = set()
    for ref in allowed_knowledge_source_refs or []:
        # 只解析书源 ref；同一本书的多个 ref（如 source-books 与 graph-summaries）只处理一次
        if not ref.startswith("object://source-books/"):
            continue
        book_id = ref.rsplit("/", 1)[-1]
        if book_id in seen_books:
            continue
        book = STORE.books.get(book_id)
        if not book:
            continue
        seen_books.add(book_id)
        source_labels.append(book.get("title", book_id))
        run = _latest_extraction_run_for_book(book_id)
        run_id = run.get("run_id") if run else None
        if run_id:
            for obj in list_knowledge_objects_for_run(run_id):
                objects.append({
                    "canonical_name": obj.get("canonical_name", ""),
                    "object_type": obj.get("object_type", ""),
                    "aliases": obj.get("payload", {}).get("aliases", []),
                    "summary": obj.get("payload", {}).get("summary", ""),
                })
        summary = get_graph_summary(book_id)
        graph_nodes.extend(summary.get("nodes", []))
        for item in list_evidence_for_book(book_id)[:max_evidence]:
            evidence.append({
                "excerpt": item.get("excerpt", ""),
                "chapter_index": item.get("chapter_index"),
            })
    objects = objects[:max_objects]
    evidence = evidence[:max_evidence]

    lines: list[str] = []
    if source_labels:
        lines.append("【可用知识源】" + "、".join(source_labels))
    if objects:
        lines.append("【人物与势力】")
        for obj in objects:
            alias_part = f"（别名：{'、'.join(obj['aliases'])}）" if obj["aliases"] else ""
            desc = f"·{obj['summary']}" if obj["summary"] else ""
            lines.append(f"- {obj['canonical_name']}[{obj['object_type']}]{alias_part}{desc}")
    if graph_nodes:
        lines.append("【图谱节点】" + "、".join(str(n.get("label", "")) for n in graph_nodes[:max_objects]))
    if evidence:
        lines.append("【原文摘录】")
        for item in evidence:
            chapter_hint = f"第{item['chapter_index']}章" if item.get("chapter_index") else ""
            lines.append(f"- {chapter_hint}「{item['excerpt']}」")
    context_text = "\n".join(lines)
    return {
        "summary": f"已汇总 {len(source_labels)} 个知识源、{len(objects)} 个对象、{len(evidence)} 条证据。" if source_labels else "",
        "objects": objects,
        "graph": {"nodes": graph_nodes[:max_objects]},
        "evidence": evidence,
        "context_text": context_text,
    }


@_persisting_mutation
def create_extraction_run(
    book_id: str,
    trace_id: str,
    request_id: str = "system-extraction",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    if book_id == BOOK_ID:
        return STORE.extraction_runs[RUN_ID]

    run_id = str(ulid.new())
    task_id = str(ulid.new())
    now = utc_now()
    task = _build_task(
        task_id=task_id,
        task_type="extract_knowledge",
        workspace_id=context["workspace_id"],
        input_refs=[f"object://source-books/{book_id}"],
        output_refs=[
            f"object://extraction-runs/{run_id}",
            f"object://knowledge-packages/{run_id}",
            f"object://graph-packages/{book_id}",
            f"object://extraction-reports/{run_id}",
            f"object://quality-reports/{run_id}",
        ],
        status="queued",
        progress=0,
        idempotency_key=f"extract-{book_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        retry_count=0,
        created_at=now,
        started_at=None,
        finished_at=None,
        latency_ms=None,
    )
    run = {
        "schema_version": 1,
        "run_id": run_id,
        "book_id": book_id,
        "workspace_id": context["workspace_id"],
        "task_id": task_id,
        "status": "queued",
        "current_stage": "source_submission",
        "chapter_count": 0,
        "scene_count": 0,
        "object_count": 0,
        "evidence_count": 0,
        "low_confidence_count": 0,
        "knowledge_package_ref": f"object://knowledge-packages/{run_id}",
        "graph_package_ref": f"object://graph-packages/{book_id}",
        "extraction_report_ref": f"object://extraction-reports/{run_id}",
        "quality_report_ref": f"object://quality-reports/{run_id}",
        "errors": [],
        "created_at": now,
        "started_at": None,
        "finished_at": None,
        "task": task,
    }
    STORE.extraction_runs[run_id] = run
    STORE.knowledge_by_run[run_id] = []
    STORE.task_events_by_task[task_id] = []
    _append_task_event(
        task,
        "created",
        "Extraction run queued.",
        task["status"],
        request_id,
        trace_id,
        context["actor_id"],
        payload_json={"book_id": book_id, "run_id": run_id},
        created_at=now,
    )
    return run


def get_extraction_run(run_id: str) -> Optional[dict[str, Any]]:
    return STORE.extraction_runs.get(run_id)


def get_extraction_report(run_id: str) -> Optional[dict[str, Any]]:
    run = STORE.extraction_runs.get(run_id)
    if not run:
        return None
    task_id = run["task_id"]
    return {
        "run": run,
        "task": run["task"],
        "events": STORE.task_events_by_task.get(task_id, []),
        "knowledge_package_ref": run.get("knowledge_package_ref"),
        "graph_package_ref": run.get("graph_package_ref"),
        "extraction_report_ref": run.get("extraction_report_ref"),
        "quality_report_ref": run.get("quality_report_ref"),
        "low_confidence_items": [
            obj for obj in list_knowledge_objects_for_run(run_id)
            if obj["confidence"] < 0.8 and obj["review_status"] == "pending"
        ],
    }


def list_knowledge_objects_for_run(run_id: str) -> list[dict[str, Any]]:
    return [STORE.knowledge_objects[object_id] for object_id in STORE.knowledge_by_run.get(run_id, [])]


@_persisting_mutation
def apply_review_action(
    object_id: str,
    action: str,
    target_object_id: Optional[str] = None,
    request_id: str = "system-review",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    obj = STORE.knowledge_objects.get(object_id)
    if not obj:
        return None

    if action == "approve":
        obj["review_status"] = "approved"
        obj["lifecycle_status"] = "approved"
    elif action == "reject":
        obj["review_status"] = "rejected"
        obj["lifecycle_status"] = "rejected"
    elif action == "merge_alias":
        obj["review_status"] = "merged"
        obj["lifecycle_status"] = "approved"
        obj["payload"]["merged_into"] = target_object_id
    elif action == "request_reextract":
        obj["review_status"] = "reextract_requested"
    else:
        raise ValueError(f"unsupported action: {action}")

    for run in STORE.extraction_runs.values():
        object_ids = STORE.knowledge_by_run.get(run["run_id"], [])
        if object_id in object_ids:
            pending = [
                STORE.knowledge_objects[current_id]
                for current_id in object_ids
                if STORE.knowledge_objects[current_id]["confidence"] < 0.8
                and STORE.knowledge_objects[current_id]["review_status"] == "pending"
            ]
            run["low_confidence_count"] = len(pending)
            if action == "request_reextract":
                run["status"] = "queued"
                run["current_stage"] = "source_submission"
                run["finished_at"] = None
                run["errors"] = []
                run["task"]["status"] = "queued"
                run["task"]["progress"] = 0
                run["task"]["retry_count"] = 0
                run["task"]["dispatch_attempt"] = 0
                run["task"]["started_at"] = None
                run["task"]["finished_at"] = None
                run["task"]["latency_ms"] = None
                run["task"]["error_code"] = None
                _clear_task_lock(run["task"])
                run["task"]["next_retry_at"] = None
                run["task"]["review_required"] = False
                run["task"]["blocked_reason"] = None
                _append_task_event(
                    run["task"],
                    "requeued",
                    "Knowledge re-extraction requested.",
                    run["task"]["status"],
                    request_id,
                    trace_id,
                    context["actor_id"],
                    payload_json={"run_id": run["run_id"], "object_id": object_id, "low_confidence_count": len(pending)},
                )
            elif run["status"] == "requires_review" and not pending:
                run["status"] = "succeeded"
                run["current_stage"] = "knowledge_package_export"
                run["task"]["status"] = "succeeded"
                run["task"]["progress"] = 100
                run["finished_at"] = utc_now()
                run["task"]["finished_at"] = run["finished_at"]
                run["task"]["latency_ms"] = 1000
                _append_task_event(
                    run["task"],
                    "succeeded",
                    "Knowledge review completed.",
                    run["task"]["status"],
                    request_id,
                    trace_id,
                    context["actor_id"],
                    payload_json={"run_id": run["run_id"], "low_confidence_count": 0},
                )
            else:
                _append_task_event(
                    run["task"],
                    "review_required",
                    "Knowledge review updated.",
                    run["task"]["status"],
                    request_id,
                    trace_id,
                    context["actor_id"],
                    payload_json={"run_id": run["run_id"], "low_confidence_count": len(pending)},
                )
            break

    _append_audit_event(
        action=f"knowledge.{action}",
        target_type="knowledge_object",
        target_id=object_id,
        target_ref=f"object://knowledge-objects/{object_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        actor_role=context["actor_role"],
        workspace_id=context["workspace_id"],
        payload={"target_object_id": target_object_id, "review_status": obj["review_status"]},
    )
    return obj


@_persisting_mutation
def commit_knowledge_package(run_id: str) -> Optional[dict[str, Any]]:
    run = STORE.extraction_runs.get(run_id)
    if not run:
        return None
    finished_at = utc_now()
    run["status"] = "succeeded"
    run["current_stage"] = "knowledge_base_commit"
    run["task"]["status"] = "succeeded"
    run["task"]["progress"] = 100
    run["task"]["review_required"] = False
    run["finished_at"] = finished_at
    run["task"]["finished_at"] = finished_at
    run["task"]["heartbeat_at"] = finished_at
    object_ids = STORE.knowledge_by_run.get(run_id, [])
    objects = [
        deepcopy(STORE.knowledge_objects[oid]) for oid in object_ids
        if oid in STORE.knowledge_objects
    ]
    book_id = run["book_id"]
    scenes = [
        scene for chapter in list_book_chapters(book_id)
        for scene in STORE.source_scenes_by_chapter.get(chapter["chapter_id"], [])
    ]
    relationships = [
        deepcopy(edge) for edge in STORE.relationship_edges.values()
        if edge.get("book_id") == book_id
    ]
    package_ref = f"object://knowledge-packages/{run_id}"
    STORE.knowledge_packages[run_id] = {
        "schema_version": 1,
        "package_ref": package_ref,
        "metadata": {
            "run_id": run_id, "book_id": book_id,
            "object_count": len(objects), "scene_count": len(scenes),
            "relationship_count": len(relationships), "committed_at": finished_at,
        },
        "source_book": deepcopy(get_book(book_id) or {}),
        "chapters": deepcopy(list_book_chapters(book_id)),
        "scenes": scenes,
        "objects": objects,
        "relationships": relationships,
    }
    run["knowledge_package_ref"] = package_ref
    return {
        "run_id": run_id,
        "status": run["status"],
        "committed_object_count": len(object_ids),
        "package_ref": package_ref,
    }


def get_graph_summary(book_id: Optional[str] = None) -> dict[str, Any]:
    selected_book_id = book_id or GRAPH_BOOK_ID
    return STORE.graph_summaries.get(selected_book_id, {
        "schema_version": 1,
        "book_id": selected_book_id,
        "node_count": 0,
        "edge_count": 0,
        "nodes": [],
    })


def search_graph_nodes(book_id: Optional[str] = None, query: str = "", node_type: Optional[str] = None) -> dict[str, Any]:
    summary = get_graph_summary(book_id)
    normalized_query = query.strip().lower()
    normalized_type = (node_type or "").strip().lower()
    items = []
    for node in summary.get("nodes", []):
        label = str(node.get("label", ""))
        current_type = str(node.get("node_type", ""))
        detail = STORE.graph_node_details.get(node.get("node_id", ""), {})
        summary_text = str(detail.get("summary", ""))
        haystack = f"{label} {current_type} {summary_text}".lower()
        if normalized_query and normalized_query not in haystack:
            continue
        if normalized_type and current_type.lower() != normalized_type:
            continue
        items.append(deepcopy(node))
    return {
        "book_id": summary.get("book_id"),
        "query": query,
        "node_type": node_type,
        "count": len(items),
        "items": items,
    }


def get_graph_node(node_id: str) -> Optional[dict[str, Any]]:
    node = STORE.graph_node_details.get(node_id)
    if not node:
        return None
    return deepcopy(node)


def list_graph_neighbors(node_id: str) -> Optional[dict[str, Any]]:
    node = STORE.graph_node_details.get(node_id)
    if not node:
        return None
    return {
        "node_id": node_id,
        "items": deepcopy(STORE.graph_neighbors_by_node.get(node_id, [])),
    }


def list_chapter_plans_for_project(project_id: str) -> list[dict[str, Any]]:
    return sorted(
        [plan for plan in STORE.chapter_plans.values() if plan["project_id"] == project_id],
        key=lambda item: item["chapter_index"],
    )


def _sorted_store_items(values: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return sorted(values, key=lambda item: item[key])


def get_configuration_snapshot() -> dict[str, Any]:
    return {
        "default_model_profile_id": DEFAULT_MODEL_PROFILE_ID,
        "workspace_id": default_workspace_id(),
        "trace_id": "trace-config-snapshot",
        "model_profiles": _sorted_store_items(list(STORE.model_profiles.values()), "model_profile_id"),
        "agent_model_assignments": _sorted_store_items(list(STORE.agent_model_assignments.values()), "assignment_id"),
        "quality_gate_profiles": _sorted_store_items(list(STORE.quality_gate_profiles.values()), "quality_gate_profile_id"),
        "prompt_versions": _sorted_store_items(list(STORE.prompt_versions), "agent_role"),
    }


@_persisting_mutation
def set_model_profile_enabled(
    model_profile_id: str,
    enabled: bool,
    request_id: str = "system-config",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner"})

    profile = STORE.model_profiles.get(model_profile_id)
    if not profile:
        return None
    profile["enabled"] = enabled
    _append_audit_event(
        action="configuration.model_profile_toggled",
        target_type="model_profile",
        target_id=model_profile_id,
        target_ref=f"object://model-profiles/{model_profile_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        actor_role=context["actor_role"],
        workspace_id=context["workspace_id"],
        payload={"enabled": enabled},
    )
    return {
        "model_profile": profile,
        "configuration_snapshot": get_configuration_snapshot(),
    }


@_persisting_mutation
def update_quality_gate_profile(
    quality_gate_profile_id: str,
    ai_flavor_threshold: float,
    originality_safety_threshold: float,
    request_id: str = "system-config",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner"})

    profile = STORE.quality_gate_profiles.get(quality_gate_profile_id)
    if not profile:
        return None
    profile["ai_flavor_threshold"] = ai_flavor_threshold
    profile["originality_safety_threshold"] = originality_safety_threshold
    _append_audit_event(
        action="configuration.quality_gate_profile_updated",
        target_type="quality_gate_profile",
        target_id=quality_gate_profile_id,
        target_ref=f"object://quality-gate-profiles/{quality_gate_profile_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        actor_role=context["actor_role"],
        workspace_id=context["workspace_id"],
        payload={
            "ai_flavor_threshold": ai_flavor_threshold,
            "originality_safety_threshold": originality_safety_threshold,
        },
    )
    return {
        "quality_gate_profile": profile,
        "configuration_snapshot": get_configuration_snapshot(),
    }


@_persisting_mutation
def update_agent_model_assignment(
    assignment_id: str,
    model_profile_id: str,
    max_retry: int,
    max_cost: float,
    enabled: bool,
    request_id: str = "system-config",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner"})

    assignment = STORE.agent_model_assignments.get(assignment_id)
    if not assignment:
        return None
    if model_profile_id not in STORE.model_profiles:
        return False
    assignment["model_profile_id"] = model_profile_id
    assignment["max_retry"] = max_retry
    assignment["max_cost"] = max_cost
    assignment["enabled"] = enabled
    _append_audit_event(
        action="configuration.agent_model_assignment_updated",
        target_type="agent_model_assignment",
        target_id=assignment_id,
        target_ref=f"object://agent-model-assignments/{assignment_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        actor_role=context["actor_role"],
        workspace_id=context["workspace_id"],
        payload={
            "model_profile_id": model_profile_id,
            "max_retry": max_retry,
            "max_cost": max_cost,
            "enabled": enabled,
        },
    )
    return {
        "agent_model_assignment": assignment,
        "configuration_snapshot": get_configuration_snapshot(),
    }


@_persisting_mutation
def update_prompt_version(
    agent_role: str,
    template_ref: str,
    request_id: str = "system-config",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner"})

    existing = next((item for item in STORE.prompt_versions if item["agent_role"] == agent_role), None)
    if existing:
        existing["template_ref"] = template_ref
        prompt_version = existing
    else:
        prompt_version = {"agent_role": agent_role, "template_ref": template_ref}
        STORE.prompt_versions.append(prompt_version)
    _append_audit_event(
        action="configuration.prompt_version_updated",
        target_type="prompt_version",
        target_id=agent_role,
        target_ref=f"object://prompt-versions/{agent_role}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        actor_role=context["actor_role"],
        workspace_id=context["workspace_id"],
        payload={"template_ref": template_ref},
    )
    return {
        "prompt_version": prompt_version,
        "configuration_snapshot": get_configuration_snapshot(),
    }


def _get_agent_assignment(agent_role: str) -> Optional[dict[str, Any]]:
    for assignment in _sorted_store_items(list(STORE.agent_model_assignments.values()), "assignment_id"):
        if assignment["agent_role"] == agent_role and assignment["enabled"]:
            return assignment
    return None


def _build_provider_call(
    agent_role: str,
    model_profile_id: str,
    provider_name: str,
    status: str,
    retry_count: int,
    error_code: Optional[str] = None,
    workspace_id: Optional[str] = None,
    task_id: Optional[str] = None,
    writing_run_id: Optional[str] = None,
    request_id: str = "system-request",
    trace_id: str = "system-trace",
    task_type: str = "chapter_generation",
    assignment_id: Optional[str] = None,
    prompt_package_id: Optional[str] = None,
    input_refs: Optional[list[str]] = None,
    output_ref: Optional[str] = None,
    fallback_from_call_id: Optional[str] = None,
) -> dict[str, Any]:
    metrics = ROLE_CALL_METRICS.get(agent_role, {"prompt_tokens": 1000, "completion_tokens": 300, "latency_ms": 800, "cost_estimate": 0.1})
    completion_tokens = metrics["completion_tokens"] if status == "succeeded" else 0
    cost_estimate = metrics["cost_estimate"] if status == "succeeded" else round(metrics["cost_estimate"] / 2, 2)
    latency_ms = metrics["latency_ms"] if status == "succeeded" else max(200, metrics["latency_ms"] // 2)
    profile = STORE.model_profiles.get(model_profile_id)
    provider_account = next((item for item in STORE.provider_accounts.values() if item["provider_name"] == provider_name and item["status"] == "active"), None)
    return {
        "schema_version": 1,
        "provider_call_id": str(ulid.new()),
        "workspace_id": workspace_id or default_workspace_id(),
        "task_id": task_id,
        "writing_run_id": writing_run_id,
        "request_id": request_id,
        "trace_id": trace_id,
        "agent_role": agent_role,
        "task_type": task_type,
        "assignment_id": assignment_id,
        "model_profile_id": model_profile_id,
        "provider_name": provider_name,
        "provider_model_name": profile["provider_model_name"] if profile else model_profile_id,
        "provider_account_id": provider_account["provider_account_id"] if provider_account else None,
        "prompt_package_id": prompt_package_id,
        "input_refs": deepcopy(input_refs or []),
        "output_ref": output_ref,
        "prompt_tokens": metrics["prompt_tokens"],
        "completion_tokens": completion_tokens,
        "latency_ms": latency_ms,
        "retry_count": retry_count,
        "cost_estimate": cost_estimate,
        "cost_estimate_status": "estimated",
        "status": status,
        "error_code": error_code,
        "fallback_from_call_id": fallback_from_call_id,
        "created_at": utc_now(),
    }


def resolve_model_profile(
    agent_role: str,
    requested_profile_id: Optional[str] = None,
    require_structured_output: bool = False,
) -> dict[str, Any]:
    assignment = _get_agent_assignment(agent_role)
    primary_profile_id = requested_profile_id
    fallback_profile_ids: list[str] = []
    if requested_profile_id:
        profile = STORE.model_profiles.get(requested_profile_id)
        fallback_profile_ids = list(profile["fallback_profile_ids"]) if profile else []
    elif assignment:
        primary_profile_id = assignment["model_profile_id"]
        fallback_profile_ids = list(assignment["fallback_profile_ids"])

    retry_count = 0
    provider_calls: list[dict[str, Any]] = []
    for candidate_id in [primary_profile_id, *fallback_profile_ids]:
        if not candidate_id:
            continue
        profile = STORE.model_profiles.get(candidate_id)
        if not profile or not profile["enabled"]:
            continue
        if require_structured_output and not profile["supports_structured_output"]:
            retry_count += 1
            provider_calls.append(
                _build_provider_call(
                    agent_role,
                    candidate_id,
                    profile["provider_name"],
                    "failed",
                    retry_count,
                    "structured_output_validation_failed",
                    task_type=assignment["task_type"] if assignment else f"{agent_role}_task",
                    assignment_id=assignment["assignment_id"] if assignment else None,
                    fallback_from_call_id=provider_calls[-1]["provider_call_id"] if provider_calls else None,
                )
            )
            continue
        return {
            "selected_profile": profile,
            "assignment": assignment,
            "retry_count": retry_count,
            "provider_calls": provider_calls,
        }

    return {
        "selected_profile": None,
        "assignment": assignment,
        "retry_count": retry_count,
        "provider_calls": provider_calls,
    }


def _build_model_cost(provider_calls: list[dict[str, Any]], retry_count: int) -> dict[str, Any]:
    successful_calls = [item for item in provider_calls if item["status"] == "succeeded"]
    by_role = {item["agent_role"]: item for item in successful_calls}
    return {
        "input_tokens": sum(item["prompt_tokens"] for item in successful_calls),
        "output_tokens": sum(item["completion_tokens"] for item in successful_calls),
        "estimated_total_cost": round(sum(item["cost_estimate"] for item in successful_calls), 2),
        "retry_count": retry_count,
        "writer_input_tokens": by_role.get("writer", {}).get("prompt_tokens", 0),
        "writer_output_tokens": by_role.get("writer", {}).get("completion_tokens", 0),
        "critic_input_tokens": by_role.get("critic", {}).get("prompt_tokens", 0),
        "critic_output_tokens": by_role.get("critic", {}).get("completion_tokens", 0),
        "humanizer_input_tokens": by_role.get("humanizer", {}).get("prompt_tokens", 0),
        "humanizer_output_tokens": by_role.get("humanizer", {}).get("completion_tokens", 0),
    }


def _find_consistency_issue(report: Optional[dict[str, Any]], issue_id: Optional[str]) -> Optional[dict[str, Any]]:
    if not report or not issue_id:
        return None
    return next((item for item in report["issues"] if item["issue_id"] == issue_id), None)


def _quality_issue_matches_consistency_issue(issue: dict[str, Any], candidate: dict[str, Any]) -> bool:
    if candidate.get("issue_id") == issue["issue_id"]:
        return True
    return candidate.get("rule_id") == issue.get("rule_id") and candidate.get("affected_text_ref") == issue.get("affected_text_ref")


def _sync_writing_run_phase_one_state(writing_run: dict[str, Any]) -> None:
    consistency_report_id = writing_run.get("consistency_report_id")
    revision_summary_id = writing_run.get("revision_summary_id")
    consistency_report = STORE.consistency_reports.get(consistency_report_id) if consistency_report_id else None
    revision_summary = STORE.revision_summaries.get(revision_summary_id) if revision_summary_id else None
    writing_run["provider_calls"] = deepcopy(STORE.provider_calls_by_writing.get(writing_run["writing_run_id"], []))
    writing_run["consistency_report"] = deepcopy(consistency_report) if consistency_report else None
    writing_run["revision_summary"] = deepcopy(revision_summary) if revision_summary else None
    if revision_summary:
        writing_run["revision_round"] = revision_summary["revision_round"]
        writing_run["max_revision_rounds"] = revision_summary["max_revision_rounds"]


@_persisting_mutation
def create_novel_project(
    payload: dict[str, Any],
    trace_id: str,
    request_id: str = "system-project",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    context = _actor_context(workspace_id or payload.get("workspace_id"), actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    project_id = str(ulid.new())
    story_bible_id = str(ulid.new())
    now = utc_now()
    explicit_knowledge_source_refs = "allowed_knowledge_source_refs" in payload
    allowed_knowledge_source_refs = payload.get(
        "allowed_knowledge_source_refs",
        [f"object://source-books/{BOOK_ID}"],
    )
    if explicit_knowledge_source_refs:
        available_source_refs = {item["source_ref"] for item in list_knowledge_sources(context["workspace_id"], status="all")}
        available_source_refs.update(item["graph_summary_ref"] for item in list_knowledge_sources(context["workspace_id"], status="all") if item.get("graph_summary_ref"))
        for source_ref in allowed_knowledge_source_refs:
            if source_ref not in available_source_refs:
                raise ValueError("knowledge source not found")
    project = {
        "schema_version": 1,
        "project_id": project_id,
        "workspace_id": context["workspace_id"],
        "title": payload["title"],
        "genre_scope": payload["genre_scope"],
        "status": "planning",
        "story_bible_id": story_bible_id,
        "quality_gate_profile_id": payload.get("quality_gate_profile_id", QUALITY_GATE_PROFILE_ID),
        "allowed_knowledge_source_refs": allowed_knowledge_source_refs,
        "created_at": now,
        "updated_at": now,
    }
    story_bible = {
        "schema_version": 1,
        "story_bible_id": story_bible_id,
        "workspace_id": project["workspace_id"],
        "project_id": project_id,
        "version": 1,
        "status": "draft",
        "payload": _normalize_story_bible_payload(payload.get("story_bible_payload"), payload["title"]),
        "confirmed_payload": None,
        "diff": None,
        "history": [],
        "trace_id": trace_id,
        "approved_at": None,
        "approved_by": None,
        "created_at": now,
        "updated_at": now,
    }
    _hydrate_story_bible(story_bible)
    STORE.novel_projects[project_id] = project
    STORE.story_bibles[story_bible_id] = story_bible
    _persist_store()
    return {
        "project": project,
        "story_bible": story_bible,
        "chapter_plans": [],
    }


def get_novel_project(project_id: str) -> Optional[dict[str, Any]]:
    project = STORE.novel_projects.get(project_id)
    if not project:
        return None
    story_bible = STORE.story_bibles.get(project["story_bible_id"])
    hydrated_story_bible = deepcopy(_hydrate_story_bible(story_bible)) if story_bible else None
    return {
        "project": project,
        "story_bible": hydrated_story_bible,
        "chapter_plans": list_chapter_plans_for_project(project_id),
        "patterns": list_patterns(status="approved"),
        "rhythm_profiles": list_rhythm_profiles(status="approved"),
        "assets": list_assets(status="approved"),
    }


def get_story_bible(story_bible_id: str) -> Optional[dict[str, Any]]:
    story_bible = STORE.story_bibles.get(story_bible_id)
    if not story_bible:
        return None
    return deepcopy(_hydrate_story_bible(story_bible))


def _llm_json(system: str, user: str) -> Optional[dict[str, Any]]:
    base_url = os.getenv("NOVELIST_LLM_BASE_URL")
    api_key = os.getenv("NOVELIST_LLM_API_KEY")
    if not base_url or not api_key:
        return None
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
    endpoint = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0.5,
        "max_tokens": 1200,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")
    request = Request(endpoint, data=body, headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        parsed = json.loads(payload["choices"][0]["message"]["content"])
        return parsed if isinstance(parsed, dict) else None
    except (HTTPError, URLError, TimeoutError, KeyError, IndexError, TypeError, ValueError):
        return None


def _deterministic_enhance_story_bible(current_payload: dict[str, Any]) -> dict[str, Any]:
    enhanced = deepcopy(current_payload) if isinstance(current_payload, dict) else {}
    protagonist = enhanced.get("protagonist", "主角")
    world_rules = list(enhanced.get("world_rules", []))
    # 用现有条数派生递增规则，保证每次再生都产生真实变化（非幂等 no-op）
    round_index = len(world_rules) + 1
    new_rule = f"{protagonist}在第{round_index}层设定中，每次突破都需付出与之相称的真实代价。"
    if new_rule not in world_rules:
        world_rules.append(new_rule)
    enhanced["world_rules"] = world_rules
    promises = list(enhanced.get("narrative_promises", []))
    promise_index = len(promises) + 1
    new_promise = f"第{promise_index}轮承诺：进一步夯实{protagonist}的核心动机与下一处转折。"
    if new_promise not in promises:
        promises.append(new_promise)
    enhanced["narrative_promises"] = promises
    return enhanced


def _generate_story_bible_candidate(current_payload: dict[str, Any], note: Optional[str]) -> Optional[dict[str, Any]]:
    generated = _llm_json(
        system="你是中文小说故事圣经编辑。基于当前故事圣经补强世界规则与叙事承诺，保持前提与主角一致。只输出 JSON，键：premise, protagonist, core_conflict, style_target, forbidden_similarities, world_rules(数组), narrative_promises(数组)。",
        user=f"当前故事圣经：{json.dumps(current_payload, ensure_ascii=False)}\n补强方向：{note or '强化世界观与叙事承诺'}",
    )
    return generated


@_persisting_mutation
def apply_story_bible_action(
    story_bible_id: str,
    action: str,
    request_id: str = "system-story-bible",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
    payload: Optional[dict[str, Any]] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    story_bible = STORE.story_bibles.get(story_bible_id)
    if not story_bible:
        return None

    now = utc_now()
    note = (payload or {}).get("note")
    summary = (payload or {}).get("summary")
    project = STORE.novel_projects.get(story_bible["project_id"])
    normalized_current = _normalize_story_bible_payload(story_bible.get("payload"), project.get("title") if project else None)

    if action == "confirm":
        story_bible["status"] = "approved"
        story_bible["confirmed_payload"] = deepcopy(normalized_current)
        story_bible["approved_at"] = now
        story_bible["approved_by"] = context["actor_id"]
        changed_fields = []
        final_summary = summary or "确认当前故事圣经版本。"
    elif action == "reject":
        story_bible["status"] = "rejected"
        changed_fields = []
        final_summary = summary or "驳回当前故事圣经版本。"
    elif action == "regenerate":
        explicit = (payload or {}).get("story_bible_payload")
        if explicit:
            next_payload = _normalize_story_bible_payload(explicit, project.get("title") if project else None)
        else:
            candidate = _generate_story_bible_candidate(normalized_current, note) or _deterministic_enhance_story_bible(normalized_current)
            next_payload = _normalize_story_bible_payload(candidate, project.get("title") if project else None)
        previous_version = story_bible.get("version", 1)
        previous_payload = deepcopy(story_bible.get("payload"))
        story_bible["version"] = previous_version + 1
        story_bible["status"] = "pending_review"
        story_bible["payload"] = deepcopy(next_payload)
        story_bible["diff"] = _story_bible_diff(
            previous_version,
            story_bible["version"],
            previous_payload,
            next_payload,
            summary or "补强故事圣经候选版本。",
        )
        changed_fields = story_bible["diff"]["changed_fields"]
        final_summary = story_bible["diff"]["summary"]
    else:
        raise ValueError(f"unsupported action: {action}")

    story_bible["updated_at"] = now
    story_bible.setdefault("history", []).append(
        _story_bible_history_entry(
            version=story_bible["version"],
            status=story_bible["status"],
            change_type=action,
            payload=story_bible["payload"],
            changed_fields=changed_fields,
            summary=final_summary,
            trace_id=trace_id,
            actor_id=context["actor_id"],
            created_at=now,
            note=note,
        )
    )
    if action != "regenerate":
        story_bible["diff"] = None

    _append_audit_event(
        action=f"story_bible.{action}",
        target_type="story_bible",
        target_id=story_bible_id,
        target_ref=f"object://story-bibles/{story_bible_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        actor_role=context["actor_role"],
        workspace_id=context["workspace_id"],
        reason=note,
        payload={
            "version": story_bible["version"],
            "status": story_bible["status"],
            "changed_fields": changed_fields,
        },
        created_at=now,
    )
    return deepcopy(_hydrate_story_bible(story_bible))


@_persisting_mutation
def create_chapter_plan(
    payload: dict[str, Any],
    trace_id: str,
    request_id: str = "system-plan",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id or payload.get("workspace_id"), actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    project_id = payload["project_id"]
    if project_id not in STORE.novel_projects:
        return None

    chapter_plan_id = str(ulid.new())
    task_id = str(ulid.new())
    now = utc_now()
    chapter_plan = {
        "schema_version": 1,
        "chapter_plan_id": chapter_plan_id,
        "workspace_id": context["workspace_id"],
        "project_id": project_id,
        "trace_id": trace_id,
        "input_refs": [f"object://novel-projects/{project_id}"],
        "output_refs": [f"object://chapter-plans/{chapter_plan_id}"],
        "chapter_index": payload["chapter_index"],
        "status": "queued",
        "target_word_count": payload["target_word_count"],
        "payload": payload.get("payload", {}),
        "created_at": now,
        "updated_at": now,
    }
    task = _build_task(
        task_id=task_id,
        task_type="create_chapter_plan",
        workspace_id=chapter_plan["workspace_id"],
        input_refs=chapter_plan["input_refs"],
        output_refs=chapter_plan["output_refs"],
        status="queued",
        progress=0,
        idempotency_key=f"plan-{project_id}-{payload['chapter_index']}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        retry_count=0,
        created_at=now,
        started_at=None,
        finished_at=None,
        latency_ms=None,
    )
    STORE.chapter_plans[chapter_plan_id] = chapter_plan
    STORE.chapter_plan_tasks[chapter_plan_id] = task
    STORE.section_plans_by_chapter[chapter_plan_id] = []
    STORE.task_events_by_task[task_id] = []
    _append_task_event(
        task,
        "created",
        "Chapter plan queued.",
        task["status"],
        request_id,
        trace_id,
        context["actor_id"],
        payload_json={"chapter_index": payload["chapter_index"], "chapter_plan_id": chapter_plan_id},
        created_at=now,
    )
    return {
        "chapter_plan": chapter_plan,
        "task": task,
        "events": STORE.task_events_by_task[task_id],
    }


def get_chapter_plan(chapter_plan_id: str) -> Optional[dict[str, Any]]:
    chapter_plan = STORE.chapter_plans.get(chapter_plan_id)
    if not chapter_plan:
        return None
    task = STORE.chapter_plan_tasks.get(chapter_plan_id)
    events = STORE.task_events_by_task.get(task["task_id"], []) if task else []
    return {
        "chapter_plan": chapter_plan,
        "task": task,
        "events": events,
        "section_plan_count": len(STORE.section_plans_by_chapter.get(chapter_plan_id, [])),
        "pattern_options": list_patterns(status="approved"),
        "rhythm_profile_options": list_rhythm_profiles(status="approved", target_id=chapter_plan_id),
        "asset_options": list_assets(status="approved"),
    }


def list_section_plans(chapter_plan_id: str) -> Optional[dict[str, Any]]:
    if chapter_plan_id not in STORE.chapter_plans:
        return None
    task = STORE.section_plan_tasks.get(chapter_plan_id)
    events = STORE.task_events_by_task.get(task["task_id"], []) if task else []
    return {
        "chapter_plan_id": chapter_plan_id,
        "items": STORE.section_plans_by_chapter.get(chapter_plan_id, []),
        "task": task,
        "events": events,
        "pattern_options": list_patterns(status="approved"),
        "rhythm_profile_options": list_rhythm_profiles(status="approved", target_id=chapter_plan_id),
        "asset_options": list_assets(status="approved"),
    }


@_persisting_mutation
def create_section_plans(
    chapter_plan_id: str,
    section_count: int,
    trace_id: str,
    request_id: str = "system-plan",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    chapter_plan = STORE.chapter_plans.get(chapter_plan_id)
    if not chapter_plan:
        return None

    existing_items = STORE.section_plans_by_chapter.get(chapter_plan_id, [])
    if existing_items:
        task = STORE.section_plan_tasks.get(chapter_plan_id)
        events = STORE.task_events_by_task.get(task["task_id"], []) if task else []
        return {
            "chapter_plan_id": chapter_plan_id,
            "items": existing_items,
            "task": task,
            "events": events,
            "pattern_options": list_patterns(status="approved"),
            "rhythm_profile_options": list_rhythm_profiles(status="approved", target_id=chapter_plan_id),
            "asset_options": list_assets(status="approved"),
        }

    task_id = str(ulid.new())
    now = utc_now()
    roles = ["setup", "conflict", "turn", "payoff"]
    items = []
    for section_index, role in enumerate(roles[:section_count], start=1):
        items.append(
            {
                "schema_version": 1,
                "section_plan_id": str(ulid.new()),
                "workspace_id": chapter_plan["workspace_id"],
                "chapter_plan_id": chapter_plan_id,
                "trace_id": trace_id,
                "input_refs": [f"object://chapter-plans/{chapter_plan_id}"],
                "output_refs": [f"object://section-plans/{chapter_plan_id}:{section_index}"],
                "section_index": section_index,
                "planning_role": role,
                "payload": {
                    "scene_goal": f"第 {section_index} 节聚焦 {role} 段落。",
                    "beats": [
                        {"index": 1, "summary": f"{role} 节奏起势"},
                        {"index": 2, "summary": f"{role} 节奏收束"},
                    ],
                },
                "created_at": now,
                "updated_at": now,
            }
        )

    task = _build_task(
        task_id=task_id,
        task_type="create_section_plans",
        workspace_id=chapter_plan["workspace_id"],
        input_refs=[f"object://chapter-plans/{chapter_plan_id}"],
        output_refs=[f"object://section-plans/{item['section_plan_id']}" for item in items],
        status="succeeded",
        progress=100,
        idempotency_key=f"section-{chapter_plan_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        retry_count=0,
        created_at=now,
        started_at=now,
        finished_at=now,
        latency_ms=1000,
    )
    STORE.section_plans_by_chapter[chapter_plan_id] = items
    STORE.section_plan_tasks[chapter_plan_id] = task
    STORE.task_events_by_task[task_id] = []
    _append_task_event(
        task,
        "created",
        "Section plan generation started.",
        task["status"],
        request_id,
        trace_id,
        context["actor_id"],
        payload_json={"section_count": len(items)},
        created_at=now,
    )
    _append_task_event(
        task,
        "succeeded",
        "Section plans generated.",
        task["status"],
        request_id,
        trace_id,
        context["actor_id"],
        payload_json={"section_count": len(items)},
        created_at=now,
    )
    chapter_plan["status"] = "requires_review"
    chapter_plan["updated_at"] = now
    return {
        "chapter_plan_id": chapter_plan_id,
        "items": items,
        "task": task,
        "events": STORE.task_events_by_task[task_id],
        "pattern_options": list_patterns(status="approved"),
        "rhythm_profile_options": list_rhythm_profiles(status="approved", target_id=chapter_plan_id),
        "asset_options": list_assets(status="approved"),
    }


@_persisting_mutation
def create_writing_run(
    payload: dict[str, Any],
    trace_id: str,
    request_id: str = "system-writing",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id or payload.get("workspace_id"), actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    project_id = payload["project_id"]
    chapter_plan_id = payload["chapter_plan_id"]
    if project_id not in STORE.novel_projects or chapter_plan_id not in STORE.chapter_plans:
        return None

    if chapter_plan_id == CHAPTER_PLAN_ID:
        return get_writing_run(WRITING_RUN_ID)

    writing_run_id = str(ulid.new())
    task_id = str(ulid.new())
    memory_package_id = str(ulid.new())
    prompt_package_id = str(ulid.new())
    quality_report_id = str(ulid.new())
    chapter_draft_id = str(ulid.new())
    consistency_report_id = str(ulid.new())
    revision_summary_id = str(ulid.new())
    now = utc_now()

    prior_state = STORE.manuscript_states_by_project.get(project_id)
    prior_context = ""
    if prior_state:
        prior_lines = [item["summary"] for item in prior_state.get("prior_summary_pack", [])]
        prior_context = "【前情提要】\n" + "\n".join(prior_lines) + f"\n当前故事状态：{prior_state.get('current_story_state', {}).get('summary', '')}"

    section_plans = STORE.section_plans_by_chapter.get(chapter_plan_id, [])
    if not section_plans:
        return None

    writer_resolution = resolve_model_profile("writer", payload.get("writer_model_profile_id"))
    critic_resolution = resolve_model_profile(
        "critic",
        payload.get("critic_model_profile_id"),
        require_structured_output=True,
    )
    humanizer_resolution = resolve_model_profile("humanizer", payload.get("humanizer_model_profile_id"))
    if not writer_resolution["selected_profile"] or not critic_resolution["selected_profile"] or not humanizer_resolution["selected_profile"]:
        return None

    writer_input_refs = [
        f"object://chapter-plans/{chapter_plan_id}",
        f"object://memory-packages/{memory_package_id}",
        f"object://prompt-packages/{prompt_package_id}",
    ]
    critic_input_refs = [f"object://writing-runs/{writing_run_id}"]
    humanizer_input_refs = [f"object://writing-runs/{writing_run_id}"]
    writer_assignment = writer_resolution["assignment"]
    critic_assignment = critic_resolution["assignment"]
    humanizer_assignment = humanizer_resolution["assignment"]
    provider_calls = [
        *writer_resolution["provider_calls"],
        _build_provider_call(
            "writer",
            writer_resolution["selected_profile"]["model_profile_id"],
            writer_resolution["selected_profile"]["provider_name"],
            "succeeded",
            writer_resolution["retry_count"],
            workspace_id=context["workspace_id"],
            task_id=task_id,
            writing_run_id=writing_run_id,
            request_id=request_id,
            trace_id=trace_id,
            task_type=writer_assignment["task_type"] if writer_assignment else "writer_task",
            assignment_id=writer_assignment["assignment_id"] if writer_assignment else None,
            prompt_package_id=prompt_package_id,
            input_refs=writer_input_refs,
            output_ref=f"object://drafts/{chapter_draft_id}",
            fallback_from_call_id=writer_resolution["provider_calls"][-1]["provider_call_id"] if writer_resolution["provider_calls"] else None,
        ),
        *critic_resolution["provider_calls"],
        _build_provider_call(
            "critic",
            critic_resolution["selected_profile"]["model_profile_id"],
            critic_resolution["selected_profile"]["provider_name"],
            "succeeded",
            critic_resolution["retry_count"],
            workspace_id=context["workspace_id"],
            task_id=task_id,
            writing_run_id=writing_run_id,
            request_id=request_id,
            trace_id=trace_id,
            task_type=critic_assignment["task_type"] if critic_assignment else "critic_task",
            assignment_id=critic_assignment["assignment_id"] if critic_assignment else None,
            prompt_package_id=prompt_package_id,
            input_refs=critic_input_refs,
            output_ref=f"object://consistency-reports/{consistency_report_id}",
            fallback_from_call_id=critic_resolution["provider_calls"][-1]["provider_call_id"] if critic_resolution["provider_calls"] else None,
        ),
        *humanizer_resolution["provider_calls"],
        _build_provider_call(
            "humanizer",
            humanizer_resolution["selected_profile"]["model_profile_id"],
            humanizer_resolution["selected_profile"]["provider_name"],
            "succeeded",
            humanizer_resolution["retry_count"],
            workspace_id=context["workspace_id"],
            task_id=task_id,
            writing_run_id=writing_run_id,
            request_id=request_id,
            trace_id=trace_id,
            task_type=humanizer_assignment["task_type"] if humanizer_assignment else "humanizer_task",
            assignment_id=humanizer_assignment["assignment_id"] if humanizer_assignment else None,
            prompt_package_id=prompt_package_id,
            input_refs=humanizer_input_refs,
            output_ref=f"object://writing-runs/{writing_run_id}",
            fallback_from_call_id=humanizer_resolution["provider_calls"][-1]["provider_call_id"] if humanizer_resolution["provider_calls"] else None,
        ),
    ]
    retry_count = max(
        writer_resolution["retry_count"],
        critic_resolution["retry_count"],
        humanizer_resolution["retry_count"],
    )
    provider_calls = [
        {
            **call,
            "workspace_id": context["workspace_id"],
            "task_id": task_id,
            "writing_run_id": writing_run_id,
            "request_id": request_id,
            "trace_id": trace_id,
        }
        for call in provider_calls
    ]

    STORE.memory_packages[memory_package_id] = {
        "schema_version": 1,
        "memory_package_id": memory_package_id,
        "workspace_id": context["workspace_id"],
        "project_id": project_id,
        "writing_run_id": writing_run_id,
        "summary": "已组装章节规划、故事设定与知识证据。",
        "source_refs": [
            f"object://chapter-plans/{chapter_plan_id}",
            f"object://story-bibles/{STORE.novel_projects[project_id]['story_bible_id']}",
        ],
        "source_snapshot_id": f"snapshot://knowledge-state/{writing_run_id}",
        "created_at": now,
        "updated_at": now,
    }
    STORE.prompt_packages[prompt_package_id] = {
        "schema_version": 1,
        "prompt_package_id": prompt_package_id,
        "workspace_id": context["workspace_id"],
        "project_id": project_id,
        "writing_run_id": writing_run_id,
        "summary": "写手与润色阶段共用提示包。",
        "template_refs": [
            "prompt://writer/chapter-default",
            "prompt://critic/chapter-default",
            "prompt://humanizer/chapter-default",
        ],
        "created_at": now,
        "updated_at": now,
    }

    section_runs = []
    for section in section_plans:
        section_runs.append(
            {
                "schema_version": 1,
                "section_run_id": str(ulid.new()),
                "workspace_id": context["workspace_id"],
                "writing_run_id": writing_run_id,
                "section_plan_id": section["section_plan_id"],
                "status": "planned",
                "draft_object_ref": f"object://drafts/{section['section_plan_id']}",
                "critic_report_ref": f"object://critic-reports/{section['section_plan_id']}",
                "humanized_object_ref": f"object://humanized/{section['section_plan_id']}",
                "model_profile_id": writer_resolution["selected_profile"]["model_profile_id"],
                "beat_status": [
                    {"index": beat["index"], "status": "planned"}
                    for beat in section["payload"].get("beats", [])
                ],
                "writer_output": "",
                "critic_issues": [],
                "humanized_text": "",
                "created_at": now,
                "updated_at": now,
            }
        )

    task = _build_task(
        task_id=task_id,
        task_type="create_writing_run",
        workspace_id=context["workspace_id"],
        input_refs=writer_input_refs,
        output_refs=[f"object://writing-runs/{writing_run_id}"],
        status="queued",
        progress=0,
        idempotency_key=f"writing-{chapter_plan_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        retry_count=retry_count,
        created_at=now,
        started_at=None,
        finished_at=None,
        latency_ms=None,
    )
    consistency_report_id = str(ulid.new())
    revision_summary_id = str(ulid.new())
    writing_run = {
        "schema_version": 1,
        "writing_run_id": writing_run_id,
        "workspace_id": context["workspace_id"],
        "project_id": project_id,
        "chapter_plan_id": chapter_plan_id,
        "status": "queued",
        "task_id": task_id,
        "memory_package_id": memory_package_id,
        "prompt_package_id": prompt_package_id,
        "chapter_draft_id": chapter_draft_id,
        "quality_report_id": quality_report_id,
        "trace_id": trace_id,
        "current_stage": "queued",
        "writer_model_profile_id": writer_resolution["selected_profile"]["model_profile_id"],
        "critic_model_profile_id": critic_resolution["selected_profile"]["model_profile_id"],
        "humanizer_model_profile_id": humanizer_resolution["selected_profile"]["model_profile_id"],
        "assembled_chapter": "",
        "prior_context": prior_context,
        "model_cost": _build_model_cost(provider_calls, retry_count),
        "provider_calls": deepcopy(provider_calls),
        "accepted_into_manuscript_at": None,
        "accepted_chapter_ref": None,
        "chapter_snapshot_id": None,
        "manuscript_state_id": None,
        "chapter_snapshot": None,
        "manuscript_state": None,
        "consistency_report_id": consistency_report_id,
        "consistency_report": None,
        "revision_summary_id": revision_summary_id,
        "revision_summary": None,
        "revision_round": 0,
        "max_revision_rounds": 3,
        "created_at": now,
        "updated_at": now,
    }
    quality_report = {
        "schema_version": 1,
        "quality_report_id": quality_report_id,
        "workspace_id": context["workspace_id"],
        "writing_run_id": writing_run_id,
        "status": "queued",
        "ai_flavor_score": 0,
        "mobile_readability_score": 0,
        "originality_safety_score": 0,
        "human_review_required": False,
        "blocking_issues": [],
        "created_at": now,
        "updated_at": now,
    }
    consistency_report = {
        "schema_version": 1,
        "consistency_report_id": consistency_report_id,
        "workspace_id": context["workspace_id"],
        "writing_run_id": writing_run_id,
        "trace_id": trace_id,
        "task_id": task_id,
        "status": "queued",
        "issue_count": 0,
        "blocking_issue_count": 0,
        "checked_domains": ["character_continuity", "power_system_constraint"],
        "issues": [],
        "input_refs": [f"object://writing-runs/{writing_run_id}"],
        "output_refs": [f"object://consistency-reports/{consistency_report_id}"],
        "created_at": now,
        "updated_at": now,
    }
    revision_summary = {
        "schema_version": 1,
        "revision_summary_id": revision_summary_id,
        "workspace_id": context["workspace_id"],
        "writing_run_id": writing_run_id,
        "trace_id": trace_id,
        "status": "queued",
        "revision_round": 0,
        "max_revision_rounds": 3,
        "source_issue_ids": [],
        "change_summary": "待一致性复核完成后生成修订要求。",
        "revision_diff_ref": None,
        "reviewer_note_ref": None,
        "input_refs": [f"object://consistency-reports/{consistency_report_id}"],
        "output_refs": [f"object://revision-summaries/{revision_summary_id}"],
        "created_at": now,
        "updated_at": now,
    }

    STORE.writing_runs[writing_run_id] = writing_run
    STORE.writing_run_tasks[writing_run_id] = task
    STORE.provider_calls_by_writing[writing_run_id] = provider_calls
    STORE.section_runs_by_writing[writing_run_id] = section_runs
    STORE.quality_reports[quality_report_id] = quality_report
    STORE.consistency_reports[consistency_report_id] = consistency_report
    STORE.revision_summaries[revision_summary_id] = revision_summary
    _sync_writing_run_phase_one_state(writing_run)
    STORE.task_events_by_task[task_id] = []
    _append_task_event(
        task,
        "created",
        "Writing run queued.",
        task["status"],
        request_id,
        trace_id,
        context["actor_id"],
        payload_json={"writing_run_id": writing_run_id},
        created_at=now,
    )
    return get_writing_run(writing_run_id)


def list_feedback_records(target_type: Optional[str] = None, target_id: Optional[str] = None) -> list[dict[str, Any]]:
    records = list(STORE.feedback_records.values())
    if target_type:
        records = [item for item in records if item["target_type"] == target_type]
    if target_id:
        records = [item for item in records if item["target_id"] == target_id]
    return sorted(records, key=lambda item: item["created_at"])


def get_prompt_ranking_snapshot(target_id: Optional[str] = None) -> Optional[dict[str, Any]]:
    snapshot = STORE.ranking_snapshots.get("prompt")
    if not snapshot:
        return None
    if target_id and target_id not in snapshot.get("scope_ref", ""):
        return None
    return deepcopy(snapshot)


@_persisting_mutation
def promote_feedback_record(
    feedback_record_id: str,
    promotion_status: str,
    output_ref: Optional[str],
    request_id: str = "system-feedback",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    record = STORE.feedback_records.get(feedback_record_id)
    if not record:
        return None
    record["promotion_status"] = promotion_status
    record["updated_at"] = utc_now()
    if output_ref:
        record["output_refs"] = [output_ref]
    _append_audit_event(
        action="feedback.record_promoted",
        target_type="feedback_record",
        target_id=feedback_record_id,
        target_ref=f"object://feedback-records/{feedback_record_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        actor_role=context["actor_role"],
        workspace_id=context["workspace_id"],
        after_ref=output_ref,
        payload={"promotion_status": promotion_status},
    )
    return record


@_persisting_mutation
def create_agent_task(
    payload: dict[str, Any],
    request_id: str = "system-task",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    context = _actor_context(workspace_id or payload.get("workspace_id"), actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    existing = next((item for item in STORE.agent_tasks.values() if item["idempotency_key"] == payload["idempotency_key"]), None)
    if existing:
        return {
            "task": existing,
            "events": STORE.task_events_by_task.get(existing["task_id"], []),
        }

    task_id = str(ulid.new())
    now = utc_now()
    task = _build_task(
        task_id=task_id,
        task_type=payload["task_type"],
        workspace_id=context["workspace_id"],
        input_refs=payload["input_refs"],
        output_refs=[],
        status="queued",
        progress=0,
        idempotency_key=payload["idempotency_key"],
        request_id=request_id,
        trace_id=trace_id,
        actor_id=payload["requested_by"],
        retry_count=0,
        created_at=now,
        started_at=None,
        finished_at=None,
        latency_ms=0,
    )
    task["owner_module"] = payload["owner_module"]
    STORE.agent_tasks[task_id] = task
    STORE.task_events_by_task[task_id] = []
    _append_task_event(
        task,
        "created",
        f"{payload['task_type']} queued.",
        task["status"],
        request_id,
        trace_id,
        context["actor_id"],
        payload_json={"owner_module": payload["owner_module"]},
        created_at=now,
    )
    return {
        "task": task,
        "events": STORE.task_events_by_task[task_id],
    }


def get_agent_task(task_id: str) -> Optional[dict[str, Any]]:
    task = STORE.agent_tasks.get(task_id)
    if not task:
        return None
    return {
        "task": task,
        "events": STORE.task_events_by_task.get(task_id, []),
    }


@_persisting_mutation
def list_runtime_tasks(status: Optional[str] = None) -> list[dict[str, Any]]:
    tasks = [
        *[run["task"] for run in STORE.extraction_runs.values() if run.get("task")],
        *STORE.chapter_plan_tasks.values(),
        *STORE.section_plan_tasks.values(),
        *STORE.writing_run_tasks.values(),
        *STORE.agent_tasks.values(),
    ]
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    return sorted((deepcopy(task) for task in tasks), key=lambda item: (item["created_at"], item["task_id"]))


@_persisting_mutation
def schedule_task_retry(
    task_id: str,
    error_code: str,
    trace_id: str,
    request_id: str = "system-scheduler",
    actor_id: str = "scheduler",
    retry_at: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    task, task_kind, entity_id = _find_task_record(task_id)
    if not task or not _can_schedule_retry(task):
        return deepcopy(task) if task else None
    now = utc_now()
    next_retry_at = retry_at or _isoformat_utc(datetime.now(timezone.utc) + timedelta(minutes=1))
    task["status"] = "retrying"
    task["retry_count"] = task.get("retry_count", 0) + 1
    task["next_retry_at"] = next_retry_at
    task["error_code"] = error_code
    task["finished_at"] = None
    task["review_required"] = False
    task["blocked_reason"] = None
    _clear_task_lock(task)
    _sync_task_owner_runtime_status(task_kind, entity_id, "retrying", now, task)
    _append_task_event(
        task,
        "retry_scheduled",
        f"{task['task_type']} scheduled for retry.",
        task["status"],
        request_id,
        trace_id,
        actor_id,
        agent_role="scheduler",
        payload_json={"task_kind": task_kind, "entity_id": entity_id, "next_retry_at": next_retry_at},
        error_code=error_code,
        created_at=now,
    )
    return deepcopy(task)


@_persisting_mutation
def recover_task_for_manual_review(
    task_id: str,
    error_code: str,
    trace_id: str,
    request_id: str = "system-scheduler",
    actor_id: str = "scheduler",
) -> Optional[dict[str, Any]]:
    task, task_kind, entity_id = _find_task_record(task_id)
    if not task or not _can_require_manual_review(task):
        return deepcopy(task) if task else None
    now = utc_now()
    task["status"] = "requires_review"
    task["error_code"] = error_code
    task["finished_at"] = now
    task["review_required"] = True
    task["blocked_reason"] = None
    _clear_task_lock(task)
    task["dispatch_attempt"] = 0
    _sync_task_owner_runtime_status(task_kind, entity_id, "requires_review", now, task)
    _append_task_event(
        task,
        "review_required",
        f"{task['task_type']} requires manual review.",
        task["status"],
        request_id,
        trace_id,
        actor_id,
        agent_role="scheduler",
        payload_json={"task_kind": task_kind, "entity_id": entity_id, "reason": error_code},
        error_code=error_code,
        created_at=now,
    )
    return deepcopy(task)


@_persisting_mutation
def fail_task_recovery(
    task_id: str,
    error_code: str,
    trace_id: str,
    request_id: str = "system-scheduler",
    actor_id: str = "scheduler",
) -> Optional[dict[str, Any]]:
    task, task_kind, entity_id = _find_task_record(task_id)
    if not task:
        return None
    now = utc_now()
    task["status"] = "failed"
    task["error_code"] = error_code
    task["finished_at"] = now
    task["review_required"] = False
    task["blocked_reason"] = None
    _clear_task_lock(task)
    task["dispatch_attempt"] = 0
    _sync_task_owner_runtime_status(task_kind, entity_id, "failed", now, task)
    _append_task_event(
        task,
        "failed",
        f"{task['task_type']} marked failed by recovery.",
        task["status"],
        request_id,
        trace_id,
        actor_id,
        agent_role="scheduler",
        payload_json={"task_kind": task_kind, "entity_id": entity_id, "reason": error_code},
        error_code=error_code,
        created_at=now,
    )
    return deepcopy(task)


@_persisting_mutation
def recover_expired_runtime_tasks(
    now: Optional[str] = None,
    request_id: str = "system-scheduler",
    trace_id: str = "system-trace",
    actor_id: str = "scheduler",
) -> list[dict[str, Any]]:
    current = now or utc_now()
    current_dt = _as_utc_datetime(current)
    recovered = []
    for task in list_runtime_tasks("running"):
        lease_expires_at = task.get("lease_expires_at")
        if not lease_expires_at or _as_utc_datetime(lease_expires_at) > current_dt:
            continue
        if task.get("retry_count", 0) < task.get("max_retry_count", 3):
            recovered_task = schedule_task_retry(
                task["task_id"],
                task.get("error_code") or "lease_expired",
                trace_id=trace_id,
                request_id=request_id,
                actor_id=actor_id,
                retry_at=current,
            )
        else:
            terminal_status = _terminal_recovery_status(task)
            if terminal_status == "requires_review":
                recovered_task = recover_task_for_manual_review(
                    task["task_id"],
                    task.get("error_code") or "lease_expired",
                    trace_id=trace_id,
                    request_id=request_id,
                    actor_id=actor_id,
                )
            else:
                recovered_task = fail_task_recovery(
                    task["task_id"],
                    task.get("error_code") or "lease_expired",
                    trace_id=trace_id,
                    request_id=request_id,
                    actor_id=actor_id,
                )
        if recovered_task:
            recovered.append(recovered_task)
    return recovered


@_persisting_mutation
def list_due_retry_tasks(now: Optional[str] = None) -> list[dict[str, Any]]:
    current = _as_utc_datetime(now or utc_now())
    due = []
    for task in list_runtime_tasks("retrying"):
        next_retry_at = task.get("next_retry_at")
        if next_retry_at and _as_utc_datetime(next_retry_at) <= current:
            due.append(task)
    return sorted(due, key=lambda item: (item.get("next_retry_at") or "", item["task_id"]))


def _find_task_record(task_id: str) -> tuple[Optional[dict[str, Any]], Optional[str], Optional[str]]:
    for run_id, run in STORE.extraction_runs.items():
        task = run.get("task")
        if task and task["task_id"] == task_id:
            return task, "extraction_run", run_id
    for chapter_plan_id, task in STORE.chapter_plan_tasks.items():
        if task["task_id"] == task_id:
            return task, "chapter_plan", chapter_plan_id
    for chapter_plan_id, task in STORE.section_plan_tasks.items():
        if task["task_id"] == task_id:
            return task, "section_plan", chapter_plan_id
    for writing_run_id, task in STORE.writing_run_tasks.items():
        if task["task_id"] == task_id:
            return task, "writing_run", writing_run_id
    task = STORE.agent_tasks.get(task_id)
    if task:
        return task, "agent_task", task_id
    return None, None, None


@_persisting_mutation
def mark_task_dispatched(
    task_id: str,
    request_id: str = "system-dispatch",
    trace_id: str = "system-trace",
    actor_id: str = "scheduler",
    dispatched_at: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    task, task_kind, entity_id = _find_task_record(task_id)
    if not task:
        return None
    if not _can_dispatch_task(task):
        return deepcopy(task)
    now = dispatched_at or utc_now()
    lease_expires_at = _isoformat_utc(_as_utc_datetime(now) + timedelta(minutes=5))
    dispatch_attempt = _next_dispatch_attempt(task)
    dispatch_token = _dispatch_token(trace_id, actor_id, request_id, dispatch_attempt)
    task["status"] = "running"
    task["progress"] = max(task.get("progress", 0), 10)
    task["started_at"] = task.get("started_at") or now
    task["finished_at"] = None
    task["error_code"] = None
    task["lease_owner"] = actor_id
    task["lease_expires_at"] = lease_expires_at
    task["heartbeat_at"] = now
    task["next_retry_at"] = None
    task["review_required"] = False
    task["blocked_reason"] = None
    task["dispatch_attempt"] = dispatch_attempt
    _set_task_dispatch_token(task, dispatch_token)
    _sync_task_owner_runtime_status(task_kind, entity_id, "running", now, task)
    _append_task_event(
        task,
        "dispatched",
        f"{task['task_type']} dispatched to worker.",
        task["status"],
        request_id,
        trace_id,
        actor_id,
        agent_role="scheduler",
        payload_json={"task_kind": task_kind, "entity_id": entity_id, "lease_expires_at": lease_expires_at, "dispatch_token": dispatch_token},
        created_at=now,
    )
    return deepcopy(task)


@_persisting_mutation
def apply_task_execution_result(
    task_id: str,
    status: str,
    output_refs: list[str],
    metrics: dict[str, Any],
    trace_id: str,
    request_id: str = "system-worker",
    actor_id: str = "ai-worker",
    dispatch_token: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    task, task_kind, entity_id = _find_task_record(task_id)
    if not task or not task_kind or not entity_id:
        return None
    if not _completion_matches_active_dispatch(task, dispatch_token=dispatch_token):
        return deepcopy(task)
    now = utc_now()
    task["status"] = status
    task["output_refs"] = output_refs
    task["progress"] = 100 if status in {"succeeded", "requires_review"} else max(task.get("progress", 0), 85)
    task["finished_at"] = now if status in {"succeeded", "requires_review", "blocked", "failed"} else task.get("finished_at")
    task["latency_ms"] = metrics.get("latency_ms", 1000)
    task["error_code"] = metrics.get("error_code")
    task["heartbeat_at"] = now
    task["review_required"] = status == "requires_review"
    task["blocked_reason"] = metrics.get("blocked_reason") if status == "blocked" else None
    if status in {"succeeded", "requires_review", "failed", "blocked"}:
        _clear_task_lock(task)
    if status != "retrying":
        task["next_retry_at"] = None

    if task_kind == "extraction_run":
        run = STORE.extraction_runs.get(entity_id)
        graph_summary = metrics.get("graph_summary")
        knowledge_objects = metrics.get("knowledge_objects")
        if run:
            run["status"] = status
            run["current_stage"] = metrics.get("current_stage", run["current_stage"])
            run["chapter_count"] = metrics.get("chapter_count", run["chapter_count"])
            run["scene_count"] = metrics.get("scene_count", run["scene_count"])
            run["object_count"] = metrics.get("object_count", run["object_count"])
            run["evidence_count"] = metrics.get("evidence_count", run["evidence_count"])
            run["low_confidence_count"] = metrics.get("low_confidence_count", run["low_confidence_count"])
            run["knowledge_package_ref"] = metrics.get("knowledge_package_ref", run.get("knowledge_package_ref"))
            run["graph_package_ref"] = metrics.get("graph_package_ref", run.get("graph_package_ref"))
            run["extraction_report_ref"] = metrics.get("extraction_report_ref", run.get("extraction_report_ref"))
            run["quality_report_ref"] = metrics.get("quality_report_ref", run.get("quality_report_ref"))
            run["errors"] = deepcopy(metrics.get("errors", run["errors"]))
            run["started_at"] = task.get("started_at") or run.get("started_at")
            run["finished_at"] = task.get("finished_at")
            if knowledge_objects is not None:
                STORE.knowledge_by_run[entity_id] = []
                for item in knowledge_objects:
                    STORE.knowledge_objects[item["object_id"]] = deepcopy(item)
                    STORE.knowledge_by_run[entity_id].append(item["object_id"])
            evidences = metrics.get("evidences")
            if evidences is not None:
                STORE.evidence_by_run[entity_id] = []
                STORE.evidence_by_book[run["book_id"]] = []
                for item in evidences:
                    evidence_id = item["evidence_id"]
                    STORE.evidences[evidence_id] = deepcopy(item)
                    STORE.evidence_by_run[entity_id].append(evidence_id)
                    STORE.evidence_by_book[run["book_id"]].append(evidence_id)
            deep_analysis = metrics.get("deep_analysis", {})
            STORE.source_scenes_by_chapter = deepcopy(deep_analysis.get("scenes_by_chapter", STORE.source_scenes_by_chapter))
            STORE.events_by_scene = deepcopy(deep_analysis.get("events_by_scene", STORE.events_by_scene))
            for field_name in ("conflicts", "hooks", "rewards", "climaxes", "relationship_edges"):
                if field_name in deep_analysis:
                    setattr(STORE, field_name, deepcopy(deep_analysis[field_name]))
            if graph_summary is not None:
                STORE.graph_summaries[run["book_id"]] = deepcopy(graph_summary)
            node_details = metrics.get("graph_node_details")
            neighbors_map = metrics.get("graph_neighbors_by_node")
            if node_details is not None:
                book_id = run["book_id"]
                stale_nodes = [
                    node_id for node_id, node in STORE.graph_node_details.items()
                    if node.get("book_id") == book_id
                ]
                for node_id in stale_nodes:
                    STORE.graph_node_details.pop(node_id, None)
                    STORE.graph_neighbors_by_node.pop(node_id, None)
                for node_id, node in node_details.items():
                    STORE.graph_node_details[node_id] = deepcopy(node)
                if neighbors_map is not None:
                    for node_id, items in neighbors_map.items():
                        STORE.graph_neighbors_by_node[node_id] = deepcopy(items)
    elif task_kind == "chapter_plan":
        chapter_plan = STORE.chapter_plans.get(entity_id)
        if chapter_plan:
            chapter_plan["status"] = status
            chapter_plan["updated_at"] = now
            chapter_plan["payload"] = {
                **chapter_plan.get("payload", {}),
                "planning_stages": metrics.get("planning_stages", []),
                "current_stage": metrics.get("current_stage"),
                "summary": chapter_plan.get("payload", {}).get("summary") or f"第 {chapter_plan['chapter_index']} 章规划已生成。",
            }
    elif task_kind == "section_plan":
        chapter_plan = STORE.chapter_plans.get(entity_id)
        items = STORE.section_plans_by_chapter.get(entity_id, [])
        if chapter_plan:
            chapter_plan["status"] = "requires_review" if items else status
            chapter_plan["updated_at"] = now
        for item in items:
            item["updated_at"] = now
    elif task_kind == "writing_run":
        writing_run = STORE.writing_runs.get(entity_id)
        quality_report = STORE.quality_reports.get(writing_run["quality_report_id"]) if writing_run else None
        consistency_report = STORE.consistency_reports.get(writing_run.get("consistency_report_id", "")) if writing_run else None
        revision_summary = STORE.revision_summaries.get(writing_run.get("revision_summary_id", "")) if writing_run else None
        memory_package = STORE.memory_packages.get(writing_run["memory_package_id"]) if writing_run else None
        prompt_package = STORE.prompt_packages.get(writing_run["prompt_package_id"]) if writing_run else None
        quality_payload = metrics.get("quality_report")
        consistency_payload = metrics.get("consistency_report")
        revision_payload = metrics.get("revision_summary")
        memory_payload = metrics.get("memory_package")
        prompt_payload = metrics.get("prompt_package")
        section_run_updates = metrics.get("section_runs")
        provider_calls = metrics.get("provider_calls")
        feedback_records = metrics.get("feedback_records", [])
        if writing_run:
            writing_run["status"] = status
            writing_run["current_stage"] = metrics.get("current_stage", writing_run["current_stage"])
            writing_run["assembled_chapter"] = metrics.get("assembled_chapter", writing_run["assembled_chapter"])
            if "model_cost" in metrics:
                writing_run["model_cost"] = deepcopy(metrics["model_cost"])
            writing_run["updated_at"] = now
        if memory_package and memory_payload:
            memory_package["summary"] = memory_payload.get("summary", memory_package["summary"])
            memory_package["source_refs"] = deepcopy(memory_payload.get("source_refs", memory_package.get("source_refs", [])))
            memory_package["updated_at"] = now
        if prompt_package and prompt_payload:
            prompt_package["summary"] = prompt_payload.get("summary", prompt_package["summary"])
            prompt_package["template_refs"] = deepcopy(prompt_payload.get("template_refs", prompt_package.get("template_refs", [])))
            prompt_package["updated_at"] = now
        if provider_calls is not None and writing_run:
            STORE.provider_calls_by_writing[entity_id] = deepcopy(provider_calls)
        if quality_report:
            if quality_payload:
                quality_report["status"] = quality_payload.get("status", quality_report["status"])
                quality_report["human_review_required"] = quality_payload.get("human_review_required", quality_report["human_review_required"])
                quality_report["blocking_issues"] = deepcopy(quality_payload.get("blocking_issues", quality_report["blocking_issues"]))
                quality_report["ai_flavor_score"] = quality_payload.get("ai_flavor_score", quality_report["ai_flavor_score"])
                quality_report["mobile_readability_score"] = quality_payload.get("mobile_readability_score", quality_report["mobile_readability_score"])
                quality_report["originality_safety_score"] = quality_payload.get("originality_safety_score", quality_report["originality_safety_score"])
            else:
                quality_report["status"] = "requires_review" if status == "requires_review" else status
                quality_report["human_review_required"] = status == "requires_review"
                quality_report["blocking_issues"] = metrics.get("blocking_issues", quality_report["blocking_issues"])
                quality_report["ai_flavor_score"] = metrics.get("ai_flavor_score", quality_report["ai_flavor_score"])
                quality_report["mobile_readability_score"] = metrics.get("mobile_readability_score", quality_report["mobile_readability_score"])
                quality_report["originality_safety_score"] = metrics.get("originality_safety_score", quality_report["originality_safety_score"])
            quality_report["updated_at"] = now
        if consistency_report:
            if consistency_payload:
                issues = deepcopy(consistency_payload.get("issues", consistency_report.get("issues", [])))
                consistency_report["status"] = consistency_payload.get("status", consistency_report["status"])
                consistency_report["issue_count"] = consistency_payload.get("issue_count", len(issues))
                consistency_report["blocking_issue_count"] = consistency_payload.get(
                    "blocking_issue_count",
                    len([item for item in issues if item.get("resolution_status") == "open"]),
                )
                consistency_report["checked_domains"] = deepcopy(
                    consistency_payload.get("checked_domains", consistency_report.get("checked_domains", []))
                )
                consistency_report["issues"] = issues
                consistency_report["input_refs"] = deepcopy(consistency_payload.get("input_refs", consistency_report.get("input_refs", [])))
                consistency_report["output_refs"] = deepcopy(consistency_payload.get("output_refs", consistency_report.get("output_refs", [])))
            else:
                consistency_report["status"] = "blocked" if metrics.get("blocking_issue_count", 0) else "passed"
                consistency_report["issue_count"] = metrics.get("issue_count", consistency_report["issue_count"])
                consistency_report["blocking_issue_count"] = metrics.get("blocking_issue_count", consistency_report["blocking_issue_count"])
            consistency_report["updated_at"] = now
        if revision_summary:
            if revision_payload:
                revision_summary["status"] = revision_payload.get("status", revision_summary["status"])
                revision_summary["revision_round"] = revision_payload.get("revision_round", revision_summary["revision_round"])
                revision_summary["max_revision_rounds"] = revision_payload.get("max_revision_rounds", revision_summary["max_revision_rounds"])
                revision_summary["source_issue_ids"] = deepcopy(revision_payload.get("source_issue_ids", revision_summary.get("source_issue_ids", [])))
                revision_summary["change_summary"] = revision_payload.get("change_summary", revision_summary["change_summary"])
                revision_summary["revision_diff_ref"] = revision_payload.get("revision_diff_ref", revision_summary.get("revision_diff_ref"))
                revision_summary["reviewer_note_ref"] = revision_payload.get("reviewer_note_ref", revision_summary.get("reviewer_note_ref"))
                revision_summary["input_refs"] = deepcopy(revision_payload.get("input_refs", revision_summary.get("input_refs", [])))
                revision_summary["output_refs"] = deepcopy(revision_payload.get("output_refs", revision_summary.get("output_refs", [])))
            else:
                revision_summary["status"] = "requested" if metrics.get("blocking_issue_count", 0) else "accepted"
                revision_summary["change_summary"] = metrics.get("revision_summary", revision_summary["change_summary"])
            revision_summary["updated_at"] = now
        current_section_runs = STORE.section_runs_by_writing.get(entity_id, [])
        if section_run_updates:
            by_id = {item["section_run_id"]: item for item in current_section_runs}
            for item in section_run_updates:
                section_run = by_id.get(item["section_run_id"])
                if not section_run:
                    continue
                for field in ("status", "writer_output", "critic_issues", "humanized_text", "beat_status", "draft_object_ref", "critic_report_ref", "humanized_object_ref", "model_profile_id"):
                    if field in item:
                        section_run[field] = deepcopy(item[field])
                section_run["updated_at"] = now
        else:
            for section_run in current_section_runs:
                section_run["status"] = "humanized"
                section_run["writer_output"] = metrics.get("assembled_chapter", section_run["writer_output"] or "已生成段落。")
                section_run["humanized_text"] = metrics.get("assembled_chapter", section_run["humanized_text"] or "已润色段落。")
                section_run["updated_at"] = now
        for feedback_record in feedback_records:
            STORE.feedback_records[feedback_record["feedback_record_id"]] = deepcopy(feedback_record)
        if writing_run:
            _sync_writing_run_phase_one_state(writing_run)

    _sync_task_owner_runtime_status(task_kind, entity_id, status, now, task)
    event_type = "review_required" if status == "requires_review" else status
    _append_task_event(
        task,
        event_type,
        f"{task['task_type']} finished with status {status}.",
        task["status"],
        request_id,
        trace_id,
        actor_id,
        agent_role="ai-worker",
        payload_json={"metrics": metrics, "output_refs": output_refs, "task_kind": task_kind, "entity_id": entity_id},
        error_code=metrics.get("error_code"),
        created_at=now,
    )
    return deepcopy(task)


def _build_chapter_snapshot(
    writing_run: dict[str, Any],
    section_runs: list[dict[str, Any]],
    chapter_plan: Optional[dict[str, Any]],
    accepted_chapter_ref: str,
    created_at: str,
) -> dict[str, Any]:
    chapter_snapshot_id = writing_run.get("chapter_snapshot_id") or f"chapter-snapshot:{writing_run['writing_run_id']}"
    chapter_payload = chapter_plan.get("payload", {}) if chapter_plan else {}
    return {
        "schema_version": 1,
        "chapter_snapshot_id": chapter_snapshot_id,
        "writing_run_id": writing_run["writing_run_id"],
        "project_id": writing_run["project_id"],
        "chapter_plan_id": writing_run["chapter_plan_id"],
        "accepted_chapter_ref": accepted_chapter_ref,
        "chapter_title": chapter_payload.get("title", "已接受章节"),
        "chapter_text": writing_run["assembled_chapter"],
        "source_section_refs": [
            f"object://section-runs/{section_run['section_run_id']}"
            for section_run in section_runs
        ],
        "created_at": created_at,
    }


def _build_manuscript_state(writing_run: dict[str, Any], chapter_plan: Optional[dict[str, Any]], accepted_chapter_ref: str, updated_at: str) -> dict[str, Any]:
    manuscript_state_id = writing_run.get("manuscript_state_id") or f"manuscript-state:{writing_run['project_id']}"
    chapter_payload = chapter_plan.get("payload", {}) if chapter_plan else {}
    chapter_title = chapter_payload.get("title", "当前章节")
    chapter_summary = chapter_payload.get("summary") or ""
    assembled = writing_run.get("assembled_chapter") or ""
    project = STORE.novel_projects.get(writing_run["project_id"])
    story_bible = STORE.story_bibles.get(project["story_bible_id"]) if project else None
    protagonist = (story_bible or {}).get("payload", {}).get("protagonist", "主角")
    core_conflict = (story_bible or {}).get("payload", {}).get("core_conflict", "")
    # 前情摘要包：从真实组章文本分句派生
    sentences = [s.strip() for s in assembled.replace("。", "。\n").split("\n") if s.strip()]
    prior_pack = [{"summary_index": i + 1, "summary": s} for i, s in enumerate(sentences[:3])] or (
        [{"summary_index": 1, "summary": chapter_summary or f"{chapter_title}已进入 manuscript。"}]
    )
    state_summary = (
        f"第 {chapter_plan['chapter_index']} 章《{chapter_title}》已进入 manuscript：{chapter_summary or assembled[:60]}"
        if chapter_plan else f"《{chapter_title}》已进入 manuscript。"
    )
    return {
        "schema_version": 1,
        "manuscript_state_id": manuscript_state_id,
        "project_id": writing_run["project_id"],
        "writing_run_id": writing_run["writing_run_id"],
        "current_story_state": {
            "summary": state_summary,
            "accepted_chapter_ref": accepted_chapter_ref,
            "quality_gate_status": "passed",
        },
        "character_dynamic_state": [
            {"character_name": protagonist, "state_summary": f"在本章推进「{core_conflict or chapter_summary}」，动机与处境更新。"}
        ],
        "relationship_state": [
            {"subject": protagonist, "object": core_conflict or "核心冲突", "state_summary": "人物与核心冲突的关系随本章推进。"}
        ],
        "hook_state": [
            {"hook_key": "core_conflict", "status": "active", "summary": core_conflict or chapter_summary or "核心挂钩持续推进。"}
        ],
        "prior_summary_pack": prior_pack,
        "updated_at": updated_at,
    }


def _acceptance_ready(writing_run: dict[str, Any], quality_report: Optional[dict[str, Any]], section_runs: list[dict[str, Any]]) -> bool:
    if not quality_report or not section_runs:
        return False
    consistency_report = STORE.consistency_reports.get(writing_run.get("consistency_report_id", ""))
    revision_summary = STORE.revision_summaries.get(writing_run.get("revision_summary_id", ""))
    has_feedback = any(item["target_id"] in {writing_run["writing_run_id"], writing_run["quality_report_id"]} for item in STORE.feedback_records.values())
    has_section_outputs = all(section_run["writer_output"] and section_run["humanized_text"] for section_run in section_runs)
    consistency_clear = not consistency_report or consistency_report["blocking_issue_count"] == 0
    quality_clear = quality_report["status"] in {"passed", "requires_review"} and not quality_report["blocking_issues"]
    review_clear = not quality_report["human_review_required"]
    revision_clear = not revision_summary or revision_summary["status"] in {"accepted", "revised"}
    return has_feedback and has_section_outputs and consistency_clear and quality_clear and review_clear and revision_clear


@_persisting_mutation
def accept_chapter(
    writing_run_id: str,
    trace_id: str,
    request_id: str = "system-accept",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    writing_run = STORE.writing_runs.get(writing_run_id)
    if not writing_run:
        return None
    _sync_writing_run_phase_one_state(writing_run)

    task = STORE.writing_run_tasks.get(writing_run_id)
    quality_report = STORE.quality_reports.get(writing_run["quality_report_id"])
    section_runs = STORE.section_runs_by_writing.get(writing_run_id, [])
    if not _acceptance_ready(writing_run, quality_report, section_runs):
        if task:
            task["status"] = "blocked"
            task["error_code"] = "acceptance_dependencies_incomplete"
            _append_task_event(
                task,
                "blocked",
                "Writing run acceptance dependencies incomplete.",
                task["status"],
                request_id,
                trace_id,
                context["actor_id"],
                error_code="acceptance_dependencies_incomplete",
                payload_json={"writing_run_id": writing_run_id},
            )
        return False

    chapter_plan = STORE.chapter_plans.get(writing_run["chapter_plan_id"])
    now = utc_now()

    for section_run in section_runs:
        section_run["status"] = "beat_approved"
        section_run["beat_status"] = [
            {**beat, "status": "beat_approved"}
            for beat in section_run["beat_status"]
        ]
        section_run["critic_issues"] = []
        section_run["updated_at"] = now

    accepted_chapter_ref = writing_run["accepted_chapter_ref"] or f"object://manuscripts/{writing_run_id}/chapters/1"
    chapter_snapshot = _build_chapter_snapshot(writing_run, section_runs, chapter_plan, accepted_chapter_ref, now)
    manuscript_state = _build_manuscript_state(writing_run, chapter_plan, accepted_chapter_ref, now)
    STORE.chapter_snapshots[chapter_snapshot["chapter_snapshot_id"]] = chapter_snapshot
    STORE.manuscript_states_by_project[writing_run["project_id"]] = manuscript_state

    writing_run["status"] = "succeeded"
    writing_run["current_stage"] = "quality_gate"
    writing_run["accepted_into_manuscript_at"] = writing_run["accepted_into_manuscript_at"] or now
    writing_run["accepted_chapter_ref"] = accepted_chapter_ref
    writing_run["chapter_snapshot_id"] = chapter_snapshot["chapter_snapshot_id"]
    writing_run["manuscript_state_id"] = manuscript_state["manuscript_state_id"]
    writing_run["updated_at"] = now

    if task:
        task["status"] = "succeeded"
        task["progress"] = 100
        task["finished_at"] = task["finished_at"] or now
        task["latency_ms"] = 1000
        task["error_code"] = None

    if quality_report:
        quality_report["status"] = "passed"
        quality_report["human_review_required"] = False
        quality_report["blocking_issues"] = []
        quality_report["updated_at"] = now

    consistency_report = STORE.consistency_reports.get(writing_run.get("consistency_report_id", ""))
    if consistency_report:
        consistency_report["status"] = "passed"
        consistency_report["blocking_issue_count"] = 0
        for issue in consistency_report["issues"]:
            if issue["resolution_status"] == "open":
                issue["resolution_status"] = "resolved"
                issue["note"] = issue.get("note") or "Accepted into manuscript after review."
        consistency_report["updated_at"] = now

    revision_summary = STORE.revision_summaries.get(writing_run.get("revision_summary_id", ""))
    if revision_summary:
        revision_summary["status"] = "accepted"
        revision_summary["updated_at"] = now

    _sync_writing_run_phase_one_state(writing_run)

    run_records = list_feedback_records("writing_run", writing_run_id)
    run_feedback_types = {item["feedback_type"] for item in run_records}
    if "acceptance" not in run_feedback_types:
        acceptance_id = str(ulid.new())
        STORE.feedback_records[acceptance_id] = _build_feedback_record(
            feedback_record_id=acceptance_id,
            workspace_id=writing_run["workspace_id"],
            target_type="writing_run",
            target_id=writing_run_id,
            feedback_type="acceptance",
            score=1.0,
            source="human_review",
            request_id=request_id,
            trace_id=trace_id,
            actor_id=context["actor_id"],
            comment_ref=f"object://feedback-comments/{acceptance_id}",
            payload={
                "accepted_chapter_ref": writing_run["accepted_chapter_ref"],
                "chapter_snapshot_id": chapter_snapshot["chapter_snapshot_id"],
                "manuscript_state_id": manuscript_state["manuscript_state_id"],
                "summary": "人工复核已接受本章进入 manuscript。",
            },
            promotion_status="promoted",
            input_refs=[f"object://writing-runs/{writing_run_id}"],
            output_refs=[accepted_chapter_ref],
            created_at=now,
        )
    if "cost" not in run_feedback_types:
        cost_id = str(ulid.new())
        STORE.feedback_records[cost_id] = _build_feedback_record(
            feedback_record_id=cost_id,
            workspace_id=writing_run["workspace_id"],
            target_type="writing_run",
            target_id=writing_run_id,
            feedback_type="cost",
            score=0.78,
            source="system",
            request_id=request_id,
            trace_id=trace_id,
            actor_id=context["actor_id"],
            payload={
                "estimated_total_cost": writing_run["model_cost"]["estimated_total_cost"],
                "retry_count": writing_run["model_cost"]["retry_count"],
            },
            input_refs=[f"object://writing-runs/{writing_run_id}"],
            output_refs=[],
            created_at=now,
        )

    if task:
        _append_task_event(
            task,
            "succeeded",
            "Chapter accepted into manuscript.",
            task["status"],
            request_id,
            trace_id,
            context["actor_id"],
            payload_json={
                "accepted_chapter_ref": writing_run["accepted_chapter_ref"],
                "chapter_snapshot_id": chapter_snapshot["chapter_snapshot_id"],
                "manuscript_state_id": manuscript_state["manuscript_state_id"],
            },
            created_at=now,
        )

    _append_audit_event(
        action="writing.accept_chapter",
        target_type="writing_run",
        target_id=writing_run_id,
        target_ref=f"object://writing-runs/{writing_run_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        actor_role=context["actor_role"],
        workspace_id=context["workspace_id"],
        after_ref=accepted_chapter_ref,
        payload={
            "chapter_snapshot_id": chapter_snapshot["chapter_snapshot_id"],
            "manuscript_state_id": manuscript_state["manuscript_state_id"],
        },
        created_at=now,
    )

    return get_writing_run(writing_run_id)


def get_writing_run(writing_run_id: str) -> Optional[dict[str, Any]]:
    writing_run = STORE.writing_runs.get(writing_run_id)
    if not writing_run:
        return None
    _sync_writing_run_phase_one_state(writing_run)
    task = STORE.writing_run_tasks.get(writing_run_id)
    memory_package = STORE.memory_packages.get(writing_run["memory_package_id"])
    prompt_package = STORE.prompt_packages.get(writing_run["prompt_package_id"])
    quality_report = STORE.quality_reports.get(writing_run["quality_report_id"])
    consistency_report = STORE.consistency_reports.get(writing_run.get("consistency_report_id", "")) if writing_run.get("consistency_report_id") else None
    revision_summary = STORE.revision_summaries.get(writing_run.get("revision_summary_id", "")) if writing_run.get("revision_summary_id") else None
    chapter_snapshot = STORE.chapter_snapshots.get(writing_run.get("chapter_snapshot_id", "")) if writing_run.get("chapter_snapshot_id") else None
    manuscript_state = STORE.manuscript_states_by_project.get(writing_run["project_id"])
    events = STORE.task_events_by_task.get(task["task_id"], []) if task else []
    return {
        "writing_run": {
            **writing_run,
            "provider_calls": deepcopy(STORE.provider_calls_by_writing.get(writing_run_id, [])),
            "chapter_snapshot": chapter_snapshot,
            "manuscript_state": manuscript_state,
            "consistency_report": deepcopy(consistency_report) if consistency_report else None,
            "revision_summary": deepcopy(revision_summary) if revision_summary else None,
        },
        "task": task,
        "events": events,
        "memory_package": memory_package,
        "prompt_package": prompt_package,
        "section_runs": STORE.section_runs_by_writing.get(writing_run_id, []),
        "quality_report": quality_report,
        "consistency_report": deepcopy(consistency_report) if consistency_report else None,
        "revision_summary": deepcopy(revision_summary) if revision_summary else None,
        "provider_calls": deepcopy(STORE.provider_calls_by_writing.get(writing_run_id, [])),
        "feedback_records": [
            item
            for item in list_feedback_records()
            if item["target_id"] in {writing_run_id, writing_run["quality_report_id"]}
        ],
        "pattern_selection": list_patterns(status="approved"),
        "rhythm_profile_selection": list_rhythm_profiles(status="approved", target_id=writing_run["chapter_plan_id"]),
        "asset_selection": list_assets(status="approved"),
        "chapter_snapshot": chapter_snapshot,
        "manuscript_state": manuscript_state,
    }


def get_quality_report(quality_report_id: str) -> Optional[dict[str, Any]]:
    return STORE.quality_reports.get(quality_report_id)


def get_consistency_report(consistency_report_id: str) -> Optional[dict[str, Any]]:
    report = STORE.consistency_reports.get(consistency_report_id)
    return deepcopy(report) if report else None


def get_revision_summary(revision_summary_id: str) -> Optional[dict[str, Any]]:
    summary = STORE.revision_summaries.get(revision_summary_id)
    return deepcopy(summary) if summary else None


def list_rules() -> list[dict[str, Any]]:
    return _sorted_store_items(list(STORE.rules.values()), "rule_id")


def list_patterns(status: Optional[str] = None, pattern_type: Optional[str] = None) -> list[dict[str, Any]]:
    items = list(STORE.patterns.values())
    if status:
        items = [item for item in items if item["status"] == status]
    if pattern_type:
        items = [item for item in items if item["pattern_type"] == pattern_type]
    return _sorted_store_items(items, "pattern_id")


def get_pattern(pattern_id: str) -> Optional[dict[str, Any]]:
    pattern = STORE.patterns.get(pattern_id)
    return deepcopy(pattern) if pattern else None


@_persisting_mutation
def create_pattern(
    payload: dict[str, Any],
    request_id: str = "system-pattern",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    context = _actor_context(workspace_id or payload.get("workspace_id"), actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})
    pattern_id = payload.get("pattern_id") or str(ulid.new())
    now = utc_now()
    pattern = {
        "schema_version": 1,
        "pattern_id": pattern_id,
        "workspace_id": context["workspace_id"],
        "trace_id": trace_id,
        "canonical_name": payload["canonical_name"],
        "pattern_type": payload["pattern_type"],
        "status": payload.get("status", "draft"),
        "intent": payload["intent"],
        "preconditions": payload["preconditions"],
        "steps": payload["steps"],
        "slots": payload["slots"],
        "expected_reader_effect": payload["expected_reader_effect"],
        "compatible_rhythm_profile_id": payload.get("compatible_rhythm_profile_id"),
        "evidence_refs": payload["evidence_refs"],
        "created_at": now,
        "updated_at": now,
    }
    STORE.patterns[pattern_id] = pattern
    _append_audit_event(
        action="feedback.ranking_suggestion_approved",
        target_type="pattern",
        target_id=pattern_id,
        target_ref=f"object://patterns/{pattern_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        actor_role=context["actor_role"],
        workspace_id=context["workspace_id"],
        payload={"status": pattern["status"]},
        created_at=now,
    )
    return deepcopy(pattern)


def list_rhythm_profiles(status: Optional[str] = None, target_id: Optional[str] = None) -> list[dict[str, Any]]:
    items = list(STORE.rhythm_profiles.values())
    if status:
        items = [item for item in items if item["status"] == status]
    if target_id:
        items = [item for item in items if item["target_id"] == target_id]
    return _sorted_store_items(items, "rhythm_profile_id")


def get_rhythm_profile(rhythm_profile_id: str) -> Optional[dict[str, Any]]:
    profile = STORE.rhythm_profiles.get(rhythm_profile_id)
    return deepcopy(profile) if profile else None


@_persisting_mutation
def create_rhythm_profile(
    payload: dict[str, Any],
    request_id: str = "system-rhythm",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    context = _actor_context(workspace_id or payload.get("workspace_id"), actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})
    rhythm_profile_id = payload.get("rhythm_profile_id") or str(ulid.new())
    now = utc_now()
    profile = {
        "schema_version": 1,
        "rhythm_profile_id": rhythm_profile_id,
        "workspace_id": context["workspace_id"],
        "trace_id": trace_id,
        "target_id": payload["target_id"],
        "status": payload.get("status", "draft"),
        "label": payload["label"],
        "climax_index": payload["climax_index"],
        "conflict_index": payload["conflict_index"],
        "dialogue_ratio": payload["dialogue_ratio"],
        "description_ratio": payload["description_ratio"],
        "battle_ratio": payload["battle_ratio"],
        "information_density": payload["information_density"],
        "suspense_index": payload["suspense_index"],
        "reward_count": payload["reward_count"],
        "emotion_curve": payload["emotion_curve"],
        "created_at": now,
        "updated_at": now,
    }
    STORE.rhythm_profiles[rhythm_profile_id] = profile
    return deepcopy(profile)


def list_assets(status: Optional[str] = None, asset_type: Optional[str] = None) -> list[dict[str, Any]]:
    items = list(STORE.assets.values())
    if status:
        items = [item for item in items if item["status"] == status]
    if asset_type:
        items = [item for item in items if item["asset_type"] == asset_type]
    return _sorted_store_items(items, "asset_id")


def get_asset(asset_id: str) -> Optional[dict[str, Any]]:
    asset = STORE.assets.get(asset_id)
    return deepcopy(asset) if asset else None


@_persisting_mutation
def create_asset(
    payload: dict[str, Any],
    request_id: str = "system-asset",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    context = _actor_context(workspace_id or payload.get("workspace_id"), actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})
    asset_id = payload.get("asset_id") or str(ulid.new())
    now = utc_now()
    asset = {
        "schema_version": 1,
        "asset_id": asset_id,
        "workspace_id": context["workspace_id"],
        "trace_id": trace_id,
        "asset_type": payload["asset_type"],
        "canonical_name": payload["canonical_name"],
        "status": payload.get("status", "draft"),
        "content_summary": payload["content_summary"],
        "style_tags": payload["style_tags"],
        "genre_scope": payload["genre_scope"],
        "usage_context": payload["usage_context"],
        "constraints": payload["constraints"],
        "expression_type_refs": payload["expression_type_refs"],
        "source_refs": payload["source_refs"],
        "evidence_refs": payload["evidence_refs"],
        "quality_score": payload["quality_score"],
        "created_at": now,
        "updated_at": now,
    }
    STORE.assets[asset_id] = asset
    return deepcopy(asset)


def get_rule(rule_id: str) -> Optional[dict[str, Any]]:
    return STORE.rules.get(rule_id)


@_persisting_mutation
def apply_writing_review_action(
    writing_run_id: str,
    payload: dict[str, Any],
    request_id: str = "system-writing-review",
    trace_id: str = "system-trace",
    actor_id: str = USER_ID,
    actor_role: str = "owner",
    workspace_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    context = _actor_context(workspace_id, actor_id, actor_role)
    _require_role(context["actor_role"], {"owner", "editor"})

    writing_run = STORE.writing_runs.get(writing_run_id)
    if not writing_run:
        return None
    task = STORE.writing_run_tasks.get(writing_run_id)
    quality_report = STORE.quality_reports.get(writing_run["quality_report_id"])
    consistency_report = STORE.consistency_reports.get(writing_run.get("consistency_report_id", ""))
    revision_summary = STORE.revision_summaries.get(writing_run.get("revision_summary_id", ""))
    if not consistency_report or not revision_summary:
        return None

    action = payload["action"]
    issue = _find_consistency_issue(consistency_report, payload.get("issue_id"))
    now = utc_now()

    if action == "approve_draft":
        writing_run["status"] = "requires_review"
        writing_run["current_stage"] = "quality_gate"
        quality_report["status"] = "requires_review"
        quality_report["human_review_required"] = False
        quality_report["blocking_issues"] = []
        consistency_report["status"] = "passed"
        consistency_report["blocking_issue_count"] = 0
        revision_summary["status"] = "accepted"
    elif action == "request_revision":
        writing_run["status"] = "blocked"
        writing_run["current_stage"] = "revision_loop"
        writing_run["revision_round"] = min(writing_run["revision_round"] + 1, writing_run["max_revision_rounds"])
        consistency_report["status"] = "blocked"
        consistency_report["blocking_issue_count"] = sum(1 for item in consistency_report["issues"] if item["resolution_status"] == "open")
        revision_summary["status"] = "requested" if writing_run["revision_round"] < writing_run["max_revision_rounds"] else "blocked"
        revision_summary["revision_round"] = writing_run["revision_round"]
        revision_summary["change_summary"] = payload.get("note") or revision_summary["change_summary"]
        revision_summary["reviewer_note_ref"] = payload.get("output_ref") or revision_summary.get("reviewer_note_ref")
        quality_report["status"] = "blocked"
        quality_report["human_review_required"] = True
    elif action == "reject_draft":
        writing_run["status"] = "blocked"
        writing_run["current_stage"] = "human_review"
        consistency_report["status"] = "blocked"
        revision_summary["status"] = "blocked"
        quality_report["status"] = "blocked"
        quality_report["human_review_required"] = True
    elif action == "edit_draft":
        writing_run["status"] = "requires_review"
        writing_run["current_stage"] = "human_review"
        revision_summary["status"] = "requires_review"
        revision_summary["reviewer_note_ref"] = payload.get("output_ref") or revision_summary.get("reviewer_note_ref")
        quality_report["status"] = "requires_review"
        quality_report["human_review_required"] = True
    elif action == "mark_issue_resolved":
        if not issue:
            return False
        issue["resolution_status"] = "resolved"
        issue["note"] = payload.get("note")
        consistency_report["blocking_issue_count"] = sum(1 for item in consistency_report["issues"] if item["resolution_status"] == "open")
        consistency_report["status"] = "passed" if consistency_report["blocking_issue_count"] == 0 else "blocked"
        quality_report["blocking_issues"] = [
            item for item in quality_report["blocking_issues"] if not _quality_issue_matches_consistency_issue(issue, item)
        ]
        if consistency_report["blocking_issue_count"] == 0:
            quality_report["blocking_issues"] = []
            quality_report["status"] = "requires_review"
        revision_summary["status"] = "revised" if consistency_report["blocking_issue_count"] == 0 else revision_summary["status"]
    elif action == "create_rule_update_request":
        revision_summary["status"] = "requires_review"
        revision_summary["reviewer_note_ref"] = payload.get("output_ref") or revision_summary.get("reviewer_note_ref")
    else:
        return False

    consistency_report["issue_count"] = len(consistency_report["issues"])
    consistency_report["updated_at"] = now
    revision_summary["updated_at"] = now
    quality_report["updated_at"] = now
    writing_run["updated_at"] = now
    _sync_writing_run_phase_one_state(writing_run)

    if task:
        task["status"] = writing_run["status"]
        task["progress"] = 100 if action in {"approve_draft", "mark_issue_resolved"} else 85
        task["error_code"] = None
        _append_task_event(
            task,
            action,
            f"Writing review action applied: {action}.",
            task["status"],
            request_id,
            trace_id,
            context["actor_id"],
            payload_json={
                "writing_run_id": writing_run_id,
                "issue_id": payload.get("issue_id"),
                "output_ref": payload.get("output_ref"),
            },
            created_at=now,
        )

    _append_audit_event(
        action=f"writing.{action}",
        target_type="writing_run",
        target_id=writing_run_id,
        target_ref=f"object://writing-runs/{writing_run_id}",
        request_id=request_id,
        trace_id=trace_id,
        actor_id=context["actor_id"],
        actor_role=context["actor_role"],
        workspace_id=context["workspace_id"],
        after_ref=payload.get("output_ref"),
        reason=payload.get("note"),
        payload={
            "issue_id": payload.get("issue_id"),
            "current_stage": writing_run["current_stage"],
            "revision_round": writing_run["revision_round"],
        },
        created_at=now,
    )
    return get_writing_run(writing_run_id)

