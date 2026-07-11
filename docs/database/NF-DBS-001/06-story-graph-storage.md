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
