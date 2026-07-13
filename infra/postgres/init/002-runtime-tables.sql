CREATE TABLE IF NOT EXISTS app_state_snapshots (
    snapshot_key text PRIMARY KEY,
    payload jsonb NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS runtime_objects (
    object_ref text PRIMARY KEY,
    workspace_id text NOT NULL,
    object_kind text NOT NULL,
    bucket text,
    storage_key text,
    checksum text,
    mime_type text,
    byte_size bigint,
    access_policy text,
    owner_ref text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS runtime_tasks (
    task_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    task_type text NOT NULL,
    owner_module text NOT NULL,
    status text NOT NULL,
    progress integer NOT NULL DEFAULT 0,
    idempotency_key text NOT NULL,
    request_id text,
    trace_id text,
    actor_id text,
    retry_count integer NOT NULL DEFAULT 0,
    max_retry_count integer NOT NULL DEFAULT 3,
    latency_ms integer,
    error_code text,
    lease_owner text,
    lease_expires_at timestamptz,
    heartbeat_at timestamptz,
    next_retry_at timestamptz,
    review_required boolean NOT NULL DEFAULT false,
    blocked_reason text,
    input_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    output_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
    created_at timestamptz,
    started_at timestamptz,
    finished_at timestamptz,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS runtime_task_locks (
    task_lock_id text PRIMARY KEY,
    task_id text NOT NULL,
    lock_owner text,
    lease_expires_at timestamptz,
    heartbeat_at timestamptz,
    created_at timestamptz,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS runtime_task_events (
    task_event_id text PRIMARY KEY,
    task_id text NOT NULL,
    workspace_id text NOT NULL,
    event_type text NOT NULL,
    status text NOT NULL,
    request_id text,
    trace_id text,
    actor_id text,
    agent_role text,
    message text NOT NULL,
    payload_ref text,
    payload_json jsonb,
    error_code text,
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS runtime_audit_events (
    audit_event_id text PRIMARY KEY,
    workspace_id text NOT NULL,
    request_id text,
    trace_id text,
    actor_id text,
    actor_role text,
    action text NOT NULL,
    target_type text NOT NULL,
    target_id text NOT NULL,
    target_ref text,
    before_ref text,
    after_ref text,
    reason text,
    payload jsonb,
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);
