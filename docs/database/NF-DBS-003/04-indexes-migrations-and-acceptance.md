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
