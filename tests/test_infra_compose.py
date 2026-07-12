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
    assert "CREATE EXTENSION IF NOT EXISTS vector;" in sql

    env = Path(".env.example").read_text()
    assert "NOVEL_FACTORY_POSTGRES_URL=postgresql://novel:novel@localhost:5436/novel_factory" in env
    assert "NOVEL_FACTORY_REDIS_URL=" in env
    assert "NOVEL_FACTORY_MINIO_SECRET_KEY=replace-me" in env

    compose = Path("infra/docker-compose.yml").read_text()
    assert 'MINIO_ROOT_PASSWORD: ${NOVEL_FACTORY_MINIO_SECRET_KEY:-replace-me}' in compose
    assert 'dockerfile: apps/core-service/Dockerfile' in compose
    assert 'dockerfile: apps/api-gateway/Dockerfile' in compose
    assert 'dockerfile: apps/ai-worker/Dockerfile' in compose
    assert 'dockerfile: apps/scheduler/Dockerfile' in compose


def test_snapshot_persistence_round_trip() -> None:
    payload = {"hello": "world", "count": 2}
    save_snapshot(payload, snapshot_key="test-round-trip")
    assert load_snapshot(snapshot_key="test-round-trip") == payload
