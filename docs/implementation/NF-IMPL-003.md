---
document_id: NF-IMPL-003
title: Service Build Plan
version: 1.0.0
status: Draft
category: Implementation Blueprint
owner: Novel Factory Implementation Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-ARCH-002
  - NF-DBS-002
  - NF-DBS-003
  - NF-API-001
  - NF-AGENT-001
  - NF-PROMPT-002
  - NF-PIPE-003
  - NF-RAG-001
  - NF-QA-001
  - NF-IMPL-001
  - NF-IMPL-002
  - NF-LLM-001
  - NF-TASK-001
  - NF-CONTRACT-001
  - NF-SEC-001
  - NF-AI-001
references:
  - docs/standards/NFES-000.md
  - docs/architecture/NF-ARCH-002.md
  - docs/database/NF-DBS-002.md
  - docs/database/NF-DBS-003.md
  - docs/api/NF-API-001.md
  - docs/agents/NF-AGENT-001.md
  - docs/prompts/NF-PROMPT-002.md
  - docs/pipeline/NF-PIPE-003.md
  - docs/rag/NF-RAG-001.md
  - docs/quality/NF-QA-001.md
  - docs/implementation/NF-IMPL-001.md
  - docs/implementation/NF-IMPL-002.md
  - docs/llm/NF-LLM-001.md
  - docs/tasks/NF-TASK-001.md
  - docs/contracts/NF-CONTRACT-001.md
  - docs/security/NF-SEC-001.md
  - docs/ai/NF-AI-001.md
---

# NF-IMPL-003

# Service Build Plan

# 1. Purpose and Build Boundary

本文档定义 Novel Factory MVP 的服务构建计划。

NF-IMPL-002 定义 MVP 交付范围。NF-IMPL-003 将该范围拆成可进入代码实现的仓库结构、服务模块、数据库迁移、API/任务契约、AI Worker、前端页面、测试与交付顺序。

## 1.1 Build Goal

构建目标：

- 建立可运行的 monorepo skeleton。
- 启动 web、api-gateway、core-service、ai-worker、scheduler。
- 通过 Docker Compose 启动 PostgreSQL、Redis、MinIO。
- 实现从 Source Import 到 Writing Studio 单章成稿的 MVP 主链路。
- 确保 trace、task、audit、object_ref、quality_report 和 feedback_record 可用。

## 1.2 Build Boundary

本文档定义实现顺序和模块契约，不定义完整业务代码、完整 DDL 或视觉设计稿。

具体实现时，应将本文档拆成开发任务或代码仓库 issue。任何偏离本文档的服务边界、表族、API envelope 或任务状态模型都必须更新 NF-IMPL-003 或对应权威规范。

## 1.3 Non-Goals

本构建计划不包含：

- 云上生产部署。
- 多租户计费。
- 发布平台接入。
- 独立图数据库或专用向量数据库。
- 全自动长篇连载。
- 大规模读者行为埋点。

# 2. Repository and Runtime Structure

## 2.1 Monorepo Structure

MVP 代码仓库推荐结构：

```text
apps/
├── web/
├── api-gateway/
├── core-service/
├── ai-worker/
└── scheduler/
packages/
├── contracts/
│   ├── openapi/
│   ├── schemas/
│   └── fixtures/
├── shared-types/
├── prompt-schemas/
├── config/
└── ui/
infra/
├── docker-compose.yml
├── postgres/
├── redis/
└── minio/
scripts/
└── dev/
```

## 2.2 Package Responsibilities

| Path                    | Responsibility                                                                     |
| ----------------------- | ---------------------------------------------------------------------------------- |
| apps/web                | React + TypeScript + pnpm + shadcn/ui frontend                                     |
| apps/api-gateway        | Frontend-facing BFF, auth context, envelope, trace propagation                     |
| apps/core-service       | MVP domain modules and PostgreSQL writes                                           |
| apps/ai-worker          | LLM, extraction, retrieval, planning, generation, critic, humanizer, quality tasks |
| apps/scheduler          | retries, timeout scan, stale projection scan, periodic maintenance                 |
| packages/contracts      | OpenAPI 3.1, JSON Schema, task contracts, review action enums, response envelopes  |
| packages/shared-types   | cross-app TypeScript types generated from contracts where possible                 |
| packages/prompt-schemas | prompt package, memory package and structured output schemas                       |
| packages/config         | model profile, provider config, quality threshold defaults                         |
| packages/ui             | shared shadcn/ui wrappers and project UI primitives                                |

## 2.3 Runtime Processes

Local MVP runtime:

```text
web -> api-gateway -> core-service
api-gateway -> ai-worker command queue
ai-worker -> postgres / redis / minio / provider adapter
scheduler -> postgres / redis
```

API Gateway may call core-service synchronously for reads and simple mutations. Long-running operations must create tasks and be executed by ai-worker.

## 2.4 Development Commands

Expected developer commands:

```sh
pnpm install
pnpm contracts:lint
pnpm contracts:generate
pnpm dev
pnpm test
pnpm lint
docker compose up -d postgres redis minio
```

Python worker dependencies may be managed inside apps/ai-worker with a dedicated environment tool, but local orchestration must remain documented in one root developer guide.

# 3. Service Module Contracts

## 3.1 API Gateway Contract

API Gateway responsibilities:

- Authenticate actor or service account.
- Generate or propagate request_id and trace_id.
- Validate envelope shape.
- Route frontend requests to core-service or task creation endpoint.
- Normalize errors into NF-API-001 error envelope.

API Gateway must not directly write domain tables except gateway-owned session or auth metadata if implemented.

## 3.2 Core Service Modules

Core Service modules:

| Module    | Owns                                                                                         | Commands                                                                           |
| --------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Workspace | users, workspaces, workspace_members                                                         | create_workspace, add_member                                                       |
| Book      | source_books, source_chapters, source_files                                                  | create_book, attach_source_file, update_import_status                              |
| Task      | tasks, task_events                                                                           | create_task, append_task_event, transition_task                                    |
| Knowledge | knowledge_objects, object_aliases, object_versions                                           | create_candidate, approve_object, reject_object, merge_alias                       |
| Graph     | graph_nodes, graph_edges, graph_snapshots                                                    | upsert_graph_node, upsert_graph_edge, create_graph_snapshot                        |
| Project   | novel_projects, story_bibles, chapter_plans, scene_plans                                     | create_project, update_story_bible, create_chapter_plan, approve_chapter_direction |
| Review    | review_reports, review_items, approval_records                                               | create_review_report, submit_review_action                                         |
| Feedback  | feedback_records, ranking_suggestions                                                        | capture_feedback, create_ranking_suggestion, review_suggestion                     |
| Config    | model_profiles, agent_model_assignments, provider_accounts, quality_thresholds, config_rules | create_model_profile, update_agent_model_assignment, update_quality_threshold      |
| Audit     | audit_events                                                                                 | append_audit_event                                                                 |

## 3.3 AI Worker Modules

AI Worker modules:

| Module          | Task Types                                                         |
| --------------- | ------------------------------------------------------------------ |
| Ingestion       | ingest_book, segment_chapters                                      |
| Extraction      | extract_knowledge, normalize_candidates                            |
| Graph Builder   | build_story_graph                                                  |
| Retrieval       | assemble_memory_package                                            |
| Planning        | plan_chapter, plan_scene_and_beats                                 |
| Prompt Assembly | assemble_prompt_package                                            |
| Generation      | generate_chapter_draft, rewrite_blocked_sections, assemble_chapter |
| Critic          | critic_review_chapter                                              |
| Humanizer       | humanize_chapter                                                   |
| Quality         | run_quality_gate                                                   |
| Feedback        | capture_feedback                                                   |

AI Worker may read approved knowledge and task payloads, but persistent state transitions must go through Core Service commands or owned task update APIs.

External writing APIs expose chapter-level writing runs and section-level recovery units. Beat remains an internal planning concept inside `section_plans.payload` unless a later UI explicitly promotes Beat to a first-class resource.

## 3.4 Boundary Rules

- No module writes another module's owned table without command boundary.
- No provider SDK leaks outside ai-worker provider adapter.
- No generated draft enters manuscript without Review Module approval.
- No feedback suggestion changes config without Review Module approval.

# 4. Database Migration Plan

## 4.1 Migration Order

MVP migrations should land in this order:

1. identity and workspace tables.
2. task and audit tables.
3. source and object storage metadata tables.
4. evidence tables.
5. knowledge and review tables.
6. graph tables.
7. project planning tables.
8. prompt and memory tables.
9. generation and quality tables.
10. feedback and config tables.

Physical table names, schema ownership, ULID rules, embedding table rules and migration boundaries are defined by NF-DBS-003.

This order allows early slices to run without waiting for writing-specific tables.

## 4.2 Required Table Families

MVP table families must match NF-IMPL-002:

- identity
- source
- task
- evidence
- knowledge
- graph
- review
- project
- prompt
- memory
- generation
- quality
- feedback
- config
- audit

## 4.3 Universal Columns

Persistent tables should include:

- id
- workspace_id when scoped
- lifecycle_status or status when applicable
- created_at
- updated_at
- created_by or actor_id when user initiated
- trace_id for mutation lineage

Versioned or review-sensitive tables should include:

- version
- review_status
- source_snapshot_id when reading knowledge state

## 4.4 Object Reference Rule

Tables that reference large text, reports or diff payloads must store object_ref instead of inline large payloads.

object_ref metadata must include checksum, byte_size, mime_type, owner_ref, access_policy and created_at.

## 4.5 Seed Data

MVP seed data must include:

- local admin user.
- default workspace.
- default model profiles.
- default agent model assignments.
- default quality thresholds.
- default config rules.
- minimal prompt templates.

Seed data must be safe for local development and must not include secrets.

# 5. API, Task and Event Contracts

## 5.1 API Envelope

All HTTP responses must follow NF-API-001 envelope:

```json
{
  "data": {},
  "meta": {
    "request_id": "REQ-000001",
    "trace_id": "TRC-000001"
  },
  "errors": []
}
```

Errors must include code, message, target and recovery_hint when possible.

## 5.2 Task Contract

Task record fields:

- task_id
- task_type
- workspace_id
- owner_module
- input_refs
- output_refs
- status
- progress
- idempotency_key
- retry_count
- error_code
- created_at
- started_at
- finished_at

Allowed status:

```text
queued
running
retrying
succeeded
failed
cancelled
requires_review
blocked
```

Task queue, lease, retry, scheduler recovery and idempotency semantics are defined by NF-TASK-001.

## 5.3 Task Event Contract

Task event fields:

- task_event_id
- task_id
- event_type
- message
- payload_ref or payload_json
- created_at

Required event_type:

- created
- started
- progress
- retry_scheduled
- review_required
- blocked
- failed
- succeeded

## 5.4 Command Contract

Worker command payload must include:

- command_id
- task_id
- task_type
- workspace_id
- input_refs
- idempotency_key
- trace_id
- requested_by

Worker result must include:

- task_id
- status
- output_refs
- metrics
- errors
- trace_id

## 5.5 Domain Event Contract

MVP domain events are internal and persisted through task_events or audit_events.

Allowed initial events:

- source_book_created
- ingestion_completed
- knowledge_candidate_created
- knowledge_object_approved
- graph_snapshot_created
- chapter_plan_created
- writing_run_created
- section_accepted
- chapter_accepted
- quality_gate_failed
- feedback_record_created

# 6. AI Worker and Provider Adapter Plan

## 6.1 Provider Adapter Interface

Provider adapter must expose a provider-neutral call boundary:

```text
generate_structured(model_profile_id, prompt_package_ref, output_schema_ref, trace_id)
generate_text(model_profile_id, prompt_package_ref, trace_id)
embed_text(model_profile_id, text_ref, trace_id)
rerank(model_profile_id, query_ref, candidate_refs, trace_id)
```

Each call returns:

- provider_call_id
- model_profile_id
- output_ref or output_json
- prompt_tokens
- completion_tokens
- latency_ms
- retry_count
- cost_estimate
- status
- error_code

## 6.2 Model Profile

model_profile must include:

- model_profile_id
- provider_name
- provider_model_name
- display_name
- capability_tags
- supported_call_types
- max_context_tokens
- max_output_tokens
- default_temperature
- cost_weight
- quality_weight
- latency_weight
- enabled
- fallback_profile_ids
- version

Provider credentials must not be stored in documentation or committed configuration.

## 6.3 Agent Model Assignment

AI Worker must not select provider model names directly.

Before every model call, AI Worker resolves:

```text
agent_role + task_type + output_mode + optional genre_scope
↓
agent_model_assignment
↓
model_profile_id
↓
provider adapter
```

MVP may configure a single default assignment for all generation and structured-output tasks. The database and config package must still support multiple assignments so that Writer, Critic, Humanizer, Extraction and Planning can later use different models without code changes.

Required assignment fields:

- assignment_id
- agent_role
- task_type
- output_mode
- primary_model_profile_id
- fallback_model_profile_ids
- selection_policy
- max_retry
- max_cost
- enabled

## 6.4 Structured Output Validation

AI Worker must validate structured outputs for:

- extraction candidates.
- chapter plans.
- beat plans.
- critic reports.
- quality reports.
- feedback records.

Invalid structured output consumes retry budget. Repeated failure transitions task to requires_review.

## 6.5 Writing Task Sequence

MVP Creator-facing writing sequence:

```text
assemble_memory_package
↓
assemble_prompt_package
↓
generate_chapter_draft
↓
critic_review_chapter
↓
auto_rewrite_blocked_sections
↓
humanize_chapter
↓
assemble_chapter
↓
run_quality_gate
↓
capture_feedback
```

Each step must persist output_refs before the next step starts.

Internal Scene, Beat or Section runs may exist, but they are implementation details under the writing_run.

## 6.6 Cost Guardrails

AI Worker must stop automatic processing when:

- retry budget is exceeded.
- model call returns policy or lifecycle violation.
- quality gate returns blocking issue.
- projected cost exceeds configured task budget.
- required memory package or prompt package is stale.

Provider error normalization, structured output validation strategy, streaming behavior and cost calculation are defined by NF-AI-001.

## 6.7 MVP to Multi-Model Evolution

MVP starts with one default model profile. The implementation must still seed assignment rows for each Agent role:

- extraction_default
- normalization_default
- planning_default
- memory_default
- style_analyzer_default
- writer_default
- critic_default
- humanizer_default
- review_default
- feedback_default

Initially these assignments can point to the same model_profile_id. Later releases can update assignment configuration to route Writer to a Chinese long-form model, Critic to a structured reasoning model, Humanizer to a rewriting model, and Memory/RAG to a long-context model.

# 7. Frontend Build Plan

## 7.1 Frontend Stack

Frontend must use:

- React
- TypeScript
- pnpm
- shadcn/ui preferred for common components

The MVP frontend is a working tool surface, not a marketing site.

## 7.2 Route Groups

MVP route groups:

```text
/workspaces/:workspaceId
/sources
/sources/:bookId
/extraction-runs/:runId
/knowledge/review
/graph
/projects
/projects/:projectId
/projects/:projectId/planner
/projects/:projectId/writing/:writingRunId
/feedback
/configuration
```

## 7.3 Shared UI Components

Shared components:

- AppShell
- WorkspaceSwitcher
- TaskStatusBadge
- TraceLinkList
- ReviewActionPanel
- EvidencePanel
- QualityScorePanel
- CostMetricPanel
- SectionList
- DraftDiffViewer

## 7.4 Page Data Rule

Pages must read state from API responses and task status. Frontend must not invent lifecycle state locally.

Long-running operations should show task progress, latest task event, retry_count and next required action.

## 7.5 Writing Studio Minimum Behavior

Writing Studio must allow:

- selecting a section or viewing internal Beat plan details.
- starting a writing_run.
- viewing Memory Package summary.
- viewing Writer output.
- viewing Critic issues.
- accepting Humanizer output.
- running chapter assembly.
- viewing Quality Gate result.
- submitting human review action.

## 7.6 Frontend Test Scope

MVP frontend tests should cover:

- task status rendering.
- review action form validation.
- Writing Studio state transitions.
- quality score panel thresholds.
- trace link rendering.

# 8. Testing, Observability and CI

## 8.1 Test Layers

MVP must include:

- unit tests for contracts and schema validation.
- service tests for core module commands.
- worker tests for task lifecycle and retry budget.
- API tests for envelope, errors and idempotency.
- frontend tests for key workflow states.
- end-to-end smoke test for MVP demo script.

## 8.2 Contract Tests

Contract tests must validate:

- response envelope shape.
- task status enum.
- review action enum.
- provider adapter result shape.
- quality report shape.
- feedback record shape.

## 8.3 Observability Fields

Every request, task and model call must include or propagate:

- request_id
- trace_id
- workspace_id
- actor_id or agent_role
- status
- latency
- error_code

Model calls also require prompt_tokens, completion_tokens, retry_count and cost_estimate.

## 8.4 Audit Tests

Audit tests must verify audit_event creation for:

- approving knowledge object.
- accepting chapter into manuscript.
- changing model profile.
- changing quality threshold.
- promoting feedback suggestion.

## 8.5 CI Minimum Gate

MVP CI should run:

```sh
pnpm lint
pnpm contracts:lint
pnpm contracts:test
pnpm test
python scripts/build_docs.py --check
```

If Python worker has its own test command, it must be added to CI before ai-worker tasks become production-critical.

# 9. Delivery Order, Risks and Change Log

## 9.1 Recommended Build Order

Recommended build order:

1. Repository skeleton and local infrastructure.
2. API envelope, trace middleware and task model.
3. Source import and object storage metadata.
4. Knowledge extraction placeholder and review workflow.
5. Graph snapshot and basic graph browse.
6. Project, Story Bible and planning records.
7. Memory Package and Prompt Package contracts.
8. Provider adapter, model profile and agent assignment config.
9. Chapter generation, Critic and Humanizer tasks.
10. Chapter Assembly, Quality Gate and Feedback.
11. Writing Studio integration.
12. MVP demo script and CI smoke test.

## 9.2 Slice Review Gate

Each slice must pass:

- tests for touched contracts and modules.
- API envelope checks for new endpoints.
- task lifecycle check for long tasks.
- trace_id propagation check.
- documentation update when contract changes.

## 9.3 Key Build Risks

| Risk                                    | Mitigation                                               |
| --------------------------------------- | -------------------------------------------------------- |
| Contract drift between web and services | Put DTOs and enums in packages/contracts                 |
| Worker bypasses service ownership       | Require Core Service commands for persistent transitions |
| Provider SDK spreads across codebase    | Keep provider SDK only inside adapter module             |
| Migration order blocks early slices     | Create identity, task, source and audit first            |
| Writing Studio becomes too large        | Build state panels separately and compose page late      |
| Quality gate too vague for tests        | Start with explicit score fields and threshold fixtures  |

## 9.4 Boundaries

NF-IMPL-003 defines service build order and implementation contracts. It does not replace detailed code-level implementation plans, migrations or API OpenAPI schemas.

## 9.5 References

- NF-IMPL-001
- NF-IMPL-002
- NF-ARCH-002
- NF-DBS-002
- NF-API-001
- NF-AGENT-001
- NF-PROMPT-002
- NF-PIPE-003
- NF-RAG-001
- NF-QA-001

## 9.6 Approval

Document Status: Draft

Next Review: Service build plan review

Next Document: Repository Scaffold Implementation Plan

## 9.7 Change Log

| Version | Date       | Author                            | Change                            |
| ------- | ---------- | --------------------------------- | --------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Implementation Team | Initial service build plan draft. |
