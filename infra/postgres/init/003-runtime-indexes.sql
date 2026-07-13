CREATE INDEX IF NOT EXISTS idx_runtime_tasks_status_next_retry_at
    ON runtime_tasks (status, next_retry_at);

CREATE INDEX IF NOT EXISTS idx_runtime_tasks_trace_id
    ON runtime_tasks (trace_id);

CREATE INDEX IF NOT EXISTS idx_runtime_tasks_idempotency_key
    ON runtime_tasks (idempotency_key);

CREATE INDEX IF NOT EXISTS idx_runtime_task_events_task_id_created_at
    ON runtime_task_events (task_id, created_at);

CREATE INDEX IF NOT EXISTS idx_runtime_task_locks_task_id
    ON runtime_task_locks (task_id);

CREATE INDEX IF NOT EXISTS idx_runtime_objects_owner_ref
    ON runtime_objects (owner_ref);
