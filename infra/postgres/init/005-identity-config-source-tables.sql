CREATE TABLE IF NOT EXISTS identity.users (
    user_id text PRIMARY KEY,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS identity.workspaces (
    workspace_id text PRIMARY KEY,
    owner_user_id text,
    name text NOT NULL,
    slug text NOT NULL UNIQUE,
    default_language text,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS identity.workspace_members (
    workspace_member_id text PRIMARY KEY,
    workspace_id text NOT NULL REFERENCES identity.workspaces(workspace_id) ON DELETE CASCADE,
    user_id text NOT NULL,
    role text NOT NULL,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now(),
    UNIQUE (workspace_id, user_id)
);

CREATE TABLE IF NOT EXISTS config.model_profiles (
    model_profile_id text PRIMARY KEY,
    provider_name text NOT NULL,
    provider_model_name text NOT NULL,
    label text NOT NULL,
    enabled boolean NOT NULL DEFAULT true,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS config.provider_accounts (
    provider_account_id text PRIMARY KEY,
    provider_name text NOT NULL,
    account_label text NOT NULL,
    secret_ref text NOT NULL,
    status text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS config.agent_model_assignments (
    assignment_id text PRIMARY KEY,
    agent_role text NOT NULL,
    task_type text NOT NULL,
    model_profile_id text NOT NULL REFERENCES config.model_profiles(model_profile_id),
    enabled boolean NOT NULL DEFAULT true,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS config.quality_gate_profiles (
    quality_gate_profile_id text PRIMARY KEY,
    workspace_id text,
    label text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS config.prompt_versions (
    prompt_version_id text PRIMARY KEY,
    agent_role text NOT NULL,
    template_ref text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.source_books (
    book_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    title text NOT NULL,
    author_name text NOT NULL,
    source_type text NOT NULL,
    import_status text NOT NULL,
    source_content_ref text,
    content_checksum text,
    content_byte_size bigint,
    chapter_count integer NOT NULL DEFAULT 0,
    trace_id text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.source_contents (
    source_content_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    object_ref text NOT NULL UNIQUE,
    mime_type text NOT NULL,
    checksum text NOT NULL,
    byte_size bigint NOT NULL DEFAULT 0,
    content_text text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.source_chapters (
    chapter_id text PRIMARY KEY,
    book_id text NOT NULL REFERENCES core.source_books(book_id) ON DELETE CASCADE,
    chapter_index integer NOT NULL,
    title text NOT NULL,
    segmentation_status text NOT NULL,
    text_object_ref text,
    text_range text,
    raw_text text,
    text_excerpt text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz,
    updated_at timestamptz DEFAULT now(),
    UNIQUE (book_id, chapter_index)
);
