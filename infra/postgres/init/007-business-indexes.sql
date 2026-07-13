CREATE INDEX IF NOT EXISTS idx_source_books_workspace_title_author
    ON core.source_books (workspace_id, title, author_name);

CREATE UNIQUE INDEX IF NOT EXISTS idx_source_chapters_book_index
    ON core.source_chapters (book_id, chapter_index);

CREATE INDEX IF NOT EXISTS idx_evidence_records_book_chapter
    ON core.evidence_records (book_id, chapter_id);

CREATE INDEX IF NOT EXISTS idx_knowledge_objects_workspace_type_name
    ON core.knowledge_objects (workspace_id, object_type, canonical_name);

CREATE INDEX IF NOT EXISTS idx_extraction_runs_book_status
    ON core.extraction_runs (book_id, status);

CREATE INDEX IF NOT EXISTS idx_novel_projects_workspace_title
    ON core.novel_projects (workspace_id, title);

CREATE UNIQUE INDEX IF NOT EXISTS idx_chapter_plans_project_index
    ON core.chapter_plans (project_id, chapter_index);

CREATE INDEX IF NOT EXISTS idx_section_plans_chapter_index
    ON core.section_plans (chapter_plan_id, section_index);

CREATE INDEX IF NOT EXISTS idx_writing_runs_project_chapter
    ON ai.writing_runs (project_id, chapter_plan_id);

CREATE INDEX IF NOT EXISTS idx_provider_calls_writing_role
    ON ai.provider_calls (writing_run_id, agent_role);

CREATE INDEX IF NOT EXISTS idx_feedback_records_target
    ON core.feedback_records (target_type, target_id);

CREATE INDEX IF NOT EXISTS idx_audit_events_workspace_created_at
    ON audit.audit_events (workspace_id, created_at);

CREATE INDEX IF NOT EXISTS idx_source_scenes_chapter_index
    ON core.source_scenes (chapter_id, scene_index);

CREATE INDEX IF NOT EXISTS idx_story_events_scene_index
    ON core.story_events (scene_id, event_index);

CREATE INDEX IF NOT EXISTS idx_story_conflicts_book_chapter
    ON core.story_conflicts (book_id, chapter_id);

CREATE INDEX IF NOT EXISTS idx_story_hooks_book_chapter
    ON core.story_hooks (book_id, chapter_id);

CREATE INDEX IF NOT EXISTS idx_story_rewards_book_chapter
    ON core.story_rewards (book_id, chapter_id);

CREATE INDEX IF NOT EXISTS idx_story_climaxes_scope
    ON core.story_climaxes (scope_type, scope_id);

CREATE INDEX IF NOT EXISTS idx_relationship_edges_book_relation
    ON core.relationship_edges (book_id, relation_type);
