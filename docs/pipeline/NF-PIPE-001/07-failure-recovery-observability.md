# 7. Failure Recovery and Observability

## 7.1 Error Categories

Pipeline 错误至少分为：

- source_format_error
- metadata_error
- normalization_error
- segmentation_error
- extraction_error
- evidence_binding_error
- object_normalization_error
- review_blocked
- package_export_error
- storage_error
- llm_provider_error
- unknown_error

## 7.2 Recovery Actions

每个错误必须指定 recovery_action。

允许值：

- retry
- resume_from_checkpoint
- require_human_fix
- require_human_review
- skip_with_reason
- abort_pipeline

## 7.3 Observability Signals

Pipeline 必须记录：

- run_duration
- stage_duration
- queue_wait_time
- llm_call_count
- token_usage
- object_count
- relationship_count
- evidence_count
- unresolved_object_ratio
- review_blocker_count
- retry_count
- package_export_size

## 7.4 Audit Rule

所有人工修正、状态覆盖、重新导出和强制通过操作必须写入 audit_events。

Audit record 必须包含 actor、action、reason、target_type、target_id、before_ref、after_ref 和 created_at。

## 7.5 Data Retention

原始输入、标准化文本、抽取包、审核报告和导出清单必须按 NF-OPS-001 的保留策略保存。

临时中间件缓存可以过期，但必须能从 PostgreSQL checkpoint 和 Object Storage artifact 恢复。
