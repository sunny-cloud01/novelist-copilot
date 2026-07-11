# 6. AI Worker and Provider Adapter Plan

## 6.1 Provider Adapter Interface

Provider adapter must expose a provider-neutral call boundary:

```text
generate_structured(model_profile_id, prompt_package_ref, output_schema_ref, trace_id)
generate_text(model_profile_id, prompt_package_ref, trace_id)
embed_text(model_profile_id, text_ref, trace_id)
rerank(model_profile_id, query_ref, candidate_refs, trace_id)
```

Each call returns:

- provider_call_id
- model_profile_id
- output_ref or output_json
- prompt_tokens
- completion_tokens
- latency_ms
- retry_count
- cost_estimate
- status
- error_code

## 6.2 Model Profile

model_profile must include:

- model_profile_id
- provider_name
- provider_model_name
- display_name
- capability_tags
- supported_call_types
- max_context_tokens
- max_output_tokens
- default_temperature
- cost_weight
- quality_weight
- latency_weight
- enabled
- fallback_profile_ids
- version

Provider credentials must not be stored in documentation or committed configuration.

## 6.3 Agent Model Assignment

AI Worker must not select provider model names directly.

Before every model call, AI Worker resolves:

```text
agent_role + task_type + output_mode + optional genre_scope
↓
agent_model_assignment
↓
model_profile_id
↓
provider adapter
```

MVP may configure a single default assignment for all generation and structured-output tasks. The database and config package must still support multiple assignments so that Writer, Critic, Humanizer, Extraction and Planning can later use different models without code changes.

Required assignment fields:

- assignment_id
- agent_role
- task_type
- output_mode
- primary_model_profile_id
- fallback_model_profile_ids
- selection_policy
- max_retry
- max_cost
- enabled

## 6.4 Structured Output Validation

AI Worker must validate structured outputs for:

- extraction candidates.
- chapter plans.
- beat plans.
- critic reports.
- quality reports.
- feedback records.

Invalid structured output consumes retry budget. Repeated failure transitions task to requires_review.

## 6.5 Writing Task Sequence

MVP Creator-facing writing sequence:

```text
assemble_memory_package
↓
assemble_prompt_package
↓
generate_chapter_draft
↓
critic_review_chapter
↓
auto_rewrite_blocked_sections
↓
humanize_chapter
↓
assemble_chapter
↓
run_quality_gate
↓
capture_feedback
```

Each step must persist output_refs before the next step starts.

Internal Scene, Beat or Section runs may exist, but they are implementation details under the writing_run.

## 6.6 Cost Guardrails

AI Worker must stop automatic processing when:

- retry budget is exceeded.
- model call returns policy or lifecycle violation.
- quality gate returns blocking issue.
- projected cost exceeds configured task budget.
- required memory package or prompt package is stale.

Provider error normalization, structured output validation strategy, streaming behavior and cost calculation are defined by NF-AI-001.

## 6.7 MVP to Multi-Model Evolution

MVP starts with one default model profile. The implementation must still seed assignment rows for each Agent role:

- extraction_default
- normalization_default
- planning_default
- memory_default
- style_analyzer_default
- writer_default
- critic_default
- humanizer_default
- review_default
- feedback_default

Initially these assignments can point to the same model_profile_id. Later releases can update assignment configuration to route Writer to a Chinese long-form model, Critic to a structured reasoning model, Humanizer to a rewriting model, and Memory/RAG to a long-context model.
