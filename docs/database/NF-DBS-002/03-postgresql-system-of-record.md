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
