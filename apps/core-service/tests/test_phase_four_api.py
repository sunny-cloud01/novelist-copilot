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


def test_get_seed_writing_run_and_quality_report() -> None:
    client = make_client()

    writing_response = client.get("/v1/writing-runs/01JZWRITING00000000000001")
    quality_response = client.get("/v1/quality-reports/01JZQLTREP000000000000001")
    consistency_response = client.get("/v1/consistency-reports/01JZCONSIST00000000000001")
    revision_response = client.get("/v1/revision-summaries/01JZREVISION0000000000001")
    rules_response = client.get("/v1/rules")
    feedback_response = client.get("/v1/feedback-records", params={"targetId": "01JZWRITING00000000000001"})
    rankings_response = client.get("/v1/rankings/prompt", params={"targetId": "01JZWRITING00000000000001"})

    assert writing_response.status_code == 200
    payload = writing_response.json()["data"]
    assert payload["writing_run"]["current_stage"] == "consistency_review"
    assert payload["writing_run"]["consistency_report_id"] == "01JZCONSIST00000000000001"
    assert payload["writing_run"]["revision_summary_id"] == "01JZREVISION0000000000001"
    assert payload["memory_package"]["memory_package_id"] == "01JZMEMPKG000000000000001"
    assert len(payload["section_runs"]) == 3
    assert len(payload["feedback_records"]) >= 2
    assert quality_response.status_code == 200
    assert quality_response.json()["data"]["status"] == "blocked"
    assert consistency_response.status_code == 200
    assert consistency_response.json()["data"]["blocking_issue_count"] == 1
    assert revision_response.status_code == 200
    assert revision_response.json()["data"]["status"] == "requested"
    assert rules_response.status_code == 200
    assert rules_response.json()["data"]["items"][0]["rule_id"] == "rule-01JZPOWER000000000000001"
    assert feedback_response.status_code == 200
    assert len(feedback_response.json()["data"]["items"]) >= 1
    assert rankings_response.status_code == 200
    rankings = rankings_response.json()["data"]
    assert rankings["ranking_type"] == "prompt"
    assert rankings["items"][0]["target_id"] == "prompt://writer/chapter-default"
    assert rankings["suggestions"][0]["summary"] == "收紧 writer 默认提示中对金手指线索的显性表达。"


def test_get_configuration_snapshot_and_toggle_model_profile() -> None:
    client = make_client()

    snapshot_response = client.get("/v1/configuration")
    disable_response = client.post("/v1/model-profiles/model_profile_default/disable")
    enable_response = client.post("/v1/model-profiles/model_profile_default/enable")

    assert snapshot_response.status_code == 200
    snapshot = snapshot_response.json()["data"]
    assert snapshot["default_model_profile_id"] == "model_profile_default"
    assert snapshot["workspace_id"] == "demo-workspace"
    assert snapshot["trace_id"] == "trace-config-snapshot"
    assert any(item["agent_role"] == "writer" and item["enabled"] for item in snapshot["agent_model_assignments"])
    assert any(item["agent_role"] == "feedback" and item["enabled"] for item in snapshot["agent_model_assignments"])
    assert disable_response.status_code == 200
    assert disable_response.json()["data"]["model_profile"]["enabled"] is False
    assert enable_response.status_code == 200
    assert enable_response.json()["data"]["model_profile"]["enabled"] is True

    audit_response = client.get("/v1/audit-events")
    assert any(item["action"] == "configuration.model_profile_toggled" for item in audit_response.json()["data"]["items"])


def test_model_profile_toggle_requires_owner() -> None:
    client = make_client()

    response = client.post(
        "/v1/model-profiles/model_profile_default/disable",
        headers={"x-actor-role": "editor", "x-actor-id": "editor-user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "forbidden"


def test_create_writing_run_returns_seeded_quality_and_provider_calls() -> None:
    client = make_client()

    create_plan = client.post(
        "/v1/chapter-plans",
        json={
            "project_id": "01JZPROJECT000000000000001",
            "chapter_index": 4,
            "target_word_count": 3800,
        },
        headers={"x-trace-id": "trace-writing-plan"},
    )
    chapter_plan_id = create_plan.json()["data"]["chapter_plan"]["chapter_plan_id"]
    client.post(
        f"/v1/chapter-plans/{chapter_plan_id}/section-plans",
        json={"section_count": 3},
        headers={"x-trace-id": "trace-writing-sections"},
    )

    writing_response = client.post(
        "/v1/writing-runs",
        json={
            "project_id": "01JZPROJECT000000000000001",
            "chapter_plan_id": chapter_plan_id,
        },
        headers={"x-request-id": "req-writing", "x-trace-id": "trace-writing"},
    )

    assert writing_response.status_code == 202
    payload = writing_response.json()
    assert payload["meta"] == {
        "request_id": "req-writing",
        "trace_id": "trace-writing",
        "workspace_id": "demo-workspace",
        "actor_id": "demo-user",
        "actor_role": "owner",
    }
    assert payload["data"]["writing_run"]["status"] == "queued"
    assert payload["data"]["writing_run"]["critic_model_profile_id"] == "model_profile_structured_fallback"
    assert payload["data"]["task"]["task_type"] == "create_writing_run"
    assert len(payload["data"]["section_runs"]) == 3
    assert payload["data"]["quality_report"]["status"] == "queued"
    assert len(payload["data"]["provider_calls"]) == 4
    assert payload["data"]["provider_calls"][0]["provider_model_name"] == "claude-sonnet-5"
    assert payload["data"]["provider_calls"][0]["provider_account_id"] == "provider-account-anthropic-default"
    assert payload["data"]["provider_calls"][0]["output_ref"].startswith("object://drafts/")
    assert payload["data"]["provider_calls"][1]["error_code"] == "structured_output_validation_failed"




def test_accept_chapter_marks_writing_run_and_returns_feedback_records() -> None:
    client = make_client()

    resolve_response = client.post(
        "/v1/writing-runs/01JZWRITING00000000000001/review-actions",
        json={
            "schema_version": 1,
            "writing_run_id": "01JZWRITING00000000000001",
            "action": "mark_issue_resolved",
            "requested_by": "demo-reviewer",
            "trace_id": "trace-accept-resolve",
            "issue_id": "01JZCONSISTISSUE000000001",
            "note": "已人工确认并补写修订。",
            "output_ref": "object://revision-summaries/01JZREVISION0000000000001",
        },
        headers={"x-request-id": "req-accept-resolve", "x-trace-id": "trace-accept-resolve"},
    )
    approve_response = client.post(
        "/v1/writing-runs/01JZWRITING00000000000001/review-actions",
        json={
            "schema_version": 1,
            "writing_run_id": "01JZWRITING00000000000001",
            "action": "approve_draft",
            "requested_by": "demo-reviewer",
            "trace_id": "trace-accept-approve",
            "note": "一致性问题已关闭，允许收录。",
            "output_ref": "object://review-notes/approve-draft",
        },
        headers={"x-request-id": "req-accept-approve", "x-trace-id": "trace-accept-approve"},
    )
    response = client.post(
        "/v1/writing-runs/01JZWRITING00000000000001/accept-chapter",
        headers={"x-request-id": "req-accept", "x-trace-id": "trace-accept"},
    )

    assert resolve_response.status_code == 200
    assert approve_response.status_code == 200
    assert response.status_code == 200
    payload = response.json()
    assert payload["meta"] == {
        "request_id": "req-accept",
        "trace_id": "trace-accept",
        "workspace_id": "demo-workspace",
        "actor_id": "demo-user",
        "actor_role": "owner",
    }
    assert payload["data"]["writing_run"]["status"] == "succeeded"
    assert payload["data"]["writing_run"]["accepted_chapter_ref"]
    assert payload["data"]["writing_run"]["chapter_snapshot"]["chapter_title"] == "乌坦城风起"
    assert payload["data"]["writing_run"]["manuscript_state"]["current_story_state"]["quality_gate_status"] == "passed"
    assert payload["data"]["writing_run"]["consistency_report"]["status"] == "passed"
    assert payload["data"]["writing_run"]["revision_summary"]["status"] == "accepted"
    assert payload["data"]["chapter_snapshot"]["chapter_snapshot_id"].startswith("chapter-snapshot:")
    assert payload["data"]["manuscript_state"]["manuscript_state_id"].startswith("manuscript-state:")

    audit_response = client.get("/v1/audit-events")
    assert any(item["action"] == "writing.accept_chapter" and item["trace_id"] == "trace-accept" for item in audit_response.json()["data"]["items"])


def test_accept_chapter_returns_conflict_when_dependencies_incomplete() -> None:
    client = make_client()

    create_plan = client.post(
        "/v1/chapter-plans",
        json={
            "project_id": "01JZPROJECT000000000000001",
            "chapter_index": 6,
            "target_word_count": 3600,
        },
        headers={"x-trace-id": "trace-incomplete-plan"},
    )
    chapter_plan_id = create_plan.json()["data"]["chapter_plan"]["chapter_plan_id"]
    client.post(
        f"/v1/chapter-plans/{chapter_plan_id}/section-plans",
        json={"section_count": 2},
        headers={"x-trace-id": "trace-incomplete-sections"},
    )

    create_run = client.post(
        "/v1/writing-runs",
        json={
            "project_id": "01JZPROJECT000000000000001",
            "chapter_plan_id": chapter_plan_id,
        },
        headers={"x-request-id": "req-incomplete-run", "x-trace-id": "trace-incomplete-run"},
    )
    writing_run_id = create_run.json()["data"]["writing_run"]["writing_run_id"]

    response = client.post(
        f"/v1/writing-runs/{writing_run_id}/accept-chapter",
        headers={"x-request-id": "req-incomplete-accept", "x-trace-id": "trace-incomplete-accept"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "writing run acceptance dependencies incomplete"


def test_writing_review_action_resolves_issue_and_writes_audit() -> None:
    client = make_client()

    response = client.post(
        "/v1/writing-runs/01JZWRITING00000000000001/review-actions",
        json={
            "schema_version": 1,
            "writing_run_id": "01JZWRITING00000000000001",
            "action": "mark_issue_resolved",
            "requested_by": "demo-reviewer",
            "trace_id": "trace-writing-review",
            "issue_id": "01JZCONSISTISSUE000000001",
            "note": "已人工确认并补写修订。",
            "output_ref": "object://revision-summaries/01JZREVISION0000000000001",
        },
        headers={"x-request-id": "req-writing-review", "x-trace-id": "trace-writing-review"},
    )

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["consistency_report"]["blocking_issue_count"] == 0
    assert payload["revision_summary"]["status"] == "revised"
    assert payload["quality_report"]["status"] == "requires_review"

    audit_response = client.get("/v1/audit-events")
    assert any(item["action"] == "writing.mark_issue_resolved" for item in audit_response.json()["data"]["items"])


def test_writing_resources_missing_return_not_found() -> None:
    client = make_client()

    assert client.get("/v1/writing-runs/missing").status_code == 404
    assert client.post("/v1/writing-runs/missing/accept-chapter").status_code == 404
    assert client.post(
        "/v1/writing-runs/missing/review-actions",
        json={
            "schema_version": 1,
            "writing_run_id": "missing",
            "action": "approve_draft",
            "requested_by": "demo-reviewer",
            "trace_id": "trace-missing",
        },
    ).status_code == 404
    assert client.get("/v1/quality-reports/missing").status_code == 404
    assert client.get("/v1/consistency-reports/missing").status_code == 404
    assert client.get("/v1/revision-summaries/missing").status_code == 404
    assert client.get("/v1/rules/missing").status_code == 404
    assert client.post(
        "/v1/writing-runs",
        json={"project_id": "missing", "chapter_plan_id": "missing"},
    ).status_code == 404
