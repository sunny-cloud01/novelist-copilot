---
document_id: NF-TASK-001
title: Task Queue, Worker Runtime and Recovery Specification
version: 1.0.0
status: Draft
category: Task Runtime Specification
owner: Novel Factory Platform Runtime Team
created: 2026-07-11
updated: 2026-07-11
dependencies:
  - NFES-000
  - NF-ARCH-002
  - NF-DBS-003
  - NF-IMPL-003
  - NF-LLM-001
references:
  - docs/standards/NFES-000.md
  - docs/architecture/NF-ARCH-002.md
  - docs/database/NF-DBS-003.md
  - docs/implementation/NF-IMPL-003.md
  - docs/llm/NF-LLM-001.md
---

# NF-TASK-001

# Task Queue, Worker Runtime and Recovery Specification

# 1. Runtime Decision

本文档定义 Novel Factory MVP 的后台任务队列、Worker 运行时、重试、租约、恢复和调度规则。

## 1.1 Queue Decision

MVP ai-worker 使用 Python worker runtime。队列库优先选择 Dramatiq + Redis broker。

选择理由：

- Python worker 与 LLM、抽取、RAG、质量检查同栈。
- Redis 已作为运行期协调组件。
- Dramatiq 比 Celery 更轻，适合 MVP；后续可迁移到 Celery 或云队列。

如果实现团队已有 Celery 标准，也可以替换为 Celery，但必须保留本文档定义的 PostgreSQL task source-of-truth、lease、idempotency 和 recovery 语义。

## 1.2 Source of Truth

PostgreSQL `ai.tasks` 是任务状态权威源。

Redis 只负责：

- queue delivery
- delayed retry wakeup
- short-lived worker coordination
- rate limit counters

Redis 消息丢失、重复投递或 worker 崩溃时，系统必须能通过 PostgreSQL task state 恢复。

## 1.3 Task Status

允许状态：

```text
queued
running
retrying
succeeded
failed
cancelled
requires_review
blocked
```

状态含义：

| Status          | Meaning                        |
| --------------- | ------------------------------ |
| queued          | 已创建，等待 worker 获取       |
| running         | worker 已获得 lease 并执行     |
| retrying        | 等待下一次自动重试             |
| succeeded       | 已完成并写入 output_refs       |
| failed          | 自动流程失败且不可恢复         |
| cancelled       | 用户或系统取消                 |
| requires_review | 需要人审或配置介入             |
| blocked         | 成本、质量、安全或依赖条件阻塞 |

## 1.4 Task Creation Rule

所有长任务必须先写入 `ai.tasks`，再投递 queue message。

创建顺序：

```text
validate command
↓
insert ai.tasks with status=queued
↓
insert ai.task_events created
↓
commit transaction
↓
publish queue message with task_id
```

如果 queue publish 失败，scheduler 必须能扫描 `queued` task 并重新投递。

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
