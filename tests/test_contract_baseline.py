from pathlib import Path
import json

EXPECTED_STATUS = [
    "queued",
    "running",
    "retrying",
    "succeeded",
    "failed",
    "cancelled",
    "requires_review",
    "blocked",
]


def test_task_status_schema_matches_spec() -> None:
    schema = json.loads(Path("packages/contracts/schemas/task-status.schema.json").read_text())
    assert schema["enum"] == EXPECTED_STATUS


def test_openapi_declares_v1_and_agent_task_paths() -> None:
    text = Path("packages/contracts/openapi/novel-factory.v1.yaml").read_text()
    assert "url: /v1" in text
    assert "/agent-tasks:" in text
    assert "/agent-tasks/{taskId}:" in text


def test_fixture_directories_exist() -> None:
    assert Path("packages/contracts/fixtures/tasks/valid/create-task-command.json").exists()
    assert Path("packages/contracts/fixtures/tasks/invalid/create-task-command-missing-idempotency-key.json").exists()
