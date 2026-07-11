# 5. MVP Data and Storage Scope

## 5.1 Storage Baseline

MVP 使用：

- PostgreSQL + pgvector as system of record。
- MinIO as local S3-compatible object storage。
- Redis as runtime coordination。

不引入独立图数据库、专用向量数据库或搜索集群。

## 5.2 MVP Table Families

MVP 表族：

| Family     | Required Examples                                          |
| ---------- | ---------------------------------------------------------- |
| identity   | users, workspaces, workspace_members                       |
| source     | source_books, source_chapters, source_files                |
| task       | tasks, task_events                                         |
| evidence   | evidence_records, evidence_bindings                        |
| knowledge  | knowledge_objects, object_aliases, object_versions         |
| graph      | graph_nodes, graph_edges, graph_snapshots                  |
| review     | review_reports, review_items, approval_records             |
| project    | novel_projects, story_bibles, chapter_plans, section_plans |
| prompt     | prompt_templates, prompt_packages                          |
| memory     | memory_packages, retrieval_results                         |
| generation | writing_runs, section_runs, chapter_drafts, revision_diffs |
| quality    | quality_reports, quality_gate_runs                         |
| feedback   | feedback_records, ranking_suggestions                      |
| config     | model_profiles, quality_thresholds, config_rules           |
| audit      | audit_events                                               |

## 5.3 Object Storage Objects

Object Storage 保存：

- uploaded_source_file
- normalized_book_text
- chapter_text_snapshot
- extraction_package
- memory_package_snapshot
- prompt_package_snapshot
- section_draft_text
- humanized_section_text
- assembled_chapter_text
- quality_report_payload
- revision_diff_payload

PostgreSQL 保存 object_ref、checksum、byte_size、owner_ref、created_at 和 access_policy。

## 5.4 Trace Requirements

MVP 必须能从 accepted chapter 追踪到：

- source evidence。
- approved knowledge。
- memory_package_id。
- prompt_package_id。
- writing_run_id。
- section_run_id。
- model_profile_id。
- quality_report_id。
- feedback_record_id。

## 5.5 Migration Rule

MVP migration 必须按表族分组。破坏性迁移必须记录 rollback_strategy，并在本地种子数据上验证。
