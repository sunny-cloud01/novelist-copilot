import importlib
import sys
from pathlib import Path

from fastapi.testclient import TestClient


def load_app():
    root = Path(__file__).resolve().parents[1]
    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            sys.modules.pop(name)
    sys.path.insert(0, str(root))
    try:
        return importlib.import_module("app.main").app
    finally:
        sys.path.pop(0)


def test_core_service_health_uses_api_envelope() -> None:
    client = TestClient(load_app())
    response = client.get("/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["service"] == "core-service"
    assert payload["data"]["status"] == "ok"
    assert payload["data"]["runtime"]["postgres_url"].startswith("postgresql://")
    assert payload["data"]["runtime"]["redis_url"].startswith("redis://")
    assert payload["data"]["runtime"]["minio_bucket"] == "novel-factory-dev"
    assert payload["errors"] == []
    assert payload["meta"]["request_id"]
    assert payload["meta"]["trace_id"]
    assert payload["meta"]["workspace_id"] == "demo-workspace"
    assert payload["meta"]["actor_id"] == "demo-user"
    assert payload["meta"]["actor_role"] == "owner"
    assert response.headers["x-request-id"] == payload["meta"]["request_id"]
    assert response.headers["x-trace-id"] == payload["meta"]["trace_id"]
    assert response.headers["x-workspace-id"] == payload["meta"]["workspace_id"]
    assert response.headers["x-actor-id"] == payload["meta"]["actor_id"]
    assert response.headers["x-actor-role"] == payload["meta"]["actor_role"]
