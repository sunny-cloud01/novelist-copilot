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
        store = importlib.import_module("app.core.phase_two_store")
        store.reset_store()
        store.seed_phase_two_demo_data()
        return importlib.import_module("app.main").app
    finally:
        sys.path.pop(0)


def make_client() -> TestClient:
    return TestClient(load_app())


def test_create_book_with_source_text_persists_content_and_chapters() -> None:
    client = make_client()
    source_text = "第一章 山边小村\n韩立站在村口，看见远山雾气。\n第二章 入门试炼\n少年踏上青石阶。"

    response = client.post(
        "/v1/books",
        json={
            "title": "凡人修仙传",
            "author_name": "忘语",
            "source_type": "reference_novel",
            "platform": "起点中文网",
            "genre": "仙侠成长流",
            "usage_boundary": "仅供结构学习，不直接复写原文。",
            "source_text": source_text,
        },
        headers={"x-request-id": "req-source-text", "x-trace-id": "trace-source-text"},
    )

    assert response.status_code == 201
    book = response.json()["data"]
    assert book["title"] == "凡人修仙传"
    assert book["source_content_ref"].startswith("object://source-contents/")
    assert book["content_checksum"].startswith("sha256:")
    assert book["content_byte_size"] == len(source_text.encode("utf-8"))
    assert book["chapter_count"] == 2

    chapters_response = client.get(f"/v1/books/{book['book_id']}/chapters")
    content_response = client.get(f"/v1/books/{book['book_id']}/content")
    evidence_response = client.get(f"/v1/books/{book['book_id']}/evidence")
    analysis_response = client.get(f"/v1/books/{book['book_id']}/analysis")

    assert chapters_response.status_code == 200
    chapters = chapters_response.json()["data"]["items"]
    assert len(chapters) == 2
    assert chapters[0]["raw_text"].startswith("第一章 山边小村")
    assert chapters[0]["text_object_ref"].startswith("object://source-chapters/")
    assert content_response.status_code == 200
    assert content_response.json()["data"]["content"] == source_text
    assert evidence_response.status_code == 200
    assert evidence_response.json()["data"]["items"] == []
    assert analysis_response.status_code == 200
    analysis = analysis_response.json()["data"]
    assert analysis["book"]["title"] == "凡人修仙传"
    assert analysis["summary"]["book_id"] == book["book_id"]
    assert analysis["chapters"][0]["raw_text"].startswith("第一章 山边小村")


def test_source_text_extraction_result_populates_analysis_evidence() -> None:
    from app.core import phase_two_store as store

    store.reset_store()
    store.seed_phase_two_demo_data()
    source_text = "第一章 山边小村\n韩立站在村口，看见远山雾气。\n第二章 入门试炼\n少年踏上青石阶。"
    created = store.create_book(
        {
            "title": "凡人修仙传",
            "author_name": "忘语",
            "source_type": "reference_novel",
            "source_text": source_text,
        },
        trace_id="trace-analysis-evidence",
    )
    run = store.create_extraction_run(created["book_id"], trace_id="trace-analysis-evidence")
    dispatched = store.mark_task_dispatched(run["task"]["task_id"], trace_id="trace-analysis-evidence")
    evidence_id = "01JZUPLOADEDEVIDENCE000001"
    evidence_ref = f"evidence://{evidence_id}"
    knowledge_object = {
        "schema_version": 1,
        "object_id": "01JZUPLOADEDOBJ000000001",
        "workspace_id": created["workspace_id"],
        "object_type": "character",
        "canonical_name": "韩立",
        "lifecycle_status": "candidate",
        "review_status": "pending",
        "confidence": 0.67,
        "evidence_refs": [evidence_ref],
        "input_refs": [f"object://source-books/{created['book_id']}"],
        "output_refs": ["object://knowledge-objects/01JZUPLOADEDOBJ000000001"],
        "payload": {"schema_version": 1, "aliases": []},
    }
    evidence = {
        "schema_version": 1,
        "evidence_id": evidence_id,
        "evidence_ref": evidence_ref,
        "book_id": created["book_id"],
        "chapter_id": store.list_book_chapters(created["book_id"])[0]["chapter_id"],
        "chapter_index": 1,
        "text_range": "c1:p1-p2",
        "excerpt": "韩立站在村口，看见远山雾气。",
        "source_object_refs": ["object://knowledge-objects/01JZUPLOADEDOBJ000000001"],
        "source_content_ref": created["source_content_ref"],
        "confidence": 0.84,
        "trace_id": "trace-analysis-evidence",
    }
    store.apply_task_execution_result(
        run["task"]["task_id"],
        "requires_review",
        [run["knowledge_package_ref"], run["graph_package_ref"], run["extraction_report_ref"], run["quality_report_ref"]],
        {
            "current_stage": "quality_review",
            "chapter_count": 2,
            "scene_count": 2,
            "object_count": 1,
            "evidence_count": 1,
            "low_confidence_count": 1,
            "knowledge_objects": [knowledge_object],
            "evidences": [evidence],
            "graph_summary": {"schema_version": 1, "book_id": created["book_id"], "node_count": 1, "edge_count": 0, "nodes": []},
        },
        trace_id="trace-analysis-evidence",
        dispatch_token=dispatched["current_dispatch_token"],
    )

    analysis = store.get_book_analysis(created["book_id"])

    assert analysis["summary"]["knowledge_object_count"] == 1
    assert analysis["summary"]["needs_attention_count"] == 1
    assert analysis["evidence_samples"][0]["excerpt"] == "韩立站在村口，看见远山雾气。"
    assert analysis["exceptions"][0]["target_ref"] == "object://knowledge-objects/01JZUPLOADEDOBJ000000001"


def test_source_content_and_evidence_missing_resources_return_not_found() -> None:
    client = make_client()

    assert client.get("/v1/books/missing/content").status_code == 404
    assert client.get("/v1/books/missing/evidence").status_code == 404
    assert client.get("/v1/evidence/missing").status_code == 404


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


def test_request_reextract_requeues_run() -> None:
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


def test_graph_search_and_evidence_ref_lookup() -> None:
    client = make_client()

    search_response = client.get("/v1/graph/search?query=Yao&node_type=mentor")
    evidence_response = client.get("/v1/evidence/01JZEVIDENCE0000000000002")

    assert search_response.status_code == 200
    payload = search_response.json()["data"]
    assert payload["count"] == 1
    assert payload["items"][0]["label"] == "Yao Lao"
    assert evidence_response.status_code == 200
    assert evidence_response.json()["data"]["excerpt"].startswith("戒指中传来苍老的低笑")


    client = make_client()

    assert client.get("/v1/books/missing").status_code == 404
    assert client.get("/v1/extraction-runs/missing").status_code == 404
    assert client.get("/v1/graph/nodes/missing").status_code == 404
    assert client.get("/v1/graph/nodes/missing/neighbors").status_code == 404
    assert client.post(
        "/v1/knowledge-objects/missing/review-actions",
        json={"action": "approve"},
    ).status_code == 404


def test_commit_knowledge_package_assembles_real_package():
    from app.core import phase_two_store as store
    store.reset_store()
    store.seed_phase_two_demo_data()
    run_id = store.RUN_ID
    result = store.commit_knowledge_package(run_id)
    assert result["status"] == "succeeded"
    assert "package_ref" in result
    package = store.STORE.knowledge_packages[run_id]
    assert "metadata" in package
    assert "objects" in package
    assert "relationships" in package
    assert "scenes" in package
    assert "source_book" in package
    assert "chapters" in package
    assert package["metadata"]["run_id"] == run_id
    # objects must be non-empty: seed data has 3 objects (2 candidate + 1 approved)
    assert len(package["objects"]) >= 1, "knowledge package objects must not be empty"
    assert package["metadata"]["object_count"] == len(package["objects"])


def test_build_knowledge_context_from_source_refs():
    from app.core import phase_two_store as store
    store.reset_store()
    store.seed_phase_two_demo_data()
    book_id = store.BOOK_ID
    context = store.build_knowledge_context([f"object://source-books/{book_id}"])
    assert isinstance(context["context_text"], str)
    assert context["objects"]
    assert context["context_text"].strip()
    # 含真实对象名
    names = {o["canonical_name"] for o in context["objects"]}
    assert any(name in context["context_text"] for name in names)


def test_build_knowledge_context_empty_refs_safe():
    from app.core import phase_two_store as store
    store.reset_store()
    context = store.build_knowledge_context([])
    assert context["context_text"] == ""
    assert context["objects"] == []


def test_resolve_model_profile_skips_over_max_cost():
    from app.core import phase_two_store as store
    store.reset_store()
    store.seed_phase_two_demo_data()
    # 给 default profile 标一个高 est_cost，assignment max_cost 很低 → 跳过走 fallback
    default_id = store.MODEL_PROFILE_DEFAULT_ID
    store.STORE.model_profiles[default_id]["est_cost"] = 9.99
    assignment = store._get_agent_assignment("writer")
    assignment["max_cost"] = 0.5
    result = store.resolve_model_profile("writer")
    # 应跳过超成本的 default，落到 fallback（structured）或返回 None 记 failed call
    assert result["selected_profile"] is None or result["selected_profile"]["model_profile_id"] != default_id
