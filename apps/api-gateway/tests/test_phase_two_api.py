import importlib
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]


def load_app():
    for name in list(sys.modules):
        if name == "app" or name.startswith("app.") or name == "phase_two_store_gateway":
            sys.modules.pop(name)
    sys.path.insert(0, str(ROOT))
    try:
        adapter = importlib.import_module("app.core.phase_two_adapter")
        adapter._STORE.reset_store()
        adapter._STORE.seed_phase_two_demo_data()
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
        "workspace_id": "demo-workspace",
        "actor_id": "demo-user",
        "actor_role": "owner",
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


def test_gateway_graph_node_detail_and_neighbors() -> None:
    client = make_client()

    node_response = client.get("/v1/graph/nodes/01JZNODE000000000000000001")
    neighbors_response = client.get("/v1/graph/nodes/01JZNODE000000000000000001/neighbors")

    assert node_response.status_code == 200
    node_payload = node_response.json()["data"]
    assert node_payload["canonical_object_id"] == "01JZOBJ0000000000000000001"
    assert node_payload["summary"] == "乌坦城萧家少年，正处于天赋跌落后的低谷期。"
    assert neighbors_response.status_code == 200
    neighbor_payload = neighbors_response.json()["data"]
    assert neighbor_payload["node_id"] == "01JZNODE000000000000000001"
    assert len(neighbor_payload["items"]) == 2
    assert neighbor_payload["items"][1]["neighbor_label"] == "Xiao Clan"


def test_gateway_request_reextract_requeues_run() -> None:
    client = make_client()

    response = client.post(
        "/v1/knowledge-objects/01JZOBJ0000000000000000001/review-actions",
        json={"action": "request_reextract"},
    )
    report_response = client.get("/v1/extraction-runs/01JZRUN0000000000000000001/report")

    assert response.status_code == 200
    assert response.json()["data"]["review_status"] == "reextract_requested"
    payload = report_response.json()["data"]
    assert payload["run"]["status"] == "queued"
    assert payload["run"]["current_stage"] == "source_submission"
    assert payload["run"]["low_confidence_count"] == 1
    assert payload["task"]["status"] == "queued"


def test_gateway_review_action_requires_editor_or_owner() -> None:
    client = make_client()

    response = client.post(
        "/v1/knowledge-objects/01JZOBJ0000000000000000001/review-actions",
        json={"action": "approve"},
        headers={"x-actor-role": "viewer", "x-actor-id": "viewer-user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "forbidden"


def test_gateway_extraction_run_requires_editor_or_owner() -> None:
    client = make_client()

    response = client.post(
        "/v1/extraction-runs",
        json={"book_id": "01JZBOOK000000000000000001"},
        headers={"x-actor-role": "viewer", "x-actor-id": "viewer-user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "forbidden"


def test_gateway_graph_missing_resources_return_not_found() -> None:
    client = make_client()

    assert client.get("/v1/graph/nodes/missing").status_code == 404
    assert client.get("/v1/graph/nodes/missing/neighbors").status_code == 404


