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
