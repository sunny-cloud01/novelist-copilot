from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

try:
    import psycopg
except ImportError:  # pragma: no cover - exercised by environments without psycopg
    psycopg = None

try:
    from app.core.persistence import _ensure_tables, _postgres_url
except ModuleNotFoundError:
    spec = importlib.util.spec_from_file_location("phase_two_persistence", Path(__file__).with_name("persistence.py"))
    if spec is None or spec.loader is None:
        raise
    persistence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(persistence)
    _ensure_tables = persistence._ensure_tables
    _postgres_url = persistence._postgres_url

FILE_PERSISTENCE_FALLBACK_ENV = "NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK"


def _fallback_allowed() -> bool:
    return os.getenv(FILE_PERSISTENCE_FALLBACK_ENV, "").strip().lower() in {"1", "true", "yes", "on"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _snapshot_hash(snapshot: dict[str, Any]) -> str:
    return f"sha256:{hashlib.sha256(_json(snapshot).encode('utf-8')).hexdigest()}"


def _build_migration_event(snapshot: dict[str, Any]) -> dict[str, Any]:
    row_counts = {
        "users": len(snapshot.get("users") or {}),
        "workspaces": len(snapshot.get("workspaces") or {}),
        "workspace_members": len(snapshot.get("workspace_members") or {}),
        "books": len(snapshot.get("books") or {}),
        "source_contents": len(snapshot.get("source_contents") or {}),
        "source_chapters": sum(len(chapters) for chapters in (snapshot.get("chapters_by_book") or {}).values()),
        "source_scenes": sum(len(scenes) for scenes in (snapshot.get("source_scenes_by_chapter") or {}).values()),
        "story_events": sum(len(events) for events in (snapshot.get("events_by_scene") or {}).values()),
        "conflicts": len(snapshot.get("conflicts") or {}),
        "hooks": len(snapshot.get("hooks") or {}),
        "rewards": len(snapshot.get("rewards") or {}),
        "climaxes": len(snapshot.get("climaxes") or {}),
        "relationship_edges": len(snapshot.get("relationship_edges") or {}),
        "extraction_runs": len(snapshot.get("extraction_runs") or {}),
        "evidences": len(snapshot.get("evidences") or {}),
        "knowledge_objects": len(snapshot.get("knowledge_objects") or {}),
        "graph_summaries": len(snapshot.get("graph_summaries") or {}),
        "graph_nodes": len(snapshot.get("graph_node_details") or {}),
        "graph_edges": sum(len(edges) for edges in (snapshot.get("graph_neighbors_by_node") or {}).values()),
        "novel_projects": len(snapshot.get("novel_projects") or {}),
        "story_bibles": len(snapshot.get("story_bibles") or {}),
        "chapter_plans": len(snapshot.get("chapter_plans") or {}),
        "section_plans": sum(len(sections) for sections in (snapshot.get("section_plans_by_chapter") or {}).values()),
        "writing_runs": len(snapshot.get("writing_runs") or {}),
        "section_runs": sum(len(sections) for sections in (snapshot.get("section_runs_by_writing") or {}).values()),
        "memory_packages": len(snapshot.get("memory_packages") or {}),
        "prompt_packages": len(snapshot.get("prompt_packages") or {}),
        "provider_calls": sum(len(calls) for calls in (snapshot.get("provider_calls_by_writing") or {}).values()),
        "quality_reports": len(snapshot.get("quality_reports") or {}),
        "consistency_reports": len(snapshot.get("consistency_reports") or {}),
        "revision_summaries": len(snapshot.get("revision_summaries") or {}),
        "chapter_snapshots": len(snapshot.get("chapter_snapshots") or {}),
        "manuscript_states": len(snapshot.get("manuscript_states_by_project") or {}),
        "feedback_records": len(snapshot.get("feedback_records") or {}),
        "ranking_snapshots": len(snapshot.get("ranking_snapshots") or {}),
        "rules": len(snapshot.get("rules") or {}),
        "patterns": len(snapshot.get("patterns") or {}),
        "rhythm_profiles": len(snapshot.get("rhythm_profiles") or {}),
        "assets": len(snapshot.get("assets") or {}),
        "audit_events": len(snapshot.get("audit_events") or []),
    }
    return {
        "migration_id": f"business-backfill:{_utc_now()}",
        "snapshot_hash": _snapshot_hash(snapshot),
        "affected_tables": [
            "identity.users",
            "identity.workspaces",
            "identity.workspace_members",
            "core.source_books",
            "core.source_contents",
            "core.source_chapters",
            "core.source_scenes",
            "core.story_events",
            "core.story_conflicts",
            "core.story_hooks",
            "core.story_rewards",
            "core.story_climaxes",
            "core.relationship_edges",
            "core.extraction_runs",
            "core.evidence_records",
            "core.knowledge_objects",
            "core.graph_snapshots",
            "core.graph_nodes",
            "core.graph_edges",
            "core.novel_projects",
            "core.story_bibles",
            "core.chapter_plans",
            "core.section_plans",
            "ai.writing_runs",
            "ai.section_runs",
            "ai.memory_packages",
            "ai.prompt_packages",
            "ai.provider_calls",
            "core.quality_reports",
            "core.consistency_reports",
            "core.revision_summaries",
            "core.chapter_snapshots",
            "core.manuscript_states",
            "core.feedback_records",
            "core.ranking_snapshots",
            "core.rules",
            "core.patterns",
            "core.rhythm_profiles",
            "core.assets",
            "audit.audit_events",
        ],
        "row_counts": row_counts,
        "rollback_note": "business tables backfilled from snapshot",
        "created_at": _utc_now(),
    }


def _connect():
    if psycopg is None:
        if _fallback_allowed():
            return None
        raise RuntimeError("psycopg unavailable and business persistence fallback disabled")
    try:
        _ensure_tables()
        return psycopg.connect(_postgres_url())
    except Exception:
        if _fallback_allowed():
            return None
        raise


def _rows(mapping: Optional[dict[str, dict[str, Any]]]) -> list[dict[str, Any]]:
    return list((mapping or {}).values())


def _list_rows(items: Optional[Iterable[dict[str, Any]]]) -> list[dict[str, Any]]:
    return list(items or [])


def _json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _execute_many(cursor: Any, sql: str, rows: Iterable[tuple[Any, ...]]) -> None:
    for row in rows:
        cursor.execute(sql, row)


DELETE_ORDER = [
    "audit.migration_events",
    "audit.audit_events",
    "core.ranking_snapshots",
    "core.feedback_records",
    "core.manuscript_states",
    "core.chapter_snapshots",
    "core.revision_summaries",
    "core.consistency_reports",
    "core.quality_reports",
    "ai.provider_calls",
    "ai.prompt_packages",
    "ai.memory_packages",
    "ai.section_runs",
    "ai.writing_runs",
    "core.assets",
    "core.rhythm_profiles",
    "core.patterns",
    "core.rules",
    "core.section_plans",
    "core.chapter_plans",
    "core.story_bibles",
    "core.novel_projects",
    "core.relationship_edges",
    "core.story_climaxes",
    "core.story_rewards",
    "core.story_hooks",
    "core.story_conflicts",
    "core.story_events",
    "core.source_scenes",
    "core.graph_edges",
    "core.graph_nodes",
    "core.graph_snapshots",
    "core.object_versions",
    "core.object_aliases",
    "core.evidence_bindings",
    "core.extraction_run_evidences",
    "core.extraction_run_objects",
    "core.knowledge_objects",
    "core.evidence_records",
    "core.extraction_runs",
    "core.source_chapters",
    "core.source_contents",
    "core.source_books",
    "config.prompt_versions",
    "config.quality_gate_profiles",
    "config.agent_model_assignments",
    "config.provider_accounts",
    "config.model_profiles",
    "identity.workspace_members",
    "identity.workspaces",
    "identity.users",
]


def business_state_exists() -> bool:
    connection = _connect()
    if connection is None:
        return False
    with connection:
        with connection.cursor() as cursor:
            for table_name in ("identity.workspaces", "core.source_books", "core.novel_projects", "ai.writing_runs"):
                cursor.execute(f"SELECT EXISTS (SELECT 1 FROM {table_name} LIMIT 1)")
                if cursor.fetchone()[0]:
                    return True
    return False


def validate_business_state(snapshot: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(snapshot, dict):
        raise ValueError("business state must be a dict")
    required = {"workspaces", "books", "novel_projects", "model_profiles"}
    missing = required - set(snapshot)
    if missing:
        raise ValueError(f"business state missing fields: {sorted(missing)}")
    return snapshot


def _delete_all(cursor: Any) -> None:
    for table_name in DELETE_ORDER:
        cursor.execute(f"DELETE FROM {table_name}")


def save_business_state(snapshot: dict[str, Any]) -> None:
    snapshot = validate_business_state(snapshot)
    migration_events = _list_rows(snapshot.get("migration_events"))
    connection = _connect()
    if connection is None:
        return
    with connection:
        with connection.cursor() as cursor:
            _delete_all(cursor)
            _save_identity(cursor, snapshot)
            _save_config(cursor, snapshot)
            _save_source(cursor, snapshot)
            _save_story_structure(cursor, snapshot)
            _save_extraction_knowledge_graph(cursor, snapshot)
            _save_project_planning(cursor, snapshot)
            _save_writing_quality_feedback(cursor, snapshot)
            _save_nks_support(cursor, snapshot)
            _save_audit(cursor, {**snapshot, "migration_events": migration_events})


def backfill_business_state_from_snapshot(snapshot: dict[str, Any]) -> None:
    snapshot = validate_business_state(snapshot)
    migration_event = _build_migration_event(snapshot)
    migration_events = [
        *[item for item in _list_rows(snapshot.get("migration_events")) if item.get("migration_id") != migration_event["migration_id"]],
        migration_event,
    ]
    save_business_state({**snapshot, "migration_events": migration_events})


def load_business_state() -> Optional[dict[str, Any]]:
    connection = _connect()
    if connection is None:
        return None
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM identity.workspaces LIMIT 1)")
            if not cursor.fetchone()[0]:
                return None
            state = _empty_state()
            _load_identity(cursor, state)
            _load_config(cursor, state)
            _load_source(cursor, state)
            _load_story_structure(cursor, state)
            _load_extraction_knowledge_graph(cursor, state)
            _load_project_planning(cursor, state)
            _load_writing_quality_feedback(cursor, state)
            _load_nks_support(cursor, state)
            _load_audit(cursor, state)
            return state


def _empty_state() -> dict[str, Any]:
    return {
        "users": {},
        "workspaces": {},
        "workspace_members": {},
        "books": {},
        "source_contents": {},
        "source_content_by_book": {},
        "evidences": {},
        "evidence_by_book": {},
        "evidence_by_run": {},
        "chapters_by_book": {},
        "source_scenes_by_chapter": {},
        "events_by_scene": {},
        "conflicts": {},
        "hooks": {},
        "rewards": {},
        "climaxes": {},
        "relationship_edges": {},
        "extraction_runs": {},
        "knowledge_objects": {},
        "knowledge_by_run": {},
        "graph_summaries": {},
        "graph_node_details": {},
        "graph_neighbors_by_node": {},
        "novel_projects": {},
        "story_bibles": {},
        "chapter_plans": {},
        "chapter_plan_tasks": {},
        "section_plan_tasks": {},
        "section_plans_by_chapter": {},
        "model_profiles": {},
        "agent_model_assignments": {},
        "provider_accounts": {},
        "quality_gate_profiles": {},
        "prompt_versions": [],
        "writing_runs": {},
        "writing_run_tasks": {},
        "provider_calls_by_writing": {},
        "section_runs_by_writing": {},
        "memory_packages": {},
        "prompt_packages": {},
        "quality_reports": {},
        "consistency_reports": {},
        "revision_summaries": {},
        "rules": {},
        "chapter_snapshots": {},
        "manuscript_states_by_project": {},
        "feedback_records": {},
        "ranking_snapshots": {},
        "patterns": {},
        "rhythm_profiles": {},
        "assets": {},
        "agent_tasks": {},
        "task_events_by_task": {},
        "audit_events": [],
        "migration_events": [],
    }


def _payload_rows(cursor: Any, table_name: str, id_column: str) -> list[tuple[str, dict[str, Any]]]:
    cursor.execute(f"SELECT {id_column}, payload FROM {table_name}")
    return [(row[0], row[1] or {}) for row in cursor.fetchall()]


def _save_identity(cursor: Any, snapshot: dict[str, Any]) -> None:
    _execute_many(
        cursor,
        "INSERT INTO identity.users (user_id, payload, created_at, updated_at) VALUES (%s, %s::jsonb, %s, %s)",
        ((item["user_id"], _json(item), item.get("created_at"), item.get("updated_at")) for item in _rows(snapshot.get("users"))),
    )
    _execute_many(
        cursor,
        """
        INSERT INTO identity.workspaces (workspace_id, owner_user_id, name, slug, default_language, status, payload, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)
        """,
        (
            (
                item["workspace_id"],
                item.get("owner_user_id"),
                item.get("name", item["workspace_id"]),
                item.get("slug", item["workspace_id"]),
                item.get("default_language"),
                item.get("status", "active"),
                _json(item),
                item.get("created_at"),
                item.get("updated_at"),
            )
            for item in _rows(snapshot.get("workspaces"))
        ),
    )
    _execute_many(
        cursor,
        """
        INSERT INTO identity.workspace_members (workspace_member_id, workspace_id, user_id, role, status, payload, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s)
        """,
        (
            (item["workspace_member_id"], item["workspace_id"], item["user_id"], item["role"], item.get("status", "active"), _json(item), item.get("created_at"), item.get("updated_at"))
            for item in _rows(snapshot.get("workspace_members"))
        ),
    )


def _load_identity(cursor: Any, state: dict[str, Any]) -> None:
    state["users"] = {key: payload for key, payload in _payload_rows(cursor, "identity.users", "user_id")}
    state["workspaces"] = {key: payload for key, payload in _payload_rows(cursor, "identity.workspaces", "workspace_id")}
    state["workspace_members"] = {key: payload for key, payload in _payload_rows(cursor, "identity.workspace_members", "workspace_member_id")}


def _save_config(cursor: Any, snapshot: dict[str, Any]) -> None:
    _execute_many(cursor, "INSERT INTO config.model_profiles (model_profile_id, provider_name, provider_model_name, label, enabled, payload) VALUES (%s, %s, %s, %s, %s, %s::jsonb)", ((i["model_profile_id"], i["provider_name"], i["provider_model_name"], i.get("label", i["model_profile_id"]), i.get("enabled", True), _json(i)) for i in _rows(snapshot.get("model_profiles"))))
    _execute_many(cursor, "INSERT INTO config.provider_accounts (provider_account_id, provider_name, account_label, secret_ref, status, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["provider_account_id"], i["provider_name"], i.get("account_label", i["provider_name"]), i.get("secret_ref", "secret://providers/default"), i.get("status", "active"), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("provider_accounts"))))
    _execute_many(cursor, "INSERT INTO config.agent_model_assignments (assignment_id, agent_role, task_type, model_profile_id, enabled, payload) VALUES (%s, %s, %s, %s, %s, %s::jsonb)", ((i["assignment_id"], i["agent_role"], i["task_type"], i["model_profile_id"], i.get("enabled", True), _json(i)) for i in _rows(snapshot.get("agent_model_assignments"))))
    _execute_many(cursor, "INSERT INTO config.quality_gate_profiles (quality_gate_profile_id, workspace_id, label, payload) VALUES (%s, %s, %s, %s::jsonb)", ((i["quality_gate_profile_id"], i.get("workspace_id"), i.get("label", i["quality_gate_profile_id"]), _json(i)) for i in _rows(snapshot.get("quality_gate_profiles"))))
    _execute_many(cursor, "INSERT INTO config.prompt_versions (prompt_version_id, agent_role, template_ref, payload) VALUES (%s, %s, %s, %s::jsonb)", ((f"{i['agent_role']}:{i['template_ref']}", i["agent_role"], i["template_ref"], _json(i)) for i in _list_rows(snapshot.get("prompt_versions"))))


def _load_config(cursor: Any, state: dict[str, Any]) -> None:
    state["model_profiles"] = {key: payload for key, payload in _payload_rows(cursor, "config.model_profiles", "model_profile_id")}
    state["provider_accounts"] = {key: payload for key, payload in _payload_rows(cursor, "config.provider_accounts", "provider_account_id")}
    state["agent_model_assignments"] = {key: payload for key, payload in _payload_rows(cursor, "config.agent_model_assignments", "assignment_id")}
    state["quality_gate_profiles"] = {key: payload for key, payload in _payload_rows(cursor, "config.quality_gate_profiles", "quality_gate_profile_id")}
    state["prompt_versions"] = [payload for _, payload in _payload_rows(cursor, "config.prompt_versions", "prompt_version_id")]


def _save_source(cursor: Any, snapshot: dict[str, Any]) -> None:
    _execute_many(cursor, """
        INSERT INTO core.source_books (book_id, workspace_id, title, author_name, source_type, import_status, source_content_ref, content_checksum, content_byte_size, chapter_count, trace_id, payload, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)
    """, ((i["book_id"], i["workspace_id"], i["title"], i["author_name"], i["source_type"], i.get("import_status", "uploaded"), i.get("source_content_ref"), i.get("content_checksum"), i.get("content_byte_size"), i.get("chapter_count") or len(snapshot.get("chapters_by_book", {}).get(i["book_id"], [])), i.get("trace_id"), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("books"))))
    _execute_many(cursor, "INSERT INTO core.source_contents (source_content_id, book_id, object_ref, mime_type, checksum, byte_size, content_text, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["source_content_id"], i["book_id"], i["object_ref"], i.get("mime_type", "text/plain; charset=utf-8"), i.get("checksum", "sha256:"), i.get("byte_size", 0), i.get("content"), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("source_contents"))))
    chapters = [chapter for chapters in (snapshot.get("chapters_by_book") or {}).values() for chapter in chapters]
    _execute_many(cursor, "INSERT INTO core.source_chapters (chapter_id, book_id, chapter_index, title, segmentation_status, text_object_ref, text_range, raw_text, text_excerpt, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["chapter_id"], i["book_id"], i["chapter_index"], i["title"], i.get("segmentation_status", "segmented"), i.get("text_object_ref"), i.get("text_range"), i.get("raw_text"), i.get("text_excerpt"), _json(i), i.get("created_at"), i.get("updated_at")) for i in chapters))


def _load_source(cursor: Any, state: dict[str, Any]) -> None:
    state["books"] = {key: payload for key, payload in _payload_rows(cursor, "core.source_books", "book_id")}
    state["source_contents"] = {key: payload for key, payload in _payload_rows(cursor, "core.source_contents", "source_content_id")}
    state["source_content_by_book"] = {payload["book_id"]: key for key, payload in _payload_rows(cursor, "core.source_contents", "source_content_id")}
    chapters: dict[str, list[dict[str, Any]]] = {}
    for _, payload in _payload_rows(cursor, "core.source_chapters", "chapter_id"):
        chapters.setdefault(payload["book_id"], []).append(payload)
    for items in chapters.values():
        items.sort(key=lambda item: item.get("chapter_index", 0))
    state["chapters_by_book"] = chapters


def _save_story_structure(cursor: Any, snapshot: dict[str, Any]) -> None:
    scenes = [scene for scenes in (snapshot.get("source_scenes_by_chapter") or {}).values() for scene in scenes]
    _execute_many(cursor, "INSERT INTO core.source_scenes (scene_id, book_id, chapter_id, workspace_id, scene_index, title, text_range, segmentation_status, segmentation_confidence, evidence_refs, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s)", ((i["scene_id"], i["book_id"], i["chapter_id"], i["workspace_id"], i["scene_index"], i["title"], i["text_range"], i.get("segmentation_status", "segmented"), i.get("segmentation_confidence", 0), _json(i.get("evidence_refs", [])), _json(i), i.get("created_at"), i.get("updated_at")) for i in scenes))
    events = [event for events in (snapshot.get("events_by_scene") or {}).values() for event in events]
    _execute_many(cursor, "INSERT INTO core.story_events (event_id, book_id, chapter_id, scene_id, workspace_id, event_index, event_type, cause, action, result, consequence, participants, evidence_refs, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s::jsonb, %s, %s)", ((i["event_id"], i["book_id"], i["chapter_id"], i.get("scene_id"), i["workspace_id"], i["event_index"], i["event_type"], i["cause"], i["action"], i["result"], i["consequence"], _json(i.get("participants", [])), _json(i.get("evidence_refs", [])), _json(i), i.get("created_at"), i.get("updated_at")) for i in events))
    for item in _rows(snapshot.get("conflicts")):
        cursor.execute("INSERT INTO core.story_conflicts (conflict_id, book_id, chapter_id, scene_id, workspace_id, parties, objective, pressure, escalation_level, resolution_state, trigger_event_id, evidence_refs, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s)", (item["conflict_id"], item["book_id"], item["chapter_id"], item.get("scene_id"), item["workspace_id"], _json(item.get("parties", [])), item["objective"], item["pressure"], item.get("escalation_level", 0), item["resolution_state"], item.get("trigger_event_id"), _json(item.get("evidence_refs", [])), _json(item), item.get("created_at"), item.get("updated_at")))
    for item in _rows(snapshot.get("hooks")):
        cursor.execute("INSERT INTO core.story_hooks (hook_id, book_id, chapter_id, scene_id, workspace_id, hook_type, open_question, introduced_at, expected_resolution_range, linked_conflict_id, linked_event_id, evidence_refs, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s)", (item["hook_id"], item["book_id"], item["chapter_id"], item.get("scene_id"), item["workspace_id"], item["hook_type"], item["open_question"], item["introduced_at"], item["expected_resolution_range"], item.get("linked_conflict_id"), item.get("linked_event_id"), _json(item.get("evidence_refs", [])), _json(item), item.get("created_at"), item.get("updated_at")))
    for item in _rows(snapshot.get("rewards")):
        cursor.execute("INSERT INTO core.story_rewards (reward_id, book_id, chapter_id, scene_id, workspace_id, reward_type, trigger_event_id, beneficiary_character_id, reader_effect, intensity, payoff_target, evidence_refs, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s)", (item["reward_id"], item["book_id"], item["chapter_id"], item.get("scene_id"), item["workspace_id"], item["reward_type"], item.get("trigger_event_id"), item.get("beneficiary_character_id"), item["reader_effect"], item.get("intensity", 0), item.get("payoff_target"), _json(item.get("evidence_refs", [])), _json(item), item.get("created_at"), item.get("updated_at")))
    for item in _rows(snapshot.get("climaxes")):
        cursor.execute("INSERT INTO core.story_climaxes (climax_id, book_id, chapter_id, scene_id, workspace_id, scope_type, scope_id, event_id, conflict_id, reward_refs, hook_refs, intensity, aftermath, evidence_refs, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s, %s::jsonb, %s::jsonb, %s, %s)", (item["climax_id"], item["book_id"], item.get("chapter_id"), item.get("scene_id"), item["workspace_id"], item["scope_type"], item["scope_id"], item.get("event_id"), item.get("conflict_id"), _json(item.get("reward_refs", [])), _json(item.get("hook_refs", [])), item.get("intensity", 0), item["aftermath"], _json(item.get("evidence_refs", [])), _json(item), item.get("created_at"), item.get("updated_at")))
    for item in _rows(snapshot.get("relationship_edges")):
        cursor.execute("INSERT INTO core.relationship_edges (edge_id, book_id, workspace_id, source_id, relation_type, target_id, confidence, evidence_id, evidence_refs, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s)", (item["edge_id"], item["book_id"], item["workspace_id"], item["source_id"], item["relation_type"], item["target_id"], item.get("confidence", 0), item.get("evidence_id"), _json(item.get("evidence_refs", [])), _json(item), item.get("created_at"), item.get("updated_at")))


def _load_story_structure(cursor: Any, state: dict[str, Any]) -> None:
    for _, payload in _payload_rows(cursor, "core.source_scenes", "scene_id"):
        state["source_scenes_by_chapter"].setdefault(payload["chapter_id"], []).append(payload)
    for _, payload in _payload_rows(cursor, "core.story_events", "event_id"):
        state["events_by_scene"].setdefault(payload.get("scene_id") or payload["chapter_id"], []).append(payload)
    state["conflicts"] = {key: payload for key, payload in _payload_rows(cursor, "core.story_conflicts", "conflict_id")}
    state["hooks"] = {key: payload for key, payload in _payload_rows(cursor, "core.story_hooks", "hook_id")}
    state["rewards"] = {key: payload for key, payload in _payload_rows(cursor, "core.story_rewards", "reward_id")}
    state["climaxes"] = {key: payload for key, payload in _payload_rows(cursor, "core.story_climaxes", "climax_id")}
    state["relationship_edges"] = {key: payload for key, payload in _payload_rows(cursor, "core.relationship_edges", "edge_id")}


def _save_extraction_knowledge_graph(cursor: Any, snapshot: dict[str, Any]) -> None:
    _execute_many(cursor, "INSERT INTO core.extraction_runs (run_id, book_id, workspace_id, task_id, status, current_stage, knowledge_package_ref, graph_package_ref, extraction_report_ref, quality_report_ref, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["run_id"], i["book_id"], i["workspace_id"], i.get("task_id"), i.get("status", "queued"), i.get("current_stage"), i.get("knowledge_package_ref"), i.get("graph_package_ref"), i.get("extraction_report_ref"), i.get("quality_report_ref"), _json(i), i.get("created_at"), i.get("updated_at") or i.get("finished_at") or i.get("started_at")) for i in _rows(snapshot.get("extraction_runs"))))
    _execute_many(cursor, "INSERT INTO core.evidence_records (evidence_id, evidence_ref, book_id, chapter_id, chapter_index, text_range, excerpt, source_content_ref, confidence, trace_id, payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)", ((i["evidence_id"], i["evidence_ref"], i["book_id"], i.get("chapter_id"), i.get("chapter_index"), i["text_range"], i["excerpt"], i.get("source_content_ref"), i.get("confidence", 0), i.get("trace_id"), _json(i)) for i in _rows(snapshot.get("evidences"))))
    _execute_many(cursor, "INSERT INTO core.knowledge_objects (object_id, workspace_id, object_type, canonical_name, lifecycle_status, review_status, confidence, trace_id, payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)", ((i["object_id"], i["workspace_id"], i["object_type"], i["canonical_name"], i.get("lifecycle_status", "candidate"), i.get("review_status", "pending"), i.get("confidence", 0), i.get("trace_id"), _json(i)) for i in _rows(snapshot.get("knowledge_objects"))))
    _execute_many(cursor, "INSERT INTO core.extraction_run_objects (run_id, object_id) VALUES (%s, %s)", ((run_id, object_id) for run_id, ids in (snapshot.get("knowledge_by_run") or {}).items() for object_id in ids))
    _execute_many(cursor, "INSERT INTO core.extraction_run_evidences (run_id, evidence_id) VALUES (%s, %s)", ((run_id, evidence_id) for run_id, ids in (snapshot.get("evidence_by_run") or {}).items() for evidence_id in ids))
    evidence_ids = set((snapshot.get("evidences") or {}).keys())
    _execute_many(cursor, "INSERT INTO core.evidence_bindings (evidence_id, target_ref, target_type) VALUES (%s, %s, %s)", ((_evidence_id(ref), f"object://knowledge-objects/{obj['object_id']}", "knowledge_object") for obj in _rows(snapshot.get("knowledge_objects")) for ref in obj.get("evidence_refs", []) if _evidence_id(ref) in evidence_ids))
    _execute_many(cursor, "INSERT INTO core.graph_snapshots (graph_snapshot_id, book_id, workspace_id, payload, created_at, updated_at) VALUES (%s, %s, %s, %s::jsonb, %s, %s)", ((book_id, book_id, i.get("workspace_id", "demo-workspace"), _json(i), i.get("created_at"), i.get("updated_at")) for book_id, i in (snapshot.get("graph_summaries") or {}).items()))
    _execute_many(cursor, "INSERT INTO core.graph_nodes (node_id, book_id, label, node_type, canonical_object_id, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["node_id"], i.get("book_id", ""), i.get("label", i["node_id"]), i.get("node_type", "unknown"), i.get("canonical_object_id"), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("graph_node_details"))))
    _execute_many(cursor, "INSERT INTO core.graph_edges (edge_id, source_node_id, target_node_id, relation_type, confidence, payload) VALUES (%s, %s, %s, %s, %s, %s::jsonb)", ((f"{edge['edge_id']}:{node_id}", node_id, edge["neighbor_node_id"], edge["relation_type"], edge.get("confidence"), _json(edge)) for node_id, edges in (snapshot.get("graph_neighbors_by_node") or {}).items() for edge in edges))


def _load_extraction_knowledge_graph(cursor: Any, state: dict[str, Any]) -> None:
    state["extraction_runs"] = {key: payload for key, payload in _payload_rows(cursor, "core.extraction_runs", "run_id")}
    state["evidences"] = {key: payload for key, payload in _payload_rows(cursor, "core.evidence_records", "evidence_id")}
    state["knowledge_objects"] = {key: payload for key, payload in _payload_rows(cursor, "core.knowledge_objects", "object_id")}
    state["graph_summaries"] = {payload["book_id"]: payload for _, payload in _payload_rows(cursor, "core.graph_snapshots", "graph_snapshot_id")}
    state["graph_node_details"] = {key: payload for key, payload in _payload_rows(cursor, "core.graph_nodes", "node_id")}
    cursor.execute("SELECT run_id, object_id FROM core.extraction_run_objects")
    for run_id, object_id in cursor.fetchall():
        state["knowledge_by_run"].setdefault(run_id, []).append(object_id)
    cursor.execute("SELECT run_id, evidence_id FROM core.extraction_run_evidences")
    for run_id, evidence_id in cursor.fetchall():
        state["evidence_by_run"].setdefault(run_id, []).append(evidence_id)
    for evidence_id, evidence in state["evidences"].items():
        state["evidence_by_book"].setdefault(evidence["book_id"], []).append(evidence_id)
    cursor.execute("SELECT source_node_id, payload FROM core.graph_edges")
    for node_id, payload in cursor.fetchall():
        state["graph_neighbors_by_node"].setdefault(node_id, []).append(payload)


def _evidence_id(ref: str) -> str:
    return ref.removeprefix("evidence://")


def _save_project_planning(cursor: Any, snapshot: dict[str, Any]) -> None:
    _execute_many(cursor, "INSERT INTO core.novel_projects (project_id, workspace_id, title, genre_scope, status, story_bible_id, quality_gate_profile_id, allowed_knowledge_source_refs, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s)", ((i["project_id"], i["workspace_id"], i["title"], i.get("genre_scope"), i.get("status", "planning"), i.get("story_bible_id"), i.get("quality_gate_profile_id"), _json(i.get("allowed_knowledge_source_refs", [])), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("novel_projects"))))
    _execute_many(cursor, "INSERT INTO core.story_bibles (story_bible_id, project_id, workspace_id, version, status, payload, trace_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s)", ((i["story_bible_id"], i["project_id"], i["workspace_id"], i.get("version", 1), i.get("status", "draft"), _json(i), i.get("trace_id"), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("story_bibles"))))
    _execute_many(cursor, "INSERT INTO core.chapter_plans (chapter_plan_id, project_id, workspace_id, chapter_index, status, target_word_count, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["chapter_plan_id"], i["project_id"], i["workspace_id"], i["chapter_index"], i.get("status", "queued"), i.get("target_word_count"), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("chapter_plans"))))
    sections = [section for sections in (snapshot.get("section_plans_by_chapter") or {}).values() for section in sections]
    _execute_many(cursor, "INSERT INTO core.section_plans (section_plan_id, chapter_plan_id, workspace_id, section_index, planning_role, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["section_plan_id"], i["chapter_plan_id"], i["workspace_id"], i["section_index"], i.get("planning_role"), _json(i), i.get("created_at"), i.get("updated_at")) for i in sections))


def _load_project_planning(cursor: Any, state: dict[str, Any]) -> None:
    state["novel_projects"] = {key: payload for key, payload in _payload_rows(cursor, "core.novel_projects", "project_id")}
    state["story_bibles"] = {key: payload for key, payload in _payload_rows(cursor, "core.story_bibles", "story_bible_id")}
    state["chapter_plans"] = {key: payload for key, payload in _payload_rows(cursor, "core.chapter_plans", "chapter_plan_id")}
    for _, payload in _payload_rows(cursor, "core.section_plans", "section_plan_id"):
        state["section_plans_by_chapter"].setdefault(payload["chapter_plan_id"], []).append(payload)


def _save_writing_quality_feedback(cursor: Any, snapshot: dict[str, Any]) -> None:
    _execute_many(cursor, "INSERT INTO ai.writing_runs (writing_run_id, project_id, chapter_plan_id, workspace_id, task_id, status, current_stage, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["writing_run_id"], i["project_id"], i["chapter_plan_id"], i["workspace_id"], i.get("task_id"), i.get("status", "queued"), i.get("current_stage"), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("writing_runs"))))
    section_runs = [section for sections in (snapshot.get("section_runs_by_writing") or {}).values() for section in sections]
    _execute_many(cursor, "INSERT INTO ai.section_runs (section_run_id, writing_run_id, section_plan_id, status, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["section_run_id"], i["writing_run_id"], i.get("section_plan_id"), i.get("status", "queued"), _json(i), i.get("created_at"), i.get("updated_at")) for i in section_runs))
    _execute_many(cursor, "INSERT INTO ai.memory_packages (memory_package_id, writing_run_id, workspace_id, summary, source_refs, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s)", ((i["memory_package_id"], i.get("writing_run_id"), i["workspace_id"], i.get("summary"), _json(i.get("source_refs", [])), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("memory_packages"))))
    _execute_many(cursor, "INSERT INTO ai.prompt_packages (prompt_package_id, writing_run_id, workspace_id, summary, template_refs, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s)", ((i["prompt_package_id"], i.get("writing_run_id"), i["workspace_id"], i.get("summary"), _json(i.get("template_refs", [])), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("prompt_packages"))))
    provider_calls = [call for calls in (snapshot.get("provider_calls_by_writing") or {}).values() for call in calls]
    _execute_many(cursor, "INSERT INTO ai.provider_calls (provider_call_id, writing_run_id, workspace_id, agent_role, model_profile_id, provider_name, provider_model_name, status, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["provider_call_id"], i.get("writing_run_id"), i["workspace_id"], i["agent_role"], i.get("model_profile_id"), i.get("provider_name"), i.get("provider_model_name"), i.get("status", "succeeded"), _json(i), i.get("created_at"), i.get("updated_at")) for i in provider_calls))
    for field, table, key in (("quality_reports", "core.quality_reports", "quality_report_id"), ("consistency_reports", "core.consistency_reports", "consistency_report_id"), ("revision_summaries", "core.revision_summaries", "revision_summary_id")):
        _execute_many(cursor, f"INSERT INTO {table} ({key}, writing_run_id, workspace_id, status, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s::jsonb, %s, %s)", ((i[key], i.get("writing_run_id"), i["workspace_id"], i.get("status", "queued"), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get(field))))
    _execute_many(cursor, "INSERT INTO core.chapter_snapshots (chapter_snapshot_id, writing_run_id, project_id, chapter_plan_id, accepted_chapter_ref, chapter_text, payload, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s)", ((i["chapter_snapshot_id"], i["writing_run_id"], i["project_id"], i["chapter_plan_id"], i.get("accepted_chapter_ref"), i["chapter_text"], _json(i), i.get("created_at")) for i in _rows(snapshot.get("chapter_snapshots"))))
    _execute_many(cursor, "INSERT INTO core.manuscript_states (manuscript_state_id, project_id, writing_run_id, payload, updated_at) VALUES (%s, %s, %s, %s::jsonb, %s)", ((i.get("manuscript_state_id", key), i["project_id"], i.get("writing_run_id"), _json(i), i.get("updated_at")) for key, i in (snapshot.get("manuscript_states_by_project") or {}).items()))
    _execute_many(cursor, "INSERT INTO core.feedback_records (feedback_record_id, workspace_id, target_type, target_id, feedback_type, score, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)", ((i["feedback_record_id"], i["workspace_id"], i["target_type"], i["target_id"], i["feedback_type"], i.get("score"), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get("feedback_records"))))
    _execute_many(cursor, "INSERT INTO core.ranking_snapshots (ranking_snapshot_id, ranking_type, scope_ref, version, payload, updated_at) VALUES (%s, %s, %s, %s, %s::jsonb, %s)", ((i["ranking_snapshot_id"], i["ranking_type"], i["scope_ref"], i.get("version", 1), _json(i), i.get("updated_at")) for i in _rows(snapshot.get("ranking_snapshots"))))


def _load_writing_quality_feedback(cursor: Any, state: dict[str, Any]) -> None:
    state["writing_runs"] = {key: payload for key, payload in _payload_rows(cursor, "ai.writing_runs", "writing_run_id")}
    for _, payload in _payload_rows(cursor, "ai.section_runs", "section_run_id"):
        state["section_runs_by_writing"].setdefault(payload["writing_run_id"], []).append(payload)
    state["memory_packages"] = {key: payload for key, payload in _payload_rows(cursor, "ai.memory_packages", "memory_package_id")}
    state["prompt_packages"] = {key: payload for key, payload in _payload_rows(cursor, "ai.prompt_packages", "prompt_package_id")}
    for _, payload in _payload_rows(cursor, "ai.provider_calls", "provider_call_id"):
        state["provider_calls_by_writing"].setdefault(payload["writing_run_id"], []).append(payload)
    state["quality_reports"] = {key: payload for key, payload in _payload_rows(cursor, "core.quality_reports", "quality_report_id")}
    state["consistency_reports"] = {key: payload for key, payload in _payload_rows(cursor, "core.consistency_reports", "consistency_report_id")}
    state["revision_summaries"] = {key: payload for key, payload in _payload_rows(cursor, "core.revision_summaries", "revision_summary_id")}
    state["chapter_snapshots"] = {key: payload for key, payload in _payload_rows(cursor, "core.chapter_snapshots", "chapter_snapshot_id")}
    state["manuscript_states_by_project"] = {payload["project_id"]: payload for _, payload in _payload_rows(cursor, "core.manuscript_states", "manuscript_state_id")}
    state["feedback_records"] = {key: payload for key, payload in _payload_rows(cursor, "core.feedback_records", "feedback_record_id")}
    state["ranking_snapshots"] = {key: payload for key, payload in _payload_rows(cursor, "core.ranking_snapshots", "ranking_snapshot_id")}


def _save_nks_support(cursor: Any, snapshot: dict[str, Any]) -> None:
    for field, table, key, type_key in (("rules", "core.rules", "rule_id", "rule_type"), ("patterns", "core.patterns", "pattern_id", "pattern_type"), ("rhythm_profiles", "core.rhythm_profiles", "rhythm_profile_id", None), ("assets", "core.assets", "asset_id", "asset_type")):
        _execute_many(cursor, f"INSERT INTO {table} ({key}, workspace_id, {type_key or 'target_id'}, status, payload, created_at, updated_at) VALUES (%s, %s, %s, %s, %s::jsonb, %s, %s)", ((i[key], i["workspace_id"], i.get(type_key) if type_key else i.get("target_id"), i.get("status", "approved"), _json(i), i.get("created_at"), i.get("updated_at")) for i in _rows(snapshot.get(field))))


def _load_nks_support(cursor: Any, state: dict[str, Any]) -> None:
    state["rules"] = {key: payload for key, payload in _payload_rows(cursor, "core.rules", "rule_id")}
    state["patterns"] = {key: payload for key, payload in _payload_rows(cursor, "core.patterns", "pattern_id")}
    state["rhythm_profiles"] = {key: payload for key, payload in _payload_rows(cursor, "core.rhythm_profiles", "rhythm_profile_id")}
    state["assets"] = {key: payload for key, payload in _payload_rows(cursor, "core.assets", "asset_id")}


def _save_audit(cursor: Any, snapshot: dict[str, Any]) -> None:
    _execute_many(cursor, "INSERT INTO audit.audit_events (audit_event_id, workspace_id, action, target_type, target_id, payload, created_at) VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s)", ((i["audit_event_id"], i["workspace_id"], i["action"], i["target_type"], i["target_id"], _json(i), i.get("created_at")) for i in _list_rows(snapshot.get("audit_events"))))
    _execute_many(cursor, "INSERT INTO audit.migration_events (migration_id, snapshot_hash, affected_tables, row_counts, rollback_note, created_at) VALUES (%s, %s, %s::jsonb, %s::jsonb, %s, %s)", ((i["migration_id"], i.get("snapshot_hash"), _json(i.get("affected_tables", [])), _json(i.get("row_counts", {})), i.get("rollback_note"), i.get("created_at")) for i in _list_rows(snapshot.get("migration_events"))))


def _load_audit(cursor: Any, state: dict[str, Any]) -> None:
    state["audit_events"] = [payload for _, payload in _payload_rows(cursor, "audit.audit_events", "audit_event_id")]
    cursor.execute("SELECT migration_id, snapshot_hash, affected_tables, row_counts, rollback_note, created_at FROM audit.migration_events ORDER BY created_at, migration_id")
    state["migration_events"] = [
        {
            "migration_id": migration_id,
            "snapshot_hash": snapshot_hash,
            "affected_tables": affected_tables or [],
            "row_counts": row_counts or {},
            "rollback_note": rollback_note,
            "created_at": created_at.isoformat() if hasattr(created_at, "isoformat") else created_at,
        }
        for migration_id, snapshot_hash, affected_tables, row_counts, rollback_note, created_at in cursor.fetchall()
    ]
