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
] });
addFormats(ajv);

const validateCreateTaskCommand = ajv.getSchema("https://novelfactory.dev/schemas/create-task-command.schema.json");
if (!validateCreateTaskCommand) {
  throw new Error("create-task-command validator missing");
}

const validPayload = JSON.parse(
  fs.readFileSync(path.join(root, "fixtures/tasks/valid/create-task-command.json"), "utf8"),
);
const invalidPayload = JSON.parse(
  fs.readFileSync(path.join(root, "fixtures/tasks/invalid/create-task-command-missing-idempotency-key.json"), "utf8"),
);

if (!validateCreateTaskCommand(validPayload)) {
  throw new Error(`valid fixture failed: ${JSON.stringify(validateCreateTaskCommand.errors)}`);
}

if (validateCreateTaskCommand(invalidPayload)) {
  throw new Error("invalid fixture unexpectedly passed");
}

console.log("contracts test ok");
