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
