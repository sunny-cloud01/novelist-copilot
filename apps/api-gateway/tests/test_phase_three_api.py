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
    detail = detail_response.json()["data"]
    assert detail["project"]["title"] == "遮天衍生稿"
    assert len(detail["patterns"]) >= 1
    assert len(detail["rhythm_profiles"]) >= 1
    assert len(detail["assets"]) >= 1


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
    project_payload = project_response.json()["data"]
    assert project_payload["story_bible"]["status"] == "approved"
    assert project_payload["patterns"][0]["pattern_id"] == "01JZPATTERN00000000000001"
    assert chapter_response.status_code == 200
    chapter_payload = chapter_response.json()["data"]
    assert chapter_payload["task"]["task_type"] == "create_chapter_plan"
    assert chapter_payload["rhythm_profile_options"][0]["rhythm_profile_id"] == "01JZRHYTHM00000000000001"
    assert sections_response.status_code == 200
    sections_payload = sections_response.json()["data"]
    assert len(sections_payload["items"]) == 3
    assert sections_payload["asset_options"][0]["asset_id"] == "01JZASSET000000000000001"


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
    assert section_payload["pattern_options"][0]["canonical_name"] == "退婚立誓"
    assert section_payload["asset_options"][0]["canonical_name"] == "三年之约宣言模板"


def test_gateway_chapter_plan_requires_editor_or_owner() -> None:
    client = make_client()

    response = client.post(
        "/v1/chapter-plans",
        json={"project_id": "01JZPROJECT000000000000001", "chapter_index": 3, "target_word_count": 4200},
        headers={"x-actor-role": "viewer", "x-actor-id": "viewer-user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "forbidden"




def test_gateway_pattern_rhythm_asset_routes() -> None:
    client = make_client()

    pattern_list = client.get("/v1/patterns")
    pattern_detail = client.get("/v1/patterns/01JZPATTERN00000000000001")
    rhythm_list = client.get("/v1/rhythm-profiles", params={"targetId": "01JZCHPLAN000000000000001"})
    rhythm_detail = client.get("/v1/rhythm-profiles/01JZRHYTHM00000000000001")
    asset_list = client.get("/v1/assets")
    asset_detail = client.get("/v1/assets/01JZASSET000000000000001")

    assert pattern_list.status_code == 200
    assert pattern_list.json()["data"]["items"][0]["canonical_name"] == "退婚立誓"
    assert pattern_detail.status_code == 200
    assert pattern_detail.json()["data"]["compatible_rhythm_profile_id"] == "01JZRHYTHM00000000000001"
    assert rhythm_list.status_code == 200
    assert rhythm_list.json()["data"]["items"][0]["label"] == "退婚压迫三段式"
    assert rhythm_detail.status_code == 200
    assert rhythm_detail.json()["data"]["target_id"] == "01JZCHPLAN000000000000001"
    assert asset_list.status_code == 200
    assert asset_list.json()["data"]["items"][0]["canonical_name"] == "三年之约宣言模板"
    assert asset_detail.status_code == 200
    assert asset_detail.json()["data"]["quality_score"] == 0.88


def test_gateway_create_pattern_rhythm_and_asset() -> None:
    client = make_client()

    pattern_response = client.post(
        "/v1/patterns",
        json={
            "canonical_name": "压迫后逆袭",
            "pattern_type": "conflict_escalation",
            "intent": "先压后扬。",
            "preconditions": ["主角失势"],
            "steps": [{"index": 1, "summary": "压低主角处境"}],
            "slots": ["压迫者"],
            "expected_reader_effect": "形成反弹期待。",
            "evidence_refs": ["evidence://demo-pattern"],
        },
        headers={"x-request-id": "req-pattern", "x-trace-id": "trace-pattern"},
    )
    rhythm_response = client.post(
        "/v1/rhythm-profiles",
        json={
            "target_id": "01JZCHPLAN000000000000001",
            "label": "高压三拍",
            "climax_index": 0.9,
            "conflict_index": 0.8,
            "dialogue_ratio": 0.4,
            "description_ratio": 0.3,
            "battle_ratio": 0.0,
            "information_density": 0.6,
            "suspense_index": 0.7,
            "reward_count": 2,
            "emotion_curve": [{"beat": 1, "intensity": 0.5, "summary": "起压"}],
        },
        headers={"x-request-id": "req-rhythm", "x-trace-id": "trace-rhythm"},
    )
    asset_response = client.post(
        "/v1/assets",
        json={
            "asset_type": "expression",
            "canonical_name": "短誓句式",
            "content_summary": "短句誓言模板。",
            "style_tags": ["克制"],
            "genre_scope": "玄幻升级流",
            "usage_context": "公开反击",
            "constraints": ["不超过两行"],
            "expression_type_refs": ["expression://oath-line"],
            "source_refs": ["object://source-books/01JZBOOK000000000000000001"],
            "evidence_refs": ["evidence://demo-asset"],
            "quality_score": 0.9,
        },
        headers={"x-request-id": "req-asset", "x-trace-id": "trace-asset"},
    )

    assert pattern_response.status_code == 201
    assert pattern_response.json()["data"]["trace_id"] == "trace-pattern"
    assert rhythm_response.status_code == 201
    assert rhythm_response.json()["data"]["target_id"] == "01JZCHPLAN000000000000001"
    assert asset_response.status_code == 201
    assert asset_response.json()["data"]["canonical_name"] == "短誓句式"


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
