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


def test_get_seed_writing_run_and_quality_report() -> None:
    client = make_client()

    writing_response = client.get("/v1/writing-runs/01JZWRITING00000000000001")
    quality_response = client.get("/v1/quality-reports/01JZQLTREP000000000000001")
    feedback_response = client.get("/v1/feedback-records", params={"targetId": "01JZWRITING00000000000001"})

    assert writing_response.status_code == 200
    payload = writing_response.json()["data"]
    assert payload["writing_run"]["current_stage"] == "humanizer_pass"
    assert payload["memory_package"]["memory_package_id"] == "01JZMEMPKG000000000000001"
    assert len(payload["section_runs"]) == 3
    assert len(payload["feedback_records"]) >= 2
    assert quality_response.status_code == 200
    assert quality_response.json()["data"]["status"] == "blocked"
    assert feedback_response.status_code == 200
    assert len(feedback_response.json()["data"]["items"]) >= 1


def test_get_configuration_snapshot_and_toggle_model_profile() -> None:
    client = make_client()

    snapshot_response = client.get("/v1/configuration")
    disable_response = client.post("/v1/model-profiles/model_profile_default/disable")
    enable_response = client.post("/v1/model-profiles/model_profile_default/enable")

    assert snapshot_response.status_code == 200
    snapshot = snapshot_response.json()["data"]
    assert snapshot["default_model_profile_id"] == "model_profile_default"
    assert any(item["agent_role"] == "writer" and item["enabled"] for item in snapshot["agent_model_assignments"])
    assert any(item["agent_role"] == "feedback" and item["enabled"] for item in snapshot["agent_model_assignments"])
    assert disable_response.status_code == 200
    assert disable_response.json()["data"]["model_profile"]["enabled"] is False
    assert enable_response.status_code == 200
    assert enable_response.json()["data"]["model_profile"]["enabled"] is True


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
    assert payload["meta"] == {"request_id": "req-writing", "trace_id": "trace-writing"}
    assert payload["data"]["writing_run"]["status"] == "queued"
    assert payload["data"]["writing_run"]["critic_model_profile_id"] == "model_profile_structured_fallback"
    assert payload["data"]["task"]["task_type"] == "create_writing_run"
    assert len(payload["data"]["section_runs"]) == 3
    assert payload["data"]["quality_report"]["status"] == "queued"
    assert len(payload["data"]["provider_calls"]) == 4
    assert payload["data"]["provider_calls"][1]["error_code"] == "structured_output_validation_failed"




def test_accept_chapter_marks_writing_run_and_returns_feedback_records() -> None:
    client = make_client()

    response = client.post(
        "/v1/writing-runs/01JZWRITING00000000000001/accept-chapter",
        headers={"x-request-id": "req-accept", "x-trace-id": "trace-accept"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["meta"] == {"request_id": "req-accept", "trace_id": "trace-accept"}
    assert payload["data"]["writing_run"]["status"] == "succeeded"
    assert payload["data"]["writing_run"]["accepted_chapter_ref"]
    assert payload["data"]["writing_run"]["chapter_snapshot"]["chapter_title"] == "乌坦城风起"
    assert payload["data"]["writing_run"]["manuscript_state"]["current_story_state"]["quality_gate_status"] == "passed"
    assert payload["data"]["chapter_snapshot"]["chapter_snapshot_id"].startswith("chapter-snapshot:")
    assert payload["data"]["manuscript_state"]["manuscript_state_id"].startswith("manuscript-state:")


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


def test_writing_resources_missing_return_not_found() -> None:
    client = make_client()

    assert client.get("/v1/writing-runs/missing").status_code == 404
    assert client.post("/v1/writing-runs/missing/accept-chapter").status_code == 404
    assert client.get("/v1/quality-reports/missing").status_code == 404
    assert client.post(
        "/v1/writing-runs",
        json={"project_id": "missing", "chapter_plan_id": "missing"},
    ).status_code == 404
