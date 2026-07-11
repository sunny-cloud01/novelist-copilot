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
