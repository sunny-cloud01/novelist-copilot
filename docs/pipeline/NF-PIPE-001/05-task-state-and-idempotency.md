# 5. Task State and Idempotency

## 5.1 Pipeline Run

每次流水线执行必须创建 pipeline_run。

最小字段：

- run_id
- book_id
- pipeline_version
- requested_by
- status
- current_stage
- input_refs
- output_refs
- idempotency_key
- started_at
- finished_at

## 5.2 Stage Status

标准 stage status：

```text
pending -> running -> succeeded
pending -> skipped
running -> failed
running -> requires_review
running -> retrying -> running
```

`requires_review` 表示自动流程无法安全继续。

## 5.3 Idempotency Rule

Pipeline 必须支持幂等重试。

同一个 book_id、source checksum、pipeline_version 和 idempotency_key 的重复请求，不得创建互相冲突的 source_book、chapter、scene、object 或 package。

## 5.4 Checkpoint Rule

每个重要阶段完成后必须写入 checkpoint。

建议 checkpoint：

- file_intake_completed
- normalization_completed
- chapter_segmentation_completed
- scene_segmentation_completed
- entity_extraction_completed
- relationship_extraction_completed
- review_completed
- package_export_completed

失败恢复必须从最近安全 checkpoint 继续，而不是默认重跑全流程。

## 5.5 Retry Policy

可重试错误：

- transient_llm_provider_error
- temporary_storage_error
- queue_timeout
- projection_update_failure

不可直接重试错误：

- invalid_source_format
- missing_required_metadata
- severe_chapter_order_conflict
- evidence_binding_failure
- schema_validation_failure

不可直接重试错误必须进入人工审核或人工修复流程。
