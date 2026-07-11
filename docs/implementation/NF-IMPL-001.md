---
document_id: NF-IMPL-001
title: Product-Level Implementation Blueprint
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
  - NF-API-001
  - NF-AGENT-001
  - NF-PROMPT-001
  - NF-PROMPT-002
  - NF-PIPE-001
  - NF-PIPE-002
  - NF-PIPE-003
  - NF-RAG-001
  - NF-QA-001
  - NF-NKS-290
  - NF-IMPL-002
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/architecture/NF-ARCH-001.md
  - docs/architecture/NF-ARCH-002.md
  - docs/database/NF-DBS-002.md
  - docs/api/NF-API-001.md
  - docs/agents/NF-AGENT-001.md
  - docs/prompts/NF-PROMPT-001.md
  - docs/prompts/NF-PROMPT-002.md
  - docs/pipeline/NF-PIPE-001.md
  - docs/pipeline/NF-PIPE-002.md
  - docs/pipeline/NF-PIPE-003.md
  - docs/rag/NF-RAG-001.md
  - docs/quality/NF-QA-001.md
  - docs/nks/NF-NKS-290.md
  - docs/implementation/NF-IMPL-002.md
---

# NF-IMPL-001

# Product-Level Implementation Blueprint

# 1. Purpose and Positioning

本文档定义 Novel Factory 的产品级实现蓝图。

NF-PRD-001 定义产品愿景，NF-ARCH-001 和 NF-ARCH-002 定义系统架构与后端技术架构，NF-PIPE-003 定义写作编排流水线。NF-IMPL-001 在这些规范之上，回答产品落地时如何从用户开始使用，一直走到形成自己的小说，并保证过程可追踪、可审核、可回滚、不过度消耗人力。

## 1.1 Implementation Goal

产品级实现目标：

- 支持用户导入作品或自有素材。
- 支持自动拆书和知识结构化。
- 支持人审形成 Approved Knowledge Base。
- 支持创建原创小说项目、设定目标题材和写作策略。
- 支持规划卷纲、章纲、Scene 和 Beat。
- 支持按 Beat 生成、检查、重写、人类化和组章。
- 支持质量门禁、证据追踪和反馈学习。
- 支持用较少人力维护高质量长篇写作流程。

## 1.2 Product Boundary

NF-IMPL-001 覆盖产品实现蓝图、用户路径、服务协作、运行态、数据追踪、人力与成本控制、MVP 阶段和演进路线。

本文档不定义具体 UI 视觉稿、数据库字段 DDL、完整 API schema、模型供应商商业配置或发布平台接入。

## 1.3 Implementation Principle

实现必须遵守：

- Specification first: 所有对象和流程必须引用既有规范。
- Human decision at key points: 人工处理关键审核和审美选择，不承担批量机械修改。
- Trace by default: 每次导入、抽取、生成、审查、编辑和反馈都必须有 trace_id 或等价引用链。
- Progressive automation: 第一阶段先让流程可控，再逐步自动化低风险环节。
- Cost aware: 每个模型调用、重写次数、人工编辑距离和质量收益都必须可统计。

# 2. Product Experience Map

## 2.1 Primary User Roles

产品第一阶段支持以下角色：

| Role               | Responsibility                                       |
| ------------------ | ---------------------------------------------------- |
| Creator            | 创建原创小说项目、选择题材、审核方向、接受或修改章节 |
| Knowledge Reviewer | 审核拆书结果、合并对象、批准知识和规则               |
| Writing Reviewer   | 审核章节质量、处理阻塞问题、批准重要改写             |
| Operator           | 管理模型配置、质量阈值、任务队列和成本报表           |
| Service Account    | 执行 Agent、Worker、Scheduler 和系统内部任务         |

## 2.2 User Journey

从开始使用到形成自己的小说，产品路径如下：

```text
Create Workspace
↓
Import Source Books or Materials
↓
Run Ingestion and Book Analysis
↓
Review Extraction Summary and Exceptions
↓
Commit Knowledge Package and Inspect Story Graph
↓
Create Original Novel Project
↓
Configure Genre, Rules, Style and Constraints
↓
Confirm AI-Generated Story Bible and Chapter Direction
↓
Generate Chapter in One Click
↓
Critic Review and Humanizer Pass
↓
Assemble Chapter
↓
Quality Gate and Human Review
↓
Accept Chapter into Project Manuscript
↓
Capture Feedback and Improve Strategy
```

## 2.3 Frontend Workspaces

第一阶段前端应拆为以下工作区：

- Source Workspace: 导入、清洗状态、章节预览。
- Knowledge Workspace: 自动抽取摘要、证据、低置信度异常和知识包落库。
- Story Graph View: 图谱辅助查看、关系来源、伏笔状态，不作为默认重编辑入口。
- Novel Project Workspace: 原创项目设定、卷纲、章纲、角色和规则。
- Writing Studio: 一键章节生成、内部 Scene/Beat 编排状态、Critic、Humanizer、组章和质量报告。
- Feedback and Analytics Workspace: 模型成本、质量趋势、人工编辑模式和策略建议。
- Configuration Workspace: 模型路由、规则、质量阈值、Prompt 版本和权限。

## 2.4 UX Rule

用户不应被要求理解所有底层服务。

界面必须把复杂流水线压缩为可操作状态：queued、running、requires_review、blocked、approved、failed。详细证据、模型调用、质量项和反馈记录可以展开查看，但默认页面应围绕下一步决策呈现。

# 3. End-to-End Platform Flow

## 3.1 Source to Knowledge Flow

```text
Book Upload
↓
Ingestion Task
↓
Chapter Segmentation
↓
Scene Segmentation
↓
Knowledge Extraction
↓
Normalization and Alias Merge
↓
Story Graph Build
↓
Knowledge Review
↓
Approved Knowledge Base
```

每个抽取对象必须保留 evidence_refs。未审核对象只能作为 candidate 使用，不得进入正式写作上下文。

## 3.2 Knowledge to Original Project Flow

原创项目不是简单复制来源作品。

系统必须将 Approved Knowledge 抽象为可复用知识资产：Pattern、Rhythm Profile、Asset、Rule、Expression Type、Genre Playbook 和 Feedback Knowledge。

原创项目创建时，用户选择或配置：

- genre_scope
- target_reader_profile
- originality_boundary
- allowed_knowledge_sources
- style_profile_seed
- forbidden_changes
- quality_gate_profile

## 3.3 Project Planning Flow

```text
Project Setting
↓
Story Bible
↓
Volume Plan
↓
Chapter Plan
↓
Scene Plan
↓
Beat Plan
```

Planner 输出必须引用 Knowledge Base、Pattern、Rhythm Profile、Rule 和项目自有设定。新增关键设定必须进入 review 状态。

## 3.4 Writing Flow

写作阶段执行 NF-PIPE-003 的 Creator-facing 一键章节生成流程。Beat、Scene 或 Section 仍作为系统内部编排单元存在，但不要求 Creator 默认逐项推进：

```text
Memory Package
↓
Style Profile
↓
Generate Chapter Draft
↓
Critic Report
↓
Auto Rewrite Blocked Sections
↓
Humanizer Pass
↓
Chapter Assembly
↓
Quality Gate
↓
Human Review or Accept
```

## 3.5 Feedback Flow

完成章节后必须采集：

- writer_model_profile_id
- critic_model_profile_id
- humanizer_model_profile_id
- prompt_package_id
- memory_package_id
- quality_report_id
- human_edit_distance
- accepted_output_ratio
- ai_flavor_issue_category
- reader_reward_signal
- model_cost_quality_ratio

反馈进入 NF-NKS-290 定义的 Feedback Knowledge，不得直接覆盖正式策略。

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

# 5. Data Traceability and Audit

## 5.1 Traceability Goal

系统必须能够回答：

- 某个知识对象来自哪本书、哪一章、哪段证据。
- 某个章节计划引用了哪些 Pattern、Rule、Rhythm 和 Story Graph 状态。
- 某个 Beat 由哪个 Prompt Package、Memory Package 和模型生成。
- Critic 为什么打回，Humanizer 改了什么。
- 人工最终改了哪些文字，原因是什么。
- 哪些反馈影响了后续 Prompt、Model Router 或检索策略。

## 5.2 Core Trace Chain

最小追踪链：

```text
source_book
→ source_chapter
→ evidence_record
→ knowledge_object / graph_edge
→ memory_package
→ prompt_package
→ writing_run
→ beat_run
→ beat_draft
→ critic_report
→ humanizer_report
→ quality_report
→ approved_chapter
→ feedback_record
```

## 5.3 Required References

关键对象必须保存：

- request_id
- trace_id
- actor_id or agent_role
- input_refs
- output_refs
- evidence_refs
- model_profile_id when model is used
- prompt_package_id when prompt is used
- source_snapshot_id when knowledge is read
- quality_report_id when quality gate is executed

## 5.4 Audit Policy

以下操作必须产生 audit_event：

- 修改 Approved 或 Frozen knowledge。
- 批准或驳回知识对象。
- 修改质量阈值、模型路由、Prompt 版本或规则配置。
- 接受章节进入正式 manuscript。
- 反馈驱动策略 promotion 或 rollback。

## 5.5 Evidence and Storage Rule

大文本、草稿、报告、diff 和长证据片段进入 Object Storage。PostgreSQL 保存 object_ref、checksum、owner、version、review_status 和 access policy。

embedding、图数据库和搜索索引都是 projection，不得作为唯一事实来源。

# 6. AI Writing Production Workflow

## 6.1 Writing Studio Contract

Writing Studio 是产品落地的核心工作台。

它必须展示：

- current project state
- chapter plan
- scene plan
- beat list
- memory package summary
- style profile summary
- writer draft
- critic issues
- humanizer diff
- quality gate result
- human review actions

## 6.2 Beat Production Contract

每个 Beat 生产必须有独立状态：

```text
planned
writing
critic_review
rewrite_required
humanizer_pass
beat_approved
blocked
```

Writer 不得默认一次生成完整章节。默认每次生成 300 到 800 中文字。

## 6.3 Quality Gate Contract

章节进入正式稿前必须满足：

- no blocking knowledge consistency issue
- no blocking character consistency issue
- ai_flavor_score <= configured threshold
- mobile_readability_score >= configured threshold
- originality_safety_score >= configured threshold
- Humanizer revision_diff persisted
- human_review_required is false or approved by reviewer

## 6.4 Human Review Actions

Writing Reviewer 可执行：

- accept_section
- accept_chapter
- request_rewrite
- edit_and_accept
- send_to_planner
- update_rule_request
- mark_style_preference
- block_generation

所有人工操作必须记录 reason。

## 6.5 Manuscript Assembly

正式 manuscript 只接受 approved chapter。

章节进入 manuscript 后，系统必须生成 chapter_snapshot，并更新 current_story_state、character_dynamic_state、relationship_state、hook_state 和 prior_summary_pack。

后续章节检索必须读取最新动态状态，不得只依赖角色静态卡或旧摘要。

# 7. Human Labor and Cost Control

## 7.1 Labor Control Principle

产品目标不是完全无人写作，而是把人工集中在高价值判断上。

人工负责：

- 审核关键知识和冲突合并。
- 决定原创项目方向、题材、人物关系和风格边界。
- 处理 blocking quality issue。
- 审核反馈驱动的策略变更。
- 把少量关键章节调到最终审美标准。

系统负责：

- 批量抽取、归一化和证据绑定。
- 结构化规划和 Beat 拆分。
- 生成、Critic、Humanizer 和质量报告。
- 一致性检查、AI 味检查和手机阅读检查。
- 成本统计、反馈归因和策略建议。

## 7.2 Human Review Budget

第一阶段建议目标：

| Stage                | Human Review Target                        |
| -------------------- | ------------------------------------------ |
| Knowledge extraction | 只审高置信冲突、主角、核心规则和高影响对象 |
| Chapter planning     | 审核章纲和关键 Beat，不逐句改写计划        |
| Beat drafting        | 只处理自动重写失败或 blocking issue        |
| Chapter approval     | 重点审开头、高潮、结尾和一致性报告         |
| Feedback promotion   | 人工批准策略变更，不人工处理每条低风险反馈 |

## 7.3 Cost Control

必须记录：

- prompt_tokens
- completion_tokens
- retry_count
- rewrite_count
- model_profile_id
- accepted_output_ratio
- human_edit_distance
- quality_score
- model_cost_quality_ratio

低质量高成本路线必须自动降权或进入人工配置审查。

## 7.4 Automation Safety

可以自动执行：

- 低风险重写。
- forbidden phrase 替换建议。
- Memory Package 重新组装。
- stale context 拦截。
- 质量报告生成。

不得自动执行：

- 覆盖 Approved Knowledge。
- 改变核心设定。
- 发布章节。
- promotion blocking feedback。
- 大规模改变项目风格。

# 8. MVP and Phased Delivery

## 8.1 Phase 0 Documentation and Contracts

目标：把产品实现所需规范收敛到可开发状态。

交付物：

- NF-IMPL-001 Product-Level Implementation Blueprint。
- MVP API endpoint list。
- MVP database table family draft。
- Writing Studio interaction specification。
- model profile and provider adapter contract。

## 8.2 Phase 1 Knowledge MVP

目标：完成从导入到自动分析和知识包落库。

范围：

- Source import。
- Chapter segmentation。
- Basic extraction run。
- Extraction summary and exception review。
- Evidence binding。
- Knowledge Package commit。
- Basic Story Graph browse。

验收：用户可以导入一本书，系统自动抽取主要人物、地点、事件、伏笔和规则；用户只处理低置信度或冲突异常，并将知识包提交为可用于新书项目的 Knowledge Package。

## 8.3 Phase 2 Writing MVP

目标：完成从原创项目到单章成稿。

范围：

- Novel Project creation。
- Story Bible and chapter plan。
- Memory Package assembly。
- Prompt Pack assembly。
- Creator-facing one-click chapter generation with internal Scene/Beat orchestration。
- Critic and Humanizer loop。
- Chapter Assembly。
- Quality Gate。

验收：用户可以基于 Approved Knowledge 和自有设定生成一章可审稿章节，并查看证据链、质量报告和模型成本。

## 8.4 Phase 3 Feedback and Optimization

目标：让系统从写作过程学习。

范围：

- Human edit capture。
- Feedback Record。
- model_cost_quality dashboard。
- Prompt ranking suggestion。
- Retrieval strategy suggestion。
- Manual promotion and rollback。

验收：用户修改章节后，系统能归因修改原因，并生成可审核的策略优化建议。

## 8.5 Phase 4 Scale and Collaboration

目标：支持多项目、多角色和更长篇幅。

范围：

- Multi-project dashboard。
- Role-based permissions。
- Batch writing queue。
- Long-running manuscript state。
- Dedicated vector DB or graph DB upgrade when thresholds are met。
- Export and publication preparation。

# 9. Risks, Validation and Change Log

## 9.1 Key Risks

| Risk                            | Mitigation                                                                             |
| ------------------------------- | -------------------------------------------------------------------------------------- |
| Microservice overhead too early | Use service boundaries first; deploy coarse-grained services until load requires split |
| Quality score instability       | Start with rule checks, LLM judge and human sampling; calibrate thresholds per genre   |
| AI flavor remains high          | Keep Style Analyzer before Writer; Humanizer is only a micro-pass                      |
| Knowledge drift                 | Use source_snapshot_id, dynamic state override and stale context blocking              |
| Human review overload           | Use severity, confidence, retry budget and blocking-only handoff                       |
| Copyright and originality risk  | Use authorized sources, abstract style features and originality safety gate            |
| Cost explosion                  | Track token, retry, accepted_output_ratio and model_cost_quality_ratio                 |

## 9.2 Validation Strategy

产品级验证分为：

- Documentation validation: build_docs check must pass。
- Contract validation: API envelope、task model、output package schema 可校验。
- Pipeline validation: sample book can move through extraction, review, planning and writing。
- Trace validation: selected generated Beat can trace back to source knowledge, prompt, memory and quality report。
- Cost validation: every model call has model_profile_id and token metrics。
- Labor validation: review queue volume and human_edit_distance remain within configured threshold。

## 9.3 Implementation Readiness Checklist

进入代码实现前必须确认：

- MVP scope locked。
- Service ownership table accepted。
- Table family draft created。
- API endpoint families selected。
- Writing Studio first workflow accepted。
- Model provider adapter interface accepted。
- Human review thresholds configured。

## 9.4 Boundaries

NF-IMPL-001 是产品级实现蓝图，不替代 PRD、ARCH、DBS、API、PIPE、RAG、QA、AGENT、PROMPT 或 NKS 文档。

当具体实现细节与本蓝图冲突时，应优先更新对应权威规范，再同步更新 NF-IMPL-001。

## 9.5 References

- NF-PRD-001
- NF-ARCH-001
- NF-ARCH-002
- NF-DBS-002
- NF-API-001
- NF-AGENT-001
- NF-PROMPT-001
- NF-PROMPT-002
- NF-PIPE-001
- NF-PIPE-002
- NF-PIPE-003
- NF-RAG-001
- NF-QA-001
- NF-NKS-290
- NF-IMPL-002

## 9.6 Approval

Document Status: Draft

Next Review: Product implementation blueprint review

Next Document: NF-IMPL-002 MVP Delivery Plan

## 9.7 Change Log

| Version | Date       | Author                            | Change                                          |
| ------- | ---------- | --------------------------------- | ----------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Implementation Team | Initial product-level implementation blueprint. |
