CREATE TABLE IF NOT EXISTS core.extraction_runs (
    run_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    workspace_id text NOT NULL,
    task_id text,
    status text NOT NULL,
    current_stage text,
    knowledge_package_ref text,
    graph_package_ref text,
    extraction_report_ref text,
    quality_report_ref text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.evidence_records (
    evidence_id text PRIMARY KEY,
    evidence_ref text NOT NULL UNIQUE,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    chapter_id text REFERENCES core.source_chapters(chapter_id) ON DELETE SET NULL,
    chapter_index integer,
    text_range text NOT NULL,
    excerpt text NOT NULL,
    source_content_ref text,
    confidence numeric NOT NULL DEFAULT 0,
    trace_id text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.knowledge_objects (
    object_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    object_type text NOT NULL,
    canonical_name text NOT NULL,
    lifecycle_status text NOT NULL,
    review_status text NOT NULL,
    confidence numeric NOT NULL DEFAULT 0,
    trace_id text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.extraction_run_objects (
    run_id text NOT NULL REFERENCES core.extraction_runs(run_id) ON DELETE CASCADE,
    object_id text NOT NULL REFERENCES core.knowledge_objects(object_id) ON DELETE CASCADE,
    PRIMARY KEY (run_id, object_id)
);

CREATE TABLE IF NOT EXISTS core.extraction_run_evidences (
    run_id text NOT NULL REFERENCES core.extraction_runs(run_id) ON DELETE CASCADE,
    evidence_id text NOT NULL REFERENCES core.evidence_records(evidence_id) ON DELETE CASCADE,
    PRIMARY KEY (run_id, evidence_id)
);

CREATE TABLE IF NOT EXISTS core.evidence_bindings (
    evidence_id text NOT NULL REFERENCES core.evidence_records(evidence_id) ON DELETE CASCADE,
    target_ref text NOT NULL,
    target_type text,
    PRIMARY KEY (evidence_id, target_ref)
);

CREATE TABLE IF NOT EXISTS core.object_aliases (
    alias_id text PRIMARY KEY,
    object_id text NOT NULL REFERENCES core.knowledge_objects(object_id) ON DELETE CASCADE,
    alias text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS core.object_versions (
    object_version_id text PRIMARY KEY,
    object_id text NOT NULL REFERENCES core.knowledge_objects(object_id) ON DELETE CASCADE,
    version integer NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.graph_snapshots (
    graph_snapshot_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    workspace_id text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.graph_nodes (
    node_id text PRIMARY KEY,
    book_id text NOT NULL,
    label text NOT NULL,
    node_type text NOT NULL,
    canonical_object_id text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.graph_edges (
    edge_id text PRIMARY KEY,
    source_node_id text NOT NULL,
    target_node_id text NOT NULL,
    relation_type text NOT NULL,
    confidence numeric,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.novel_projects (
    project_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    title text NOT NULL,
    genre_scope text,
    status text NOT NULL,
    story_bible_id text,
    quality_gate_profile_id text,
    allowed_knowledge_source_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.story_bibles (
    story_bible_id text PRIMARY KEY,
    project_id text NOT NULL REFERENCES core.novel_projects(project_id) ON DELETE CASCADE,
    workspace_id text NOT NULL,
    version integer NOT NULL DEFAULT 1,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    trace_id text,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.chapter_plans (
    chapter_plan_id text PRIMARY KEY,
    project_id text NOT NULL REFERENCES core.novel_projects(project_id) ON DELETE CASCADE,
    workspace_id text NOT NULL,
    chapter_index integer NOT NULL,
    status text NOT NULL,
    target_word_count integer,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now(),
    UNIQUE (project_id, chapter_index)
);

CREATE TABLE IF NOT EXISTS core.section_plans (
    section_plan_id text PRIMARY KEY,
    chapter_plan_id text NOT NULL REFERENCES core.chapter_plans(chapter_plan_id) ON DELETE CASCADE,
    workspace_id text NOT NULL,
    section_index integer NOT NULL,
    planning_role text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now(),
    UNIQUE (chapter_plan_id, section_index)
);

CREATE TABLE IF NOT EXISTS ai.writing_runs (
    writing_run_id text PRIMARY KEY,
    project_id text NOT NULL,
    chapter_plan_id text NOT NULL,
    workspace_id text NOT NULL,
    task_id text,
    status text NOT NULL,
    current_stage text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ai.section_runs (
    section_run_id text PRIMARY KEY,
    writing_run_id text NOT NULL REFERENCES ai.writing_runs(writing_run_id) ON DELETE CASCADE,
    section_plan_id text,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ai.memory_packages (
    memory_package_id text PRIMARY KEY,
    writing_run_id text,
    workspace_id text NOT NULL,
    summary text,
    source_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ai.prompt_packages (
    prompt_package_id text PRIMARY KEY,
    writing_run_id text,
    workspace_id text NOT NULL,
    summary text,
    template_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ai.provider_calls (
    provider_call_id text PRIMARY KEY,
    writing_run_id text,
    workspace_id text NOT NULL,
    agent_role text NOT NULL,
    model_profile_id text,
    provider_name text,
    provider_model_name text,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.quality_reports (
    quality_report_id text PRIMARY KEY,
    writing_run_id text,
    workspace_id text NOT NULL,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.consistency_reports (
    consistency_report_id text PRIMARY KEY,
    writing_run_id text,
    workspace_id text NOT NULL,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.revision_summaries (
    revision_summary_id text PRIMARY KEY,
    writing_run_id text,
    workspace_id text NOT NULL,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.chapter_snapshots (
    chapter_snapshot_id text PRIMARY KEY,
    writing_run_id text,
    project_id text NOT NULL,
    chapter_plan_id text,
    accepted_chapter_ref text,
    chapter_text text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE core.chapter_snapshots
    ADD COLUMN IF NOT EXISTS accepted_chapter_ref text;

CREATE TABLE IF NOT EXISTS core.manuscript_states (
    manuscript_state_id text PRIMARY KEY,
    project_id text NOT NULL,
    writing_run_id text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.feedback_records (
    feedback_record_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    target_type text NOT NULL,
    target_id text NOT NULL,
    feedback_type text NOT NULL,
    score numeric,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.ranking_snapshots (
    ranking_snapshot_id text PRIMARY KEY,
    ranking_type text NOT NULL,
    scope_ref text NOT NULL,
    version integer NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.rules (
    rule_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    rule_type text NOT NULL,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.patterns (
    pattern_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    pattern_type text NOT NULL,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.rhythm_profiles (
    rhythm_profile_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    target_id text,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.assets (
    asset_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    asset_type text NOT NULL,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS audit.audit_events (
    audit_event_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    action text NOT NULL,
    target_type text NOT NULL,
    target_id text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS audit.migration_events (
    migration_id text PRIMARY KEY,
    snapshot_hash text,
    affected_tables jsonb NOT NULL DEFAULT '[]'::jsonb,
    row_counts jsonb NOT NULL DEFAULT '{}'::jsonb,
    rollback_note text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.source_scenes (
    scene_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    chapter_id text NOT NULL REFERENCES core.source_chapters(chapter_id) ON DELETE CASCADE,
    workspace_id text NOT NULL,
    scene_index integer NOT NULL,
    title text NOT NULL,
    text_range text NOT NULL,
    segmentation_status text NOT NULL,
    segmentation_confidence numeric NOT NULL DEFAULT 0,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now(),
    UNIQUE (chapter_id, scene_index)
);

CREATE TABLE IF NOT EXISTS core.story_events (
    event_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    chapter_id text NOT NULL REFERENCES core.source_chapters(chapter_id) ON DELETE CASCADE,
    scene_id text REFERENCES core.source_scenes(scene_id) ON DELETE SET NULL,
    workspace_id text NOT NULL,
    event_index integer NOT NULL,
    event_type text NOT NULL,
    cause text NOT NULL,
    action text NOT NULL,
    result text NOT NULL,
    consequence text NOT NULL,
    participants jsonb NOT NULL DEFAULT '[]'::jsonb,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now(),
    UNIQUE (scene_id, event_index)
);

CREATE TABLE IF NOT EXISTS core.story_conflicts (
    conflict_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    chapter_id text NOT NULL REFERENCES core.source_chapters(chapter_id) ON DELETE CASCADE,
    scene_id text REFERENCES core.source_scenes(scene_id) ON DELETE SET NULL,
    workspace_id text NOT NULL,
    parties jsonb NOT NULL DEFAULT '[]'::jsonb,
    objective text NOT NULL,
    pressure text NOT NULL,
    escalation_level integer NOT NULL DEFAULT 0,
    resolution_state text NOT NULL,
    trigger_event_id text,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.story_hooks (
    hook_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    chapter_id text NOT NULL REFERENCES core.source_chapters(chapter_id) ON DELETE CASCADE,
    scene_id text REFERENCES core.source_scenes(scene_id) ON DELETE SET NULL,
    workspace_id text NOT NULL,
    hook_type text NOT NULL,
    open_question text NOT NULL,
    introduced_at text NOT NULL,
    expected_resolution_range text NOT NULL,
    linked_conflict_id text,
    linked_event_id text,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.story_rewards (
    reward_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    chapter_id text NOT NULL REFERENCES core.source_chapters(chapter_id) ON DELETE CASCADE,
    scene_id text REFERENCES core.source_scenes(scene_id) ON DELETE SET NULL,
    workspace_id text NOT NULL,
    reward_type text NOT NULL,
    trigger_event_id text,
    beneficiary_character_id text,
    reader_effect text NOT NULL,
    intensity numeric NOT NULL DEFAULT 0,
    payoff_target text,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.story_climaxes (
    climax_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    chapter_id text REFERENCES core.source_chapters(chapter_id) ON DELETE SET NULL,
    scene_id text REFERENCES core.source_scenes(scene_id) ON DELETE SET NULL,
    workspace_id text NOT NULL,
    scope_type text NOT NULL,
    scope_id text NOT NULL,
    event_id text,
    conflict_id text,
    reward_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    hook_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    intensity numeric NOT NULL DEFAULT 0,
    aftermath text NOT NULL,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.relationship_edges (
    edge_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    workspace_id text NOT NULL,
    source_id text NOT NULL,
    relation_type text NOT NULL,
    target_id text NOT NULL,
    confidence numeric NOT NULL DEFAULT 0,
    evidence_id text,
    evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);
