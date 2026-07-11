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


def test_openapi_declares_phase_two_and_agent_task_paths() -> None:
    text = Path("packages/contracts/openapi/novel-factory.v1.yaml").read_text()
    assert "url: /v1" in text
    assert "/books:" in text
    assert "/books/{bookId}:" in text
    assert "/books/{bookId}/chapters:" in text
    assert "/extraction-runs:" in text
    assert "/extraction-runs/{runId}:" in text
    assert "/extraction-runs/{runId}/report:" in text
    assert "/knowledge-objects:" in text
    assert "/knowledge-objects/{objectId}/review-actions:" in text
    assert "/graph/summary:" in text
    assert "/novel-projects:" in text
    assert "/novel-projects/{projectId}:" in text
    assert "/workspaces:" in text
    assert "/workspaces/{workspaceId}:" in text
    assert "/workspaces/{workspaceId}/home:" in text
    assert "/chapter-plans:" in text
    assert "/chapter-plans/{chapterPlanId}:" in text
    assert "/chapter-plans/{chapterPlanId}/section-plans:" in text
    assert "/writing-runs:" in text
    assert "/writing-runs/{writingRunId}:" in text
    assert "/writing-runs/{writingRunId}/accept-chapter:" in text
    assert "/quality-reports/{qualityReportId}:" in text
    assert "/feedback-records:" in text
    assert "/configuration:" in text
    assert "/model-profiles/{modelProfileId}/enable:" in text
    assert "/model-profiles/{modelProfileId}/disable:" in text
    assert "/agent-tasks:" in text
    assert "/agent-tasks/{taskId}:" in text


def test_phase_two_schema_files_exist() -> None:
    assert Path("packages/contracts/schemas/source-book.schema.json").exists()
    assert Path("packages/contracts/schemas/source-chapter.schema.json").exists()
    assert Path("packages/contracts/schemas/extraction-run.schema.json").exists()
    assert Path("packages/contracts/schemas/knowledge-object.schema.json").exists()
    assert Path("packages/contracts/schemas/review-action-command.schema.json").exists()
    assert Path("packages/contracts/schemas/graph-summary.schema.json").exists()
    assert Path("packages/contracts/schemas/novel-project.schema.json").exists()
    assert Path("packages/contracts/schemas/workspace.schema.json").exists()
    assert Path("packages/contracts/schemas/workspace-member.schema.json").exists()
    assert Path("packages/contracts/schemas/workspace-home.schema.json").exists()
    assert Path("packages/contracts/schemas/story-bible.schema.json").exists()
    assert Path("packages/contracts/schemas/chapter-plan.schema.json").exists()
    assert Path("packages/contracts/schemas/section-plan.schema.json").exists()
    assert Path("packages/contracts/schemas/model-profile.schema.json").exists()
    assert Path("packages/contracts/schemas/agent-model-assignment.schema.json").exists()
    assert Path("packages/contracts/schemas/provider-call.schema.json").exists()
    assert Path("packages/contracts/schemas/configuration-snapshot.schema.json").exists()
    assert Path("packages/contracts/schemas/chapter-snapshot.schema.json").exists()
    assert Path("packages/contracts/schemas/manuscript-state.schema.json").exists()
    assert Path("packages/contracts/schemas/writing-run.schema.json").exists()
    assert Path("packages/contracts/schemas/quality-report.schema.json").exists()
    assert Path("packages/contracts/schemas/feedback-record.schema.json").exists()
    assert Path("packages/contracts/schemas/audit-event.schema.json").exists()


def test_fixture_directories_exist() -> None:
    assert Path("packages/contracts/fixtures/tasks/valid/create-task-command.json").exists()
    assert Path("packages/contracts/fixtures/tasks/invalid/create-task-command-missing-idempotency-key.json").exists()
    assert Path("packages/contracts/fixtures/books/valid/source-book.json").exists()
    assert Path("packages/contracts/fixtures/books/invalid/source-book-missing-title.json").exists()
    assert Path("packages/contracts/fixtures/extraction-runs/valid/extraction-run.json").exists()
    assert Path("packages/contracts/fixtures/extraction-runs/invalid/extraction-run-invalid-stage.json").exists()
    assert Path("packages/contracts/fixtures/knowledge-review/valid/review-action-merge-alias.json").exists()
    assert Path("packages/contracts/fixtures/knowledge-review/valid/knowledge-object.json").exists()
    assert Path("packages/contracts/fixtures/knowledge-review/invalid/review-action-merge-alias-missing-target.json").exists()
    assert Path("packages/contracts/fixtures/projects/valid/novel-project.json").exists()
    assert Path("packages/contracts/fixtures/projects/invalid/novel-project-missing-title.json").exists()
    assert Path("packages/contracts/fixtures/workspace/valid/workspace.json").exists()
    assert Path("packages/contracts/fixtures/workspace/invalid/workspace-missing-owner-user.json").exists()
    assert Path("packages/contracts/fixtures/workspace/valid/workspace-member.json").exists()
    assert Path("packages/contracts/fixtures/workspace/invalid/workspace-member-invalid-role.json").exists()
    assert Path("packages/contracts/fixtures/workspace/valid/workspace-home.json").exists()
    assert Path("packages/contracts/fixtures/workspace/invalid/workspace-home-empty-links.json").exists()
    assert Path("packages/contracts/fixtures/planning/valid/chapter-plan.json").exists()
    assert Path("packages/contracts/fixtures/planning/invalid/chapter-plan-invalid-status.json").exists()
    assert Path("packages/contracts/fixtures/planning/valid/section-plan.json").exists()
    assert Path("packages/contracts/fixtures/planning/invalid/section-plan-invalid-role.json").exists()
    assert Path("packages/contracts/fixtures/configuration/valid/model-profile.json").exists()
    assert Path("packages/contracts/fixtures/configuration/invalid/model-profile-missing-id.json").exists()
    assert Path("packages/contracts/fixtures/configuration/valid/agent-model-assignment.json").exists()
    assert Path("packages/contracts/fixtures/configuration/invalid/agent-model-assignment-invalid-retry.json").exists()
    assert Path("packages/contracts/fixtures/configuration/valid/provider-call.json").exists()
    assert Path("packages/contracts/fixtures/configuration/invalid/provider-call-invalid-latency.json").exists()
    assert Path("packages/contracts/fixtures/configuration/valid/configuration-snapshot.json").exists()
    assert Path("packages/contracts/fixtures/configuration/invalid/configuration-snapshot-empty.json").exists()
    assert Path("packages/contracts/fixtures/configuration/valid/audit-event.json").exists()
    assert Path("packages/contracts/fixtures/configuration/invalid/audit-event-missing-request-id.json").exists()
    assert Path("packages/contracts/fixtures/manuscript/valid/chapter-snapshot.json").exists()
    assert Path("packages/contracts/fixtures/manuscript/invalid/chapter-snapshot-missing-text.json").exists()
    assert Path("packages/contracts/fixtures/manuscript/valid/manuscript-state.json").exists()
    assert Path("packages/contracts/fixtures/manuscript/invalid/manuscript-state-missing-prior-summary-pack.json").exists()
    assert Path("packages/contracts/fixtures/writing/valid/writing-run.json").exists()
    assert Path("packages/contracts/fixtures/writing/invalid/writing-run-invalid-status.json").exists()
    assert Path("packages/contracts/fixtures/writing/valid/quality-report.json").exists()
    assert Path("packages/contracts/fixtures/writing/invalid/quality-report-invalid-status.json").exists()
    assert Path("packages/contracts/fixtures/writing/valid/feedback-record.json").exists()
    assert Path("packages/contracts/fixtures/writing/invalid/feedback-record-invalid-score.json").exists()
