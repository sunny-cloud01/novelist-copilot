# 4. MVP Service Scope

## 4.1 Deployment Style

MVP 采用 microservice-oriented architecture，但部署可以先使用粗粒度服务。

推荐 MVP 运行单元：

```text
web
api-gateway
core-service
ai-worker
scheduler
postgres
redis
minio
```

其中 core-service 内部保持 Book、Knowledge、Graph、Review、Project、Feedback 的模块边界；ai-worker 承担 Ingestion、Extraction、Retrieval、Planning、Prompt Assembly、Generation、Critic、Humanizer 和 Quality Gate 的后台任务。

## 4.2 Service Boundaries

MVP 内部边界：

| Boundary         | Runtime      | Responsibility                                                          |
| ---------------- | ------------ | ----------------------------------------------------------------------- |
| API Gateway      | api-gateway  | 前端 API、认证上下文、request_id、trace_id、BFF aggregation             |
| Book Module      | core-service | source_books、source_chapters、upload metadata                          |
| Knowledge Module | core-service | knowledge_objects、aliases、versions、review states                     |
| Graph Module     | core-service | graph_nodes、graph_edges、graph_snapshots                               |
| Project Module   | core-service | novel_projects、story_bibles、chapter plans                             |
| Review Module    | core-service | review_reports、approval_records、human actions                         |
| Feedback Module  | core-service | feedback_records、ranking_suggestions                                   |
| AI Worker        | ai-worker    | extraction、retrieval、planning、generation、critic、humanizer、quality |
| Scheduler        | scheduler    | retry、timeout、stale projection check、background maintenance          |

## 4.3 Worker Task Types

MVP 必须支持任务类型：

- ingest_book
- segment_chapters
- extract_knowledge
- build_story_graph
- assemble_memory_package
- assemble_prompt_package
- plan_chapter
- plan_scene_and_beats
- generate_chapter_draft
- critic_review_chapter
- rewrite_blocked_sections
- humanize_chapter
- assemble_chapter
- run_quality_gate
- capture_feedback

## 4.4 Runtime Constraints

- API 不同步执行 LLM 长任务。
- 所有任务状态保存在 PostgreSQL。
- Redis 仅用于队列、锁和短缓存。
- Object Storage 保存上传文件、标准化文本、草稿、报告和 diff。
- 每个任务必须记录 idempotency_key。
