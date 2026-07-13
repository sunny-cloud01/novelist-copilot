from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import psycopg
except ImportError:
    psycopg = None


RUNTIME_PROJECTION_FILE = "runtime-projection"
FILE_PERSISTENCE_FALLBACK_ENV = "NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK"
POSTGRES_INIT_DIR = Path(__file__).resolve().parents[4] / "infra/postgres/init"


def _postgres_url() -> str:
    return os.getenv("NOVEL_FACTORY_POSTGRES_URL", "postgresql://novel:novel@localhost:5436/novel_factory")


def _file_persistence_fallback_allowed() -> bool:
    return os.getenv(FILE_PERSISTENCE_FALLBACK_ENV, "").strip().lower() in {"1", "true", "yes", "on"}


def _json_dumps(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def _snapshot_path(snapshot_key: str) -> Path:
    parsed = urlparse(_postgres_url())
    host = parsed.hostname or "local"
    port = parsed.port or 5432
    database = parsed.path.lstrip("/") or "novel_factory"
    return Path("/tmp") / f"{database}-{host}-{port}-{snapshot_key}.snapshot.json"


def _projection_path(projection_key: str = RUNTIME_PROJECTION_FILE) -> Path:
    return _snapshot_path(projection_key)


def _runtime_schema_paths() -> list[Path]:
    return sorted(POSTGRES_INIT_DIR.glob("[0-9][0-9][0-9]-*.sql"))


def _ensure_tables() -> None:
    if psycopg is None:
        return
    schema_paths = _runtime_schema_paths()
    if not schema_paths:
        raise RuntimeError(f"runtime schema files missing under {POSTGRES_INIT_DIR}")
    with psycopg.connect(_postgres_url()) as connection:
        with connection.cursor() as cursor:
            for schema_path in schema_paths:
                cursor.execute(schema_path.read_text())
        connection.commit()


def _raise_persistence_unavailable(exc: Exception | None = None) -> None:
    if exc is None and psycopg is None:
        raise RuntimeError("psycopg unavailable and file persistence fallback disabled")
    raise RuntimeError("Postgres persistence unavailable and file persistence fallback disabled") from exc


def _load_json_file(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def _write_json_file(path: Path, payload: Any) -> None:
    path.write_text(_json_dumps(payload))


def _normalize_timestamp_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.replace(" ", "T")
    if normalized.endswith("Z"):
        return normalized
    if len(normalized) >= 3 and normalized[-3] in {"+", "-"}:
        normalized = f"{normalized}:00"
    return normalized


def _sync_projection_with_postgres(projection: dict[str, list[dict[str, Any]]]) -> None:
    if psycopg is None:
        raise RuntimeError("psycopg unavailable")
    _ensure_tables()
    with psycopg.connect(_postgres_url()) as connection:
        with connection.cursor() as cursor:
            object_refs = [row["object_ref"] for row in projection["objects"]]
            task_ids = [row["task_id"] for row in projection["tasks"]]
            task_lock_ids = [row["task_lock_id"] for row in projection["task_locks"]]
            task_event_ids = [row["task_event_id"] for row in projection["task_events"]]
            audit_event_ids = [row["audit_event_id"] for row in projection["audit_events"]]

            for row in projection["objects"]:
                cursor.execute(
                    """
                    INSERT INTO runtime_objects (
                        object_ref, workspace_id, object_kind, bucket, storage_key, checksum, mime_type,
                        byte_size, access_policy, owner_ref, payload, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s::jsonb, %s, %s
                    )
                    ON CONFLICT (object_ref)
                    DO UPDATE SET
                        workspace_id = EXCLUDED.workspace_id,
                        object_kind = EXCLUDED.object_kind,
                        bucket = EXCLUDED.bucket,
                        storage_key = EXCLUDED.storage_key,
                        checksum = EXCLUDED.checksum,
                        mime_type = EXCLUDED.mime_type,
                        byte_size = EXCLUDED.byte_size,
                        access_policy = EXCLUDED.access_policy,
                        owner_ref = EXCLUDED.owner_ref,
                        payload = EXCLUDED.payload,
                        created_at = EXCLUDED.created_at,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (
                        row["object_ref"],
                        row["workspace_id"],
                        row["object_kind"],
                        row.get("bucket"),
                        row.get("storage_key"),
                        row.get("checksum"),
                        row.get("mime_type"),
                        row.get("byte_size"),
                        row.get("access_policy"),
                        row.get("owner_ref"),
                        _json_dumps(row.get("payload", {})),
                        row.get("created_at"),
                        row.get("updated_at"),
                    ),
                )
            for row in projection["tasks"]:
                cursor.execute(
                    """
                    INSERT INTO runtime_tasks (
                        task_id, workspace_id, task_type, owner_module, status, progress, idempotency_key,
                        request_id, trace_id, actor_id, retry_count, max_retry_count, latency_ms, error_code,
                        lease_owner, lease_expires_at, heartbeat_at, next_retry_at, review_required, blocked_reason,
                        input_refs, output_refs, created_at, started_at, finished_at, payload, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s::jsonb, %s::jsonb, %s, %s, %s, %s::jsonb, %s
                    )
                    ON CONFLICT (task_id)
                    DO UPDATE SET
                        workspace_id = EXCLUDED.workspace_id,
                        task_type = EXCLUDED.task_type,
                        owner_module = EXCLUDED.owner_module,
                        status = EXCLUDED.status,
                        progress = EXCLUDED.progress,
                        idempotency_key = EXCLUDED.idempotency_key,
                        request_id = EXCLUDED.request_id,
                        trace_id = EXCLUDED.trace_id,
                        actor_id = EXCLUDED.actor_id,
                        retry_count = EXCLUDED.retry_count,
                        max_retry_count = EXCLUDED.max_retry_count,
                        latency_ms = EXCLUDED.latency_ms,
                        error_code = EXCLUDED.error_code,
                        lease_owner = EXCLUDED.lease_owner,
                        lease_expires_at = EXCLUDED.lease_expires_at,
                        heartbeat_at = EXCLUDED.heartbeat_at,
                        next_retry_at = EXCLUDED.next_retry_at,
                        review_required = EXCLUDED.review_required,
                        blocked_reason = EXCLUDED.blocked_reason,
                        input_refs = EXCLUDED.input_refs,
                        output_refs = EXCLUDED.output_refs,
                        created_at = EXCLUDED.created_at,
                        started_at = EXCLUDED.started_at,
                        finished_at = EXCLUDED.finished_at,
                        payload = EXCLUDED.payload,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (
                        row["task_id"],
                        row["workspace_id"],
                        row["task_type"],
                        row["owner_module"],
                        row["status"],
                        row.get("progress", 0),
                        row["idempotency_key"],
                        row.get("request_id"),
                        row.get("trace_id"),
                        row.get("actor_id"),
                        row.get("retry_count", 0),
                        row.get("max_retry_count", 3),
                        row.get("latency_ms"),
                        row.get("error_code"),
                        row.get("lease_owner"),
                        row.get("lease_expires_at"),
                        row.get("heartbeat_at"),
                        row.get("next_retry_at"),
                        row.get("review_required", False),
                        row.get("blocked_reason"),
                        _json_dumps(row.get("input_refs", [])),
                        _json_dumps(row.get("output_refs", [])),
                        row.get("created_at"),
                        row.get("started_at"),
                        row.get("finished_at"),
                        _json_dumps(row.get("payload", {})),
                        row.get("updated_at") or row.get("finished_at") or row.get("started_at") or row.get("created_at"),
                    ),
                )
            for row in projection["task_locks"]:
                cursor.execute(
                    """
                    INSERT INTO runtime_task_locks (
                        task_lock_id, task_id, lock_owner, lease_expires_at, heartbeat_at, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (task_lock_id)
                    DO UPDATE SET
                        task_id = EXCLUDED.task_id,
                        lock_owner = EXCLUDED.lock_owner,
                        lease_expires_at = EXCLUDED.lease_expires_at,
                        heartbeat_at = EXCLUDED.heartbeat_at,
                        created_at = EXCLUDED.created_at,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (
                        row["task_lock_id"],
                        row["task_id"],
                        row.get("lock_owner"),
                        row.get("lease_expires_at"),
                        row.get("heartbeat_at"),
                        row.get("created_at"),
                        row.get("updated_at") or row.get("heartbeat_at") or row.get("created_at"),
                    ),
                )
            for row in projection["task_events"]:
                cursor.execute(
                    """
                    INSERT INTO runtime_task_events (
                        task_event_id, task_id, workspace_id, event_type, status, request_id, trace_id,
                        actor_id, agent_role, message, payload_ref, payload_json, error_code, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s::jsonb, %s, %s, %s
                    )
                    ON CONFLICT (task_event_id)
                    DO UPDATE SET
                        task_id = EXCLUDED.task_id,
                        workspace_id = EXCLUDED.workspace_id,
                        event_type = EXCLUDED.event_type,
                        status = EXCLUDED.status,
                        request_id = EXCLUDED.request_id,
                        trace_id = EXCLUDED.trace_id,
                        actor_id = EXCLUDED.actor_id,
                        agent_role = EXCLUDED.agent_role,
                        message = EXCLUDED.message,
                        payload_ref = EXCLUDED.payload_ref,
                        payload_json = EXCLUDED.payload_json,
                        error_code = EXCLUDED.error_code,
                        created_at = EXCLUDED.created_at,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (
                        row["task_event_id"],
                        row["task_id"],
                        row["workspace_id"],
                        row["event_type"],
                        row["status"],
                        row.get("request_id"),
                        row.get("trace_id"),
                        row.get("actor_id"),
                        row.get("agent_role"),
                        row["message"],
                        row.get("payload_ref"),
                        _json_dumps(row.get("payload_json", {})),
                        row.get("error_code"),
                        row["created_at"],
                        row.get("updated_at") or row["created_at"],
                    ),
                )
            for row in projection["audit_events"]:
                cursor.execute(
                    """
                    INSERT INTO runtime_audit_events (
                        audit_event_id, workspace_id, request_id, trace_id, actor_id, actor_role,
                        action, target_type, target_id, target_ref, before_ref, after_ref,
                        reason, payload, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s, %s::jsonb, %s, %s
                    )
                    ON CONFLICT (audit_event_id)
                    DO UPDATE SET
                        workspace_id = EXCLUDED.workspace_id,
                        request_id = EXCLUDED.request_id,
                        trace_id = EXCLUDED.trace_id,
                        actor_id = EXCLUDED.actor_id,
                        actor_role = EXCLUDED.actor_role,
                        action = EXCLUDED.action,
                        target_type = EXCLUDED.target_type,
                        target_id = EXCLUDED.target_id,
                        target_ref = EXCLUDED.target_ref,
                        before_ref = EXCLUDED.before_ref,
                        after_ref = EXCLUDED.after_ref,
                        reason = EXCLUDED.reason,
                        payload = EXCLUDED.payload,
                        created_at = EXCLUDED.created_at,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (
                        row["audit_event_id"],
                        row["workspace_id"],
                        row.get("request_id"),
                        row.get("trace_id"),
                        row.get("actor_id"),
                        row.get("actor_role"),
                        row["action"],
                        row["target_type"],
                        row["target_id"],
                        row.get("target_ref"),
                        row.get("before_ref"),
                        row.get("after_ref"),
                        row.get("reason"),
                        _json_dumps(row.get("payload", {})),
                        row["created_at"],
                        row.get("updated_at") or row["created_at"],
                    ),
                )

            cursor.execute("DELETE FROM runtime_objects WHERE NOT (object_ref = ANY(%s))", (object_refs or ["__none__"],))
            cursor.execute("DELETE FROM runtime_tasks WHERE NOT (task_id = ANY(%s))", (task_ids or ["__none__"],))
            cursor.execute("DELETE FROM runtime_task_locks WHERE NOT (task_lock_id = ANY(%s))", (task_lock_ids or ["__none__"],))
            cursor.execute("DELETE FROM runtime_task_events WHERE NOT (task_event_id = ANY(%s))", (task_event_ids or ["__none__"],))
            cursor.execute("DELETE FROM runtime_audit_events WHERE NOT (audit_event_id = ANY(%s))", (audit_event_ids or ["__none__"],))
        connection.commit()


def _load_projection_from_postgres() -> dict[str, list[dict[str, Any]]]:
    if psycopg is None:
        raise RuntimeError("psycopg unavailable")
    _ensure_tables()
    with psycopg.connect(_postgres_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT object_ref, workspace_id, object_kind, bucket, storage_key, checksum, mime_type, byte_size, access_policy, owner_ref, payload::text, created_at::text, updated_at::text FROM runtime_objects ORDER BY object_ref"
            )
            objects = [
                {
                    "object_ref": row[0],
                    "workspace_id": row[1],
                    "object_kind": row[2],
                    "bucket": row[3],
                    "storage_key": row[4],
                    "checksum": row[5],
                    "mime_type": row[6],
                    "byte_size": row[7],
                    "access_policy": row[8],
                    "owner_ref": row[9],
                    "payload": json.loads(row[10]) if row[10] else {},
                    "created_at": _normalize_timestamp_text(row[11]),
                    "updated_at": _normalize_timestamp_text(row[12]),
                }
                for row in cursor.fetchall()
            ]
            cursor.execute(
                "SELECT task_id, workspace_id, task_type, owner_module, status, progress, idempotency_key, request_id, trace_id, actor_id, retry_count, max_retry_count, latency_ms, error_code, lease_owner, lease_expires_at::text, heartbeat_at::text, next_retry_at::text, review_required, blocked_reason, input_refs::text, output_refs::text, created_at::text, started_at::text, finished_at::text, payload::text, updated_at::text FROM runtime_tasks ORDER BY created_at NULLS FIRST, task_id"
            )
            tasks = [
                {
                    "task_id": row[0],
                    "workspace_id": row[1],
                    "task_type": row[2],
                    "owner_module": row[3],
                    "status": row[4],
                    "progress": row[5],
                    "idempotency_key": row[6],
                    "request_id": row[7],
                    "trace_id": row[8],
                    "actor_id": row[9],
                    "retry_count": row[10],
                    "max_retry_count": row[11],
                    "latency_ms": row[12],
                    "error_code": row[13],
                    "lease_owner": row[14],
                    "lease_expires_at": _normalize_timestamp_text(row[15]),
                    "heartbeat_at": _normalize_timestamp_text(row[16]),
                    "next_retry_at": _normalize_timestamp_text(row[17]),
                    "review_required": row[18],
                    "blocked_reason": row[19],
                    "input_refs": json.loads(row[20]) if row[20] else [],
                    "output_refs": json.loads(row[21]) if row[21] else [],
                    "created_at": _normalize_timestamp_text(row[22]),
                    "started_at": _normalize_timestamp_text(row[23]),
                    "finished_at": _normalize_timestamp_text(row[24]),
                    "payload": json.loads(row[25]) if row[25] else {},
                    "updated_at": row[26],
                }
                for row in cursor.fetchall()
            ]
            cursor.execute(
                "SELECT task_lock_id, task_id, lock_owner, lease_expires_at::text, heartbeat_at::text, created_at::text, updated_at::text FROM runtime_task_locks ORDER BY task_id"
            )
            task_locks = [
                {
                    "task_lock_id": row[0],
                    "task_id": row[1],
                    "lock_owner": row[2],
                    "lease_expires_at": _normalize_timestamp_text(row[3]),
                    "heartbeat_at": _normalize_timestamp_text(row[4]),
                    "created_at": _normalize_timestamp_text(row[5]),
                    "updated_at": _normalize_timestamp_text(row[6]),
                }
                for row in cursor.fetchall()
            ]
            cursor.execute(
                "SELECT task_event_id, task_id, workspace_id, event_type, status, request_id, trace_id, actor_id, agent_role, message, payload_ref, payload_json::text, error_code, created_at::text, updated_at::text FROM runtime_task_events ORDER BY created_at, task_event_id"
            )
            task_events = [
                {
                    "task_event_id": row[0],
                    "task_id": row[1],
                    "workspace_id": row[2],
                    "event_type": row[3],
                    "status": row[4],
                    "request_id": row[5],
                    "trace_id": row[6],
                    "actor_id": row[7],
                    "agent_role": row[8],
                    "message": row[9],
                    "payload_ref": row[10],
                    "payload_json": json.loads(row[11]) if row[11] else {},
                    "error_code": row[12],
                    "created_at": row[13],
                    "updated_at": row[14],
                }
                for row in cursor.fetchall()
            ]
            cursor.execute(
                "SELECT audit_event_id, workspace_id, request_id, trace_id, actor_id, actor_role, action, target_type, target_id, target_ref, before_ref, after_ref, reason, payload::text, created_at::text, updated_at::text FROM runtime_audit_events ORDER BY created_at, audit_event_id"
            )
            audit_events = [
                {
                    "audit_event_id": row[0],
                    "workspace_id": row[1],
                    "request_id": row[2],
                    "trace_id": row[3],
                    "actor_id": row[4],
                    "actor_role": row[5],
                    "action": row[6],
                    "target_type": row[7],
                    "target_id": row[8],
                    "target_ref": row[9],
                    "before_ref": row[10],
                    "after_ref": row[11],
                    "reason": row[12],
                    "payload": json.loads(row[13]) if row[13] else {},
                    "created_at": row[14],
                    "updated_at": row[15],
                }
                for row in cursor.fetchall()
            ]
    return {
        "objects": objects,
        "tasks": tasks,
        "task_locks": task_locks,
        "task_events": task_events,
        "audit_events": audit_events,
    }


def load_snapshot(snapshot_key: str = "core-store") -> dict[str, Any] | None:
    if psycopg is not None:
        try:
            _ensure_tables()
            with psycopg.connect(_postgres_url()) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT payload::text FROM app_state_snapshots WHERE snapshot_key = %s",
                        (snapshot_key,),
                    )
                    row = cursor.fetchone()
                    if row:
                        return json.loads(row[0])
                    return None
        except Exception as exc:
            if not _file_persistence_fallback_allowed():
                _raise_persistence_unavailable(exc)
    elif not _file_persistence_fallback_allowed():
        _raise_persistence_unavailable()

    path = _snapshot_path(snapshot_key)
    if not path.exists():
        return None
    return json.loads(path.read_text())


def save_snapshot(payload: dict[str, Any], snapshot_key: str = "core-store") -> None:
    serialized = _json_dumps(payload)

    if psycopg is not None:
        try:
            _ensure_tables()
            with psycopg.connect(_postgres_url()) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO app_state_snapshots (snapshot_key, payload, updated_at)
                        VALUES (%s, %s::jsonb, now())
                        ON CONFLICT (snapshot_key)
                        DO UPDATE SET payload = EXCLUDED.payload, updated_at = now()
                        """,
                        (snapshot_key, serialized),
                    )
                connection.commit()
            return
        except Exception as exc:
            if not _file_persistence_fallback_allowed():
                _raise_persistence_unavailable(exc)
    elif not _file_persistence_fallback_allowed():
        _raise_persistence_unavailable()

    _snapshot_path(snapshot_key).write_text(serialized)


def sync_runtime_projection(
    *,
    objects: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
    task_locks: list[dict[str, Any]],
    task_events: list[dict[str, Any]],
    audit_events: list[dict[str, Any]],
) -> None:
    projection = {
        "objects": objects,
        "tasks": tasks,
        "task_locks": task_locks,
        "task_events": task_events,
        "audit_events": audit_events,
    }
    if psycopg is not None:
        try:
            _sync_projection_with_postgres(projection)
            return
        except Exception as exc:
            if not _file_persistence_fallback_allowed():
                _raise_persistence_unavailable(exc)
    elif not _file_persistence_fallback_allowed():
        _raise_persistence_unavailable()
    _write_json_file(_projection_path(), projection)


def load_runtime_projection() -> dict[str, list[dict[str, Any]]]:
    if psycopg is not None:
        try:
            return _load_projection_from_postgres()
        except Exception as exc:
            if not _file_persistence_fallback_allowed():
                _raise_persistence_unavailable(exc)
    elif not _file_persistence_fallback_allowed():
        _raise_persistence_unavailable()
    payload = _load_json_file(_projection_path())
    if isinstance(payload, dict):
        return {
            "objects": payload.get("objects", []),
            "tasks": payload.get("tasks", []),
            "task_locks": payload.get("task_locks", []),
            "task_events": payload.get("task_events", []),
            "audit_events": payload.get("audit_events", []),
        }
    return {
        "objects": [],
        "tasks": [],
        "task_locks": [],
        "task_events": [],
        "audit_events": [],
    }
