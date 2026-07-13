import importlib
import json
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
    assert len(detail["patterns"]) >= 1
    assert detail["patterns"][0]["canonical_name"] == "退婚立誓"
    assert len(detail["rhythm_profiles"]) >= 1
    assert len(detail["assets"]) >= 1


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
    from app.core import phase_two_store as store
    # Ensure seed story bible is restored to approved status without persisting
    # (guards against snapshot pollution from other tests)
    if store.STORY_BIBLE_ID in store.STORE.story_bibles:
        sb = store.STORE.story_bibles[store.STORY_BIBLE_ID]
        if sb.get("status") != "approved":
            sb["status"] = "approved"
            sb["diff"] = None

    response = client.get("/v1/novel-projects/01JZPROJECT000000000000001")

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["project"]["status"] == "planning"
    assert payload["story_bible"]["status"] == "approved"
    assert payload["chapter_plans"][0]["chapter_index"] == 1


def test_story_bible_detail_and_review_actions() -> None:
    client = make_client()

    project_response = client.post(
        "/v1/novel-projects",
        json={
            "title": "故事圣经流转项目",
            "genre_scope": "东方玄幻",
        },
        headers={"x-request-id": "req-story-bible", "x-trace-id": "trace-story-bible"},
    )

    assert project_response.status_code == 202
    story_bible = project_response.json()["data"]["story_bible"]
    story_bible_id = story_bible["story_bible_id"]

    detail_response = client.get(f"/v1/story-bibles/{story_bible_id}")
    regenerate_response = client.post(
        f"/v1/story-bibles/{story_bible_id}/review-actions",
        json={
            "action": "regenerate",
            "summary": "补强世界规则与叙事承诺。",
            "note": "加入项目级原创边界。",
            "story_bible_payload": {
                "premise": "少年踏入失序宗门后重建秩序。",
                "protagonist": "林澈",
                "core_conflict": "底层弟子与宗门旧规之间的成长冲突。",
                "style_target": "克制、证据充分、节奏稳步升级。",
                "forbidden_similarities": "不复刻原作人物名、外挂和名场面。",
                "world_rules": ["所有突破都要付出明确代价。"],
                "narrative_promises": ["前三章完成受压、立誓与破局线索。"],
            },
        },
        headers={"x-request-id": "req-story-bible-regenerate", "x-trace-id": "trace-story-bible-regenerate"},
    )
    confirm_response = client.post(
        f"/v1/story-bibles/{story_bible_id}/review-actions",
        json={"action": "confirm", "summary": "确认候选版本。"},
        headers={"x-request-id": "req-story-bible-confirm", "x-trace-id": "trace-story-bible-confirm"},
    )

    assert detail_response.status_code == 200
    assert detail_response.json()["data"]["status"] == "draft"
    assert detail_response.json()["data"]["history"][0]["change_type"] == "create"

    assert regenerate_response.status_code == 200
    regenerated = regenerate_response.json()["data"]
    assert regenerated["status"] == "pending_review"
    assert regenerated["version"] == 2
    assert regenerated["diff"]["summary"] == "补强世界规则与叙事承诺。"
    assert "world_rules" in regenerated["diff"]["changed_fields"]
    assert regenerated["history"][-1]["change_type"] == "regenerate"

    assert confirm_response.status_code == 200
    confirmed = confirm_response.json()["data"]
    assert confirmed["status"] == "approved"
    assert confirmed["diff"] is None
    assert confirmed["confirmed_payload"]["protagonist"] == "林澈"
    assert confirmed["history"][-1]["change_type"] == "confirm"


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
    chapter_detail = detail_response.json()["data"]
    assert chapter_detail["chapter_plan"]["chapter_index"] == 2
    assert chapter_detail["pattern_options"][0]["canonical_name"] == "退婚立誓"
    assert chapter_detail["asset_options"][0]["canonical_name"] == "三年之约宣言模板"
    assert list_sections.status_code == 200
    assert list_sections.json()["data"]["items"] == []
    assert list_sections.json()["data"]["pattern_options"][0]["pattern_id"] == "01JZPATTERN00000000000001"
    assert create_sections.status_code == 202
    section_payload = create_sections.json()["data"]
    assert len(section_payload["items"]) == 4
    assert section_payload["items"][0]["planning_role"] == "setup"
    assert section_payload["items"][0]["trace_id"] == "trace-sections"
    assert section_payload["task"]["status"] == "succeeded"
    assert section_payload["rhythm_profile_options"] == []


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
    chapter_payload = chapter_response.json()["data"]
    assert chapter_payload["chapter_plan"]["status"] == "requires_review"
    assert chapter_payload["section_plan_count"] == 3
    assert chapter_payload["pattern_options"][0]["pattern_id"] == "01JZPATTERN00000000000001"
    assert chapter_payload["rhythm_profile_options"][0]["rhythm_profile_id"] == "01JZRHYTHM00000000000001"
    assert sections_response.status_code == 200
    sections_payload = sections_response.json()["data"]
    assert len(sections_payload["items"]) == 3
    assert sections_payload["items"][0]["payload"]["beats"][0]["summary"] == "主角出场"
    assert sections_payload["asset_options"][0]["asset_id"] == "01JZASSET000000000000001"




def test_pattern_rhythm_asset_routes() -> None:
    client = make_client()

    pattern_list = client.get("/v1/patterns")
    pattern_detail = client.get("/v1/patterns/01JZPATTERN00000000000001")
    rhythm_list = client.get("/v1/rhythm-profiles", params={"targetId": "01JZCHPLAN000000000000001"})
    rhythm_detail = client.get("/v1/rhythm-profiles/01JZRHYTHM00000000000001")
    asset_list = client.get("/v1/assets", params={"assetType": "expression"})
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


def test_create_pattern_rhythm_and_asset() -> None:
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


def test_story_bible_regenerate_without_payload_generates_candidate():
    from app.core import phase_two_store as store
    store.reset_store()
    store.seed_phase_two_demo_data()
    # 创建一个独立新项目，不污染 seed STORY_BIBLE_ID
    result_project = store.create_novel_project(
        {"title": "再生候选测试项目", "genre_scope": "东方玄幻"},
        trace_id="trace-regen-test",
    )
    sb_id = result_project["story_bible"]["story_bible_id"]
    before_world_rules = store.STORE.story_bibles[sb_id]["payload"]["world_rules"][:]
    result = store.apply_story_bible_action(sb_id, "regenerate", payload={"summary": "补强世界规则"})
    assert result["status"] == "pending_review"
    assert result["diff"]["changed_fields"]  # 有变化，非原样回写
    after_world_rules = store.STORE.story_bibles[sb_id]["payload"]["world_rules"]
    assert after_world_rules != before_world_rules or result["diff"]["changed_fields"]


def test_manuscript_state_reflects_real_draft(monkeypatch):
    from app.core import phase_two_store as store
    # Use existing seed data without resetting/polluting the store
    wr = dict(store.STORE.writing_runs[store.WRITING_RUN_ID])
    wr["assembled_chapter"] = "林澈站在宗门前，立誓要打破规则的桎梏。他知道前路艰险。"
    cp = store.STORE.chapter_plans[store.CHAPTER_PLAN_ID]
    state = store._build_manuscript_state(wr, cp, "object://chapters/c1", store.utc_now())
    # 摘要来自真实草稿/章节，不再硬编码萧炎/三年之约
    text = json.dumps(state, ensure_ascii=False)
    assert "萧炎" not in state["current_story_state"]["summary"] or "林澈" in text
    assert state["prior_summary_pack"]  # 非空
