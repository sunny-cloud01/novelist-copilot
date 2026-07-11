# 7. Deployment, Observability and Security

## 7.1 Local Deployment

本地开发推荐使用：

```text
React Web App
API Gateway / BFF
Domain Services
Worker Services
Scheduler Service
PostgreSQL + pgvector
Redis
MinIO
```

所有组件必须可通过 Docker Compose 或等价容器编排启动，并通过环境变量配置连接信息。

前端容器必须使用 pnpm 安装和运行脚本。前端公共组件优先从 shadcn/ui 生成或封装。

## 7.2 Environment Strategy

必须区分 local、development、staging 和 production。

环境之间不得共享 PostgreSQL database、Redis namespace、Object Storage bucket 或 LLM callback secret。

## 7.3 Observability

后端必须记录：

- request_id
- task_id
- run_id
- book_id
- generation_request_id
- llm_call_id
- latency
- token_usage
- retry_count
- error_code
- projection_lag
- queue_depth

## 7.4 Logging Rule

日志不得直接打印完整原文、完整 Prompt、LLM provider secret 或用户凭据。

大文本内容应通过 object_ref 追踪。调试时只能记录摘要、hash、长度、范围和受控 excerpt。

## 7.5 Security Rule

后端必须支持：

- service role database credentials
- secret manager or environment based secrets
- signed object storage access
- audit_events for privileged changes
- explicit approval path for destructive operations

## 7.6 Backup and Recovery

PostgreSQL 和 Object Storage 的备份策略引用 NF-DBS-002 和 NF-OPS-001。

Worker 和 Redis 故障恢复必须以 PostgreSQL task state 为准。

## 7.7 Performance Principle

第一阶段优先优化：

- long task recoverability
- retrieval relevance
- generation traceability
- database migration safety
- review workflow reliability

不得为了早期吞吐牺牲证据链和审核边界。
