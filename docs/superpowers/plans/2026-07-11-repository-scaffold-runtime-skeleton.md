# Repository Scaffold and Runtime Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a runnable Novel Factory MVP scaffold with local infrastructure, contract validation, backend service shells, worker/scheduler shells, and a route-complete web shell so later domain slices can land without reworking project structure.

**Architecture:** Use a pnpm workspace for the React web app and TypeScript contract tooling, Python packages for `api-gateway`, `core-service`, `ai-worker`, and `scheduler`, and Docker Compose for PostgreSQL, Redis, and MinIO. This plan intentionally covers NF-IMPL-003 build order items 1-2 plus a minimal frontend shell: health, trace, contracts, boot surfaces, and smoke checks only; domain workflows, DB migrations, and LLM runtime details belong to follow-on plans.

**Tech Stack:** React, TypeScript, Vite, React Router, pnpm, FastAPI, Pydantic, Dramatiq, Redis, PostgreSQL 16 + pgvector, MinIO, Docker Compose, pytest, Vitest, AJV, Swagger Parser

## Global Constraints

- Frontend must use: React, TypeScript, pnpm, shadcn/ui preferred for common components.
- API Gateway / BFF: NestJS or FastAPI.
- AI / Knowledge Services: Python FastAPI.
- Python Data Validation: Pydantic.
- Queue / Runtime Coordination: Redis.
- Database: PostgreSQL with pgvector.
- Object Storage: MinIO locally, S3-compatible storage later.
- MVP ai-worker uses Python worker runtime. Queue library priority Dramatiq + Redis broker.
- PostgreSQL `ai.tasks` is task state authority source.
- All endpoints must use the NF-API-001 envelope.
- API version path: `/v1`.
- `TaskStatus` enum values: `queued`, `running`, `retrying`, `succeeded`, `failed`, `cancelled`, `requires_review`, `blocked`.
- Long-running operations must create tasks and be executed by ai-worker.
- No task handler may call provider SDK directly.
- Provider API key must not be written to Markdown, seed data, or PostgreSQL plain text fields.
- Signed URL must expire. Default MVP expiration: 15 minutes.
- Execution constraint from current implementation phase: each task gets at most two iterations and about 15 minutes before stopping to report status.
- This workspace is currently not a Git repository, so commit steps must be skipped until Git is initialized.

## Scope Check

Current design documents cover multiple independent subsystems: scaffold/runtime, source import and knowledge review, planning and writing orchestration, and feedback/configuration. Do **not** try to execute all of them in one giant branchless session. This plan covers only first working subsystem: repository scaffold and runtime skeleton. After this lands, create separate plans for:

1. Source import + extraction + knowledge review.
2. Project planning + memory/prompt package assembly.
3. Writing run + quality gate + feedback dashboard.

## File Structure

- `package.json` — root workspace commands for scaffold verification, contracts, web tests, and smoke checks.
- `pnpm-workspace.yaml` — pnpm workspace membership for TypeScript packages.
- `tsconfig.base.json` — shared TypeScript compiler defaults.
- `.gitignore` — ignore Python, Node, Vite, Docker, and env artifacts.
- `README.md` — append implementation bootstrap commands without removing existing documentation-project guidance.
- `tests/test_repo_layout.py` — root red test for workspace bootstrap files and commands.
- `tests/test_infra_compose.py` — root red test for local PostgreSQL/Redis/MinIO compose config.
- `tests/test_contract_baseline.py` — root red test for required OpenAPI and task contract artifacts.
- `infra/docker-compose.yml` — local PostgreSQL 16 + pgvector, Redis, MinIO, and health checks.
- `infra/postgres/init/001-enable-extensions.sql` — bootstrap `vector` extension for local PostgreSQL.
- `packages/contracts/package.json` — contract tooling entrypoint.
- `packages/contracts/openapi/novel-factory.v1.yaml` — HTTP source of truth for `/v1` health and task shell endpoints.
- `packages/contracts/schemas/*.schema.json` — JSON Schema source of truth for envelope and task payloads.
- `packages/contracts/fixtures/**` — valid/invalid payload fixtures for schema tests.
- `packages/contracts/scripts/lint-contracts.mjs` — OpenAPI parse and `$ref` resolution check.
- `packages/contracts/scripts/test-contracts.mjs` — JSON Schema fixture validation.
- `apps/api-gateway/pyproject.toml` — editable Python package metadata for FastAPI BFF shell.
- `apps/api-gateway/app/core/envelope.py` — success envelope helper matching NF-API-001.
- `apps/api-gateway/app/core/request_context.py` — request/trace ID propagation middleware.
- `apps/api-gateway/app/api/v1/health.py` — versioned gateway health endpoint.
- `apps/api-gateway/app/main.py` — FastAPI app bootstrap.
- `apps/api-gateway/tests/test_health.py` — gateway health and envelope tests.
- `apps/core-service/pyproject.toml` — editable Python package metadata for FastAPI domain-service shell.
- `apps/core-service/app/core/envelope.py` — success envelope helper for core-service shell.
- `apps/core-service/app/core/request_context.py` — request/trace ID propagation middleware for core-service.
- `apps/core-service/app/api/v1/health.py` — versioned core-service health endpoint.
- `apps/core-service/app/main.py` — FastAPI app bootstrap.
- `apps/core-service/tests/test_health.py` — core-service health and envelope tests.
- `apps/ai-worker/pyproject.toml` — editable Python package metadata for Dramatiq worker shell.
- `apps/ai-worker/worker/bootstrap.py` — Redis broker bootstrap.
- `apps/ai-worker/worker/main.py` — no-op actor import surface for smoke tests.
- `apps/ai-worker/tests/test_bootstrap.py` — broker and actor bootstrap tests.
- `apps/scheduler/pyproject.toml` — editable Python package metadata for scheduler shell.
- `apps/scheduler/scheduler/main.py` — one-tick scheduler bootstrap surface.
- `apps/scheduler/tests/test_tick.py` — scheduler tick shape test.
- `apps/web/package.json` — Vite/React web shell package.
- `apps/web/tsconfig.json` — app-local TypeScript config extending root base.
- `apps/web/vite.config.ts` — Vite and Vitest config.
- `apps/web/index.html` — Vite entry HTML.
- `apps/web/src/main.tsx` — React mount point.
- `apps/web/src/App.tsx` — router host.
- `apps/web/src/router.tsx` — MVP route groups.
- `apps/web/src/components/app-shell.tsx` — left-nav layout for MVP shell.
- `apps/web/src/pages.tsx` — simple route-complete placeholder pages.
- `apps/web/src/test/app-shell.test.tsx` — route shell render test.
- `scripts/dev/smoke.sh` — one-command local verification of scaffold, contracts, Python tests, and web tests.

---

### Task 1: Root Workspace Bootstrap

**Files:**
- Modify: `README.md`
- Create: `package.json`
- Create: `pnpm-workspace.yaml`
- Create: `tsconfig.base.json`
- Create: `.gitignore`
- Test: `tests/test_repo_layout.py`

**Interfaces:**
- Consumes: existing `README.md` documentation-project overview.
- Produces:
  - root commands `pnpm contracts:lint`, `pnpm contracts:test`, `pnpm test`, `pnpm lint`
  - shared TypeScript base config at `tsconfig.base.json`
  - workspace membership for `apps/web` and `packages/*`

- [ ] **Step 1: Write the failing root-layout test**

```python
from pathlib import Path
import json


def test_root_workspace_files_exist_and_expose_required_scripts() -> None:
    package = json.loads(Path("package.json").read_text())
    assert package["private"] is True
    assert package["scripts"]["contracts:lint"] == "pnpm --filter @novel-factory/contracts lint"
    assert package["scripts"]["contracts:test"] == "pnpm --filter @novel-factory/contracts test"
    assert package["scripts"]["lint"] == "pnpm contracts:lint && pnpm --filter @novel-factory/web lint && pytest tests/test_repo_layout.py tests/test_infra_compose.py tests/test_contract_baseline.py -q"
    assert package["scripts"]["test"] == "pytest -q && pnpm contracts:test && pnpm --filter @novel-factory/web test --run"


def test_workspace_membership_and_bootstrap_docs_are_present() -> None:
    workspace = Path("pnpm-workspace.yaml").read_text()
    assert "apps/web" in workspace
    assert "packages/*" in workspace

    tsconfig = json.loads(Path("tsconfig.base.json").read_text())
    assert tsconfig["compilerOptions"]["strict"] is True
    assert tsconfig["compilerOptions"]["module"] == "ESNext"

    readme = Path("README.md").read_text()
    assert "## Implementation Bootstrap" in readme
    assert "pnpm contracts:lint" in readme
    assert "docker compose -f infra/docker-compose.yml up -d" in readme
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_repo_layout.py -q`

Expected: FAIL with `FileNotFoundError: [Errno 2] No such file or directory: 'package.json'`

- [ ] **Step 3: Write the minimal root workspace files**

```json
// package.json
{
  "name": "novel-factory",
  "private": true,
  "packageManager": "pnpm@10.0.0",
  "scripts": {
    "contracts:lint": "pnpm --filter @novel-factory/contracts lint",
    "contracts:test": "pnpm --filter @novel-factory/contracts test",
    "lint": "pnpm contracts:lint && pnpm --filter @novel-factory/web lint && pytest tests/test_repo_layout.py tests/test_infra_compose.py tests/test_contract_baseline.py -q",
    "test": "pytest -q && pnpm contracts:test && pnpm --filter @novel-factory/web test --run"
  }
}
```

```yaml
# pnpm-workspace.yaml
packages:
  - apps/web
  - packages/*
```

```json
// tsconfig.base.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "jsx": "react-jsx",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "types": ["vite/client"]
  }
}
```

```gitignore
# .gitignore
node_modules/
dist/
coverage/
.venv/
__pycache__/
.pytest_cache/
.env
.env.local
*.pyc
.DS_Store
```

```markdown
<!-- Append this exact section to README.md -->
## Implementation Bootstrap

```sh
pnpm install
python -m pip install -e apps/api-gateway -e apps/core-service -e apps/ai-worker -e apps/scheduler pytest
Docker compose -f infra/docker-compose.yml up -d
pnpm contracts:lint
pnpm contracts:test
pytest -q
pnpm --filter @novel-factory/web dev
```
```

- [ ] **Step 4: Run the root-layout test to verify it passes**

Run: `pytest tests/test_repo_layout.py -q`

Expected: PASS with `2 passed`

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add README.md package.json pnpm-workspace.yaml tsconfig.base.json .gitignore tests/test_repo_layout.py
  git commit -m "feat: bootstrap root workspace"
else
  echo "skip: no git repo"
fi
```

### Task 2: Local Infrastructure Skeleton

**Files:**
- Create: `infra/docker-compose.yml`
- Create: `infra/postgres/init/001-enable-extensions.sql`
- Create: `.env.example`
- Test: `tests/test_infra_compose.py`

**Interfaces:**
- Consumes: root workspace from Task 1.
- Produces:
  - `docker compose -f infra/docker-compose.yml up -d postgres redis minio`
  - local PostgreSQL 16 + pgvector, Redis, and MinIO health-checked endpoints
  - safe development env variable names with fake values only

- [ ] **Step 1: Write the failing infrastructure test**

```python
from pathlib import Path
import subprocess


def test_docker_compose_file_is_valid() -> None:
    compose_path = Path("infra/docker-compose.yml")
    assert compose_path.exists()

    result = subprocess.run(
        ["docker", "compose", "-f", str(compose_path), "config"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "postgres:" in result.stdout
    assert "redis:" in result.stdout
    assert "minio:" in result.stdout


def test_pgvector_init_and_env_example_exist() -> None:
    sql = Path("infra/postgres/init/001-enable-extensions.sql").read_text()
    assert "CREATE EXTENSION IF NOT EXISTS vector;" in sql

    env = Path(".env.example").read_text()
    assert "NOVEL_FACTORY_POSTGRES_URL=" in env
    assert "NOVEL_FACTORY_REDIS_URL=" in env
    assert "NOVEL_FACTORY_MINIO_SECRET_KEY=" in env
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_infra_compose.py -q`

Expected: FAIL with `AssertionError: assert False` on missing `infra/docker-compose.yml`

- [ ] **Step 3: Write the local infrastructure files**

```yaml
# infra/docker-compose.yml
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: novel_factory
      POSTGRES_USER: novel
      POSTGRES_PASSWORD: novel
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U novel -d novel_factory"]
      interval: 5s
      timeout: 5s
      retries: 10
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./postgres/init:/docker-entrypoint-initdb.d

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 10

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: novel-factory
      MINIO_ROOT_PASSWORD: novel-factory-secret
    ports:
      - "9000:9000"
      - "9001:9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 5s
      timeout: 5s
      retries: 10
    volumes:
      - minio-data:/data

volumes:
  postgres-data:
  minio-data:
```

```sql
-- infra/postgres/init/001-enable-extensions.sql
CREATE EXTENSION IF NOT EXISTS vector;
```

```dotenv
# .env.example
NOVEL_FACTORY_POSTGRES_URL=postgresql://novel:novel@localhost:5432/novel_factory
NOVEL_FACTORY_REDIS_URL=redis://localhost:6379/0
NOVEL_FACTORY_MINIO_ENDPOINT=http://localhost:9000
NOVEL_FACTORY_MINIO_ACCESS_KEY=novel-factory
NOVEL_FACTORY_MINIO_SECRET_KEY=replace-me
NOVEL_FACTORY_MINIO_BUCKET=novel-factory-dev
```

- [ ] **Step 4: Run the infrastructure checks**

Run: `pytest tests/test_infra_compose.py -q && docker compose -f infra/docker-compose.yml config >/tmp/novel-factory.compose.out`

Expected: pytest PASS with `2 passed`, and `docker compose config` exits `0`

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add infra/docker-compose.yml infra/postgres/init/001-enable-extensions.sql .env.example tests/test_infra_compose.py
  git commit -m "feat: add local infrastructure skeleton"
else
  echo "skip: no git repo"
fi
```

### Task 3: Contract Baseline for Envelope and Task Payloads

**Files:**
- Create: `packages/contracts/package.json`
- Create: `packages/contracts/openapi/novel-factory.v1.yaml`
- Create: `packages/contracts/schemas/api-success-envelope.schema.json`
- Create: `packages/contracts/schemas/api-error-envelope.schema.json`
- Create: `packages/contracts/schemas/task-status.schema.json`
- Create: `packages/contracts/schemas/task.schema.json`
- Create: `packages/contracts/schemas/task-event.schema.json`
- Create: `packages/contracts/schemas/create-task-command.schema.json`
- Create: `packages/contracts/schemas/worker-command.schema.json`
- Create: `packages/contracts/schemas/worker-result.schema.json`
- Create: `packages/contracts/fixtures/tasks/valid/create-task-command.json`
- Create: `packages/contracts/fixtures/tasks/invalid/create-task-command-missing-idempotency-key.json`
- Create: `packages/contracts/scripts/lint-contracts.mjs`
- Create: `packages/contracts/scripts/test-contracts.mjs`
- Test: `tests/test_contract_baseline.py`

**Interfaces:**
- Consumes: root pnpm workspace from Task 1.
- Produces:
  - `pnpm contracts:lint`
  - `pnpm contracts:test`
  - schema names `ApiSuccessEnvelope`, `ApiErrorEnvelope`, `Task`, `TaskEvent`, `CreateTaskCommand`, `WorkerCommand`, `WorkerResult`, `TaskStatus`
  - OpenAPI path prefix `/v1`

- [ ] **Step 1: Write the failing contract-baseline test**

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_contract_baseline.py -q`

Expected: FAIL with missing `packages/contracts/schemas/task-status.schema.json`

- [ ] **Step 3: Write the contract package, OpenAPI file, schemas, fixtures, and scripts**

```json
// packages/contracts/package.json
{
  "name": "@novel-factory/contracts",
  "private": true,
  "type": "module",
  "scripts": {
    "lint": "node ./scripts/lint-contracts.mjs",
    "test": "node ./scripts/test-contracts.mjs"
  },
  "devDependencies": {
    "@apidevtools/swagger-parser": "^12.1.0",
    "ajv": "^8.17.1",
    "ajv-formats": "^3.0.1",
    "glob": "^11.0.0"
  }
}
```

```yaml
# packages/contracts/openapi/novel-factory.v1.yaml
openapi: 3.1.0
info:
  title: Novel Factory API
  version: 1.0.0
servers:
  - url: /v1
paths:
  /health:
    get:
      operationId: getGatewayHealth
      responses:
        '200':
          description: Gateway health
          content:
            application/json:
              schema:
                $ref: './schemas/api-success-envelope.schema.json'
  /agent-tasks:
    post:
      operationId: createAgentTask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: './schemas/create-task-command.schema.json'
      responses:
        '202':
          description: Task accepted
          content:
            application/json:
              schema:
                $ref: './schemas/api-success-envelope.schema.json'
  /agent-tasks/{taskId}:
    get:
      operationId: getAgentTask
      parameters:
        - in: path
          name: taskId
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Task detail
          content:
            application/json:
              schema:
                $ref: './schemas/api-success-envelope.schema.json'
        '404':
          description: Task not found
          content:
            application/json:
              schema:
                $ref: './schemas/api-error-envelope.schema.json'
```

```json
// packages/contracts/schemas/api-success-envelope.schema.json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://novelfactory.dev/schemas/api-success-envelope.schema.json",
  "type": "object",
  "required": ["data", "meta", "errors"],
  "properties": {
    "data": {},
    "meta": {
      "type": "object",
      "required": ["request_id", "trace_id"],
      "properties": {
        "request_id": { "type": "string", "minLength": 1 },
        "trace_id": { "type": "string", "minLength": 1 }
      },
      "additionalProperties": false
    },
    "errors": {
      "type": "array",
      "items": { "type": "object" }
    }
  },
  "additionalProperties": false
}
```

```json
// packages/contracts/schemas/api-error-envelope.schema.json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://novelfactory.dev/schemas/api-error-envelope.schema.json",
  "type": "object",
  "required": ["data", "meta", "errors"],
  "properties": {
    "data": { "type": ["null", "object", "array", "string", "number", "boolean"] },
    "meta": {
      "type": "object",
      "required": ["request_id", "trace_id"],
      "properties": {
        "request_id": { "type": "string", "minLength": 1 },
        "trace_id": { "type": "string", "minLength": 1 }
      },
      "additionalProperties": false
    },
    "errors": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["code", "message"],
        "properties": {
          "code": { "type": "string", "minLength": 1 },
          "message": { "type": "string", "minLength": 1 },
          "target": { "type": "string" },
          "recovery_hint": { "type": "string" }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

```json
// packages/contracts/schemas/task-status.schema.json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://novelfactory.dev/schemas/task-status.schema.json",
  "type": "string",
  "enum": [
    "queued",
    "running",
    "retrying",
    "succeeded",
    "failed",
    "cancelled",
    "requires_review",
    "blocked"
  ]
}
```

```json
// packages/contracts/schemas/task.schema.json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://novelfactory.dev/schemas/task.schema.json",
  "type": "object",
  "required": [
    "task_id",
    "task_type",
    "workspace_id",
    "owner_module",
    "input_refs",
    "output_refs",
    "status",
    "progress",
    "idempotency_key",
    "retry_count",
    "created_at"
  ],
  "properties": {
    "task_id": { "type": "string", "minLength": 1 },
    "task_type": { "type": "string", "minLength": 1 },
    "workspace_id": { "type": "string", "minLength": 1 },
    "owner_module": { "type": "string", "minLength": 1 },
    "input_refs": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "output_refs": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "status": { "$ref": "./task-status.schema.json" },
    "progress": { "type": "number", "minimum": 0, "maximum": 100 },
    "idempotency_key": { "type": "string", "minLength": 1 },
    "retry_count": { "type": "integer", "minimum": 0 },
    "error_code": { "type": ["string", "null"] },
    "created_at": { "type": "string", "format": "date-time" },
    "started_at": { "type": ["string", "null"], "format": "date-time" },
    "finished_at": { "type": ["string", "null"], "format": "date-time" }
  },
  "additionalProperties": false
}
```

```json
// packages/contracts/schemas/task-event.schema.json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://novelfactory.dev/schemas/task-event.schema.json",
  "type": "object",
  "required": ["task_event_id", "task_id", "event_type", "message", "created_at"],
  "properties": {
    "task_event_id": { "type": "string", "minLength": 1 },
    "task_id": { "type": "string", "minLength": 1 },
    "event_type": {
      "type": "string",
      "enum": ["created", "started", "progress", "retry_scheduled", "review_required", "blocked", "failed", "succeeded"]
    },
    "message": { "type": "string", "minLength": 1 },
    "payload_ref": { "type": ["string", "null"] },
    "payload_json": { "type": ["object", "null"] },
    "created_at": { "type": "string", "format": "date-time" }
  },
  "additionalProperties": false
}
```

```json
// packages/contracts/schemas/create-task-command.schema.json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://novelfactory.dev/schemas/create-task-command.schema.json",
  "type": "object",
  "required": ["task_type", "workspace_id", "owner_module", "input_refs", "idempotency_key", "trace_id", "requested_by"],
  "properties": {
    "task_type": { "type": "string", "minLength": 1 },
    "workspace_id": { "type": "string", "minLength": 1 },
    "owner_module": { "type": "string", "minLength": 1 },
    "input_refs": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "idempotency_key": { "type": "string", "minLength": 1 },
    "trace_id": { "type": "string", "minLength": 1 },
    "requested_by": { "type": "string", "minLength": 1 }
  },
  "additionalProperties": false
}
```

```json
// packages/contracts/schemas/worker-command.schema.json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://novelfactory.dev/schemas/worker-command.schema.json",
  "type": "object",
  "required": ["command_id", "task_id", "task_type", "workspace_id", "input_refs", "idempotency_key", "trace_id", "requested_by"],
  "properties": {
    "command_id": { "type": "string", "minLength": 1 },
    "task_id": { "type": "string", "minLength": 1 },
    "task_type": { "type": "string", "minLength": 1 },
    "workspace_id": { "type": "string", "minLength": 1 },
    "input_refs": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "idempotency_key": { "type": "string", "minLength": 1 },
    "trace_id": { "type": "string", "minLength": 1 },
    "requested_by": { "type": "string", "minLength": 1 }
  },
  "additionalProperties": false
}
```

```json
// packages/contracts/schemas/worker-result.schema.json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://novelfactory.dev/schemas/worker-result.schema.json",
  "type": "object",
  "required": ["task_id", "status", "output_refs", "metrics", "errors", "trace_id"],
  "properties": {
    "task_id": { "type": "string", "minLength": 1 },
    "status": { "$ref": "./task-status.schema.json" },
    "output_refs": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "metrics": { "type": "object" },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["code", "message"],
        "properties": {
          "code": { "type": "string", "minLength": 1 },
          "message": { "type": "string", "minLength": 1 }
        },
        "additionalProperties": false
      }
    },
    "trace_id": { "type": "string", "minLength": 1 }
  },
  "additionalProperties": false
}
```

```json
// packages/contracts/fixtures/tasks/valid/create-task-command.json
{
  "task_type": "extract_knowledge",
  "workspace_id": "01JZ0000000000000000000000",
  "owner_module": "ai-worker",
  "input_refs": ["object://source-books/01JZBOOK"],
  "idempotency_key": "extract-01JZBOOK-001",
  "trace_id": "01JZTRC000000000000000000",
  "requested_by": "system_agent"
}
```

```json
// packages/contracts/fixtures/tasks/invalid/create-task-command-missing-idempotency-key.json
{
  "task_type": "extract_knowledge",
  "workspace_id": "01JZ0000000000000000000000",
  "owner_module": "ai-worker",
  "input_refs": ["object://source-books/01JZBOOK"],
  "trace_id": "01JZTRC000000000000000000",
  "requested_by": "system_agent"
}
```

```js
// packages/contracts/scripts/lint-contracts.mjs
import SwaggerParser from "@apidevtools/swagger-parser";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const openApiPath = path.resolve(__dirname, "../openapi/novel-factory.v1.yaml");

await SwaggerParser.validate(openApiPath);
console.log("contracts lint ok");
```

```js
// packages/contracts/scripts/test-contracts.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Ajv from "ajv";
import addFormats from "ajv-formats";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);

const taskStatus = JSON.parse(fs.readFileSync(path.join(root, "schemas/task-status.schema.json"), "utf8"));
const createTaskCommand = JSON.parse(fs.readFileSync(path.join(root, "schemas/create-task-command.schema.json"), "utf8"));
const task = JSON.parse(fs.readFileSync(path.join(root, "schemas/task.schema.json"), "utf8"));
const taskEvent = JSON.parse(fs.readFileSync(path.join(root, "schemas/task-event.schema.json"), "utf8"));
const workerCommand = JSON.parse(fs.readFileSync(path.join(root, "schemas/worker-command.schema.json"), "utf8"));
const workerResult = JSON.parse(fs.readFileSync(path.join(root, "schemas/worker-result.schema.json"), "utf8"));

ajv.addSchema(taskStatus);
ajv.addSchema(task);
ajv.addSchema(taskEvent);
ajv.addSchema(createTaskCommand);
ajv.addSchema(workerCommand);
ajv.addSchema(workerResult);

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
```

- [ ] **Step 4: Run contract validation commands**

Run: `pytest tests/test_contract_baseline.py -q && pnpm install && pnpm contracts:lint && pnpm contracts:test`

Expected:
- pytest PASS with `3 passed`
- `contracts lint ok`
- `contracts test ok`

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add packages/contracts tests/test_contract_baseline.py
  git commit -m "feat: add contract baseline"
else
  echo "skip: no git repo"
fi
```

### Task 4: API Gateway and Core-Service Health Shells

**Files:**
- Create: `apps/api-gateway/pyproject.toml`
- Create: `apps/api-gateway/app/core/envelope.py`
- Create: `apps/api-gateway/app/core/request_context.py`
- Create: `apps/api-gateway/app/api/v1/health.py`
- Create: `apps/api-gateway/app/main.py`
- Create: `apps/api-gateway/tests/test_health.py`
- Create: `apps/core-service/pyproject.toml`
- Create: `apps/core-service/app/core/envelope.py`
- Create: `apps/core-service/app/core/request_context.py`
- Create: `apps/core-service/app/api/v1/health.py`
- Create: `apps/core-service/app/main.py`
- Create: `apps/core-service/tests/test_health.py`

**Interfaces:**
- Consumes: NF-API-001 envelope rules from Task 3 contract baseline.
- Produces:
  - `GET /v1/health` on api-gateway returning `{"data":{"service":"api-gateway","status":"ok"},"meta":...,"errors":[]}`
  - `GET /v1/health` on core-service returning `{"data":{"service":"core-service","status":"ok"},"meta":...,"errors":[]}`
  - Python helper `success_envelope(data: dict, request_id: str, trace_id: str) -> dict`
  - header propagation `X-Request-Id` and `X-Trace-Id`

- [ ] **Step 1: Write the failing FastAPI health tests**

```python
# apps/api-gateway/tests/test_health.py
from fastapi.testclient import TestClient
from app.main import app


def test_gateway_health_uses_api_envelope() -> None:
    client = TestClient(app)
    response = client.get("/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"] == {"service": "api-gateway", "status": "ok"}
    assert payload["errors"] == []
    assert payload["meta"]["request_id"]
    assert payload["meta"]["trace_id"]
    assert response.headers["x-request-id"] == payload["meta"]["request_id"]
    assert response.headers["x-trace-id"] == payload["meta"]["trace_id"]
```

```python
# apps/core-service/tests/test_health.py
from fastapi.testclient import TestClient
from app.main import app


def test_core_service_health_uses_api_envelope() -> None:
    client = TestClient(app)
    response = client.get("/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"] == {"service": "core-service", "status": "ok"}
    assert payload["errors"] == []
    assert payload["meta"]["request_id"]
    assert payload["meta"]["trace_id"]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest apps/api-gateway/tests/test_health.py apps/core-service/tests/test_health.py -q`

Expected: FAIL with `ModuleNotFoundError: No module named 'app'`

- [ ] **Step 3: Write the FastAPI shell implementations**

```toml
# apps/api-gateway/pyproject.toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "novel-factory-api-gateway"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
  "fastapi>=0.115,<1.0",
  "uvicorn[standard]>=0.30,<1.0",
  "pydantic>=2.8,<3.0",
  "ulid-py>=1.1,<2.0"
]

[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]
```

```python
# apps/api-gateway/app/core/envelope.py
from typing import Any


def success_envelope(data: dict[str, Any], request_id: str, trace_id: str) -> dict[str, Any]:
    return {
        "data": data,
        "meta": {
            "request_id": request_id,
            "trace_id": trace_id,
        },
        "errors": [],
    }
```

```python
# apps/api-gateway/app/core/request_context.py
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from ulid import ULID


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("x-request-id", str(ULID()))
        trace_id = request.headers.get("x-trace-id", str(ULID()))

        request.state.request_id = request_id
        request.state.trace_id = trace_id

        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        response.headers["x-trace-id"] = trace_id
        return response
```

```python
# apps/api-gateway/app/api/v1/health.py
from fastapi import APIRouter, Request

from app.core.envelope import success_envelope

router = APIRouter()


@router.get("/health")
def get_health(request: Request) -> dict:
    return success_envelope(
        data={"service": "api-gateway", "status": "ok"},
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )
```

```python
# apps/api-gateway/app/main.py
from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.core.request_context import RequestContextMiddleware

app = FastAPI(title="Novel Factory API Gateway", version="0.1.0")
app.add_middleware(RequestContextMiddleware)
app.include_router(health_router, prefix="/v1")
```

```toml
# apps/core-service/pyproject.toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "novel-factory-core-service"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
  "fastapi>=0.115,<1.0",
  "uvicorn[standard]>=0.30,<1.0",
  "pydantic>=2.8,<3.0",
  "ulid-py>=1.1,<2.0"
]

[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]
```

```python
# apps/core-service/app/core/envelope.py
from typing import Any


def success_envelope(data: dict[str, Any], request_id: str, trace_id: str) -> dict[str, Any]:
    return {
        "data": data,
        "meta": {
            "request_id": request_id,
            "trace_id": trace_id,
        },
        "errors": [],
    }
```

```python
# apps/core-service/app/core/request_context.py
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from ulid import ULID


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("x-request-id", str(ULID()))
        trace_id = request.headers.get("x-trace-id", str(ULID()))

        request.state.request_id = request_id
        request.state.trace_id = trace_id

        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        response.headers["x-trace-id"] = trace_id
        return response
```

```python
# apps/core-service/app/api/v1/health.py
from fastapi import APIRouter, Request

from app.core.envelope import success_envelope

router = APIRouter()


@router.get("/health")
def get_health(request: Request) -> dict:
    return success_envelope(
        data={"service": "core-service", "status": "ok"},
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )
```

```python
# apps/core-service/app/main.py
from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.core.request_context import RequestContextMiddleware

app = FastAPI(title="Novel Factory Core Service", version="0.1.0")
app.add_middleware(RequestContextMiddleware)
app.include_router(health_router, prefix="/v1")
```

- [ ] **Step 4: Install the Python packages and run the health tests**

Run: `python -m pip install -e apps/api-gateway -e apps/core-service pytest && pytest apps/api-gateway/tests/test_health.py apps/core-service/tests/test_health.py -q`

Expected: PASS with `2 passed`

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add apps/api-gateway apps/core-service
  git commit -m "feat: add gateway and core service shells"
else
  echo "skip: no git repo"
fi
```

### Task 5: ai-worker and Scheduler Boot Shells

**Files:**
- Create: `apps/ai-worker/pyproject.toml`
- Create: `apps/ai-worker/worker/bootstrap.py`
- Create: `apps/ai-worker/worker/main.py`
- Create: `apps/ai-worker/tests/test_bootstrap.py`
- Create: `apps/scheduler/pyproject.toml`
- Create: `apps/scheduler/scheduler/main.py`
- Create: `apps/scheduler/tests/test_tick.py`

**Interfaces:**
- Consumes: Redis runtime from Task 2 and task contract concepts from Task 3.
- Produces:
  - `build_broker(redis_url: str) -> RedisBroker`
  - `noop_task(task_id: str) -> dict[str, str]`
  - `run_scheduler_tick(now: datetime | None = None) -> SchedulerTickResult`

- [ ] **Step 1: Write the failing worker and scheduler tests**

```python
# apps/ai-worker/tests/test_bootstrap.py
from worker.bootstrap import build_broker
from worker.main import noop_task


def test_build_broker_sets_a_redis_broker() -> None:
    broker = build_broker("redis://localhost:6379/0")
    host = broker.client.connection_pool.connection_kwargs["host"]
    assert host == "localhost"


def test_noop_task_actor_name_is_stable() -> None:
    assert noop_task.actor_name == "noop_task"
```

```python
# apps/scheduler/tests/test_tick.py
from datetime import datetime, timezone

from scheduler.main import run_scheduler_tick


def test_scheduler_tick_returns_expected_counters() -> None:
    result = run_scheduler_tick(datetime(2026, 7, 11, tzinfo=timezone.utc))
    assert result.requeued == 0
    assert result.expired_leases == 0
    assert result.due_retries == 0
    assert result.ran_at == "2026-07-11T00:00:00+00:00"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest apps/ai-worker/tests/test_bootstrap.py apps/scheduler/tests/test_tick.py -q`

Expected: FAIL with `ModuleNotFoundError` for `worker` and `scheduler`

- [ ] **Step 3: Write the worker and scheduler shell implementations**

```toml
# apps/ai-worker/pyproject.toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "novel-factory-ai-worker"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
  "dramatiq[redis]>=1.17,<2.0",
  "redis>=5,<6"
]

[tool.setuptools.packages.find]
where = ["."]
include = ["worker*"]
```

```python
# apps/ai-worker/worker/bootstrap.py
import dramatiq
from dramatiq.brokers.redis import RedisBroker


def build_broker(redis_url: str) -> RedisBroker:
    broker = RedisBroker(url=redis_url)
    dramatiq.set_broker(broker)
    return broker
```

```python
# apps/ai-worker/worker/main.py
import os

import dramatiq

from worker.bootstrap import build_broker

build_broker(os.getenv("NOVEL_FACTORY_REDIS_URL", "redis://localhost:6379/0"))


@dramatiq.actor(queue_name="task-default")
def noop_task(task_id: str) -> dict[str, str]:
    return {"task_id": task_id, "status": "succeeded"}
```

```toml
# apps/scheduler/pyproject.toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "novel-factory-scheduler"
version = "0.1.0"
requires-python = ">=3.13"

[tool.setuptools.packages.find]
where = ["."]
include = ["scheduler*"]
```

```python
# apps/scheduler/scheduler/main.py
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class SchedulerTickResult:
    requeued: int
    expired_leases: int
    due_retries: int
    ran_at: str


def run_scheduler_tick(now: datetime | None = None) -> SchedulerTickResult:
    current = now or datetime.now(timezone.utc)
    return SchedulerTickResult(
        requeued=0,
        expired_leases=0,
        due_retries=0,
        ran_at=current.isoformat(),
    )


if __name__ == "__main__":
    print(run_scheduler_tick())
```

- [ ] **Step 4: Install the Python packages and run the tests**

Run: `python -m pip install -e apps/ai-worker -e apps/scheduler pytest && pytest apps/ai-worker/tests/test_bootstrap.py apps/scheduler/tests/test_tick.py -q`

Expected: PASS with `3 passed`

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add apps/ai-worker apps/scheduler
  git commit -m "feat: add worker and scheduler shells"
else
  echo "skip: no git repo"
fi
```

### Task 6: Web Route Shell and AppShell Navigation

**Files:**
- Create: `apps/web/package.json`
- Create: `apps/web/tsconfig.json`
- Create: `apps/web/vite.config.ts`
- Create: `apps/web/index.html`
- Create: `apps/web/src/main.tsx`
- Create: `apps/web/src/App.tsx`
- Create: `apps/web/src/router.tsx`
- Create: `apps/web/src/components/app-shell.tsx`
- Create: `apps/web/src/pages.tsx`
- Create: `apps/web/src/test/app-shell.test.tsx`

**Interfaces:**
- Consumes: root TypeScript config from Task 1.
- Produces:
  - route groups `/workspaces/:workspaceId`, `/sources`, `/sources/:bookId`, `/extraction-runs/:runId`, `/knowledge/review`, `/graph`, `/projects`, `/projects/:projectId`, `/projects/:projectId/planner`, `/projects/:projectId/writing/:writingRunId`, `/feedback`, `/configuration`
  - shared React component `AppShell`
  - web commands `pnpm --filter @novel-factory/web dev`, `pnpm --filter @novel-factory/web lint`, `pnpm --filter @novel-factory/web test --run`

- [ ] **Step 1: Write the failing web-shell test**

```tsx
import { render, screen } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { routes } from "../router";

describe("AppShell", () => {
  it("renders route-complete writing studio shell with left navigation", async () => {
    const router = createMemoryRouter(routes, {
      initialEntries: ["/projects/demo-project/writing/demo-run"],
    });

    render(<RouterProvider router={router} />);

    expect(screen.getByRole("heading", { name: "Writing Studio" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Workspace Home" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Feedback Dashboard" })).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pnpm --filter @novel-factory/web test --run`

Expected: FAIL with `No projects matched the filters` or missing package error

- [ ] **Step 3: Write the web shell implementation**

```json
// apps/web/package.json
{
  "name": "@novel-factory/web",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "lint": "tsc --noEmit",
    "test": "vitest"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.28.0"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.6.3",
    "@testing-library/react": "^16.0.1",
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "jsdom": "^25.0.1",
    "typescript": "^5.6.3",
    "vite": "^5.4.10",
    "vitest": "^2.1.4"
  }
}
```

```json
// apps/web/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "baseUrl": "."
  },
  "include": ["src", "vite.config.ts"]
}
```

```ts
// apps/web/vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.ts"],
  },
});
```

```html
<!-- apps/web/index.html -->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Novel Factory</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

```tsx
// apps/web/src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

```tsx
// apps/web/src/App.tsx
import { RouterProvider } from "react-router-dom";

import { router } from "./router";

export default function App() {
  return <RouterProvider router={router} />;
}
```

```tsx
// apps/web/src/components/app-shell.tsx
import { Link, Outlet } from "react-router-dom";

const navItems = [
  { to: "/workspaces/demo-workspace", label: "Workspace Home" },
  { to: "/sources", label: "Source Library" },
  { to: "/knowledge/review", label: "Knowledge Review" },
  { to: "/graph", label: "Story Graph Viewer" },
  { to: "/projects", label: "Novel Projects" },
  { to: "/feedback", label: "Feedback Dashboard" },
  { to: "/configuration", label: "Configuration" },
];

export function AppShell() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", minHeight: "100vh" }}>
      <aside style={{ borderRight: "1px solid #d4d4d8", padding: "24px" }}>
        <h1>Novel Factory</h1>
        <nav aria-label="Primary">
          <ul style={{ display: "grid", gap: "12px", padding: 0, listStyle: "none" }}>
            {navItems.map((item) => (
              <li key={item.to}>
                <Link to={item.to}>{item.label}</Link>
              </li>
            ))}
          </ul>
        </nav>
      </aside>
      <main style={{ padding: "24px" }}>
        <Outlet />
      </main>
    </div>
  );
}
```

```tsx
// apps/web/src/pages.tsx
function Page({ title, body }: { title: string; body: string }) {
  return (
    <section>
      <h2>{title}</h2>
      <p>{body}</p>
    </section>
  );
}

export const WorkspaceHomePage = () => <Page title="Workspace Home" body="Recent tasks, pending reviews, and workspace entry point." />;
export const SourceLibraryPage = () => <Page title="Source Library" body="Upload reference books and inspect chapter import state." />;
export const SourceBookPage = () => <Page title="Source Book Detail" body="Inspect chapter segmentation and source file metadata." />;
export const ExtractionRunPage = () => <Page title="Extraction Run Detail" body="Track extraction status, errors, and run reports." />;
export const KnowledgeReviewPage = () => <Page title="Knowledge Review" body="Approve, reject, merge alias, or request re-extract on candidates." />;
export const GraphPage = () => <Page title="Story Graph Viewer" body="Browse graph nodes, edges, and snapshot details." />;
export const ProjectListPage = () => <Page title="Novel Projects" body="List projects, story bibles, and chapter progress." />;
export const ProjectHomePage = () => <Page title="Novel Project Home" body="Review story bible, chapter list, and project status." />;
export const PlannerPage = () => <Page title="Chapter Planner" body="Review chapter, scene, and beat planning outputs." />;
export const WritingStudioPage = () => <Page title="Writing Studio" body="Inspect writing run state, drafts, critic issues, and quality results." />;
export const FeedbackPage = () => <Page title="Feedback Dashboard" body="Inspect cost, AI flavor, edit distance, and strategy suggestions." />;
export const ConfigurationPage = () => <Page title="Configuration" body="Manage model profiles, quality thresholds, and prompt versions." />;
```

```tsx
// apps/web/src/router.tsx
import { createBrowserRouter } from "react-router-dom";

import { AppShell } from "./components/app-shell";
import {
  ConfigurationPage,
  ExtractionRunPage,
  FeedbackPage,
  GraphPage,
  KnowledgeReviewPage,
  PlannerPage,
  ProjectHomePage,
  ProjectListPage,
  SourceBookPage,
  SourceLibraryPage,
  WorkspaceHomePage,
  WritingStudioPage,
} from "./pages";

export const routes = [
  {
    path: "/",
    element: <AppShell />,
    children: [
      { path: "workspaces/:workspaceId", element: <WorkspaceHomePage /> },
      { path: "sources", element: <SourceLibraryPage /> },
      { path: "sources/:bookId", element: <SourceBookPage /> },
      { path: "extraction-runs/:runId", element: <ExtractionRunPage /> },
      { path: "knowledge/review", element: <KnowledgeReviewPage /> },
      { path: "graph", element: <GraphPage /> },
      { path: "projects", element: <ProjectListPage /> },
      { path: "projects/:projectId", element: <ProjectHomePage /> },
      { path: "projects/:projectId/planner", element: <PlannerPage /> },
      { path: "projects/:projectId/writing/:writingRunId", element: <WritingStudioPage /> },
      { path: "feedback", element: <FeedbackPage /> },
      { path: "configuration", element: <ConfigurationPage /> },
    ],
  },
];

export const router = createBrowserRouter(routes);
```

```ts
// apps/web/src/test/setup.ts
import "@testing-library/jest-dom";
```

- [ ] **Step 4: Install web dependencies and run the web-shell test**

Run: `pnpm install && pnpm --filter @novel-factory/web test --run`

Expected: PASS with `1 passed`

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add apps/web
  git commit -m "feat: add web route shell"
else
  echo "skip: no git repo"
fi
```

### Task 7: Developer Smoke Script

**Files:**
- Modify: `package.json`
- Create: `scripts/dev/smoke.sh`

**Interfaces:**
- Consumes: Tasks 1-6 outputs.
- Produces:
  - root command `pnpm smoke`
  - one-command local verification of contracts, Python tests, and web tests

- [ ] **Step 1: Write the failing smoke-script check**

```python
from pathlib import Path
import json


def test_root_package_has_smoke_script_and_smoke_file() -> None:
    package = json.loads(Path("package.json").read_text())
    assert package["scripts"]["smoke"] == "bash scripts/dev/smoke.sh"

    script = Path("scripts/dev/smoke.sh").read_text()
    assert "pnpm contracts:lint" in script
    assert "pytest -q" in script
    assert "pnpm --filter @novel-factory/web test --run" in script
```

- [ ] **Step 2: Run the smoke-script check to verify it fails**

Run: `pytest tests/test_repo_layout.py tests/test_infra_compose.py tests/test_contract_baseline.py -q`

Expected: FAIL because `package.json` does not yet expose `smoke`

- [ ] **Step 3: Add the root smoke command and the smoke script**

```json
// package.json
{
  "name": "novel-factory",
  "private": true,
  "packageManager": "pnpm@10.0.0",
  "scripts": {
    "contracts:lint": "pnpm --filter @novel-factory/contracts lint",
    "contracts:test": "pnpm --filter @novel-factory/contracts test",
    "lint": "pnpm contracts:lint && pnpm --filter @novel-factory/web lint && pytest tests/test_repo_layout.py tests/test_infra_compose.py tests/test_contract_baseline.py -q",
    "test": "pytest -q && pnpm contracts:test && pnpm --filter @novel-factory/web test --run",
    "smoke": "bash scripts/dev/smoke.sh"
  }
}
```

```bash
# scripts/dev/smoke.sh
#!/usr/bin/env bash
set -euo pipefail

pnpm contracts:lint
pnpm contracts:test
pytest -q
pnpm --filter @novel-factory/web test --run
```

- [ ] **Step 4: Run the smoke command**

Run: `pnpm smoke`

Expected:
- `contracts lint ok`
- `contracts test ok`
- pytest PASS
- web test PASS

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add package.json scripts/dev/smoke.sh
  git commit -m "feat: add scaffold smoke gate"
else
  echo "skip: no git repo"
fi
```
