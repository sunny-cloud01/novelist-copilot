---
document_id: NF-DBS-001
title: Knowledge Database Specification
version: 1.0.0
status: Draft
category: Database Specification
owner: Novel Factory Data Architecture Team
created: 2026-07-09
updated: 2026-07-09
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
  - NF-ARCH-001
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
  - docs/architecture/NF-ARCH-001.md
---

# NF-DBS-001

# Knowledge Database Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 的 Knowledge Database 规范。

Knowledge Database 是承载 Book Library、Knowledge Base、Story Graph、Evidence、Review Report、Rule、Feedback 和运行审计数据的持久化基础。

本文档将 NF-NKS-000 的领域对象、NF-NKS-100 的 BookKnowledgePackage 和 NF-ARCH-001 的 Knowledge Storage Layer 转化为数据库级存储域、逻辑 Schema、约束、索引、迁移和备份规则。

## 1.1 Scope

本文档覆盖存储原则、存储域划分、逻辑 Schema 组、核心表或集合、Story Graph 存储模型、Evidence 与 Review 存储模型、索引与约束、数据生命周期、Migration 规则、备份与恢复要求。

本文档不覆盖 API 路径、请求体或响应体，Agent 工具调用流程，Prompt 模板正文，具体数据库产品选型或云厂商部署配置。

# 2. Storage Principles

## 2.1 Source Traceability

所有从小说文本抽取出的对象、关系和规则必须可追踪到 Evidence。

## 2.2 Logical Stability

逻辑 Schema 必须优先保持稳定。物理存储可以随技术选型演进，但跨模块数据语义不得随意变化。

## 2.3 Separation of Concerns

来源数据、规范化对象、图关系、证据、审查、反馈和运行日志必须分别建模。

## 2.4 Lifecycle Awareness

数据库必须保存对象生命周期状态。允许状态引用 NF-NKS-000：Extracted、Normalized、Reviewed、Approved、Deprecated。

## 2.5 Append-Friendly Audit

审计、抽取运行、人工审核和反馈数据应优先采用 append-friendly 记录方式，避免覆盖历史证据。

## 2.6 Implementation Neutrality

本文档定义逻辑数据库规范，不绑定 PostgreSQL、Neo4j、MongoDB、Elastic、Milvus 或其他具体产品。

# 3. Storage Domains

Novel Factory 推荐使用四类存储域：

```text
Relational Store
Graph Store
Object Store
Vector Index
```

## 3.1 Relational Store

Relational Store 负责保存强一致的核心对象、审查状态、运行记录、配置和引用关系。

适合数据：Book、Chapter、Scene、Canonical Objects、Evidence Metadata、Review Report、Extraction Run、Feedback Record。

## 3.2 Graph Store

Graph Store 负责保存 Story Graph 节点与关系，并支持多跳关系查询。

适合数据：Story Graph Node、Story Graph Edge、Relationship Confidence、Graph Snapshot。

## 3.3 Object Store

Object Store 负责保存大文本、原始文件、抽取包、导出包和质量报告。

适合数据：raw_text、normalized_text、BookKnowledgePackage、quality_report、generated_chapter_draft、long source excerpt。

## 3.4 Vector Index

Vector Index 负责支持语义检索、RAG、相似 Pattern 检索和素材召回。

适合数据：Chapter embedding、Scene embedding、Character profile embedding、Pattern embedding、Asset embedding、Evidence excerpt embedding。

# 4. Logical Schema Groups

逻辑 Schema 分为以下组：

| Group      | Responsibility                   |
| ---------- | -------------------------------- |
| source     | 原始来源、书籍、章节、文本边界   |
| knowledge  | 规范化知识对象                   |
| graph      | Story Graph 节点、边、快照       |
| evidence   | 原文证据、抽取证据、置信度       |
| extraction | 抽取运行、抽取报告、错误记录     |
| review     | 人工审核、审核状态、阻塞问题     |
| generation | 生成请求、章节草稿、质量信号     |
| feedback   | 评分、人工修改、读者反馈、排名   |
| config     | 规则配置、质量阈值、版本配置     |
| audit      | 操作审计、迁移记录、数据修正记录 |

# 5. Core Entities

## 5.1 source_books

Purpose: store Book source metadata.

Required logical fields: id, title, author, platform, genre, tags, word_count, completion_status, source, source_url, import_status, created_at, updated_at.

## 5.2 source_chapters

Purpose: store Chapter metadata and text references.

Required logical fields: id, book_id, chapter_index, title, text_range, raw_text_ref, normalized_text_ref, text_length, preprocessing_status, created_at, updated_at.

## 5.3 source_scenes

Purpose: store Scene boundaries and segmentation metadata.

Required logical fields: id, chapter_id, scene_index, text_range, location_id, primary_event_id, segmentation_confidence, created_at, updated_at.

## 5.4 knowledge_objects

Purpose: store canonical and candidate NKS objects.

Required logical fields: id, object_type, canonical_name, display_name, aliases, lifecycle_status, source_book_id, confidence, payload, created_at, updated_at.

Payload stores type-specific properties defined by NF-NKS-000 and refined by future schema documents.

## 5.5 object_aliases

Purpose: store aliases and normalization mappings.

Required logical fields: id, object_id, alias, alias_type, source_id, confidence, created_at.

## 5.6 graph_nodes

Purpose: store Story Graph node registry.

Required logical fields: id, object_id, node_type, lifecycle_status, graph_namespace, created_at, updated_at.

## 5.7 graph_edges

Purpose: store Story Graph relationships.

Required logical fields: id, source_node_id, relation_type, target_node_id, confidence, evidence_id, lifecycle_status, created_at, updated_at.

## 5.8 evidence_records

Purpose: store traceable evidence for objects, relationships, rules and extraction decisions.

Required logical fields: id, source_type, source_id, text_range, source_text_excerpt_ref, extraction_method, confidence, created_at.

## 5.9 extraction_runs

Purpose: store Book Knowledge Extraction execution records.

Required logical fields: id, book_id, extraction_version, extractor, status, started_at, finished_at, input_manifest_ref, output_package_ref.

## 5.10 extraction_errors

Purpose: store structured errors from NF-NKS-100 extraction stages.

Required logical fields: id, extraction_run_id, error_category, source_id, severity, message, recovery_action, created_at.

## 5.11 review_reports

Purpose: store human or AI review results.

Required logical fields: id, target_type, target_id, reviewer, review_status, blocking_issues, accepted_object_ids, rejected_object_ids, created_at.

## 5.12 feedback_records

Purpose: store feedback signals for Prompt, Pattern, Knowledge and Rule optimization.

Required logical fields: id, target_type, target_id, feedback_type, score, source, comment_ref, created_at.

## 5.13 config_rules

Purpose: store rule configuration and quality thresholds.

Required logical fields: id, rule_type, scope, statement, severity, validation_method, enabled, version, created_at, updated_at.

## 5.14 audit_events

Purpose: store data corrections, migrations and administrative operations.

Required logical fields: id, actor, action, target_type, target_id, before_ref, after_ref, reason, created_at.

# 6. Story Graph Storage Model

## 6.1 Node Rule

Every graph node must reference a knowledge object through object_id.

## 6.2 Edge Rule

Every graph edge must reference source_node_id, target_node_id, relation_type and evidence_id.

## 6.3 Namespace Rule

Graph namespaces allow separating:

- source-specific graph
- canonical knowledge graph
- generated-story graph
- experimental graph

## 6.4 Snapshot Rule

Important graph states should be snapshot-capable for review, rollback and comparison.

# 7. Evidence and Review Model

## 7.1 Evidence Requirement

The following records must be evidence-backed:

- knowledge_objects created from source text
- graph_edges
- extracted config_rules
- pattern records
- rhythm profile records
- contradiction candidates

## 7.2 Evidence Storage

Short excerpts may be stored inline when allowed by storage policy. Long excerpts and raw text must be stored in Object Store and referenced by source_text_excerpt_ref.

## 7.3 Review Status

Review status values:

- Pending
- Approved
- Rejected
- NeedsHumanReview
- Blocked

## 7.4 Blocking Issues

Blocking issues from NF-NKS-100 must be persisted in review_reports and linked to extraction_runs when applicable.

# 8. Indexing and Constraints

## 8.1 Required Relational Indexes

Required index groups:

- source_books(title, author)
- source_chapters(book_id, chapter_index)
- source_scenes(chapter_id, scene_index)
- knowledge_objects(object_type, lifecycle_status)
- knowledge_objects(source_book_id)
- object_aliases(alias)
- graph_edges(source_node_id, relation_type)
- graph_edges(target_node_id, relation_type)
- evidence_records(source_type, source_id)
- extraction_runs(book_id, extraction_version)
- review_reports(target_type, target_id)
- feedback_records(target_type, target_id)

## 8.2 Required Graph Indexes

Graph queries must optimize node by object_id, outgoing edges by relation_type, incoming edges by relation_type, and multi-hop traversal by node namespace.

## 8.3 Required Vector Indexes

Vector Index must support semantic retrieval for Chapter, Scene, Character profile, Pattern, Asset and Evidence excerpt.

## 8.4 ID Constraints

Object IDs must follow NF-NKS-000 ID Convention.

## 8.5 Referential Integrity

All graph_edges must reference existing graph_nodes.

All evidence-backed records must reference existing evidence_records or an approved external evidence reference.

## 8.6 Lifecycle Constraints

Deprecated objects must not be used for new generation tasks unless explicitly allowed by a reviewed compatibility rule.

## 8.7 Uniqueness Constraints

The following uniqueness constraints are required:

- source_chapters(book_id, chapter_index)
- source_scenes(chapter_id, scene_index)
- graph_edges(source_node_id, relation_type, target_node_id, evidence_id)
- config_rules(rule_type, scope, version)

## 8.8 Audit Constraints

Manual data changes to Approved or Frozen knowledge objects must create audit_events.

# 9. Migration, Backup, and Retention

## 9.1 Migration Record

Every schema migration must create a migration record containing migration_id, version, description, applied_at, actor and rollback_strategy.

## 9.2 Backward Compatibility

Minor and Patch migrations should preserve backward compatibility for canonical documents and approved data packages.

## 9.3 Data Backfill

Data backfill must be traceable and must not overwrite source evidence.

## 9.4 Rollback

Rollback must preserve audit_events and migration records.

## 9.5 Backup Scope

Backups must cover Relational Store, Graph Store, Object Store metadata, Vector Index rebuild manifests, migration records and audit_events.

## 9.6 Recovery Point

The system must define recovery points for source data, approved knowledge objects, graph snapshots, extraction packages and review reports.

## 9.7 Vector Index Recovery

Vector Index may be rebuilt from canonical objects, text references and embedding manifests. The rebuild process must be documented by NF-OPS.

## 9.8 Raw Source Retention

Raw source retention policy must preserve enough text reference to support evidence audit and legal review.

## 9.9 Deprecated Object Retention

Deprecated objects must remain queryable for historical references but excluded from default generation retrieval.

## 9.10 Audit Retention

Audit records must not be deleted during normal data cleanup.

# 10. Boundaries, References, and Change Log

## 10.1 Boundary Rules

NF-DBS-001 defines storage model, schema groups, logical fields, constraints, indexes, migration and backup rules.

NF-DBS-001 must not define API request schemas, Agent behavior, Prompt template content or runtime deployment procedures.

## 10.2 References

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

## 10.3 Approval

Document Status: Draft

Next Review: NF-DBS-001 Review

Next Document: NF-AGENT-001 Agent Collaboration Model

## 10.4 Change Log

| Version | Date       | Author                               | Change                                                       |
| ------- | ---------- | ------------------------------------ | ------------------------------------------------------------ |
| 1.0.0   | 2026-07-09 | Novel Factory Data Architecture Team | Initial Draft for Novel Factory knowledge database baseline. |
