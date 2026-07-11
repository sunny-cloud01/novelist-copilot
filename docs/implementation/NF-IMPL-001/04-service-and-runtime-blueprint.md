# 4. Service and Runtime Blueprint

## 4.1 Runtime Topology

第一阶段采用 microservice-oriented architecture，但允许在部署上保持少量粗粒度服务。

推荐运行单元：

```text
web
api-gateway
book-service
ingestion-worker
knowledge-service
story-graph-service
retrieval-service
planning-service
prompt-assembly-service
generation-worker
review-service
feedback-service
scheduler
postgres
redis
minio
```

## 4.2 Service Ownership

| Service                 | Owns                                                     | Reads                                           |
| ----------------------- | -------------------------------------------------------- | ----------------------------------------------- |
| Book Service            | source_books, source_chapters                            | import reports                                  |
| Ingestion Worker        | ingestion_runs, normalized_text refs                     | source files                                    |
| Knowledge Service       | knowledge_objects, aliases, versions                     | evidence, review records                        |
| Story Graph Service     | graph_nodes, graph_edges, graph_snapshots                | knowledge objects                               |
| Retrieval Service       | memory_packages, retrieval_results                       | knowledge, graph, evidence, prior summaries     |
| Planning Service        | story plans, chapter plans, beat plans                   | retrieval results, patterns, rhythm profiles    |
| Prompt Assembly Service | prompt_packages                                          | prompt templates, memory package, style profile |
| Generation Worker       | writing_runs, section_runs, draft refs                   | prompt packages, model profiles                 |
| Review Service          | review_reports, approval_records, quality gate decisions | drafts, quality reports                         |
| Feedback Service        | feedback_records, ranking_signals                        | edits, quality reports, cost records            |

跨服务写入必须通过 API、command、event 或 review workflow。

## 4.3 Monorepo Shape

推荐第一阶段代码仓库结构：

```text
apps/
├── web/
├── api-gateway/
├── book-service/
├── knowledge-service/
├── retrieval-service/
├── planning-service/
├── review-service/
└── worker-services/
packages/
├── contracts/
├── shared-types/
├── prompt-schemas/
└── ui/
infra/
├── docker-compose.yml
├── postgres/
├── redis/
└── minio/
```

前端必须使用 React + TypeScript + pnpm。通用组件优先使用 shadcn/ui。

## 4.4 Task Execution Rule

API 不直接执行长耗时任务。

API 创建 task 或 run，Worker 执行，前端通过 task_id、writing_run_id、section_run_id 查询进度。

所有可重试任务必须有 idempotency_key，并把任务状态保存在 PostgreSQL。Redis 只做队列、锁、短缓存和心跳。
