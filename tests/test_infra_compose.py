from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps/core-service"))

from app.core.persistence import load_snapshot, save_snapshot


@pytest.mark.skipif(shutil.which("docker") is None, reason="docker CLI is unavailable")
def test_docker_compose_file_is_valid() -> None:
    compose_path = Path("infra/docker-compose.yml")
    assert compose_path.exists()

    result = subprocess.run(
        ["docker", "compose", "-f", str(compose_path), "config"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "postgres:" in result.stdout
    assert "redis:" in result.stdout
    assert "minio:" in result.stdout
    assert "minio-bootstrap:" in result.stdout
    assert "core-service:" in result.stdout
    assert "api-gateway:" in result.stdout
    assert "ai-worker:" in result.stdout
    assert "scheduler:" in result.stdout


def test_pgvector_init_and_env_example_exist() -> None:
    sql = Path("infra/postgres/init/001-enable-extensions.sql").read_text()
    runtime_tables_sql = Path("infra/postgres/init/002-runtime-tables.sql").read_text()
    runtime_indexes_sql = Path("infra/postgres/init/003-runtime-indexes.sql").read_text()
    business_schemas_sql = Path("infra/postgres/init/004-business-schemas.sql").read_text()
    business_source_sql = Path("infra/postgres/init/005-identity-config-source-tables.sql").read_text()
    business_tables_sql = Path("infra/postgres/init/006-knowledge-project-writing-tables.sql").read_text()
    business_indexes_sql = Path("infra/postgres/init/007-business-indexes.sql").read_text()
    assert "CREATE EXTENSION IF NOT EXISTS vector;" in sql
    assert "CREATE TABLE IF NOT EXISTS runtime_tasks" in runtime_tables_sql
    assert "CREATE TABLE IF NOT EXISTS runtime_objects" in runtime_tables_sql
    assert "CREATE INDEX IF NOT EXISTS idx_runtime_tasks_status_next_retry_at" in runtime_indexes_sql
    assert "CREATE INDEX IF NOT EXISTS idx_runtime_objects_owner_ref" in runtime_indexes_sql
    assert "CREATE SCHEMA IF NOT EXISTS identity;" in business_schemas_sql
    assert "CREATE SCHEMA IF NOT EXISTS core;" in business_schemas_sql
    assert "CREATE SCHEMA IF NOT EXISTS ai;" in business_schemas_sql
    assert "CREATE SCHEMA IF NOT EXISTS config;" in business_schemas_sql
    assert "CREATE SCHEMA IF NOT EXISTS audit;" in business_schemas_sql
    for table_name in [
        "identity.users",
        "identity.workspaces",
        "identity.workspace_members",
        "config.model_profiles",
        "config.agent_model_assignments",
        "config.provider_accounts",
        "core.source_books",
        "core.source_contents",
        "core.source_chapters",
        "core.extraction_runs",
        "core.evidence_records",
        "core.knowledge_objects",
        "core.novel_projects",
        "core.story_bibles",
        "core.chapter_plans",
        "core.section_plans",
        "ai.writing_runs",
        "ai.section_runs",
        "ai.provider_calls",
        "core.quality_reports",
        "core.feedback_records",
        "audit.migration_events",
        "core.source_scenes",
        "core.story_events",
        "core.story_conflicts",
        "core.story_hooks",
        "core.story_rewards",
        "core.story_climaxes",
        "core.relationship_edges",
    ]:
        assert f"CREATE TABLE IF NOT EXISTS {table_name}" in business_source_sql + business_tables_sql
    assert "CREATE INDEX IF NOT EXISTS idx_source_books_workspace_title_author" in business_indexes_sql
    assert "CREATE UNIQUE INDEX IF NOT EXISTS idx_chapter_plans_project_index" in business_indexes_sql
    assert "CREATE INDEX IF NOT EXISTS idx_source_scenes_chapter_index" in business_indexes_sql
    assert "CREATE INDEX IF NOT EXISTS idx_story_events_scene_index" in business_indexes_sql
    assert "CREATE INDEX IF NOT EXISTS idx_relationship_edges_book_relation" in business_indexes_sql

    env = Path(".env.example").read_text()
    assert "NOVEL_FACTORY_POSTGRES_URL=postgresql://novel:novel@localhost:5436/novel_factory" in env
    assert "NOVEL_FACTORY_REDIS_URL=" in env
    assert "NOVEL_FACTORY_MINIO_SECRET_KEY=replace-me" in env
    assert "NOVEL_FACTORY_API_GATEWAY_PORT=8002" in env

    compose = Path("infra/docker-compose.yml").read_text()
    assert 'MINIO_ROOT_PASSWORD: ${NOVEL_FACTORY_MINIO_SECRET_KEY:-replace-me}' in compose
    assert 'test: ["CMD-SHELL", "test -f /tmp/bootstrap-ready"]' in compose
    assert 'condition: service_healthy' in compose
    assert 'dockerfile: apps/core-service/Dockerfile' in compose
    assert 'dockerfile: apps/api-gateway/Dockerfile' in compose
    assert 'dockerfile: apps/ai-worker/Dockerfile' in compose
    assert 'dockerfile: apps/scheduler/Dockerfile' in compose
    assert '${NOVEL_FACTORY_API_GATEWAY_PORT:-8002}:8000' in compose


def test_snapshot_persistence_round_trip(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    payload = {"hello": "world", "count": 2}
    save_snapshot(payload, snapshot_key="test-round-trip")
    assert load_snapshot(snapshot_key="test-round-trip") == payload
