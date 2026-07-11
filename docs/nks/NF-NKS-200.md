---
document_id: NF-NKS-200
title: Story Graph Model Specification
version: 1.0.0
status: Draft
category: Novel Knowledge Specification
owner: Novel Factory Knowledge Engineering Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
---

# NF-NKS-200

# Story Graph Model Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 的 Story Graph 模型规范。

Story Graph 用于表达 Character、Faction、Location、Event、Artifact、Rule、Foreshadowing、Pattern、Reward 和 Hook 等对象之间的结构化关系，使系统能够进行一致性检查、上下文召回、剧情规划和生成约束。

本文档覆盖：

- 图节点语义
- 图边语义
- 关系方向和证据要求
- 图快照
- 查询边界

本文档不覆盖数据库物理实现、图数据库产品选型、API 查询语法或具体 Prompt 模板。

# 2. Graph Model

## 2.1 Node Model

Story Graph Node 必须引用 NF-NKS-000 定义的领域对象。

每个节点至少包含：

- node_id
- object_id
- object_type
- lifecycle_status
- source_scope
- evidence_refs
- confidence

`object_id` 是节点的权威身份。`node_id` 只表示图中的节点实例，不得替代对象 ID。

## 2.2 Edge Model

Story Graph Edge 表示两个对象之间的有向关系。

每条边至少包含：

- edge_id
- source_object_id
- relation_type
- target_object_id
- direction
- temporal_scope
- evidence_refs
- confidence
- lifecycle_status

关系类型必须来自 NF-NKS-000 或对应模块规范的受控关系表。

## 2.3 Temporal Scope

Story Graph 必须支持关系随时间变化。

示例：

- Character A 在第 10 章前属于 Faction X。
- Character A 在第 20 章后背叛 Faction X。

此类关系必须通过 `temporal_scope` 或图快照表达，禁止直接覆盖历史关系。

## 2.4 Graph Snapshot

Graph Snapshot 表示某个 book、volume、chapter 或 generation context 下的图状态。

每个 Snapshot 至少包含：

- snapshot_id
- scope_type
- scope_id
- included_nodes
- included_edges
- generated_at
- source_version

Snapshot 用于生成上下文、回溯审核和一致性检查。

# 3. Validation, Boundaries and Change Log

## 3.1 Validation Rules

Story Graph 必须满足：

- 每个 node.object_id 指向已存在对象。
- 每条 edge 的 source_object_id 和 target_object_id 均存在。
- 每条关系必须绑定至少一条 evidence 或 review record。
- 关系变化不得覆盖历史关系。
- Deprecated 对象不得进入新的 generation context，除非用于历史回溯。

## 3.2 Boundaries

NF-NKS-200 定义图语义，不定义图数据库 Schema。数据库落地由 NF-DBS 文档负责。

## 3.3 References

- NF-NKS-000
- NF-NKS-001
- NF-NKS-100
- NF-DBS-001

## 3.4 Change Log

| Version | Date       | Author                                   | Change                                   |
| ------- | ---------- | ---------------------------------------- | ---------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial Story Graph model specification. |
