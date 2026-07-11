# 3. AI, Config and Vector Tables

## 3.1 Task Tables

`ai.tasks`：

- id
- workspace_id
- task_type
- owner_module
- status
- progress
- input_refs jsonb
- output_refs jsonb
- idempotency_key
- retry_count
- max_retry
- error_code
- created_at
- started_at
- finished_at
- trace_id

`ai.task_events`：

- id
- workspace_id
- task_id
- event_type
- message
- payload_json jsonb null
- payload_ref text null
- created_at

`ai.task_locks`：

- id
- task_id
- lock_owner
- lease_expires_at
- heartbeat_at
- created_at
- updated_at

## 3.2 Prompt and Memory Tables

`ai.prompt_packages`：

- id
- workspace_id
- prompt_template_id
- prompt_object_ref
- input_refs jsonb
- schema_version
- created_at
- trace_id

`ai.memory_packages`：

- id
- workspace_id
- project_id
- chapter_plan_id
- package_object_ref
- freshness_status
- source_snapshot_id
- schema_version
- created_at
- trace_id

`ai.retrieval_results`：

- id
- workspace_id
- memory_package_id
- source_channel
- target_ref
- relevance_score
- freshness
- evidence_refs jsonb
- created_at

## 3.3 LLM Call Records

`ai.llm_call_records`：

- id
- workspace_id
- task_id
- agent_role
- task_type
- assignment_id
- model_profile_id
- provider_name
- provider_model_name
- prompt_package_id
- input_refs jsonb
- output_ref
- prompt_tokens
- completion_tokens
- latency_ms
- retry_count
- cost_estimate
- status
- error_code
- fallback_from_call_id
- created_at
- trace_id

## 3.4 Config Tables

`config.model_profiles`：

- id
- provider_name
- provider_model_name
- display_name
- capability_tags text[]
- supported_call_types text[]
- max_context_tokens
- max_output_tokens
- default_temperature
- cost_weight
- quality_weight
- latency_weight
- enabled
- fallback_profile_ids text[]
- version
- created_at
- updated_at

`config.agent_model_assignments`：

- id
- agent_role
- task_type
- output_mode
- genre_scope null
- primary_model_profile_id
- fallback_model_profile_ids text[]
- selection_policy
- max_retry
- max_cost
- enabled
- created_at
- updated_at

`config.provider_accounts`：

- id
- provider_name
- account_label
- secret_ref
- status
- created_at
- updated_at

## 3.5 Embedding Tables

MVP 使用一个默认 embedding profile。默认向量维度必须在 seed config 中固定，PostgreSQL vector column 必须使用同一维度。

`ai.embedding_profiles`：

- id
- model_profile_id
- dimension
- distance_metric
- status
- created_at
- updated_at

`ai.embedding_records`：

- id
- workspace_id
- embedding_profile_id
- target_ref
- target_type
- source_object_ref
- chunk_index
- chunk_hash
- embedding vector
- created_at

如果后续新增不同 dimension 的 embedding profile，必须创建新的 physical table 或 migration，不得在同一 vector column 混用不同维度。
