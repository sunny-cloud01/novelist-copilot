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
