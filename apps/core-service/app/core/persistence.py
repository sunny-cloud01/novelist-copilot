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


def _postgres_url() -> str:
    return os.getenv("NOVEL_FACTORY_POSTGRES_URL", "postgresql://novel:novel@localhost:5436/novel_factory")


def _snapshot_path(snapshot_key: str) -> Path:
    parsed = urlparse(_postgres_url())
    host = parsed.hostname or "local"
    port = parsed.port or 5432
    database = parsed.path.lstrip("/") or "novel_factory"
    return Path("/tmp") / f"{database}-{host}-{port}-{snapshot_key}.snapshot.json"


def _ensure_table() -> None:
    if psycopg is None:
        return
    with psycopg.connect(_postgres_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS app_state_snapshots (
                    snapshot_key text PRIMARY KEY,
                    payload jsonb NOT NULL,
                    updated_at timestamptz NOT NULL DEFAULT now()
                )
                """
            )
        connection.commit()


def load_snapshot(snapshot_key: str = "core-store") -> dict[str, Any] | None:
    if psycopg is not None:
        try:
            _ensure_table()
            with psycopg.connect(_postgres_url()) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT payload::text FROM app_state_snapshots WHERE snapshot_key = %s",
                        (snapshot_key,),
                    )
                    row = cursor.fetchone()
                    if row:
                        return json.loads(row[0])
        except Exception:
            pass

    path = _snapshot_path(snapshot_key)
    if not path.exists():
        return None
    return json.loads(path.read_text())


def save_snapshot(payload: dict[str, Any], snapshot_key: str = "core-store") -> None:
    serialized = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)

    if psycopg is not None:
        try:
            _ensure_table()
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
        except Exception:
            pass

    _snapshot_path(snapshot_key).write_text(serialized)
