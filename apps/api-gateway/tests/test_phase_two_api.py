import importlib
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]


def load_app():
    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            sys.modules.pop(name)
    sys.path.insert(0, str(ROOT))
    try:
        return importlib.import_module("app.main").app
    finally:
        sys.path.pop(0)


def make_client() -> TestClient:
    return TestClient(load_app())


def test_create_book_returns_gateway_envelope() -> None:
    client = make_client()

    response = client.post(
        "/v1/books",
        json={
            "title": "Coiling Dragon",
            "author_name": "I Eat Tomatoes",
            "source_type": "reference_novel",
        },
        headers={"x-request-id": "req-gateway-book", "x-trace-id": "trace-gateway-book"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["data"]["title"] == "Coiling Dragon"
    assert payload["data"]["trace_id"] == "trace-gateway-book"
    assert payload["meta"] == {
        "request_id": "req-gateway-book",
        "trace_id": "trace-gateway-book",
    }


def test_gateway_exposes_seed_book_and_chapters() -> None:
    client = make_client()

    book_response = client.get("/v1/books/01JZBOOK000000000000000001")
    chapters_response = client.get("/v1/books/01JZBOOK000000000000000001/chapters")

    assert book_response.status_code == 200
    assert book_response.json()["data"]["title"] == "Battle Through the Heavens"
    assert chapters_response.status_code == 200
    assert len(chapters_response.json()["data"]["items"]) == 2


def test_gateway_extraction_report_and_review_flow() -> None:
    client = make_client()

    create_response = client.post("/v1/extraction-runs", json={"book_id": "01JZBOOK000000000000000001"})
    report_response = client.get("/v1/extraction-runs/01JZRUN0000000000000000001/report")
    review_response = client.post(
        "/v1/knowledge-objects/01JZOBJ0000000000000000001/review-actions",
        json={"action": "approve"},
    )
    commit_response = client.post("/v1/extraction-runs/01JZRUN0000000000000000001/commit")
    graph_response = client.get("/v1/graph/summary")

    assert create_response.status_code == 202
    assert create_response.json()["data"]["task"]["task_type"] == "extract_knowledge"
    assert report_response.status_code == 200
    assert report_response.json()["data"]["run"]["low_confidence_count"] == 2
    assert review_response.status_code == 200
    assert review_response.json()["data"]["review_status"] == "approved"
    assert commit_response.status_code == 200
    assert commit_response.json()["data"]["status"] == "succeeded"
    assert graph_response.status_code == 200
    assert graph_response.json()["data"]["node_count"] == 3


def test_gateway_missing_resources_return_not_found() -> None:
    client = make_client()

    assert client.get("/v1/books/missing").status_code == 404
    assert client.get("/v1/extraction-runs/missing").status_code == 404
    assert client.post(
        "/v1/knowledge-objects/missing/review-actions",
        json={"action": "approve"},
    ).status_code == 404
