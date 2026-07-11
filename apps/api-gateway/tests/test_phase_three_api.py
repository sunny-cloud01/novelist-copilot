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


def test_gateway_create_and_fetch_novel_project() -> None:
    client = make_client()

    create_response = client.post(
        "/v1/novel-projects",
        json={
            "title": "遮天衍生稿",
            "genre_scope": "东方玄幻",
        },
        headers={"x-request-id": "req-gateway-project", "x-trace-id": "trace-gateway-project"},
    )

    assert create_response.status_code == 202
    payload = create_response.json()
    project_id = payload["data"]["project"]["project_id"]
    assert payload["data"]["story_bible"]["trace_id"] == "trace-gateway-project"
    assert payload["meta"] == {
        "request_id": "req-gateway-project",
        "trace_id": "trace-gateway-project",
        "workspace_id": "demo-workspace",
        "actor_id": "demo-user",
        "actor_role": "owner",
    }

    detail_response = client.get(f"/v1/novel-projects/{project_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["data"]["project"]["title"] == "遮天衍生稿"


def test_gateway_novel_project_requires_editor_or_owner() -> None:
    client = make_client()

    response = client.post(
        "/v1/novel-projects",
        json={"title": "遮天衍生稿", "genre_scope": "东方玄幻"},
        headers={"x-actor-role": "viewer", "x-actor-id": "viewer-user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "forbidden"


def test_gateway_seed_project_and_planning_flow() -> None:
    client = make_client()

    project_response = client.get("/v1/novel-projects/01JZPROJECT000000000000001")
    chapter_response = client.get("/v1/chapter-plans/01JZCHPLAN000000000000001")
    sections_response = client.get("/v1/chapter-plans/01JZCHPLAN000000000000001/section-plans")

    assert project_response.status_code == 200
    assert project_response.json()["data"]["story_bible"]["status"] == "approved"
    assert chapter_response.status_code == 200
    assert chapter_response.json()["data"]["task"]["task_type"] == "create_chapter_plan"
    assert sections_response.status_code == 200
    assert len(sections_response.json()["data"]["items"]) == 3


def test_gateway_create_chapter_plan_and_sections() -> None:
    client = make_client()

    create_plan = client.post(
        "/v1/chapter-plans",
        json={
            "project_id": "01JZPROJECT000000000000001",
            "chapter_index": 3,
            "target_word_count": 4200,
        },
        headers={"x-trace-id": "trace-gateway-plan"},
    )

    assert create_plan.status_code == 202
    payload = create_plan.json()["data"]
    chapter_plan_id = payload["chapter_plan"]["chapter_plan_id"]
    assert payload["task"]["status"] == "queued"
    assert payload["chapter_plan"]["trace_id"] == "trace-gateway-plan"

    create_sections = client.post(
        f"/v1/chapter-plans/{chapter_plan_id}/section-plans",
        json={"section_count": 2},
        headers={"x-trace-id": "trace-gateway-sections"},
    )

    assert create_sections.status_code == 202
    section_payload = create_sections.json()["data"]
    assert len(section_payload["items"]) == 2
    assert section_payload["items"][1]["planning_role"] == "conflict"
    assert section_payload["items"][0]["trace_id"] == "trace-gateway-sections"


def test_gateway_chapter_plan_requires_editor_or_owner() -> None:
    client = make_client()

    response = client.post(
        "/v1/chapter-plans",
        json={"project_id": "01JZPROJECT000000000000001", "chapter_index": 3, "target_word_count": 4200},
        headers={"x-actor-role": "viewer", "x-actor-id": "viewer-user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "forbidden"


def test_gateway_workspace_create_detail_and_home() -> None:
    client = make_client()

    create_response = client.post(
        "/v1/workspaces",
        json={"name": "编辑工作区", "slug": "editor-workspace", "default_language": "zh-CN"},
        headers={"x-request-id": "req-gateway-workspace", "x-trace-id": "trace-gateway-workspace"},
    )
    detail_response = client.get("/v1/workspaces/demo-workspace")
    home_response = client.get("/v1/workspaces/demo-workspace/home")

    assert create_response.status_code == 201
    created = create_response.json()["data"]
    assert created["workspace"]["workspace_id"] == "editor-workspace"
    assert created["workspace_member"]["role"] == "owner"

    assert detail_response.status_code == 200
    detail = detail_response.json()["data"]
    assert detail["workspace"]["workspace_id"] == "demo-workspace"
    assert len(detail["members"]) >= 1

    assert home_response.status_code == 200
    home = home_response.json()["data"]
    assert home["workspace"]["workspace_id"] == "demo-workspace"
    assert len(home["recent_tasks"]) >= 1
    assert len(home["pending_reviews"]) >= 1
    assert any(item["route"] == "/configuration" for item in home["quick_links"])
def test_gateway_project_and_planning_missing_resources_return_not_found() -> None:
    client = make_client()

    assert client.get("/v1/novel-projects/missing").status_code == 404
    assert client.get("/v1/workspaces/missing").status_code == 404
    assert client.get("/v1/workspaces/missing/home").status_code == 404
    assert client.get("/v1/chapter-plans/missing").status_code == 404
    assert client.get("/v1/chapter-plans/missing/section-plans").status_code == 404
    assert client.post("/v1/chapter-plans/missing/section-plans", json={"section_count": 1}).status_code == 404
