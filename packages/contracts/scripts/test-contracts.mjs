import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

const ajv = new Ajv2020({ allErrors: true, strict: false, schemas: [
  JSON.parse(fs.readFileSync(path.join(root, "schemas/request-meta.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/api-error.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/task-status.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/api-success-envelope.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/api-error-envelope.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/task.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/task-event.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/create-task-command.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/worker-command.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/worker-result.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/source-book.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/source-chapter.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/source-content.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/evidence.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/book-analysis-report.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/source-scene.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/story-event.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/story-conflict.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/story-hook.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/story-reward.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/story-climax.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/relationship-edge.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/knowledge-source-summary.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/extraction-run.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/knowledge-object.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/review-action-command.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/graph-summary.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/graph-node.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/graph-neighbors.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/novel-project.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/workspace.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/workspace-member.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/workspace-home.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/story-bible.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/chapter-plan.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/section-plan.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/model-profile.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/agent-model-assignment.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/provider-call.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/configuration-snapshot.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/chapter-snapshot.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/manuscript-state.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/consistency-issue.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/rule-profile.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/consistency-report.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/revision-summary.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/ranking-signal.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/ranking-suggestion.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/ranking-snapshot.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/writing-review-action-command.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/writing-run.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/quality-report.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/feedback-record.schema.json"), "utf8")),
  JSON.parse(fs.readFileSync(path.join(root, "schemas/audit-event.schema.json"), "utf8")),
] });
addFormats(ajv);

function readFixture(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), "utf8"));
}

function assertValid(schemaId, payload, label) {
  const validate = ajv.getSchema(schemaId);
  if (!validate) {
    throw new Error(`${label} validator missing`);
  }
  if (!validate(payload)) {
    throw new Error(`${label} valid fixture failed: ${JSON.stringify(validate.errors)}`);
  }
}

function assertInvalid(schemaId, payload, label) {
  const validate = ajv.getSchema(schemaId);
  if (!validate) {
    throw new Error(`${label} validator missing`);
  }
  if (validate(payload)) {
    throw new Error(`${label} invalid fixture unexpectedly passed`);
  }
}

assertValid(
  "https://novelfactory.dev/schemas/create-task-command.schema.json",
  readFixture("fixtures/tasks/valid/create-task-command.json"),
  "create-task-command",
);
assertInvalid(
  "https://novelfactory.dev/schemas/create-task-command.schema.json",
  readFixture("fixtures/tasks/invalid/create-task-command-missing-idempotency-key.json"),
  "create-task-command",
);

assertValid(
  "https://novelfactory.dev/schemas/source-book.schema.json",
  readFixture("fixtures/books/valid/source-book.json"),
  "source-book",
);
assertInvalid(
  "https://novelfactory.dev/schemas/source-book.schema.json",
  readFixture("fixtures/books/invalid/source-book-missing-title.json"),
  "source-book",
);

assertValid(
  "https://novelfactory.dev/schemas/source-content.schema.json",
  readFixture("fixtures/books/valid/source-content.json"),
  "source-content",
);
assertValid(
  "https://novelfactory.dev/schemas/source-chapter.schema.json",
  readFixture("fixtures/books/valid/source-chapter.json"),
  "source-chapter",
);
assertValid(
  "https://novelfactory.dev/schemas/evidence.schema.json",
  readFixture("fixtures/knowledge-review/valid/evidence.json"),
  "evidence",
);
assertValid(
  "https://novelfactory.dev/schemas/book-analysis-report.schema.json",
  readFixture("fixtures/books/valid/book-analysis-report.json"),
  "book-analysis-report",
);

assertValid(
  "https://novelfactory.dev/schemas/source-scene.schema.json",
  readFixture("fixtures/books/valid/book-analysis-report.json").scenes[0],
  "source-scene",
);
assertValid(
  "https://novelfactory.dev/schemas/story-event.schema.json",
  readFixture("fixtures/books/valid/book-analysis-report.json").events[0],
  "story-event",
);
assertValid(
  "https://novelfactory.dev/schemas/story-conflict.schema.json",
  readFixture("fixtures/books/valid/book-analysis-report.json").conflicts[0],
  "story-conflict",
);
assertValid(
  "https://novelfactory.dev/schemas/story-hook.schema.json",
  readFixture("fixtures/books/valid/book-analysis-report.json").hooks[0],
  "story-hook",
);
assertValid(
  "https://novelfactory.dev/schemas/story-reward.schema.json",
  readFixture("fixtures/books/valid/book-analysis-report.json").rewards[0],
  "story-reward",
);
assertValid(
  "https://novelfactory.dev/schemas/story-climax.schema.json",
  readFixture("fixtures/books/valid/book-analysis-report.json").climaxes[0],
  "story-climax",
);
assertValid(
  "https://novelfactory.dev/schemas/relationship-edge.schema.json",
  readFixture("fixtures/books/valid/book-analysis-report.json").relationships[0],
  "relationship-edge",
);
assertValid(
  "https://novelfactory.dev/schemas/knowledge-source-summary.schema.json",
  readFixture("fixtures/projects/valid/knowledge-source-summary.json"),
  "knowledge-source-summary",
);

assertValid(
  "https://novelfactory.dev/schemas/extraction-run.schema.json",
  readFixture("fixtures/extraction-runs/valid/extraction-run.json"),
  "extraction-run",
);
assertInvalid(
  "https://novelfactory.dev/schemas/extraction-run.schema.json",
  readFixture("fixtures/extraction-runs/invalid/extraction-run-invalid-stage.json"),
  "extraction-run",
);

assertValid(
  "https://novelfactory.dev/schemas/knowledge-object.schema.json",
  readFixture("fixtures/knowledge-review/valid/knowledge-object.json"),
  "knowledge-object",
);
assertValid(
  "https://novelfactory.dev/schemas/graph-node.schema.json",
  readFixture("fixtures/knowledge-review/valid/graph-node.json"),
  "graph-node",
);
assertInvalid(
  "https://novelfactory.dev/schemas/graph-node.schema.json",
  readFixture("fixtures/knowledge-review/invalid/graph-node-invalid-confidence.json"),
  "graph-node",
);
assertValid(
  "https://novelfactory.dev/schemas/graph-neighbors.schema.json",
  readFixture("fixtures/knowledge-review/valid/graph-neighbors.json"),
  "graph-neighbors",
);
assertInvalid(
  "https://novelfactory.dev/schemas/graph-neighbors.schema.json",
  readFixture("fixtures/knowledge-review/invalid/graph-neighbors-invalid-direction.json"),
  "graph-neighbors",
);

assertValid(
  "https://novelfactory.dev/schemas/review-action-command.schema.json",
  readFixture("fixtures/knowledge-review/valid/review-action-merge-alias.json"),
  "review-action",
);
assertInvalid(
  "https://novelfactory.dev/schemas/review-action-command.schema.json",
  readFixture("fixtures/knowledge-review/invalid/review-action-merge-alias-missing-target.json"),
  "review-action",
);

assertValid(
  "https://novelfactory.dev/schemas/novel-project.schema.json",
  readFixture("fixtures/projects/valid/novel-project.json"),
  "novel-project",
);
assertInvalid(
  "https://novelfactory.dev/schemas/novel-project.schema.json",
  readFixture("fixtures/projects/invalid/novel-project-missing-title.json"),
  "novel-project",
);

assertValid(
  "https://novelfactory.dev/schemas/story-bible.schema.json",
  readFixture("fixtures/projects/valid/story-bible.json"),
  "story-bible",
);

assertValid(
  "https://novelfactory.dev/schemas/workspace.schema.json",
  readFixture("fixtures/workspace/valid/workspace.json"),
  "workspace",
);
assertInvalid(
  "https://novelfactory.dev/schemas/workspace.schema.json",
  readFixture("fixtures/workspace/invalid/workspace-missing-owner-user.json"),
  "workspace",
);

assertValid(
  "https://novelfactory.dev/schemas/workspace-member.schema.json",
  readFixture("fixtures/workspace/valid/workspace-member.json"),
  "workspace-member",
);
assertInvalid(
  "https://novelfactory.dev/schemas/workspace-member.schema.json",
  readFixture("fixtures/workspace/invalid/workspace-member-invalid-role.json"),
  "workspace-member",
);

assertValid(
  "https://novelfactory.dev/schemas/workspace-home.schema.json",
  readFixture("fixtures/workspace/valid/workspace-home.json"),
  "workspace-home",
);
assertInvalid(
  "https://novelfactory.dev/schemas/workspace-home.schema.json",
  readFixture("fixtures/workspace/invalid/workspace-home-empty-links.json"),
  "workspace-home",
);

assertValid(
  "https://novelfactory.dev/schemas/chapter-plan.schema.json",
  readFixture("fixtures/planning/valid/chapter-plan.json"),
  "chapter-plan",
);
assertInvalid(
  "https://novelfactory.dev/schemas/chapter-plan.schema.json",
  readFixture("fixtures/planning/invalid/chapter-plan-invalid-status.json"),
  "chapter-plan",
);

assertValid(
  "https://novelfactory.dev/schemas/section-plan.schema.json",
  readFixture("fixtures/planning/valid/section-plan.json"),
  "section-plan",
);
assertInvalid(
  "https://novelfactory.dev/schemas/section-plan.schema.json",
  readFixture("fixtures/planning/invalid/section-plan-invalid-role.json"),
  "section-plan",
);

assertValid(
  "https://novelfactory.dev/schemas/model-profile.schema.json",
  readFixture("fixtures/configuration/valid/model-profile.json"),
  "model-profile",
);
assertInvalid(
  "https://novelfactory.dev/schemas/model-profile.schema.json",
  readFixture("fixtures/configuration/invalid/model-profile-missing-id.json"),
  "model-profile",
);

assertValid(
  "https://novelfactory.dev/schemas/agent-model-assignment.schema.json",
  readFixture("fixtures/configuration/valid/agent-model-assignment.json"),
  "agent-model-assignment",
);
assertInvalid(
  "https://novelfactory.dev/schemas/agent-model-assignment.schema.json",
  readFixture("fixtures/configuration/invalid/agent-model-assignment-invalid-retry.json"),
  "agent-model-assignment",
);

assertValid(
  "https://novelfactory.dev/schemas/provider-call.schema.json",
  readFixture("fixtures/configuration/valid/provider-call.json"),
  "provider-call",
);
assertInvalid(
  "https://novelfactory.dev/schemas/provider-call.schema.json",
  readFixture("fixtures/configuration/invalid/provider-call-invalid-latency.json"),
  "provider-call",
);

assertValid(
  "https://novelfactory.dev/schemas/configuration-snapshot.schema.json",
  readFixture("fixtures/configuration/valid/configuration-snapshot.json"),
  "configuration-snapshot",
);
assertInvalid(
  "https://novelfactory.dev/schemas/configuration-snapshot.schema.json",
  readFixture("fixtures/configuration/invalid/configuration-snapshot-empty.json"),
  "configuration-snapshot",
);

assertValid(
  "https://novelfactory.dev/schemas/audit-event.schema.json",
  readFixture("fixtures/configuration/valid/audit-event.json"),
  "audit-event",
);
assertInvalid(
  "https://novelfactory.dev/schemas/audit-event.schema.json",
  readFixture("fixtures/configuration/invalid/audit-event-missing-request-id.json"),
  "audit-event",
);

assertValid(
  "https://novelfactory.dev/schemas/chapter-snapshot.schema.json",
  readFixture("fixtures/manuscript/valid/chapter-snapshot.json"),
  "chapter-snapshot",
);
assertInvalid(
  "https://novelfactory.dev/schemas/chapter-snapshot.schema.json",
  readFixture("fixtures/manuscript/invalid/chapter-snapshot-missing-text.json"),
  "chapter-snapshot",
);

assertValid(
  "https://novelfactory.dev/schemas/manuscript-state.schema.json",
  readFixture("fixtures/manuscript/valid/manuscript-state.json"),
  "manuscript-state",
);
assertInvalid(
  "https://novelfactory.dev/schemas/manuscript-state.schema.json",
  readFixture("fixtures/manuscript/invalid/manuscript-state-missing-prior-summary-pack.json"),
  "manuscript-state",
);

assertValid(
  "https://novelfactory.dev/schemas/rule-profile.schema.json",
  readFixture("fixtures/rules/valid/rule-profile.json"),
  "rule-profile",
);
assertInvalid(
  "https://novelfactory.dev/schemas/rule-profile.schema.json",
  readFixture("fixtures/rules/invalid/rule-profile-invalid-severity.json"),
  "rule-profile",
);

assertValid(
  "https://novelfactory.dev/schemas/consistency-report.schema.json",
  readFixture("fixtures/writing/valid/consistency-report.json"),
  "consistency-report",
);
assertInvalid(
  "https://novelfactory.dev/schemas/consistency-report.schema.json",
  readFixture("fixtures/writing/invalid/consistency-report-invalid-status.json"),
  "consistency-report",
);

assertValid(
  "https://novelfactory.dev/schemas/revision-summary.schema.json",
  readFixture("fixtures/writing/valid/revision-summary.json"),
  "revision-summary",
);
assertInvalid(
  "https://novelfactory.dev/schemas/revision-summary.schema.json",
  readFixture("fixtures/writing/invalid/revision-summary-invalid-round.json"),
  "revision-summary",
);

assertValid(
  "https://novelfactory.dev/schemas/writing-review-action-command.schema.json",
  readFixture("fixtures/writing/valid/writing-review-action-command.json"),
  "writing-review-action-command",
);
assertInvalid(
  "https://novelfactory.dev/schemas/writing-review-action-command.schema.json",
  readFixture("fixtures/writing/invalid/writing-review-action-command-missing-issue-id.json"),
  "writing-review-action-command",
);

assertValid(
  "https://novelfactory.dev/schemas/writing-run.schema.json",
  readFixture("fixtures/writing/valid/writing-run.json"),
  "writing-run",
);
assertInvalid(
  "https://novelfactory.dev/schemas/writing-run.schema.json",
  readFixture("fixtures/writing/invalid/writing-run-invalid-status.json"),
  "writing-run",
);

assertValid(
  "https://novelfactory.dev/schemas/quality-report.schema.json",
  readFixture("fixtures/writing/valid/quality-report.json"),
  "quality-report",
);
assertInvalid(
  "https://novelfactory.dev/schemas/quality-report.schema.json",
  readFixture("fixtures/writing/invalid/quality-report-invalid-status.json"),
  "quality-report",
);

assertValid(
  "https://novelfactory.dev/schemas/ranking-signal.schema.json",
  readFixture("fixtures/writing/valid/ranking-signal.json"),
  "ranking-signal",
);
assertInvalid(
  "https://novelfactory.dev/schemas/ranking-signal.schema.json",
  readFixture("fixtures/writing/invalid/ranking-signal-invalid-score.json"),
  "ranking-signal",
);

assertValid(
  "https://novelfactory.dev/schemas/ranking-suggestion.schema.json",
  readFixture("fixtures/writing/valid/ranking-suggestion.json"),
  "ranking-suggestion",
);
assertInvalid(
  "https://novelfactory.dev/schemas/ranking-suggestion.schema.json",
  readFixture("fixtures/writing/invalid/ranking-suggestion-missing-signals.json"),
  "ranking-suggestion",
);

assertValid(
  "https://novelfactory.dev/schemas/ranking-snapshot.schema.json",
  readFixture("fixtures/writing/valid/ranking-snapshot.json"),
  "ranking-snapshot",
);
assertInvalid(
  "https://novelfactory.dev/schemas/ranking-snapshot.schema.json",
  readFixture("fixtures/writing/invalid/ranking-snapshot-empty-items.json"),
  "ranking-snapshot",
);

assertValid(
  "https://novelfactory.dev/schemas/feedback-record.schema.json",
  readFixture("fixtures/writing/valid/feedback-record.json"),
  "feedback-record",
);
assertInvalid(
  "https://novelfactory.dev/schemas/feedback-record.schema.json",
  readFixture("fixtures/writing/invalid/feedback-record-invalid-score.json"),
  "feedback-record",
);

console.log("contracts test ok");

