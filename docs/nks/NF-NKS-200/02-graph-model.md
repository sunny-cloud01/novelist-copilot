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
