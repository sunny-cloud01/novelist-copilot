# 3. Service Module Contracts

## 3.1 API Gateway Contract

API Gateway responsibilities:

- Authenticate actor or service account.
- Generate or propagate request_id and trace_id.
- Validate envelope shape.
- Route frontend requests to core-service or task creation endpoint.
- Normalize errors into NF-API-001 error envelope.

API Gateway must not directly write domain tables except gateway-owned session or auth metadata if implemented.

## 3.2 Core Service Modules

Core Service modules:

| Module    | Owns                                                                                         | Commands                                                                           |
| --------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Workspace | users, workspaces, workspace_members                                                         | create_workspace, add_member                                                       |
| Book      | source_books, source_chapters, source_files                                                  | create_book, attach_source_file, update_import_status                              |
| Task      | tasks, task_events                                                                           | create_task, append_task_event, transition_task                                    |
| Knowledge | knowledge_objects, object_aliases, object_versions                                           | create_candidate, approve_object, reject_object, merge_alias                       |
| Graph     | graph_nodes, graph_edges, graph_snapshots                                                    | upsert_graph_node, upsert_graph_edge, create_graph_snapshot                        |
| Project   | novel_projects, story_bibles, chapter_plans, scene_plans                                     | create_project, update_story_bible, create_chapter_plan, approve_chapter_direction |
| Review    | review_reports, review_items, approval_records                                               | create_review_report, submit_review_action                                         |
| Feedback  | feedback_records, ranking_suggestions                                                        | capture_feedback, create_ranking_suggestion, review_suggestion                     |
| Config    | model_profiles, agent_model_assignments, provider_accounts, quality_thresholds, config_rules | create_model_profile, update_agent_model_assignment, update_quality_threshold      |
| Audit     | audit_events                                                                                 | append_audit_event                                                                 |

## 3.3 AI Worker Modules

AI Worker modules:

| Module          | Task Types                                                         |
| --------------- | ------------------------------------------------------------------ |
| Ingestion       | ingest_book, segment_chapters                                      |
| Extraction      | extract_knowledge, normalize_candidates                            |
| Graph Builder   | build_story_graph                                                  |
| Retrieval       | assemble_memory_package                                            |
| Planning        | plan_chapter, plan_scene_and_beats                                 |
| Prompt Assembly | assemble_prompt_package                                            |
| Generation      | generate_chapter_draft, rewrite_blocked_sections, assemble_chapter |
| Critic          | critic_review_chapter                                              |
| Humanizer       | humanize_chapter                                                   |
| Quality         | run_quality_gate                                                   |
| Feedback        | capture_feedback                                                   |

AI Worker may read approved knowledge and task payloads, but persistent state transitions must go through Core Service commands or owned task update APIs.

External writing APIs expose chapter-level writing runs and section-level recovery units. Beat remains an internal planning concept inside `section_plans.payload` unless a later UI explicitly promotes Beat to a first-class resource.

## 3.4 Boundary Rules

- No module writes another module's owned table without command boundary.
- No provider SDK leaks outside ai-worker provider adapter.
- No generated draft enters manuscript without Review Module approval.
- No feedback suggestion changes config without Review Module approval.
