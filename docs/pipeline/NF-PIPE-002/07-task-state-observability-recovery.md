# 7. Task State, Observability and Recovery

## 7.1 Generation Run

每次生成流水线必须创建 generation_run。

最小字段：

- run_id
- generation_request_id
- pipeline_version
- status
- current_stage
- input_refs
- output_refs
- idempotency_key
- retry_count
- started_at
- finished_at

## 7.2 Stage Status

标准 stage status：

```text
pending -> running -> succeeded
pending -> skipped
running -> failed
running -> requires_review
running -> retrying -> running
```

## 7.3 Checkpoints

建议 checkpoint：

- context_retrieval_completed
- chapter_plan_created
- prompt_package_created
- draft_generated
- consistency_review_completed
- revision_completed
- ai_quality_review_completed
- human_review_completed
- feedback_captured

失败恢复必须从最近安全 checkpoint 继续。

## 7.4 Error Categories

生成流水线错误至少分为：

- retrieval_error
- prompt_assembly_error
- llm_provider_error
- output_validation_error
- consistency_violation
- revision_limit_exceeded
- review_required
- storage_error
- projection_error
- unknown_error

## 7.5 Observability Signals

必须记录：

- generation_latency
- retrieval_latency
- prompt_token_count
- completion_token_count
- revision_round_count
- consistency_violation_count
- AI_flavor_signal
- human_edit_distance
- approval_rate
- rejection_rate
- provider_error_rate

## 7.6 Recovery Rule

LLM provider transient failure 可以重试。

知识冲突、角色偏离、世界规则冲突和高 AI_flavor_signal 不应盲目重试，必须进入修订或人工审核。
