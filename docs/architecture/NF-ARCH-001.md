---
document_id: NF-ARCH-001
title: Novel Factory System Architecture
version: 1.0.0
status: Draft
category: Architecture Document
owner: Novel Factory Architecture Team
created: 2026-07-09
updated: 2026-07-09
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
---

# NF-ARCH-001

# Novel Factory System Architecture

# 1. Purpose and Scope

本文档定义 Novel Factory 的系统架构基线。

本文档将 NF-PRD-001 中的产品链路转化为可开发、可拆分、可演进的架构视图，并为后续 NF-DBS、NF-API、NF-AGENT、NF-PROMPT 和 NF-OPS 文档提供模块边界与数据流依据。

## 1.1 Scope

本文档覆盖系统上下文、架构原则、逻辑架构、模块职责、数据流、集成边界、一致性架构、可观测性要求、部署视图和架构风险。

本文档不覆盖数据库字段类型、索引与迁移，API 请求响应结构，Agent 工具调用细节，Prompt 模板正文或具体基础设施供应商配置。

# 2. Architectural Principles

## 2.1 Specification Driven Architecture

系统架构必须以正式文档为依据。产品边界来源于 NF-PRD-001，领域对象来源于 NF-NKS-000，知识抽取流程来源于 NF-NKS-100。

## 2.2 Knowledge First

Novel Factory 的核心资产是结构化知识，而不是单次生成结果。所有生成模块必须围绕 Knowledge Base、Story Graph、Rule 和 Feedback Loop 设计。

## 2.3 Traceable Data Flow

从原始文本到生成章节的每个中间对象都必须可追踪。任何进入 Knowledge Base 或 Story Graph 的对象都必须保留来源证据或审查记录。

## 2.4 Modular Boundary

模块必须通过稳定数据对象和接口交互。模块内部实现可以演进，但跨模块契约必须由规范文档定义。

## 2.5 Human-in-the-Loop

Novel Factory 必须支持人工审核、人工修正和人工批准。系统不得假设 AI 抽取结果或 AI 生成结果天然可信。

## 2.6 Incremental Evolution

架构必须支持从人工拆书到自动拆书、从单 Agent 到多 Agent、从单书知识库到跨题材知识资产的演进。

# 3. System Context

Novel Factory 位于原始小说来源、知识工程系统、AI 生成系统和人工审核流程之间。

```text
External Book Sources
        │
        ▼
Novel Factory
        │
        ├── Knowledge Engineering
        ├── Story Graph
        ├── Prompt and Generation
        ├── Consistency Checking
        └── Feedback Learning
        │
        ▼
Generated Novel Assets
```

外部参与方：

- 内容来源：小说文本、平台元数据、人工整理素材。
- 人工审核者：评审抽取结果、生成章节和质量报告。
- AI 模型：执行抽取、推理、生成、评估和润色。
- 下游系统：数据库、RAG、Agent Orchestrator、Prompt Engine、发布工具。

# 4. Logical Architecture

Novel Factory 的逻辑架构分为八层：

```text
Frontend Experience Layer
↓
Source Layer
↓
Ingestion Layer
↓
Knowledge Extraction Layer
↓
Knowledge Storage Layer
↓
Planning and Prompt Layer
↓
Generation and Consistency Layer
↓
Review and Feedback Layer
```

## 4.1 Frontend Experience Layer

Frontend Experience Layer 提供人工导入、拆书审核、知识管理、章节生成、质量评审和运营配置界面。

前端技术基线：React、TypeScript、pnpm。组件库优先使用 shadcn/ui；仅当 shadcn/ui 无法满足复杂编辑器、图谱或可视化场景时，才引入专项组件或可视化库。

## 4.2 Source Layer

Source Layer 管理原始小说文本、平台元数据、人工素材和外部参考数据。

## 4.3 Ingestion Layer

Ingestion Layer 负责导入、清洗、去重、章节识别和基础预处理。

## 4.4 Knowledge Extraction Layer

Knowledge Extraction Layer 按 NF-NKS-100 将 Book、Chapter、Scene 抽取为对象、关系、Pattern、Rhythm Profile 和 Rule。

## 4.5 Knowledge Storage Layer

Knowledge Storage Layer 存储结构化数据库、Knowledge Base、Story Graph、Evidence 和 Review Report。

## 4.6 Planning and Prompt Layer

Planning and Prompt Layer 基于知识对象、套路、节奏和生成目标构造大纲、卷纲、章节计划和 Prompt。

## 4.7 Generation and Consistency Layer

Generation and Consistency Layer 负责章节生成、润色、一致性检测和规则校验。

## 4.8 Review and Feedback Layer

Review and Feedback Layer 收集人工审核、AI 质量检测、读者反馈和生成效果指标，并回流到知识系统。

# 5. Core Modules

## 5.1 Frontend Application

Frontend Application 提供 Web 操作界面。

技术基线：React、TypeScript、pnpm、shadcn/ui。

上游输入：人工审核者、运营人员、创作者。

下游输出：API Gateway / BFF 请求、审核操作、生成请求、配置变更。

## 5.2 API Gateway / BFF

API Gateway / BFF 聚合前端所需 API，负责认证上下文、请求路由、轻量编排和前端视图模型适配。

推荐技术：NestJS 或 FastAPI。若主要承担前端 BFF、权限、实时通知和 TypeScript SDK 对齐，优先 NestJS；若主要承担 AI 工作流编排和 Python schema 复用，优先 FastAPI。

上游输入：Frontend Application。

下游输出：各后端微服务 API、任务创建请求、查询请求。

## 5.3 Book Library

Book Library 管理原始作品、平台元数据、标签、来源和导入状态。

上游输入：External Book Sources。

下游输出：Book、Chapter 原始输入。

## 5.4 Rule Configuration Center

Rule Configuration Center 管理题材规则、抽取规则、生成约束、审核规则和质量阈值。

上游输入：人工配置、评审反馈、系统默认规则。

下游输出：Extraction Rules、Consistency Rules、Quality Gates。

## 5.5 Book Analysis Engine

Book Analysis Engine 执行 NF-NKS-100 定义的抽取流水线。

上游输入：Book、Chapter、Rule Configuration。

下游输出：BookKnowledgePackage。

## 5.6 Structured Database

Structured Database 存储规范化对象、审查状态、抽取报告和运行记录。

字段、索引、迁移和物理模型由 NF-DBS 文档定义。

## 5.7 Story Graph

Story Graph 存储 Character、Location、Event、Faction、Artifact、Rule、Foreshadowing 等对象之间的关系。

节点与关系定义引用 NF-NKS-000。

## 5.8 Knowledge Base

Knowledge Base 按知识类型组织可复用知识资产。

Knowledge Base 不等同于 Book Library。Book Library 是来源库，Knowledge Base 是抽取后的知识资产库。

## 5.9 Prompt Engine

Prompt Engine 根据知识、套路、节奏、角色状态和生成目标动态组合 Prompt。

Prompt 模板正文和变量规范由 NF-PROMPT 文档定义。

## 5.10 Chapter Engine

Chapter Engine 负责从大纲、卷纲、章节计划和 Prompt 生成章节内容。

Chapter Engine 必须调用 Consistency Engine 进行生成前约束检查和生成后质量检查。

## 5.11 Consistency Engine

Consistency Engine 检查人物、时间线、地图、境界、法宝、势力、伏笔和世界规则的一致性。

## 5.12 Feedback Loop

Feedback Loop 收集 Prompt 效果、章节评分、AI 错误、人工修改、重复率、读者反馈和热门章节，用于优化 Prompt、Pattern、Knowledge 和 Rule。

# 6. Data Flow

## 6.1 Knowledge Extraction Flow

```text
Book Library
↓
Ingestion Layer
↓
Book Analysis Engine
↓
BookKnowledgePackage
↓
Structured Database
↓
Knowledge Base + Story Graph
```

## 6.2 Generation Flow

```text
Generation Request
↓
Knowledge Base Query
↓
Story Graph Query
↓
Prompt Engine
↓
Chapter Engine
↓
Consistency Engine
↓
AI Quality Review
↓
Human Review
↓
Feedback Loop
```

## 6.3 Feedback Flow

```text
Generated Chapter
↓
AI Quality Signals + Human Edits + Reader Feedback
↓
Feedback Loop
↓
Prompt Ranking + Pattern Ranking + Knowledge Ranking
↓
Rule Configuration Center + Knowledge Base
```

# 7. Integration Boundaries

## 7.1 Database Boundary

NF-ARCH-001 defines database responsibilities and data ownership. NF-DBS documents define physical schema, indexes, migrations, and constraints.

## 7.2 API Boundary

NF-ARCH-001 defines module communication boundaries. NF-API documents define request paths, payloads, error codes, authentication, and compatibility rules.

## 7.3 Agent Boundary

NF-ARCH-001 defines where agents participate in the architecture. NF-AGENT documents define agent roles, tools, lifecycle, retry behavior, and orchestration.

## 7.4 Prompt Boundary

NF-ARCH-001 defines Prompt Engine placement and dependencies. NF-PROMPT documents define prompt templates, variables, examples, and evaluation rules.

## 7.5 Operations Boundary

NF-ARCH-001 defines high-level deployment and observability needs. NF-OPS documents define runtime operations, release procedures, backups, incident response, and monitoring implementation.

# 8. Consistency Architecture

Consistency checks must happen at three points.

## 8.1 Pre-Generation Check

Before generation, the system checks whether selected knowledge, character state, timeline, world rules, and prompt constraints are compatible.

## 8.2 Post-Generation Check

After generation, the system checks whether produced content violates known rules, object states, timeline constraints or foreshadowing commitments.

## 8.3 Feedback Correction

After human review or reader feedback, the system records violations and updates rules, rankings, or knowledge states.

Consistency domains:

- Character continuity
- Timeline continuity
- Location continuity
- Power System constraints
- Artifact uniqueness
- Faction relationship state
- Foreshadowing lifecycle
- Worldview rules

# 9. Observability Requirements

Novel Factory must record operational and knowledge-engineering signals.

Required signal groups:

- ingestion_metrics
- extraction_metrics
- validation_metrics
- generation_metrics
- consistency_metrics
- review_metrics
- feedback_metrics

Each pipeline run must produce a traceable run_id.

Minimum trace fields:

- run_id
- module_name
- input_ids
- output_ids
- status
- started_at
- finished_at
- error_id

# 10. Deployment View

Initial deployment is microservice-oriented and container-based.

Recommended baseline:

```text
Docker Compose Development Stack
├── Frontend Web App: React + TypeScript + pnpm + shadcn/ui
├── API Gateway / BFF: NestJS or FastAPI
├── Book and Ingestion Service
├── Knowledge and Story Graph Service
├── Retrieval and Planning Service
├── Prompt and Generation Service
├── Consistency and Review Service
├── Feedback Service
├── Worker Services
└── Scheduler Service

Storage Backends
├── PostgreSQL + pgvector
├── Redis
├── MinIO or S3-compatible Object Storage
├── Graph Projection Store when needed
└── Vector/Search Projection Store when needed

External Services
├── LLM Provider
├── OCR Provider
└── Publishing or Export Tools
```

Each service must be packaged as a Docker image or Docker Compose service. Local development must run through Docker Compose or equivalent container orchestration.

The architecture may start with a small number of backend services, but service boundaries, database ownership and events must follow microservice contracts from the beginning.

# 11. Architecture Risks

## 11.1 Knowledge Drift

Risk: Knowledge Base and Story Graph may diverge from source evidence.

Mitigation: preserve evidence, review reports, object lifecycle, and traceable extraction runs.

## 11.2 Prompt Coupling

Risk: Prompt templates may depend on undocumented object fields.

Mitigation: Prompt variables must reference NF-NKS and NF-DBS definitions.

## 11.3 Graph Inconsistency

Risk: Story Graph relationships may reference missing or deprecated objects.

Mitigation: enforce referential integrity and lifecycle validation before package approval.

## 11.4 Automation Overtrust

Risk: AI extraction and generation results may be accepted without sufficient review.

Mitigation: keep human-in-the-loop review and blocking quality gates.

## 11.5 Distributed Service Complexity

Risk: Microservices increase integration, deployment, observability and data consistency complexity.

Mitigation: keep early services coarse grained, enforce ownership through APIs and events, run all local services through Docker Compose, and only add more service processes when a boundary has stable contracts.

# 12. Boundaries, References, and Change Log

## 12.1 Boundary Rules

NF-ARCH-001 is the architecture baseline.

It must not redefine product goals from NF-PRD-001, domain objects from NF-NKS-000, NKS module semantics from NF-NKS-200 到 NF-NKS-270, or extraction process rules from NF-NKS-100.

NF-ARCH-001 may reference these documents and translate their requirements into module boundaries and data-flow responsibilities.

## 12.2 References

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

## 12.3 Approval

Document Status: Draft

Next Review: NF-ARCH-001 Review

Next Document: NF-DBS-001 Knowledge Database Specification

## 12.4 Change Log

| Version | Date       | Author                          | Change                                                        |
| ------- | ---------- | ------------------------------- | ------------------------------------------------------------- |
| 1.0.0   | 2026-07-09 | Novel Factory Architecture Team | Initial Draft for Novel Factory system architecture baseline. |
