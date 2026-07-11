---
document_id: NF-CONTRACT-001
title: API, DTO and OpenAPI Contract Specification
version: 1.0.0
status: Draft
category: Contract Specification
owner: Novel Factory Platform Contract Team
created: 2026-07-11
updated: 2026-07-11
dependencies:
  - NFES-000
  - NF-API-001
  - NF-ARCH-002
  - NF-IMPL-003
  - NF-TASK-001
references:
  - docs/standards/NFES-000.md
  - docs/api/NF-API-001.md
  - docs/architecture/NF-ARCH-002.md
  - docs/implementation/NF-IMPL-003.md
  - docs/tasks/NF-TASK-001.md
---

# NF-CONTRACT-001

# API, DTO and OpenAPI Contract Specification

# 1. Contract Source of Truth

本文档定义 Novel Factory 的 API、DTO、OpenAPI、JSON Schema 和前后端 SDK 契约规则。

## 1.1 Decision

MVP 使用 OpenAPI 3.1 作为 HTTP API source of truth，JSON Schema 2020-12 作为结构化 payload source of truth。

约定：

- `packages/contracts/openapi/novel-factory.v1.yaml` 保存 HTTP API 契约。
- `packages/contracts/schemas/` 保存 JSON Schema。
- TypeScript client 和 server DTO 从 OpenAPI/JSON Schema 生成。
- Python ai-worker 使用 Pydantic model 从 JSON Schema 对齐或手写后由 contract test 校验。

## 1.2 Contract Ownership

| Contract                | Owner                    | Consumer                                |
| ----------------------- | ------------------------ | --------------------------------------- |
| OpenAPI HTTP endpoints  | api-gateway              | web, tests, external tools              |
| Task command schemas    | ai-worker + core-service | scheduler, worker modules               |
| Prompt package schemas  | ai-worker                | prompt assembly, provider adapter       |
| Quality report schemas  | quality module           | review UI, feedback module              |
| LLM call record schemas | ai-worker                | observability, feedback, cost dashboard |

## 1.3 Versioning

API version path：`/v1`。

Schema version fields：

- every JSONB payload must include `schema_version`。
- breaking schema changes increment major version。
- additive optional fields increment minor version。

## 1.4 Generated Artifacts

Generated artifacts may be committed only if the repo build requires them. If committed, generated files must include a generated marker and must not be manually edited.

Recommended generated outputs：

- `packages/shared-types/src/api.ts`
- `packages/shared-types/src/schemas.ts`
- `apps/web/src/api/client.ts`
- `apps/api-gateway/src/generated/contracts.ts`

# 2. Required Contracts

## 2.1 API Envelope

All endpoints must use the NF-API-001 envelope.

Response schema names：

- `ApiSuccessEnvelope`
- `ApiErrorEnvelope`
- `ApiError`
- `RequestMeta`

Required meta fields：

- request_id
- trace_id

## 2.2 Task Contracts

Required schemas：

- `Task`
- `TaskEvent`
- `CreateTaskCommand`
- `WorkerCommand`
- `WorkerResult`
- `TaskStatus`

`TaskStatus` enum values：

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

## 2.3 Domain Resource Contracts

MVP must define schemas for：

- Workspace
- SourceBook
- SourceChapter
- ExtractionRun
- KnowledgeObject
- EvidenceRecord
- GraphNode
- GraphEdge
- NovelProject
- StoryBible
- ChapterPlan
- SectionPlan
- WritingRun
- SectionRun
- ChapterDraft
- ReviewReport
- QualityReport
- FeedbackRecord
- ModelProfile
- AgentModelAssignment

## 2.4 Review Action Contract

Review action enum：

```text
approve
reject
request_change
merge_alias
request_reextract
accept_section
accept_chapter
request_rewrite
edit_and_accept
block_generation
```

`accept_beat` is not an external API action. Beat may remain an internal planning concept inside `SectionPlan.payload`.

# 3. Validation and CI

## 3.1 Contract Validation

CI must validate：

- OpenAPI file parses.
- all `$ref` targets resolve.
- generated TypeScript types are up to date.
- representative API responses match schemas.
- task command payloads match JSON Schema.
- Pydantic worker models can parse contract fixtures.

## 3.2 Compatibility Rule

Backward-compatible changes：

- add optional response field。
- add endpoint。
- add enum value only when clients are documented to tolerate unknown values。

Breaking changes：

- remove field。
- rename field。
- change type。
- make optional field required。
- change lifecycle semantics。

Breaking changes require `/v2` or explicit migration plan.

## 3.3 Fixture Rule

Each contract family must include at least one valid fixture and one invalid fixture.

Fixture path convention：

```text
packages/contracts/fixtures/{contract_family}/valid/*.json
packages/contracts/fixtures/{contract_family}/invalid/*.json
```

Fixtures must not contain provider secrets, full source book text or copyrighted samples.

## 3.4 Acceptance Checklist

Contract layer is ready when：

- `pnpm contracts:lint` validates OpenAPI and JSON Schema。
- `pnpm contracts:generate` regenerates TypeScript outputs。
- `pnpm contracts:test` validates fixtures。
- Python worker contract test loads task, prompt, memory and quality fixtures。

## 3.5 Change Log

| Version | Date       | Changes                                              |
| ------- | ---------- | ---------------------------------------------------- |
| 1.0.0   | 2026-07-11 | Initial API, DTO and OpenAPI contract specification. |
