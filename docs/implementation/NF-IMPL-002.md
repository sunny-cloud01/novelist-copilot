---
document_id: NF-IMPL-002
title: MVP Delivery Plan
version: 1.0.0
status: Draft
category: Implementation Blueprint
owner: Novel Factory Implementation Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-ARCH-001
  - NF-ARCH-002
  - NF-DBS-002
  - NF-DBS-003
  - NF-API-001
  - NF-AGENT-001
  - NF-PROMPT-002
  - NF-PIPE-003
  - NF-RAG-001
  - NF-QA-001
  - NF-NKS-290
  - NF-IMPL-001
  - NF-IMPL-003
  - NF-LLM-001
  - NF-TASK-001
  - NF-CONTRACT-001
  - NF-SEC-001
  - NF-AI-001
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/architecture/NF-ARCH-001.md
  - docs/architecture/NF-ARCH-002.md
  - docs/database/NF-DBS-002.md
  - docs/database/NF-DBS-003.md
  - docs/api/NF-API-001.md
  - docs/agents/NF-AGENT-001.md
  - docs/prompts/NF-PROMPT-002.md
  - docs/pipeline/NF-PIPE-003.md
  - docs/rag/NF-RAG-001.md
  - docs/quality/NF-QA-001.md
  - docs/nks/NF-NKS-290.md
  - docs/implementation/NF-IMPL-001.md
  - docs/implementation/NF-IMPL-003.md
  - docs/llm/NF-LLM-001.md
  - docs/tasks/NF-TASK-001.md
  - docs/contracts/NF-CONTRACT-001.md
  - docs/security/NF-SEC-001.md
  - docs/ai/NF-AI-001.md
---

# NF-IMPL-002

# MVP Delivery Plan

# 1. Purpose and MVP Boundary

本文档定义 Novel Factory 第一版 MVP 的交付计划。

NF-IMPL-001 定义产品级实现蓝图。NF-IMPL-002 将蓝图中的 Phase 0、Phase 1 和 Phase 2 收敛为可开发、可验收、可演示的 MVP 范围。

## 1.1 MVP Goal

MVP 的目标不是一次性交付完整工业化写作平台，而是证明以下闭环可运行：

```text
导入一本参考作品
↓
完成基础拆书和知识审核
↓
创建一个原创小说项目
↓
生成一章可审稿章节
↓
查看证据链、质量报告、模型成本和反馈记录
```

## 1.2 MVP Must Include

MVP 必须包含：

- 用户工作区和基础权限。
- Source import 和章节管理。
- 基础抽取任务和知识候选审核。
- Approved Knowledge Base。
- 基础 Story Graph 浏览。
- Novel Project 创建和 Story Bible。
- Chapter Plan、Scene Plan、Beat Plan。
- Memory Package 和 Prompt Package 组装。
- Creator-facing one-click Chapter Generation，内部可拆分为 Beat、Scene、Critic 和 Humanizer 子任务。
- Chapter Assembly 和 Quality Gate。
- Feedback Record 和成本质量统计。

## 1.3 MVP Must Not Include

MVP 不包含：

- 多租户商业化计费。
- 发布平台接入。
- 完整移动端 App。
- 全自动长篇连载。
- 独立图数据库或专用向量数据库。
- 复杂读者平台埋点。
- 多语言完整翻译工作流。

## 1.4 Success Criteria

MVP 成功标准：

- 一名 Creator 可以在单个工作区完成从导入到生成单章。
- 每个正式章节都能追踪到 source、knowledge、memory、prompt、model、quality 和 feedback。
- 人工确认集中在来源导入、新书设定、章节最终批准和阻塞问题；拆书、抽取、图谱构建和章节生成默认自动运行。
- 本地 Docker Compose 可以启动核心依赖和服务。

# 2. MVP User Workflows

## 2.1 Workflow A: Source to Approved Knowledge

用户路径：

```text
Create Workspace
↓
Upload Source Book
↓
Run Ingestion
↓
Auto Segment Chapters and Scenes
↓
Run Basic Extraction
↓
Auto Normalize and Score Knowledge Candidates
↓
Review Exceptions or Low Confidence Items
↓
Commit Approved Knowledge Package
↓
Browse Story Graph
```

验收：系统可以自动完成章节切分、基础抽取、候选归一化和知识包提交。用户可以查看 evidence_refs、抽取报告和低置信度问题，并只对 exception item 执行 approve、reject、merge_alias 或 request_reextract。Story Graph 作为辅助查看界面，不作为 MVP 的重编辑入口。

## 2.2 Workflow B: Original Project Setup

用户路径：

```text
Create Novel Project
↓
Select Genre Scope
↓
Configure Originality Boundary
↓
Generate Story Bible Draft
↓
Review and Confirm Story Bible
↓
Select Allowed Knowledge Sources
↓
Configure Quality Gate Profile
```

验收：项目必须生成 project_id、story_bible_id、quality_gate_profile_id 和 allowed_knowledge_source_refs。Story Bible 默认由 AI 生成草稿，Creator 负责确认方向、禁用相似点和最终设定边界。

## 2.3 Workflow C: Plan One Chapter

用户路径：

```text
Open Project
↓
Create Chapter Goal
↓
Generate Chapter Plan Draft
↓
Generate Scene and Beat Plan Internally
↓
Confirm Chapter Direction
```

验收：Creator 只需要确认章目标、核心冲突、爽点、禁用变化和预估字数。系统内部仍需生成 Scene 和 Beat 计划；每个 Beat 必须包含 beat_goal、pov_character、active_characters、conflict_pressure、reward_or_hook、required_knowledge_refs 和 estimated_word_count，但不要求 Creator 默认逐项审批。

## 2.4 Workflow D: Generate One Chapter

用户路径：

```text
Assemble Memory Package
↓
Assemble Prompt Package
↓
Generate Full Chapter Draft
↓
Run Critic
↓
Auto Rewrite Blocked Sections
↓
Run Humanizer
↓
Assemble Chapter
↓
Run Quality Gate
↓
Human Review
↓
Accept Chapter
```

验收：Creator-facing 主操作是“一键生成本章”。章节被接受前必须有 writing_run、section_runs、critic_reports、humanizer_reports、quality_report 和 feedback_records。内部 Beat 可作为 section payload 的计划细节保存。只有 blocking issue、低一致性、原创性风险或 AI 味超阈值时，界面才要求 Creator 局部处理。

## 2.5 Workflow E: Review Feedback and Cost

用户路径：

```text
Open Feedback Dashboard
↓
Review AI Flavor Issues
↓
Review Human Edit Distance
↓
Review Model Cost Quality Ratio
↓
Create Strategy Suggestion
↓
Approve or Reject Suggestion
```

验收：反馈建议不得自动修改正式策略，必须进入 review 状态。

# 3. MVP Frontend Scope

## 3.1 Technical Baseline

Frontend 使用 React + TypeScript + pnpm。通用组件优先使用 shadcn/ui。

MVP 前端只实现 Web 管理和创作工作台，不实现移动端 App。

## 3.2 Required Pages

MVP 页面范围：

| Page                  | Purpose                                                     |
| --------------------- | ----------------------------------------------------------- |
| Workspace Home        | 工作区入口、最近任务、待审核项                              |
| Source Library        | 上传作品、查看书籍、章节和导入状态                          |
| Extraction Run Detail | 查看抽取任务进度、错误和报告                                |
| Knowledge Review      | 审核 candidate knowledge、证据、冲突和别名                  |
| Story Graph Viewer    | 基础图谱浏览、节点详情、关系查看                            |
| Novel Project Home    | 项目设定、Story Bible、章节列表                             |
| Chapter Planner       | 章纲、Scene 和 Beat 计划审核                                |
| Writing Studio        | 章节生成、Section 级恢复、Critic、Humanizer、组章、质量报告 |
| Feedback Dashboard    | 模型成本、AI 味、人工编辑距离和策略建议                     |
| Configuration         | 模型 profile、质量阈值、Prompt 版本和规则配置               |

## 3.3 MVP UI States

所有长任务页面必须支持：

- queued
- running
- succeeded
- failed
- requires_review
- blocked

状态必须来自后端 task 或 run，不得只由前端本地推断。

## 3.4 Writing Studio MVP Layout

Writing Studio 第一版必须展示：

- 左侧：chapter plan、scene list、section list，并可折叠查看内部 beat plan。
- 中间：当前 section draft、humanized section、assembled chapter。
- 右侧：Memory Package 摘要、Critic issues、Quality Gate、trace refs。
- 底部：model cost、retry_count、human actions。

## 3.5 Frontend Non-Goals

MVP 不实现：

- 高级协同编辑。
- 自定义可视化图谱布局编辑器。
- 发布排期。
- 商业化计费页面。
- 复杂主题系统。

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

# 5. MVP Data and Storage Scope

## 5.1 Storage Baseline

MVP 使用：

- PostgreSQL + pgvector as system of record。
- MinIO as local S3-compatible object storage。
- Redis as runtime coordination。

不引入独立图数据库、专用向量数据库或搜索集群。

## 5.2 MVP Table Families

MVP 表族：

| Family     | Required Examples                                          |
| ---------- | ---------------------------------------------------------- |
| identity   | users, workspaces, workspace_members                       |
| source     | source_books, source_chapters, source_files                |
| task       | tasks, task_events                                         |
| evidence   | evidence_records, evidence_bindings                        |
| knowledge  | knowledge_objects, object_aliases, object_versions         |
| graph      | graph_nodes, graph_edges, graph_snapshots                  |
| review     | review_reports, review_items, approval_records             |
| project    | novel_projects, story_bibles, chapter_plans, section_plans |
| prompt     | prompt_templates, prompt_packages                          |
| memory     | memory_packages, retrieval_results                         |
| generation | writing_runs, section_runs, chapter_drafts, revision_diffs |
| quality    | quality_reports, quality_gate_runs                         |
| feedback   | feedback_records, ranking_suggestions                      |
| config     | model_profiles, quality_thresholds, config_rules           |
| audit      | audit_events                                               |

## 5.3 Object Storage Objects

Object Storage 保存：

- uploaded_source_file
- normalized_book_text
- chapter_text_snapshot
- extraction_package
- memory_package_snapshot
- prompt_package_snapshot
- section_draft_text
- humanized_section_text
- assembled_chapter_text
- quality_report_payload
- revision_diff_payload

PostgreSQL 保存 object_ref、checksum、byte_size、owner_ref、created_at 和 access_policy。

## 5.4 Trace Requirements

MVP 必须能从 accepted chapter 追踪到：

- source evidence。
- approved knowledge。
- memory_package_id。
- prompt_package_id。
- writing_run_id。
- section_run_id。
- model_profile_id。
- quality_report_id。
- feedback_record_id。

## 5.5 Migration Rule

MVP migration 必须按表族分组。破坏性迁移必须记录 rollback_strategy，并在本地种子数据上验证。

# 6. MVP API and Contracts

## 6.1 API Principles

MVP API 必须遵守 NF-API-001 的 envelope、trace、idempotency 和 error model。

所有 mutation 请求必须支持 request_id 和 trace_id。创建任务类请求必须支持 idempotency_key。

## 6.2 Required Endpoint Families

MVP endpoint families：

| Family     | Required Endpoints                                                               |
| ---------- | -------------------------------------------------------------------------------- |
| Workspace  | POST /v1/workspaces, GET /v1/workspaces/{workspace_id}                           |
| Source     | POST /v1/books, GET /v1/books, GET /v1/books/{book_id}/chapters                  |
| Task       | GET /v1/tasks/{task_id}, GET /v1/tasks/{task_id}/events                          |
| Extraction | POST /v1/extraction-runs, GET /v1/extraction-runs/{run_id}                       |
| Knowledge  | GET /v1/knowledge-objects, POST /v1/knowledge-objects/{object_id}/review-actions |
| Graph      | GET /v1/graph/nodes/{node_id}, GET /v1/graph/nodes/{node_id}/neighbors           |
| Project    | POST /v1/novel-projects, GET /v1/novel-projects/{project_id}                     |
| Planning   | POST /v1/chapter-plans, POST /v1/chapter-plans/{chapter_plan_id}/section-plans   |
| Writing    | POST /v1/writing-runs, GET /v1/writing-runs/{writing_run_id}                     |
| Quality    | GET /v1/quality-reports/{quality_report_id}                                      |
| Feedback   | POST /v1/feedback-records, GET /v1/feedback-records                              |
| Config     | GET /v1/model-profiles, GET /v1/quality-thresholds                               |

## 6.3 Standard Task Response

创建长任务的 API 必须返回：

```json
{
  "data": {
    "task_id": "TASK-000001",
    "status": "queued",
    "resource_ref": "writing_run:WR-000001"
  },
  "meta": {
    "request_id": "REQ-000001",
    "trace_id": "TRC-000001"
  },
  "errors": []
}
```

## 6.4 Review Action Contract

Review action 必须包含：

- action_type
- target_ref
- reason
- reviewer_id
- expected_next_state

允许 action_type：

- approve
- reject
- request_change
- merge_alias
- request_reextract
- accept_section
- accept_chapter
- request_rewrite
- edit_and_accept
- block_generation

## 6.5 Error Contract

MVP 必须实现以下错误码：

- validation_error
- authentication_error
- authorization_error
- not_found
- conflict
- lifecycle_violation
- dependency_error
- rate_limited
- internal_error

# 7. MVP AI Workflow and Quality

## 7.1 Provider Adapter Boundary

MVP 必须通过 provider adapter 调用模型。

业务代码不得直接依赖具体供应商 SDK。所有模型调用必须记录：

- model_profile_id
- provider_name
- agent_role
- prompt_tokens
- completion_tokens
- latency
- retry_count
- cost_estimate

即使 MVP 只使用一个模型，也必须通过 model_profile_id 和 agent_model_assignment 调用，不得在 Agent 代码或 Prompt 中硬编码 provider_model_name。

## 7.2 MVP Agent Roles

MVP 启用以下 Agent role：

- Extraction Agent
- Normalization Agent
- Planning Agent
- Memory Agent
- Style Analyzer Agent
- Writer Agent
- Critic Agent
- Humanizer Agent
- Review Agent
- Feedback Agent

MVP 必须为上述 Agent role 创建默认 model assignment。初始 assignment 可以全部指向同一个 default model_profile。后续可以按 Agent role 替换模型：Writer 使用中文长文本模型，Critic 使用结构化审查模型，Humanizer 使用改写模型，Memory Agent 使用长上下文模型。

## 7.3 MVP Writing Quality Gates

单章成稿必须检查：

- knowledge_consistency_score
- character_consistency_score
- beat_goal_completion_score
- rhythm_match_score
- ai_flavor_score
- humanity_score
- mobile_readability_score
- originality_safety_score

默认 blocking：

- Approved Knowledge 被改写。
- Humanizer 改变剧情事实。
- ai_flavor_score 高于配置阈值。
- originality_safety_score 低于配置阈值。

## 7.4 Retry Budget

MVP 默认重试预算：

| Stage                   | Retry Budget |
| ----------------------- | ------------ |
| extraction task         | 2            |
| memory package assembly | 1            |
| chapter generation      | 2            |
| critic review           | 1            |
| humanizer pass          | 1            |
| quality gate            | 1            |

超过预算后进入 requires_review 或 blocked，不继续自动消耗模型调用。

## 7.5 Humanizer Boundary

Humanizer 只做微改写：句式、段落、机械转场、泛化表达、手机阅读节奏。

Humanizer 不得改变事实、角色关系、战力结果、伏笔状态或章节目标。

## 7.6 Model Routing Acceptance

MVP AI workflow 验收必须包含：

- default model_profile 可用。
- 每个 MVP Agent role 都有 enabled assignment。
- Provider Adapter 记录 token、latency、retry 和 cost。
- 禁用 model_profile 后 Router 不再选择该 profile。
- structured output validation 失败会消耗 retry budget。
- fallback_profile_ids 可以为空，但字段和流程必须存在。

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

# 9. Validation, Risks and Change Log

## 9.1 MVP Validation Plan

验证必须覆盖：

- Documentation: build_docs check passes。
- Local runtime: Docker Compose can start dependencies。
- API: required endpoint families return standard envelope。
- Task model: long tasks persist status in PostgreSQL。
- Storage: uploaded text and generated reports have object_ref and checksum。
- Traceability: accepted chapter traces to source evidence, memory, prompt, model and quality report。
- Human review: blocking issue can be routed to review action。
- Cost: model call metrics are recorded。

## 9.2 MVP Demo Script

MVP 演示必须按以下脚本执行：

1. 创建 workspace。
2. 上传一本参考作品文本。
3. 启动 ingestion 和 extraction。
4. 批准主要知识对象。
5. 创建原创小说项目。
6. 生成 chapter plan 和 section plan；内部 beat plan 作为 section payload 保存。
7. 逐 Beat 生成并通过 Critic 和 Humanizer。
8. 组章并运行 Quality Gate。
9. 接受章节进入 manuscript。
10. 打开 trace 和 feedback dashboard。

## 9.3 Key MVP Risks

| Risk                                 | Mitigation                                                |
| ------------------------------------ | --------------------------------------------------------- |
| MVP scope expands into full platform | Freeze non-goals and slice acceptance before coding       |
| LLM output instability               | Use structured output contracts, retries and human review |
| Review queue too large               | Only route blocking and low-confidence issues to humans   |
| Traceability gaps                    | Enforce input_refs and output_refs at task boundary       |
| Local infrastructure complexity      | Keep Phase 1 storage to PostgreSQL, Redis and MinIO       |
| Cost spikes                          | Enforce retry budgets and model cost metrics              |

## 9.4 Boundaries

NF-IMPL-002 定义 MVP 交付计划，不替代 NF-IMPL-001 的产品级蓝图，也不定义最终代码实现细节。

具体代码任务应由 NF-IMPL-003 Service Build Plan 或后续 implementation plan 管理。

## 9.5 References

- NF-IMPL-001
- NF-ARCH-002
- NF-DBS-002
- NF-API-001
- NF-PIPE-003
- NF-RAG-001
- NF-PROMPT-002
- NF-QA-001
- NF-NKS-290
- NF-IMPL-003

## 9.6 Approval

Document Status: Draft

Next Review: MVP scope review

Next Document: NF-IMPL-003 Service Build Plan

## 9.7 Change Log

| Version | Date       | Author                            | Change                           |
| ------- | ---------- | --------------------------------- | -------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Implementation Team | Initial MVP delivery plan draft. |
