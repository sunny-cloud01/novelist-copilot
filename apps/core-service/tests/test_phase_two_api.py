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


def test_create_book_returns_enveloped_book() -> None:
    client = make_client()

    response = client.post(
        "/v1/books",
        json={
            "title": "Coiling Dragon",
            "author_name": "I Eat Tomatoes",
            "source_type": "reference_novel",
        },
        headers={"x-request-id": "req-books", "x-trace-id": "trace-books"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["data"]["title"] == "Coiling Dragon"
    assert payload["data"]["author_name"] == "I Eat Tomatoes"
    assert payload["data"]["source_type"] == "reference_novel"
    assert payload["data"]["import_status"] == "uploaded"
    assert payload["meta"] == {
        "request_id": "req-books",
        "trace_id": "trace-books",
        "workspace_id": "demo-workspace",
        "actor_id": "demo-user",
        "actor_role": "owner",
    }


def test_get_seed_book_and_chapters() -> None:
    client = make_client()

    book_response = client.get("/v1/books/01JZBOOK000000000000000001")
    chapters_response = client.get("/v1/books/01JZBOOK000000000000000001/chapters")

    assert book_response.status_code == 200
    assert book_response.json()["data"]["title"] == "Battle Through the Heavens"
    assert chapters_response.status_code == 200
    assert len(chapters_response.json()["data"]["items"]) == 2
    assert chapters_response.json()["data"]["items"][0]["chapter_index"] == 1


def test_create_and_fetch_extraction_run() -> None:
    client = make_client()

    create_response = client.post(
        "/v1/extraction-runs",
        json={"book_id": "01JZBOOK000000000000000001"},
        headers={"x-trace-id": "trace-run"},
    )

    assert create_response.status_code == 202
    created = create_response.json()["data"]
    assert created["status"] == "requires_review"
    assert created["task"]["task_type"] == "extract_knowledge"

    detail_response = client.get(f"/v1/extraction-runs/{created['run_id']}")
    assert detail_response.status_code == 200
    assert detail_response.json()["data"]["current_stage"] == "quality_review"


def test_extraction_report_lists_low_confidence_items() -> None:
    client = make_client()

    response = client.get("/v1/extraction-runs/01JZRUN0000000000000000001/report")

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["run"]["low_confidence_count"] == 2
    assert len(payload["low_confidence_items"]) == 2
    assert payload["low_confidence_items"][0]["review_status"] == "pending"


def test_review_action_updates_object_and_run() -> None:
    client = make_client()

    approve_one = client.post(
        "/v1/knowledge-objects/01JZOBJ0000000000000000001/review-actions",
        json={"action": "approve"},
    )
    approve_two = client.post(
        "/v1/knowledge-objects/01JZOBJ0000000000000000002/review-actions",
        json={"action": "approve"},
    )
    report_response = client.get("/v1/extraction-runs/01JZRUN0000000000000000001/report")

    assert approve_one.status_code == 200
    assert approve_two.status_code == 200
    assert approve_two.json()["data"]["review_status"] == "approved"
    assert report_response.json()["data"]["run"]["status"] == "succeeded"
    assert report_response.json()["data"]["run"]["low_confidence_count"] == 0


def test_review_action_requires_editor_or_owner() -> None:
    client = make_client()

    response = client.post(
        "/v1/knowledge-objects/01JZOBJ0000000000000000001/review-actions",
        json={"action": "approve"},
        headers={"x-actor-role": "viewer", "x-actor-id": "viewer-user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "forbidden"


def test_extraction_run_requires_editor_or_owner() -> None:
    client = make_client()

    response = client.post(
        "/v1/extraction-runs",
        json={"book_id": "01JZBOOK000000000000000001"},
        headers={"x-actor-role": "viewer", "x-actor-id": "viewer-user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "forbidden"


def test_review_action_writes_audit_event() -> None:
    client = make_client()

    client.post(
        "/v1/knowledge-objects/01JZOBJ0000000000000000001/review-actions",
        json={"action": "approve"},
        headers={"x-request-id": "req-audit-review", "x-trace-id": "trace-audit-review"},
    )
    audit_response = client.get("/v1/audit-events")

    assert audit_response.status_code == 200
    items = audit_response.json()["data"]["items"]
    assert any(item["action"] == "knowledge.approve" and item["request_id"] == "req-audit-review" for item in items)


def test_missing_resources_return_not_found() -> None:
    client = make_client()

    assert client.get("/v1/books/missing").status_code == 404
    assert client.get("/v1/extraction-runs/missing").status_code == 404
    assert client.post(
        "/v1/knowledge-objects/missing/review-actions",
        json={"action": "approve"},
    ).status_code == 404
