# 2. Lease, Retry and Idempotency

## 2.1 Worker Lease

Worker 开始执行前必须获取 task lease。

Lease 规则：

- 只有 `queued` 或到期的 `retrying` task 可以被执行。
- worker 使用 compare-and-set 将 status 改为 `running`。
- `ai.task_locks.lease_expires_at` 必须晚于当前时间。
- worker 必须定期 heartbeat。
- lease 到期后 scheduler 可以将 task 标记为 retrying 或 queued。

## 2.2 Idempotency

创建类 mutation 必须提供 idempotency_key。

规则：

- 同一 workspace 内，相同 idempotency_key 只能对应一个 active task。
- 重复请求返回已有 task_id。
- Worker step 必须先检查已有 output_refs，避免重复写入章节、报告或知识对象。

## 2.3 Retry Budget

任务表保存 `retry_count` 和 `max_retry`。

Retry 触发条件：

- transient provider error。
- Redis delivery duplicate with no completed output。
- object storage temporary failure。
- database serialization failure。
- structured output validation failure within budget。

不得 retry 的条件：

- permission_error。
- lifecycle_violation。
- originality_safety blocking。
- cost budget exceeded。
- approved knowledge mutation attempt。

## 2.4 Step Idempotency

多步骤任务必须为每个 step 写 output_ref。

示例 writing run：

```text
memory_package_id
prompt_package_id
chapter_draft_id
critic_report_id
humanizer_report_id
quality_report_id
feedback_record_id
```

Worker 重新进入时，从最后一个已完成 output_ref 后继续，不得从头重复调用模型。
