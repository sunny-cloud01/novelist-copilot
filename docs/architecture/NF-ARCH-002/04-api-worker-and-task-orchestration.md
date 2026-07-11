# 4. API, Worker and Task Orchestration

## 4.1 Runtime Processes

第一阶段至少包含：

```text
API Process
Worker Process
Scheduler Process
PostgreSQL
Redis
Object Storage
```

API Process 处理同步请求、状态查询、人工审核和管理操作。Worker Process 处理耗时任务。Scheduler Process 处理重试、超时扫描、周期性索引和后台维护任务。

## 4.2 API Boundary

API 不应直接执行长耗时 LLM 任务。

API 应创建任务记录并返回 task_id。客户端通过 task_id 查询进度、结果和错误状态。

适合 API 同步执行的操作：

- 创建 Book metadata。
- 查询任务状态。
- 查询知识对象。
- 提交人工审核结果。
- 创建 generation request。

不适合 API 同步执行的操作：

- 全书拆解。
- embedding 生成。
- 大规模 Story Graph 构建。
- 多轮章节生成和改写。
- 全量一致性检查。

## 4.3 Task Model

每个后台任务至少记录：

- task_id
- task_type
- owner_module
- input_refs
- output_refs
- status
- progress
- idempotency_key
- retry_count
- error_code
- started_at
- finished_at

任务状态必须保存在 PostgreSQL。Redis 只保存队列和运行期协调状态。

## 4.4 Idempotency Rule

所有可重试任务必须支持 idempotency_key。

同一个 idempotency_key 的重复请求不得创建多个互相冲突的抽取结果、生成结果或审核记录。

## 4.5 Task Status

标准任务状态：

```text
queued -> running -> succeeded
queued -> running -> failed
queued -> cancelled
running -> retrying -> running
running -> requires_review
```

`requires_review` 表示自动流程不能安全继续，需要人审或规则配置介入。

## 4.6 Orchestration Rule

复杂流程必须拆成可恢复步骤。

示例：Book extraction 不应是一个不可中断巨型任务，而应拆为 input normalization、chapter segmentation、scene segmentation、entity extraction、relationship extraction、quality review 和 package export。
