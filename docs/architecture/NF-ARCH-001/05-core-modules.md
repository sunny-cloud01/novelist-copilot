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
