# 8. Delivery Slices and Acceptance

## 8.1 Slice 1: Local Platform Skeleton

交付：

- monorepo skeleton。
- web、api-gateway、core-service、ai-worker、scheduler。
- Docker Compose 启动 PostgreSQL、Redis、MinIO。
- health check endpoint。

验收：本地一条命令启动依赖和服务，前端可以看到 Workspace Home。

## 8.2 Slice 2: Source Import and Task Model

交付：

- Source Library 页面。
- POST /v1/books。
- upload object_ref。
- task model。
- ingest_book task。

验收：用户上传文本后，系统生成 source_book、source_chapters 和 task_events。

## 8.3 Slice 3: Knowledge Extraction and Review

交付：

- extract_knowledge task。
- knowledge_objects。
- evidence_records。
- Knowledge Review 页面。
- approve、reject、merge_alias。

验收：用户能批准主要人物、地点、事件、规则和伏笔进入 Approved Knowledge。

## 8.4 Slice 4: Project and Planning

交付：

- Novel Project Home。
- story_bible。
- chapter_plan。
- section_plans。
- Chapter Planner 页面。

验收：用户能创建原创项目，并生成一章可审核 Section Plan；内部 Beat Plan 可以作为 section payload 的一部分保存。

## 8.5 Slice 5: Writing Studio

交付：

- Memory Package。
- Prompt Package。
- writing_run。
- beat_run。
- Writer、Critic、Humanizer。
- Writing Studio 页面。

验收：用户能逐 Beat 生成、查看 Critic issue、接受 Humanizer 输出。

## 8.6 Slice 6: Quality and Feedback

交付：

- quality_report。
- chapter assembly。
- feedback_records。
- model cost metrics。
- Feedback Dashboard。

验收：用户能接受章节进入 manuscript，并查看质量报告、证据链和成本质量统计。

## 8.7 MVP Exit Criteria

MVP 完成标准：

- 从导入一本书到生成原创单章全链路可演示。
- 所有正式对象有 trace_id 或 input_refs/output_refs。
- 全部长任务有 task 状态和错误记录。
- blocking 问题进入人审，不无限自动重试。
- accepted chapter 有 quality_report 和 feedback_record。
