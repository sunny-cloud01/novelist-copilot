# 7. Deployment, Security and Observability

## 7.1 Local Development Stack

第一阶段本地开发推荐使用：

```text
React Web App
API Gateway / BFF
Domain Services
Worker Services
PostgreSQL with pgvector
Redis
MinIO
```

这些组件应通过 Docker Compose 或等价本地编排启动。每个应用服务应有独立容器、独立环境变量和明确健康检查。

## 7.2 Environment Separation

至少区分：

- local
- development
- staging
- production

生产环境不得直接复用开发环境对象存储 bucket、Redis namespace 或 PostgreSQL database。

## 7.3 Access Control

数据库访问必须按服务角色区分。

建议角色：

- api_gateway_rw
- book_service_rw
- knowledge_service_rw
- generation_service_rw
- review_service_rw
- worker_rw
- readonly_analytics
- migration_admin
- backup_operator

应用不得使用 migration_admin 执行普通运行期请求。

## 7.4 Secrets Rule

数据库密码、对象存储密钥、LLM API key 和 Redis credential 必须来自环境变量或 secret manager，不得写入 Markdown、代码或测试夹具。

## 7.5 Observability

存储层必须记录：

- query latency
- queue depth
- extraction run duration
- object storage write/read failure
- outbox lag
- projection lag
- embedding generation failure
- migration status
- backup status

这些指标应被 NF-OPS-001 的监控告警体系引用。

## 7.6 Backup and Recovery

PostgreSQL 必须定期备份，并支持 point-in-time recovery。

Object Storage 必须保存 checksum，并定期抽样验证文件可读性。

Redis 不要求持久化权威数据，但需要在重启后允许任务从 PostgreSQL 状态恢复。
