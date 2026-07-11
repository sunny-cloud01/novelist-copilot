---
document_id: NF-ARCH-002
title: Backend Technical Architecture
version: 1.0.0
status: Draft
category: Architecture Document
owner: Novel Factory Architecture Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-200
  - NF-NKS-210
  - NF-NKS-220
  - NF-NKS-230
  - NF-NKS-240
  - NF-NKS-250
  - NF-NKS-260
  - NF-NKS-270
  - NF-NKS-280
  - NF-ARCH-001
  - NF-DBS-001
  - NF-DBS-002
  - NF-DBS-003
  - NF-AGENT-001
  - NF-LLM-001
  - NF-TASK-001
  - NF-CONTRACT-001
  - NF-SEC-001
  - NF-AI-001
  - NF-PROMPT-001
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-200.md
  - docs/nks/NF-NKS-210.md
  - docs/nks/NF-NKS-220.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-240.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-260.md
  - docs/nks/NF-NKS-270.md
  - docs/nks/NF-NKS-280.md
  - docs/architecture/NF-ARCH-001.md
  - docs/database/NF-DBS-001.md
  - docs/database/NF-DBS-002.md
  - docs/database/NF-DBS-003.md
  - docs/agents/NF-AGENT-001.md
  - docs/llm/NF-LLM-001.md
  - docs/tasks/NF-TASK-001.md
  - docs/contracts/NF-CONTRACT-001.md
  - docs/security/NF-SEC-001.md
  - docs/ai/NF-AI-001.md
  - docs/prompts/NF-PROMPT-001.md
---

# NF-ARCH-002

# Backend Technical Architecture

# 1. Purpose and Scope

本文档定义 Novel Factory 第一阶段后端技术实现架构。

NF-ARCH-001 定义系统级逻辑架构。NF-ARCH-002 在该架构之上定义可落地的后端模块、运行进程、任务编排、LLM 调用边界、数据一致性和演进路线。

本文档的核心目标是支持从拆书到 AI 生成的完整工程链路：

```text
Book Ingestion
↓
Knowledge Extraction
↓
Knowledge Storage and Review
↓
Retrieval and Planning
↓
Prompt Assembly
↓
Chapter Generation and Revision
↓
Consistency Review
↓
Human Feedback
```

本文档覆盖：

- 后端技术栈建议。
- API、Worker 和后台任务边界。
- 服务模块职责。
- LLM、Agent 和生成流水线边界。
- 数据流、一致性、幂等和错误处理。
- 部署、安全和可观测性要求。

本文档不定义数据库物理 Schema、Prompt 模板正文、前端交互设计或具体云厂商基础设施脚本。

# 2. Architecture Decision

## 2.1 Phase 1 Architecture Style

Novel Factory 第一阶段采用 microservice-oriented architecture。

系统必须按前端应用、API Gateway / BFF、领域服务、Worker 服务、Scheduler 和基础设施服务拆分运行边界。第一阶段可以保持少量粗粒度服务，但不得弱化已定义的服务边界和所有权规则。

所有运行单元必须可容器化，本地开发默认通过 Docker Compose 或等价容器编排启动。

## 2.2 Recommended Stack

推荐第一阶段技术栈：

| Layer                        | Recommendation                                                           |
| ---------------------------- | ------------------------------------------------------------------------ |
| Frontend                     | React + TypeScript                                                       |
| Frontend Package Manager     | pnpm                                                                     |
| Frontend Component Library   | shadcn/ui preferred                                                      |
| API Gateway / BFF            | NestJS or FastAPI                                                        |
| AI / Knowledge Services      | Python FastAPI                                                           |
| Admin / Realtime Services    | NestJS when TypeScript integration is more valuable                      |
| Python Data Validation       | Pydantic                                                                 |
| TypeScript Validation        | Zod or class-validator                                                   |
| Python ORM / SQL             | SQLAlchemy Core or SQLAlchemy ORM                                        |
| TypeScript ORM / SQL         | Prisma or Drizzle when used by NestJS services                           |
| Migration                    | Alembic for Python-owned schemas; service-owned migration tool otherwise |
| Worker                       | Celery, Dramatiq, RQ, or service-specific worker                         |
| Queue / Runtime Coordination | Redis                                                                    |
| Database                     | PostgreSQL with pgvector                                                 |
| Object Storage               | MinIO locally, S3-compatible storage later                               |
| Local Infrastructure         | Docker Compose                                                           |
| LLM Provider Integration     | Provider adapter layer                                                   |

## 2.3 Service Technology Selection Rule

服务技术栈按职责选择，不要求所有后端服务使用同一种语言。

Python is recommended for text processing, LLM orchestration, embedding generation, extraction evaluation, retrieval, generation and consistency checking.

NestJS is recommended for API Gateway / BFF, admin APIs, authentication integration, realtime events, TypeScript SDK alignment and frontend-facing orchestration.

Service boundaries must be chosen by domain ownership and runtime profile, not by language preference alone.

## 2.4 Microservice Constraints

Microservices must obey:

- No cross-service database writes without ownership boundary.
- No direct dependency from business modules to specific LLM provider SDKs.
- No generation result enters approved knowledge without review state.
- No Redis state is treated as system of record.
- No object storage file is referenced without PostgreSQL metadata.
- No frontend service bypasses API Gateway / BFF for privileged operations.

# 3. Backend Service Boundaries

## 3.1 Service Map

第一阶段后端包含以下微服务或粗粒度服务边界：

| Service Boundary        | Preferred Stack       | Responsibility                                             |
| ----------------------- | --------------------- | ---------------------------------------------------------- |
| API Gateway / BFF       | NestJS or FastAPI     | 前端 API 聚合、认证上下文、轻量编排和请求路由              |
| Book Service            | NestJS or FastAPI     | 管理书籍、章节、来源、导入状态和文本引用                   |
| Ingestion Service       | Python FastAPI/Worker | 清洗、去重、章节识别、文本标准化和 object storage 写入     |
| Extraction Orchestrator | Python Worker         | 编排 NF-NKS-100 拆书流水线和抽取任务状态                   |
| Knowledge Service       | Python FastAPI        | 管理 knowledge_objects、aliases、versions、review states   |
| Story Graph Service     | Python FastAPI        | 管理 graph_nodes、graph_edges、snapshots 和图查询          |
| Retrieval Service       | Python FastAPI        | 组合结构化查询、向量召回、证据召回和上下文裁剪             |
| Planning Service        | Python FastAPI        | 基于知识、Pattern、Rhythm 和 Rule 生成大纲、卷纲和章节计划 |
| Prompt Assembly Service | Python FastAPI        | 根据 NF-PROMPT-001 组装 Prompt Package                     |
| Generation Service      | Python Worker         | 管理章节生成、改写、润色和候选版本                         |
| Consistency Service     | Python FastAPI/Worker | 检查人物、世界、时间线、规则、伏笔和生成结果一致性         |
| Review Service          | NestJS or FastAPI     | 管理 AI Review、人审、批准、驳回和修正记录                 |
| Feedback Service        | Python FastAPI        | 接收评分、人工修改、读者反馈并更新 ranking signals         |

## 3.2 Ownership Rule

每个服务只能直接写入自己拥有的数据表族。跨服务变更必须通过 API、command、domain event 或 outbox event 完成。

示例：Generation Service 不得直接修改 knowledge_objects。它只能提交 review item 或 feedback record，由 Knowledge Service 或 Review Service 处理状态变更。

## 3.3 Interface Style

服务内部接口优先使用 application service 函数或 class，而不是直接暴露 ORM model。服务之间接口必须通过 HTTP API、async event 或 queue command 表达，不得共享 ORM model。

推荐接口形态：

```text
command input -> application service -> transaction -> domain result/event
```

该风格可以让服务拆分、独立部署和独立测试时保留清晰边界。

## 3.4 Repository and Package Boundary

建议第一阶段使用 monorepo 管理多服务代码，但每个服务必须有独立 package、Dockerfile、依赖声明和启动命令。

建议代码结构：

```text
apps/
├── web/                    # React + TypeScript + pnpm + shadcn/ui
├── api-gateway/            # NestJS or FastAPI
├── book-service/
├── knowledge-service/
├── generation-service/
├── review-service/
└── worker-services/
packages/
├── contracts/
├── shared-types/
└── ui/
infra/
├── docker-compose.yml
├── postgres/
├── redis/
└── minio/
```

Frontend package management must use pnpm. shadcn/ui is the preferred component source for common UI primitives.

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

# 5. LLM, Agent and Generation Boundaries

## 5.1 Model Router and Provider Adapter

业务模块不得直接依赖具体 LLM provider SDK。

业务模块必须先向 AI Worker 提交 Agent Task，由 Model Router 解析 agent_model_assignment 和 model_profile_id，再通过 provider adapter 调用模型。

调用边界：

```text
Business Service
↓
AI Worker Agent Task
↓
Model Router
↓
Provider Adapter
↓
Provider API
```

Model Router 至少负责：

- 根据 agent_role、task_type、output_mode、genre_scope 选择 assignment。
- 将 assignment 解析为 primary model_profile_id。
- 判断 profile 是否 enabled。
- 处理 fallback_profile_ids。
- 应用 max_retry、max_cost 和 selection_policy。

Provider Adapter 至少负责：

- request normalization
- response normalization
- timeout handling
- retry policy
- token usage capture
- model version recording
- safety and policy error mapping

## 5.2 LLM Call Record

每次 LLM 调用必须记录：

- call_id
- trace_id
- task_id
- agent_role
- task_type
- assignment_id
- model_profile_id
- provider
- model
- prompt_ref
- input_refs
- output_ref
- token_usage
- latency
- retry_count
- cost_estimate
- fallback_from_call_id
- status
- error_code
- created_at

Prompt 正文可以进入 Object Storage，PostgreSQL 保存 prompt_ref 和元数据。

## 5.3 Agent Boundary

Agent 是任务执行角色，不是权威数据源。

Agent 输出必须进入 Review、Extraction 或 Generation 的受控流程。Agent 不得直接批准 knowledge object，不得绕过 Review Service 修改 Approved Knowledge Base。

## 5.4 Generation Pipeline

章节生成推荐流程：

```text
Generation Request
↓
Retrieve Character State + World Rules + Pattern + Rhythm + Assets
↓
Planning Service creates Chapter Plan
↓
Prompt Assembly Service creates Prompt Package
↓
Generation Service creates Draft Candidate
↓
Consistency Service checks Draft Candidate
↓
Revision Run improves Draft Candidate
↓
AI Review creates Quality Report
↓
Human Review approves or requests changes
↓
Feedback Service records signals
```

## 5.5 Human Flavor Principle

“人味”不是单次 Prompt 目标，而是后端上下文质量、角色连续性、节奏控制、素材选择、冲突压力和修订循环共同产生的结果。

生成系统必须优先召回：

- 当前角色的欲望、误解、秘密、恐惧和关系压力。
- 当前世界规则和不可违反约束。
- 章节目标、未兑现 Hook、预期 Reward 和节奏目标。
- 与题材和风格匹配的 Asset。
- 前文导致的情绪残留和后续承诺。

## 5.6 Revision Rule

第一稿不得直接视为最终章节。

每个章节草稿至少应经过：

- consistency check
- rhythm check
- repetition check
- AI flavor check
- human review or explicit auto-approval policy

# 6. Data Flow and Consistency

## 6.1 Extraction Data Flow

```text
Book Service
↓
Ingestion Service
↓
Object Storage raw_text / normalized_text
↓
Extraction Orchestrator
↓
Knowledge Service + Story Graph Service
↓
Review Service
↓
Approved Knowledge Base
```

所有从原文抽取出的对象必须绑定 evidence_refs。

## 6.2 Retrieval Data Flow

```text
Generation Request
↓
Retrieval Service
├── relational filters
├── vector search
├── Story Graph traversal
├── evidence retrieval
└── context budget trimming
↓
Planning Service
```

Retrieval Service 必须同时考虑 lifecycle_status、review_status、genre_scope、book_scope 和 permission。

## 6.3 Generation Data Flow

```text
Planning Service
↓
Prompt Assembly Service
↓
LLM Provider Adapter
↓
Generation Service
↓
Consistency Service
↓
Review Service
↓
Feedback Service
```

每个中间产物必须有 output_ref 或 database record，便于回放、审计和质量分析。

## 6.4 Consistency Layers

一致性分为三层：

| Layer                   | Responsibility                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------- |
| Transaction Consistency | PostgreSQL transaction, idempotency and ownership boundaries                          |
| Knowledge Consistency   | NKS object identity, evidence, lifecycle and review states                            |
| Narrative Consistency   | Character continuity, timeline, location, power system, rule and foreshadowing checks |

## 6.5 Outbox Rule

跨 projection 更新使用 outbox pattern。

业务事务写入 PostgreSQL 和 outbox event。后台 worker 更新 embedding、graph projection、search projection 或 object package。Projection 失败不得回滚已完成的权威业务事务，但必须留下 retryable failure record。

## 6.6 Error Taxonomy

后端错误至少分为：

- validation_error
- permission_error
- dependency_error
- llm_provider_error
- extraction_error
- consistency_violation
- review_required
- storage_error
- projection_error
- unknown_error

错误必须可追踪到 task_id、run_id、request_id 或 affected_object_id。

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

# 8. Evolution, Boundaries and Change Log

## 8.1 Evolution Path

系统架构演进分三阶段：

| Phase   | Architecture                                                                               |
| ------- | ------------------------------------------------------------------------------------------ |
| Phase 1 | Docker Compose microservice baseline, PostgreSQL + pgvector, Redis, Object Storage         |
| Phase 2 | Extract heavy workers and add graph/vector/search projections as independent services      |
| Phase 3 | Split high-load domains into independently scalable services with hardened event contracts |

## 8.2 Service Split Gate

满足以下条件之一时，可以进一步拆分或独立扩缩服务：

- 单模块负载明显影响其他模块延迟。
- 独立扩缩容收益超过部署复杂度。
- 模块有稳定 API 和事件契约。
- 模块内部依赖已经不需要共享事务。

优先候选：Extraction Worker、Generation Worker、Retrieval Service、Consistency Service、API Gateway / BFF。

## 8.3 Boundaries

NF-ARCH-002 定义后端技术架构。

NF-ARCH-002 不定义数据库物理 Schema、API 端点细节、Prompt 模板正文、Agent 角色细节或运维 runbook。

## 8.4 References

- NFES-000
- NF-PRD-001
- NF-NKS-000
- NF-NKS-001
- NF-NKS-100
- NF-NKS-200
- NF-NKS-210
- NF-NKS-220
- NF-NKS-230
- NF-NKS-240
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270
- NF-ARCH-001
- NF-DBS-001
- NF-DBS-002
- NF-AGENT-001
- NF-PROMPT-001

## 8.5 Approval

Document Status: Draft

Next Review: Backend implementation planning review

Next Document: NF-PIPE-001 Book Ingestion and Extraction Pipeline

## 8.6 Change Log

| Version | Date       | Author                          | Change                                                |
| ------- | ---------- | ------------------------------- | ----------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Architecture Team | Initial backend technical architecture specification. |
