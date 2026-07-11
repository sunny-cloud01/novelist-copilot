---
document_id: NF-DBS-003
title: Physical Schema and Migration Plan
version: 1.0.0
status: Draft
category: Database Specification
owner: Novel Factory Data Architecture Team
created: 2026-07-11
updated: 2026-07-11
dependencies:
  - NFES-000
  - NF-DBS-001
  - NF-DBS-002
  - NF-ARCH-002
  - NF-IMPL-003
  - NF-LLM-001
references:
  - docs/standards/NFES-000.md
  - docs/database/NF-DBS-001.md
  - docs/database/NF-DBS-002.md
  - docs/architecture/NF-ARCH-002.md
  - docs/implementation/NF-IMPL-003.md
  - docs/llm/NF-LLM-001.md
---

# NF-DBS-003

# Physical Schema and Migration Plan

# 1. Purpose and Decisions

本文档将 NF-DBS-001 的逻辑 Schema 和 NF-DBS-002 的物理存储选型推进到可开工的 PostgreSQL 物理表、schema 边界、ID 规则、migration ownership 和 pgvector 落地规则。

## 1.1 Build Decisions

MVP 采用以下数据库实现决策：

| Topic                 | Decision                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------- |
| Database              | PostgreSQL 16 or later with pgvector enabled                                                |
| Physical schema split | identity, core, ai, config, audit                                                           |
| Primary key           | ULID text primary key                                                                       |
| Time fields           | timestamptz in UTC                                                                          |
| JSONB payload         | 必须包含 schema_version                                                                     |
| Large text            | Object Storage 保存正文，PostgreSQL 保存 object_ref                                         |
| Embedding             | MVP 使用单一默认 embedding dimension，后续新增 profile-specific table                       |
| Migration tool        | Alembic for Python-owned schemas; Prisma/Drizzle only if TypeScript service owns the schema |

## 1.2 Physical Schemas

PostgreSQL schema 分配：

| Schema   | Owner Runtime | Responsibility                                                            |
| -------- | ------------- | ------------------------------------------------------------------------- |
| identity | core-service  | users, workspaces, membership and service accounts                        |
| core     | core-service  | source, knowledge, graph, project, review, feedback and object metadata   |
| ai       | ai-worker     | tasks, prompt packages, memory packages, writing runs, model call records |
| config   | core-service  | model profiles, agent assignments, thresholds, feature flags              |
| audit    | core-service  | audit events, migration events and outbox events                          |

服务可以读取跨 schema 数据，但只能通过 owned command 或 migration ownership 写入自己负责的 schema。

## 1.3 ID Rule

所有主键使用 ULID text：

```text
01JZ0000000000000000000000
```

规则：

- 数据库主键字段统一命名为 `id`。
- 对外 API 可以暴露 resource-specific alias，例如 `book_id`，但底层仍保存 ULID。
- `trace_id`、`request_id`、`task_id` 使用同样 ULID 格式。
- 不使用自增整数作为跨服务引用。

## 1.4 Universal Columns

所有业务表必须包含：

- id text primary key
- created_at timestamptz not null
- updated_at timestamptz not null

workspace scoped 表还必须包含：

- workspace_id text not null

可被人或系统变更的表还必须包含：

- created_by text null
- updated_by text null
- trace_id text null

# 2. Core Table Baseline

本章定义 MVP 必须落地的核心表。字段是开工基线；实现可以添加索引和只读派生字段，但不得删除这里定义的生命周期、引用和审计字段。

## 2.1 Identity Tables

`identity.users`：

- id
- email
- display_name
- status
- created_at
- updated_at

`identity.workspaces`：

- id
- name
- owner_user_id
- status
- created_at
- updated_at

`identity.workspace_members`：

- id
- workspace_id
- user_id
- role
- status
- created_at
- updated_at

## 2.2 Source Tables

`core.source_books`：

- id
- workspace_id
- title
- author_name
- source_type
- import_status
- originality_policy_id
- created_at
- updated_at
- created_by
- trace_id

`core.source_files`：

- id
- workspace_id
- source_book_id
- object_ref
- checksum
- mime_type
- byte_size
- upload_status
- created_at
- updated_at

`core.source_chapters`：

- id
- workspace_id
- source_book_id
- chapter_index
- title
- text_object_ref
- checksum
- segmentation_status
- created_at
- updated_at

## 2.3 Knowledge and Evidence Tables

`core.knowledge_objects`：

- id
- workspace_id
- object_type
- canonical_name
- lifecycle_status
- review_status
- payload jsonb
- schema_version
- source_snapshot_id
- confidence
- created_at
- updated_at
- trace_id

`core.object_aliases`：

- id
- workspace_id
- knowledge_object_id
- alias_text
- alias_type
- created_at
- updated_at

`core.object_versions`：

- id
- workspace_id
- knowledge_object_id
- version
- payload jsonb
- change_reason
- created_at
- created_by
- trace_id

`core.evidence_records`：

- id
- workspace_id
- source_book_id
- source_chapter_id
- object_ref
- excerpt_hash
- location_payload jsonb
- created_at
- updated_at

`core.evidence_bindings`：

- id
- workspace_id
- evidence_record_id
- target_ref
- binding_type
- confidence
- created_at

## 2.4 Project and Generation Tables

`core.novel_projects`：

- id
- workspace_id
- title
- genre_scope
- status
- story_bible_id
- quality_gate_profile_id
- created_at
- updated_at

`core.story_bibles`：

- id
- workspace_id
- project_id
- version
- status
- payload jsonb
- schema_version
- created_at
- updated_at
- trace_id

`core.chapter_plans`：

- id
- workspace_id
- project_id
- chapter_index
- status
- target_word_count
- payload jsonb
- schema_version
- created_at
- updated_at

`core.section_plans`：

- id
- workspace_id
- chapter_plan_id
- section_index
- planning_role
- payload jsonb
- schema_version
- created_at
- updated_at

`ai.writing_runs`：

- id
- workspace_id
- project_id
- chapter_plan_id
- status
- task_id
- memory_package_id
- prompt_package_id
- chapter_draft_id
- quality_report_id
- created_at
- updated_at
- trace_id

`ai.section_runs`：

- id
- workspace_id
- writing_run_id
- section_plan_id
- status
- draft_object_ref
- critic_report_ref
- humanized_object_ref
- model_profile_id
- created_at
- updated_at

# 3. AI, Config and Vector Tables

## 3.1 Task Tables

`ai.tasks`：

- id
- workspace_id
- task_type
- owner_module
- status
- progress
- input_refs jsonb
- output_refs jsonb
- idempotency_key
- retry_count
- max_retry
- error_code
- created_at
- started_at
- finished_at
- trace_id

`ai.task_events`：

- id
- workspace_id
- task_id
- event_type
- message
- payload_json jsonb null
- payload_ref text null
- created_at

`ai.task_locks`：

- id
- task_id
- lock_owner
- lease_expires_at
- heartbeat_at
- created_at
- updated_at

## 3.2 Prompt and Memory Tables

`ai.prompt_packages`：

- id
- workspace_id
- prompt_template_id
- prompt_object_ref
- input_refs jsonb
- schema_version
- created_at
- trace_id

`ai.memory_packages`：

- id
- workspace_id
- project_id
- chapter_plan_id
- package_object_ref
- freshness_status
- source_snapshot_id
- schema_version
- created_at
- trace_id

`ai.retrieval_results`：

- id
- workspace_id
- memory_package_id
- source_channel
- target_ref
- relevance_score
- freshness
- evidence_refs jsonb
- created_at

## 3.3 LLM Call Records

`ai.llm_call_records`：

- id
- workspace_id
- task_id
- agent_role
- task_type
- assignment_id
- model_profile_id
- provider_name
- provider_model_name
- prompt_package_id
- input_refs jsonb
- output_ref
- prompt_tokens
- completion_tokens
- latency_ms
- retry_count
- cost_estimate
- status
- error_code
- fallback_from_call_id
- created_at
- trace_id

## 3.4 Config Tables

`config.model_profiles`：

- id
- provider_name
- provider_model_name
- display_name
- capability_tags text[]
- supported_call_types text[]
- max_context_tokens
- max_output_tokens
- default_temperature
- cost_weight
- quality_weight
- latency_weight
- enabled
- fallback_profile_ids text[]
- version
- created_at
- updated_at

`config.agent_model_assignments`：

- id
- agent_role
- task_type
- output_mode
- genre_scope null
- primary_model_profile_id
- fallback_model_profile_ids text[]
- selection_policy
- max_retry
- max_cost
- enabled
- created_at
- updated_at

`config.provider_accounts`：

- id
- provider_name
- account_label
- secret_ref
- status
- created_at
- updated_at

## 3.5 Embedding Tables

MVP 使用一个默认 embedding profile。默认向量维度必须在 seed config 中固定，PostgreSQL vector column 必须使用同一维度。

`ai.embedding_profiles`：

- id
- model_profile_id
- dimension
- distance_metric
- status
- created_at
- updated_at

`ai.embedding_records`：

- id
- workspace_id
- embedding_profile_id
- target_ref
- target_type
- source_object_ref
- chunk_index
- chunk_hash
- embedding vector
- created_at

如果后续新增不同 dimension 的 embedding profile，必须创建新的 physical table 或 migration，不得在同一 vector column 混用不同维度。

# 4. Indexes, Migrations and Acceptance

## 4.1 Required Indexes

MVP 必须创建以下索引族：

- workspace scoped tables: `(workspace_id, created_at)`。
- lifecycle tables: `(workspace_id, status)` or `(workspace_id, lifecycle_status, review_status)`。
- task idempotency: unique `(workspace_id, idempotency_key)` where idempotency_key is not null。
- source chapter order: unique `(workspace_id, source_book_id, chapter_index)`。
- graph edges: `(workspace_id, source_ref, relation_type)` and `(workspace_id, target_ref, relation_type)`。
- LLM calls: `(workspace_id, task_id, created_at)` and `(workspace_id, model_profile_id, created_at)`。
- audit events: `(workspace_id, target_ref, created_at)`。

Vector index for MVP：

- `ivfflat` or `hnsw` may be used after enough rows exist.
- Before data volume is meaningful, sequential vector scan is acceptable for local MVP.

## 4.2 Migration Ownership

Migration ownership：

| Schema   | Migration Owner |
| -------- | --------------- |
| identity | core-service    |
| core     | core-service    |
| ai       | ai-worker       |
| config   | core-service    |
| audit    | core-service    |

规则：

- 一个 migration 只能修改一个 owner 的 schema。
- 跨 schema 变更必须拆成 expand、backfill、contract 三步。
- 破坏性 migration 必须有 rollback_strategy 和 local seed validation。
- 所有 migration 执行记录写入 `audit.migration_events`。

## 4.3 Outbox Tables

`audit.outbox_events`：

- id
- workspace_id
- aggregate_ref
- event_type
- payload_json
- status
- retry_count
- next_attempt_at
- created_at
- processed_at
- trace_id

Outbox event 使用 at-least-once 语义。消费者必须使用 event id 或 aggregate version 做幂等处理。

## 4.4 Acceptance Checklist

数据库开工前必须满足：

- PostgreSQL 本地容器启用 pgvector。
- 所有 schema 可由 migration 创建。
- seed data 包含 default workspace、default model profile、agent assignments 和 quality thresholds。
- `scripts/build_docs.py --check` 通过。
- migration test 能从空库建出 identity、core、ai、config、audit schema。
- 禁止在 seed、Markdown 或测试夹具中写入真实 provider secret。

## 4.5 Change Log

| Version | Date       | Changes                                     |
| ------- | ---------- | ------------------------------------------- |
| 1.0.0   | 2026-07-11 | Initial physical schema and migration plan. |
