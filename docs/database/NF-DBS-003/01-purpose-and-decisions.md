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
