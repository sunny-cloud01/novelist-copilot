from pathlib import Path
import shutil
import subprocess

import pytest


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


def test_pgvector_init_and_env_example_exist() -> None:
    sql = Path("infra/postgres/init/001-enable-extensions.sql").read_text()
    assert "CREATE EXTENSION IF NOT EXISTS vector;" in sql

    env = Path(".env.example").read_text()
    assert "NOVEL_FACTORY_POSTGRES_URL=" in env
    assert "NOVEL_FACTORY_REDIS_URL=" in env
    assert "NOVEL_FACTORY_MINIO_SECRET_KEY=" in env
