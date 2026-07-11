# 2. Core Table Baseline

本章定义 MVP 必须落地的核心表。字段是开工基线；实现可以添加索引和只读派生字段，但不得删除这里定义的生命周期、引用和审计字段。

## 2.1 Identity Tables

`identity.users`：

- id
- email
- display_name
- status
- created_at
- updated_at

`identity.workspaces`：

- id
- name
- owner_user_id
- status
- created_at
- updated_at

`identity.workspace_members`：

- id
- workspace_id
- user_id
- role
- status
- created_at
- updated_at

## 2.2 Source Tables

`core.source_books`：

- id
- workspace_id
- title
- author_name
- source_type
- import_status
- originality_policy_id
- created_at
- updated_at
- created_by
- trace_id

`core.source_files`：

- id
- workspace_id
- source_book_id
- object_ref
- checksum
- mime_type
- byte_size
- upload_status
- created_at
- updated_at

`core.source_chapters`：

- id
- workspace_id
- source_book_id
- chapter_index
- title
- text_object_ref
- checksum
- segmentation_status
- created_at
- updated_at

## 2.3 Knowledge and Evidence Tables

`core.knowledge_objects`：

- id
- workspace_id
- object_type
- canonical_name
- lifecycle_status
- review_status
- payload jsonb
- schema_version
- source_snapshot_id
- confidence
- created_at
- updated_at
- trace_id

`core.object_aliases`：

- id
- workspace_id
- knowledge_object_id
- alias_text
- alias_type
- created_at
- updated_at

`core.object_versions`：

- id
- workspace_id
- knowledge_object_id
- version
- payload jsonb
- change_reason
- created_at
- created_by
- trace_id

`core.evidence_records`：

- id
- workspace_id
- source_book_id
- source_chapter_id
- object_ref
- excerpt_hash
- location_payload jsonb
- created_at
- updated_at

`core.evidence_bindings`：

- id
- workspace_id
- evidence_record_id
- target_ref
- binding_type
- confidence
- created_at

## 2.4 Project and Generation Tables

`core.novel_projects`：

- id
- workspace_id
- title
- genre_scope
- status
- story_bible_id
- quality_gate_profile_id
- created_at
- updated_at

`core.story_bibles`：

- id
- workspace_id
- project_id
- version
- status
- payload jsonb
- schema_version
- created_at
- updated_at
- trace_id

`core.chapter_plans`：

- id
- workspace_id
- project_id
- chapter_index
- status
- target_word_count
- payload jsonb
- schema_version
- created_at
- updated_at

`core.section_plans`：

- id
- workspace_id
- chapter_plan_id
- section_index
- planning_role
- payload jsonb
- schema_version
- created_at
- updated_at

`ai.writing_runs`：

- id
- workspace_id
- project_id
- chapter_plan_id
- status
- task_id
- memory_package_id
- prompt_package_id
- chapter_draft_id
- quality_report_id
- created_at
- updated_at
- trace_id

`ai.section_runs`：

- id
- workspace_id
- writing_run_id
- section_plan_id
- status
- draft_object_ref
- critic_report_ref
- humanized_object_ref
- model_profile_id
- created_at
- updated_at
