---
document_id: NF-DBS-002
title: Physical Database and Storage Selection
version: 1.0.0
status: Draft
category: Database Specification
owner: Novel Factory Data Architecture Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-200
  - NF-NKS-210
  - NF-NKS-220
  - NF-NKS-230
  - NF-NKS-240
  - NF-NKS-250
  - NF-NKS-260
  - NF-NKS-270
  - NF-NKS-280
  - NF-NKS-290
  - NF-RAG-001
  - NF-QA-001
  - NF-ARCH-001
  - NF-DBS-001
  - NF-LLM-001
  - NF-DBS-003
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-200.md
  - docs/nks/NF-NKS-210.md
  - docs/nks/NF-NKS-220.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-240.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-260.md
  - docs/nks/NF-NKS-270.md
  - docs/nks/NF-NKS-280.md
  - docs/nks/NF-NKS-290.md
  - docs/rag/NF-RAG-001.md
  - docs/quality/NF-QA-001.md
  - docs/architecture/NF-ARCH-001.md
  - docs/database/NF-DBS-001.md
  - docs/llm/NF-LLM-001.md
  - docs/database/NF-DBS-003.md
---

# NF-DBS-002

# Physical Database and Storage Selection

# 1. Purpose and Scope

本文档定义 Novel Factory 第一阶段的物理数据库与存储选型。

NF-DBS-001 定义逻辑数据库规范，并保持实现中立。NF-DBS-002 在该逻辑模型之上给出可落地的后端存储架构，使拆书结果能够稳定支撑后续 AI 生成、检索、图谱推理、一致性检查和反馈回流。

本文档的核心目标不是追求一次性技术完备，而是为以下能力建立可演进的技术底座：

- 从原始书籍到结构化知识的可追踪存储。
- 从知识对象到 Story Graph、Pattern、Rhythm、Asset 和 Rule 的统一管理。
- 支持生成前上下文召回和生成后一致性检测。
- 支持人工审核、反馈闭环和版本演进。
- 在不牺牲数据一致性的前提下，为后续图数据库、专用向量库和搜索引擎预留升级路径。

本文档不定义 API 路由、业务 UI、LLM Prompt 模板或具体云厂商部署脚本。

# 2. Storage Stack Decision

## 2.1 Phase 1 Storage Stack

Novel Factory 第一阶段采用以下存储组合：

```text
PostgreSQL + pgvector
Object Storage
Redis
```

其中 PostgreSQL 是 system of record，Object Storage 保存大文本和包文件，Redis 保存任务状态、短期缓存和队列协调状态。

## 2.2 Phase 1 Responsibilities

| Component      | Responsibility                                                                              |
| -------------- | ------------------------------------------------------------------------------------------- |
| PostgreSQL     | 核心业务数据、知识对象、图边注册、审核、反馈、任务元数据、JSONB payload、pgvector embedding |
| Object Storage | 原文、标准化文本、抽取包、生成草稿、质量报告、长证据片段                                    |
| Redis          | Worker 队列、任务锁、短期缓存、Agent 协调状态、限流计数                                     |

## 2.3 Evolution Principle

第一阶段不直接引入独立图数据库、专用向量数据库和全文搜索集群。

原因：当前最重要的风险是知识模型、对象生命周期、证据链和审核状态仍在快速演进。过早拆分存储会增加迁移、调试和一致性成本。

## 2.4 Upgrade Targets

当 PostgreSQL 内部能力无法满足特定负载时，允许引入：

- Neo4j 或 Memgraph：复杂多跳 Story Graph 查询。
- Qdrant、Milvus 或 Weaviate：大规模向量检索和 embedding 实验。
- OpenSearch 或 Meilisearch：后台全文检索、标签检索和运营检索体验。

升级必须以 NF-DBS-001 的逻辑 Schema 和 NF-NKS 系列语义为边界，不得改变 canonical 对象身份。

# 3. PostgreSQL as System of Record

## 3.1 Primary Role

PostgreSQL 是 Novel Factory 第一阶段的权威数据源。

所有需要事务一致性、审核状态、版本追踪、对象生命周期或跨模块引用的数据，必须先进入 PostgreSQL。

## 3.2 Recommended Capabilities

第一阶段 PostgreSQL 必须启用或预留：

- JSONB：保存不同 NKS 对象的类型特定 payload。
- pgvector：保存章节、场景、角色、Pattern、Asset 和 Evidence embedding。
- Row-level timestamps：保存 created_at、updated_at 和 reviewed_at。
- Transactional migration：配合 Alembic 或等价 migration 工具。
- Stable primary keys：支持跨表、跨包和跨图谱引用。

## 3.3 Core Table Families

PostgreSQL 应承载以下表族：

| Family     | Examples                                                                                     |
| ---------- | -------------------------------------------------------------------------------------------- |
| source     | source_books, source_chapters, source_scenes                                                 |
| knowledge  | knowledge_objects, object_aliases, object_versions                                           |
| graph      | graph_nodes, graph_edges, graph_snapshots                                                    |
| evidence   | evidence_records, evidence_bindings                                                          |
| extraction | extraction_runs, extraction_errors, extraction_packages                                      |
| review     | review_reports, review_items, approval_records                                               |
| generation | generation_requests, chapter_drafts, revision_runs                                           |
| feedback   | feedback_records, ranking_signals, human_edits                                               |
| config     | config_rules, quality_thresholds, model_profiles, agent_model_assignments, provider_accounts |
| audit      | audit_events, migration_events, correction_events                                            |

## 3.4 JSONB Payload Rule

`knowledge_objects.payload` 可以使用 JSONB 保存 Character、Worldview、Pattern、Rhythm Profile、Asset、Rule 等类型特定属性。

JSONB 不得成为无约束垃圾箱。每种 object_type 必须由对应 NF-NKS 模块定义 payload 语义，并通过应用层 Pydantic schema 或等价 schema 校验。

## 3.5 Embedding Rule

pgvector embedding 应被视为派生数据。

权威文本、对象 ID、证据和审核状态必须存储在普通关系字段或 Object Storage 中。embedding 可以重算，不得作为唯一事实来源。

## 3.6 LLM Configuration Rule

`model_profiles` 保存 provider-neutral 模型能力配置，不保存密钥。

`agent_model_assignments` 保存 agent_role、task_type、output_mode 到 model_profile_id 的路由关系。

`provider_accounts` 只保存 provider account metadata、secret_ref 和启用状态。真实 API key 必须来自环境变量或 secret manager，不得写入 PostgreSQL 明文字段、Markdown、代码或测试夹具。

# 4. Object Storage and Redis

## 4.1 Object Storage Role

Object Storage 保存不适合直接进入 PostgreSQL 行字段的大文本和文件型资产。

推荐第一阶段使用 MinIO 本地兼容 S3 接口，后续可迁移到 S3-compatible 云存储。

## 4.2 Object Storage Data

Object Storage 保存：

- raw_text
- normalized_text
- source_file_uploads
- BookKnowledgePackage
- graph_package
- extraction_report
- quality_report
- generated_chapter_draft
- revision_diff
- long evidence excerpt

PostgreSQL 中只保存 object_ref、checksum、mime_type、byte_size、created_at 和 access policy。

## 4.3 Object Reference Rule

每个 object_ref 必须满足：

- 可追踪到创建任务或人工上传记录。
- 保存 checksum，支持完整性校验。
- 保存 logical owner，例如 book_id、chapter_id、extraction_run_id 或 generation_request_id。
- 不直接暴露永久公开 URL。

## 4.4 Redis Role

Redis 用于运行期协调，不作为权威数据源。

Redis 可保存：

- worker queue state
- task lock
- extraction progress cache
- generation progress cache
- rate limit counter
- short-lived retrieval cache
- agent orchestration heartbeat

Redis 中的数据必须可从 PostgreSQL 或 Object Storage 恢复，不能作为唯一事实来源。

# 5. Graph, Vector and Search Evolution

## 5.1 Story Graph Phase 1

第一阶段 Story Graph 使用 PostgreSQL 表保存 graph_nodes、graph_edges 和 graph_snapshots。

该方案适合：

- 单书或小规模跨书图谱。
- 审核友好的图边记录。
- 以 object_id、relation_type、chapter_scope、confidence 为主的查询。
- 生成前上下文召回。

## 5.2 Graph Database Upgrade Gate

满足以下条件之一时，可以引入 Neo4j 或 Memgraph：

- 多跳查询成为核心高频路径。
- PostgreSQL recursive query 无法满足交互式延迟要求。
- 需要图算法，例如 community detection、centrality、path ranking。
- 跨书知识图谱关系规模显著超过单库调优能力。

图数据库必须作为 projection store，不得替代 PostgreSQL 中的 canonical object identity。

## 5.3 Vector Search Phase 1

第一阶段使用 pgvector 支持：

- chapter embedding
- scene embedding
- character profile embedding
- pattern embedding
- asset embedding
- evidence excerpt embedding

pgvector 查询结果必须与 PostgreSQL 中的 lifecycle_status、review_status、genre_scope、source_scope 和 permission 过滤结合。

## 5.4 Dedicated Vector DB Upgrade Gate

满足以下条件之一时，可以引入 Qdrant、Milvus 或 Weaviate：

- embedding 数量达到 pgvector 维护成本明显上升的规模。
- 需要多 collection、多向量、多租户或复杂 ANN 调优。
- 需要高频在线召回并与生成流水线并发运行。
- embedding 实验迭代明显影响主库稳定性。

专用向量库必须保存 PostgreSQL object_id，不得生成新的知识对象身份。

## 5.5 Search Engine Upgrade Gate

满足以下条件之一时，可以引入 OpenSearch 或 Meilisearch：

- 后台运营需要复杂全文检索、模糊查询和聚合筛选。
- PostgreSQL full-text search 无法满足搜索体验。
- 需要跨字段、跨标签、跨题材的快速检索。

搜索引擎必须作为 read projection，不得成为写入入口。

# 6. Data Ownership, Migration and Consistency

## 6.1 Ownership Rule

每类数据必须有唯一权威写入方。

| Data                                | Owner                      |
| ----------------------------------- | -------------------------- |
| source_books, source_chapters       | Ingestion Service          |
| extraction_runs, extraction_errors  | Extraction Orchestrator    |
| knowledge_objects, object_aliases   | Knowledge Service          |
| graph_nodes, graph_edges            | Story Graph Service        |
| generation_requests, chapter_drafts | Generation Service         |
| review_reports, approval_records    | Review Service             |
| feedback_records, ranking_signals   | Feedback Service           |
| memory_packages, retrieval_results  | Retrieval Service          |
| quality_reports, quality_gate_runs  | Quality Service            |
| config_rules, quality_thresholds    | Rule Configuration Service |

其他服务只能通过 API、command 或 event 请求变更，不得直接绕过 owner 写入。

在微服务架构下，服务可以共享同一个 PostgreSQL 集群，但必须通过 schema、role、migration ownership 和应用层 contract 隔离写入边界。不得为了开发便利让多个服务共同写同一表族。

## 6.2 Migration Rule

所有 PostgreSQL schema 变更必须通过 migration 工具执行。

每个服务只能执行自己拥有 schema 或表族的 migration。跨服务 migration 必须拆分为兼容步骤，并通过 ADR 或 migration plan 记录依赖顺序。

Migration 必须记录：

- migration_id
- author
- reason
- affected_tables
- backward_compatibility
- rollback_strategy
- executed_at

破坏性迁移必须先导出受影响数据快照。

## 6.3 Projection Consistency

Graph database、Vector DB 和 Search Engine 都是 projection store。

Projection 必须保存 source_version 或 projection_version。当 projection 落后于 PostgreSQL 时，系统必须允许降级到 PostgreSQL 查询或标记结果为 stale。

## 6.4 Event and Outbox Rule

跨存储同步推荐使用 outbox pattern。

PostgreSQL 事务提交业务变更和 outbox event。Worker 从 outbox 读取事件，再更新向量、图谱、搜索或对象包。

该方式避免业务写入成功但 projection 更新失败时丢失同步信号。

## 6.5 Human Review Consistency

未通过审核的对象不得进入 Approved Knowledge Base 或正式 generation context。

生成系统只能读取：

- Approved 对象。
- 明确允许实验使用的 Reviewed 对象。
- 当前任务内的 candidate 对象，并必须在输出中标记 candidate 来源。

# 7. Deployment, Security and Observability

## 7.1 Local Development Stack

第一阶段本地开发推荐使用：

```text
React Web App
API Gateway / BFF
Domain Services
Worker Services
PostgreSQL with pgvector
Redis
MinIO
```

这些组件应通过 Docker Compose 或等价本地编排启动。每个应用服务应有独立容器、独立环境变量和明确健康检查。

## 7.2 Environment Separation

至少区分：

- local
- development
- staging
- production

生产环境不得直接复用开发环境对象存储 bucket、Redis namespace 或 PostgreSQL database。

## 7.3 Access Control

数据库访问必须按服务角色区分。

建议角色：

- api_gateway_rw
- book_service_rw
- knowledge_service_rw
- generation_service_rw
- review_service_rw
- worker_rw
- readonly_analytics
- migration_admin
- backup_operator

应用不得使用 migration_admin 执行普通运行期请求。

## 7.4 Secrets Rule

数据库密码、对象存储密钥、LLM API key 和 Redis credential 必须来自环境变量或 secret manager，不得写入 Markdown、代码或测试夹具。

## 7.5 Observability

存储层必须记录：

- query latency
- queue depth
- extraction run duration
- object storage write/read failure
- outbox lag
- projection lag
- embedding generation failure
- migration status
- backup status

这些指标应被 NF-OPS-001 的监控告警体系引用。

## 7.6 Backup and Recovery

PostgreSQL 必须定期备份，并支持 point-in-time recovery。

Object Storage 必须保存 checksum，并定期抽样验证文件可读性。

Redis 不要求持久化权威数据，但需要在重启后允许任务从 PostgreSQL 状态恢复。

# 8. Alternatives, Boundaries and Change Log

## 8.1 Alternatives Considered

### 8.1.1 Neo4j First

Rejected for Phase 1.

原因：Story Graph 语义和对象生命周期仍在演进。直接以图数据库为主库会增加迁移和审核复杂度。

### 8.1.2 Dedicated Vector DB First

Rejected for Phase 1.

原因：第一阶段 embedding 规模和召回策略尚未稳定。pgvector 足以支撑早期 RAG、相似 Pattern 和素材召回。

### 8.1.3 MongoDB First

Rejected for Phase 1.

原因：Novel Factory 需要强审计、强引用、审核状态和跨对象一致性。JSONB 已能覆盖半结构化 payload，而 PostgreSQL 提供更强事务边界。

### 8.1.4 Elasticsearch First

Rejected for Phase 1.

原因：全文检索不是第一阶段的权威存储核心。搜索引擎更适合作为后续 read projection。

## 8.2 Boundary Rules

NF-DBS-002 定义物理数据库与存储选型。

NF-DBS-002 不定义业务 API、Prompt 模板、Agent 推理策略、具体 ORM 代码或云厂商 Terraform 配置。

## 8.3 References

- NFES-000
- NF-PRD-001
- NF-NKS-000
- NF-NKS-001
- NF-NKS-100
- NF-NKS-200
- NF-NKS-210
- NF-NKS-220
- NF-NKS-230
- NF-NKS-240
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270
- NF-ARCH-001
- NF-DBS-001

## 8.4 Approval

Document Status: Draft

Next Review: Backend technical architecture review

Next Document: NF-ARCH-002 Backend Technical Architecture

## 8.5 Change Log

| Version | Date       | Author                               | Change                                                 |
| ------- | ---------- | ------------------------------------ | ------------------------------------------------------ |
| 1.0.0   | 2026-07-10 | Novel Factory Data Architecture Team | Initial physical database and storage selection draft. |
