# 3. Scheduler, Recovery and Observability

## 3.1 Scheduler Responsibilities

scheduler 负责：

- 重新投递 queued 但未进入 Redis 的任务。
- 扫描 running 且 lease expired 的任务。
- 将 retrying 且 next_attempt_at 到期的任务重新投递。
- 标记超过 retry budget 的任务为 failed、blocked 或 requires_review。
- 记录 stale projection 和 outbox lag。

## 3.2 Recovery Rules

Worker 崩溃恢复：

1. scheduler 发现 lease expired。
2. 如果 retry_count < max_retry，状态转为 retrying。
3. 写入 task_event `retry_scheduled`。
4. 到达 next_attempt_at 后重新投递。
5. worker 根据 output_refs 跳过已完成 step。

Provider 失败恢复：

- transient failure: retrying。
- policy or safety failure: blocked。
- structured output repeated failure: requires_review。
- context too long: requires_review unless fallback model supports long_context。

## 3.3 Observability

每个 task event 必须包含：

- task_id
- task_type
- workspace_id
- event_type
- status_before
- status_after
- latency_ms when applicable
- error_code when applicable
- trace_id

必备指标：

- queue_depth by task_type
- running_task_count
- retrying_task_count
- failed_task_count
- blocked_task_count
- lease_expired_count
- average_task_latency_ms
- p95_task_latency_ms
- llm_retry_count
- cost_estimate by task_type

## 3.4 Acceptance Checklist

实现前必须确认：

- 本地 Redis broker 可启动。
- PostgreSQL task table 可创建 queued task。
- worker 能获取 lease 并执行 no-op task。
- scheduler 能恢复过期 running task。
- 重复 idempotency_key 返回同一 task_id。
- task_events 可以按 cursor 增量读取。

## 3.5 Change Log

| Version | Date       | Changes                                                        |
| ------- | ---------- | -------------------------------------------------------------- |
| 1.0.0   | 2026-07-11 | Initial task queue, worker runtime and recovery specification. |
