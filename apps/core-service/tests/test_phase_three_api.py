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


def test_create_and_fetch_novel_project() -> None:
    client = make_client()

    create_response = client.post(
        "/v1/novel-projects",
        json={
            "title": "凡人修仙同人",
            "genre_scope": "仙侠成长流",
            "allowed_knowledge_source_refs": ["object://source-books/01JZBOOK000000000000000001"],
        },
        headers={"x-request-id": "req-project", "x-trace-id": "trace-project"},
    )

    assert create_response.status_code == 202
    payload = create_response.json()
    assert payload["data"]["project"]["title"] == "凡人修仙同人"
    assert payload["data"]["story_bible"]["trace_id"] == "trace-project"
    assert payload["meta"] == {
        "request_id": "req-project",
        "trace_id": "trace-project",
        "workspace_id": "demo-workspace",
        "actor_id": "demo-user",
        "actor_role": "owner",
    }

    project_id = payload["data"]["project"]["project_id"]
    detail_response = client.get(f"/v1/novel-projects/{project_id}")

    assert detail_response.status_code == 200
    detail = detail_response.json()["data"]
    assert detail["project"]["project_id"] == project_id
    assert detail["story_bible"]["project_id"] == project_id
    assert detail["chapter_plans"] == []


def test_novel_project_requires_editor_or_owner() -> None:
    client = make_client()

    response = client.post(
        "/v1/novel-projects",
        json={"title": "凡人修仙同人", "genre_scope": "仙侠成长流"},
        headers={"x-actor-role": "viewer", "x-actor-id": "viewer-user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "forbidden"


def test_get_seed_project_detail() -> None:
    client = make_client()

    response = client.get("/v1/novel-projects/01JZPROJECT000000000000001")

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["project"]["status"] == "planning"
    assert payload["story_bible"]["status"] == "approved"
    assert payload["chapter_plans"][0]["chapter_index"] == 1


def test_create_and_fetch_chapter_plan_and_section_plans() -> None:
    client = make_client()

    create_plan = client.post(
        "/v1/chapter-plans",
        json={
            "project_id": "01JZPROJECT000000000000001",
            "chapter_index": 2,
            "target_word_count": 3600,
            "payload": {"title": "新章规划"},
        },
        headers={"x-trace-id": "trace-plan"},
    )

    assert create_plan.status_code == 202
    created_plan = create_plan.json()["data"]
    assert created_plan["chapter_plan"]["status"] == "queued"
    assert created_plan["chapter_plan"]["trace_id"] == "trace-plan"
    assert created_plan["chapter_plan"]["input_refs"] == ["object://novel-projects/01JZPROJECT000000000000001"]
    assert created_plan["task"]["task_type"] == "create_chapter_plan"

    chapter_plan_id = created_plan["chapter_plan"]["chapter_plan_id"]
    detail_response = client.get(f"/v1/chapter-plans/{chapter_plan_id}")
    list_sections = client.get(f"/v1/chapter-plans/{chapter_plan_id}/section-plans")
    create_sections = client.post(
        f"/v1/chapter-plans/{chapter_plan_id}/section-plans",
        json={"section_count": 4},
        headers={"x-trace-id": "trace-sections"},
    )

    assert detail_response.status_code == 200
    assert detail_response.json()["data"]["chapter_plan"]["chapter_index"] == 2
    assert list_sections.status_code == 200
    assert list_sections.json()["data"]["items"] == []
    assert create_sections.status_code == 202
    section_payload = create_sections.json()["data"]
    assert len(section_payload["items"]) == 4
    assert section_payload["items"][0]["planning_role"] == "setup"
    assert section_payload["items"][0]["trace_id"] == "trace-sections"
    assert section_payload["task"]["status"] == "succeeded"


def test_chapter_plan_requires_editor_or_owner() -> None:
    client = make_client()

    response = client.post(
        "/v1/chapter-plans",
        json={"project_id": "01JZPROJECT000000000000001", "chapter_index": 2, "target_word_count": 3600},
        headers={"x-actor-role": "viewer", "x-actor-id": "viewer-user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "forbidden"


def test_seed_chapter_plan_lists_seed_sections() -> None:
    client = make_client()

    chapter_response = client.get("/v1/chapter-plans/01JZCHPLAN000000000000001")
    sections_response = client.get("/v1/chapter-plans/01JZCHPLAN000000000000001/section-plans")

    assert chapter_response.status_code == 200
    assert chapter_response.json()["data"]["chapter_plan"]["status"] == "requires_review"
    assert chapter_response.json()["data"]["section_plan_count"] == 3
    assert sections_response.status_code == 200
    assert len(sections_response.json()["data"]["items"]) == 3
    assert sections_response.json()["data"]["items"][0]["payload"]["beats"][0]["summary"] == "主角出场"


def test_workspace_create_detail_and_home() -> None:
    client = make_client()

    create_response = client.post(
        "/v1/workspaces",
        json={"name": "编辑工作区", "slug": "editor-workspace", "default_language": "zh-CN"},
        headers={"x-request-id": "req-workspace", "x-trace-id": "trace-workspace"},
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
def test_project_and_planning_missing_resources_return_not_found() -> None:
    client = make_client()

    assert client.get("/v1/novel-projects/missing").status_code == 404
    assert client.get("/v1/workspaces/missing").status_code == 404
    assert client.get("/v1/workspaces/missing/home").status_code == 404
    assert client.post(
        "/v1/chapter-plans",
        json={"project_id": "missing", "chapter_index": 1, "target_word_count": 3000},
    ).status_code == 404
    assert client.get("/v1/chapter-plans/missing").status_code == 404
    assert client.get("/v1/chapter-plans/missing/section-plans").status_code == 404
    assert client.post("/v1/chapter-plans/missing/section-plans", json={"section_count": 2}).status_code == 404
