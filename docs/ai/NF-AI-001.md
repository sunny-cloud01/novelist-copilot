---
document_id: NF-AI-001
title: AI Runtime Implementation Plan
version: 1.0.0
status: Draft
category: AI Runtime Specification
owner: Novel Factory AI Platform Team
created: 2026-07-11
updated: 2026-07-11
dependencies:
  - NFES-000
  - NF-LLM-001
  - NF-TASK-001
  - NF-CONTRACT-001
  - NF-SEC-001
  - NF-RAG-001
  - NF-QA-001
references:
  - docs/standards/NFES-000.md
  - docs/llm/NF-LLM-001.md
  - docs/tasks/NF-TASK-001.md
  - docs/contracts/NF-CONTRACT-001.md
  - docs/security/NF-SEC-001.md
  - docs/rag/NF-RAG-001.md
  - docs/quality/NF-QA-001.md
---

# NF-AI-001

# AI Runtime Implementation Plan

# 1. Runtime Boundary

本文档定义 AI Worker 的实现级运行边界，包括 provider adapter、model router、structured output、streaming、prompt/object storage、质量评分和成本记录。

## 1.1 Runtime Modules

AI Worker MVP 模块：

| Module            | Responsibility                                   |
| ----------------- | ------------------------------------------------ |
| model_router      | resolve agent_model_assignment and model_profile |
| provider_adapter  | provider-neutral model calls                     |
| prompt_runtime    | load prompt_package_ref and redact logs          |
| structured_output | schema validation and repair budget              |
| retrieval_runtime | assemble Memory Package                          |
| writing_runtime   | run chapter/section generation steps             |
| quality_runtime   | run Critic, Humanizer and Quality Gate           |
| cost_runtime      | estimate and record token cost                   |

## 1.2 Call Path

Every model call follows：

```text
task handler
↓
load task + workspace config
↓
resolve agent_model_assignment
↓
resolve model_profile + provider_account.secret_ref
↓
load prompt package from object_ref
↓
call provider adapter
↓
validate output
↓
persist output_ref + llm_call_record
```

No task handler may call provider SDK directly.

## 1.3 Streaming Decision

MVP Provider Adapter must support non-streaming calls.

Streaming is optional for MVP UI. If implemented, streaming chunks are transient UI events and are not system of record. Final generated text must still be persisted to Object Storage and referenced by output_ref.

# 2. Structured Output and Provider Errors

## 2.1 Structured Output Strategy

MVP structured output uses JSON Schema validation after provider response.

Preferred provider features：

1. native JSON schema or structured output mode when available。
2. JSON mode when schema mode is unavailable。
3. plain text JSON extraction only as fallback。

Validation flow：

```text
raw provider response
↓
parse JSON
↓
validate JSON Schema
↓
if invalid and retry budget remains: retry with validation error summary
↓
if still invalid: requires_review
```

Schema repair counts against retry budget.

## 2.2 Provider Error Taxonomy

Provider errors normalize to：

| Error Code                 | Task Result                 |
| -------------------------- | --------------------------- |
| provider_timeout           | retrying                    |
| provider_rate_limited      | retrying                    |
| provider_auth_failed       | blocked                     |
| provider_model_unavailable | fallback or retrying        |
| provider_policy_block      | blocked                     |
| provider_context_exceeded  | fallback or requires_review |
| provider_invalid_response  | retrying or requires_review |
| provider_unknown_error     | retrying then failed        |

## 2.3 Safety and Lifecycle Errors

Policy or lifecycle violations do not silently fallback to a weaker model.

If provider blocks content because of safety policy, task status becomes `blocked` and a task_event records sanitized reason.

If task attempts to alter Approved Knowledge outside review flow, task status becomes `blocked` with `lifecycle_violation`.

# 3. Model Cost, Quality and Acceptance

## 3.1 Cost Calculation

`cost_runtime` calculates estimated cost using model_profile price config.

Required price fields in config payload：

- input_token_unit_cost
- output_token_unit_cost
- currency
- price_effective_at

Cost estimate formula：

```text
(prompt_tokens * input_token_unit_cost) + (completion_tokens * output_token_unit_cost)
```

If price config is missing, model call may proceed in local MVP but must record `cost_estimate_status=missing_price_config`.

## 3.2 Quality Runtime

Quality Runtime combines：

- deterministic checks for forbidden changes, missing refs and paragraph length。
- Critic Agent structured review。
- Humanizer diff validation。
- originality similarity checks against source evidence refs。

Quality scores must store evidence or affected_text_ref when blocking.

## 3.3 Chapter / Section Runtime

External UI resource is chapter-level writing_run.

Internal execution unit is section_run. Beat is a planning concept inside `section_plans.payload` and should not be exposed as a required external API resource.

Required run refs：

- writing_run_id
- section_run_ids
- memory_package_id
- prompt_package_id
- chapter_draft_id
- quality_report_id
- llm_call_record_ids

## 3.4 Acceptance Checklist

AI Runtime is ready to implement when：

- default model_profile can call a test provider or mock provider。
- model_router resolves every MVP Agent role。
- structured output validation has pass and fail fixtures。
- provider errors map to normalized error codes。
- llm_call_records persist token and cost fields。
- section_run output is recoverable through object_ref。
- quality blocking issue references affected_text_ref。

## 3.5 Change Log

| Version | Date       | Changes                                 |
| ------- | ---------- | --------------------------------------- |
| 1.0.0   | 2026-07-11 | Initial AI runtime implementation plan. |
