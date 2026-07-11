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
