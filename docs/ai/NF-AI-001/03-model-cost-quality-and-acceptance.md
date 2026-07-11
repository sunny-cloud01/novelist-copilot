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
