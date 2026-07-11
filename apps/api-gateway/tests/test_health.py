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


def test_gateway_health_uses_api_envelope() -> None:
    client = TestClient(load_app())
    response = client.get("/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"] == {"service": "api-gateway", "status": "ok"}
    assert payload["errors"] == []
    assert payload["meta"]["request_id"]
    assert payload["meta"]["trace_id"]
    assert response.headers["x-request-id"] == payload["meta"]["request_id"]
    assert response.headers["x-trace-id"] == payload["meta"]["trace_id"]
