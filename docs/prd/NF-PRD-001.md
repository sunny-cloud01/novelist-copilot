---
document_id: NF-PRD-001
title: Novel Factory Product Overview
version: 2.1.0
status: Draft
category: Product Requirement Document
owner: Novel Factory Product Team
created: 2026-07-09
updated: 2026-07-11
dependencies:
  - NFES-000
    - NF-UX-001
references:
  - prod.md
    - docs/ux/NF-UX-001.md
---

# NF-PRD-001

# Novel Factory Product Overview

# 1. Purpose and Positioning

本文档定义 Novel Factory 的产品定位、系统边界、核心模块、个人创作者交互流程、知识工程流程和阶段性路线图。

Novel Factory 是面向个人创作者的 AI 生书平台，通过“上传参考作品 → 自动拆书 → 知识工程 → AI 生成新书设定 → 一键生成章节 → 质量审查 → 反馈优化”形成低人工成本、可追踪、可持续迭代的创作闭环。

## 1.1 Product Vision

Novel Factory 的目标是让个人创作者能够从参考作品和创作方向出发，快速形成可用的知识包、新书世界观、章节草稿和质量报告，而不是依赖单次 Prompt 或大量手工拆书。

传统作者流程：

```text
灵感
↓
写书
↓
修改
↓
发布
```

Novel Factory 流程：

```text
上传参考作品
↓
自动拆书
↓
知识包落库
↓
辅助查看 Story Graph
↓
AI 生成新书设定
↓
确认世界观与原创边界
↓
一键生成章节
↓
AI 质量检测
↓
处理阻塞问题
↓
批准章节
↓
反馈学习
↓
持续优化策略
```

## 1.2 Positioning

Novel Factory 不是一个只回答 Prompt 的写作聊天工具，也不是要求专业编辑逐项维护的重后台。它是一套个人创作者可使用的 AI 生书平台：系统自动完成拆书、抽取、落库、设定草稿、章节生成和质量审查，Creator 只在来源确认、设定确认、阻塞问题和最终批准处介入。

核心竞争力：

- 自动拆书和知识包生成
- 低打扰异常处理
- AI 生成 Story Bible 和章节方向
- 一键章节生成
- 证据链、质量门禁和一致性规则
- 反馈学习和策略优化

# 2. System Architecture

```text
                 Novel Factory
                       │
              Creator Workspace
                       │
              Upload Source Book
                       │
                 Auto Analyze Book
                       │
          ┌────────────┴────────────┐
          │                         │
   Knowledge Package           Story Graph View
          │                         │
          └────────────┬────────────┘
                       │
             AI Story Bible Draft
                       │
          Confirm Worldview and Boundary
                       │
              One-Click Chapter Run
                       │
        Critic / Humanizer / Quality Gate
                       │
        Blocking Issue Review / Chapter Approval
                       │
                 Feedback Loop
                       │
              Strategy Optimization
```

系统以 Creator Workspace 为入口。Creator 上传参考作品后，系统自动完成文件接收、文本标准化、章节切分、知识抽取、证据绑定、候选归一化和知识包落库。Story Graph 是辅助查看和检索视图，不作为 MVP 的重编辑入口。

新书创作从 AI Story Bible Draft 开始，Creator 确认世界观、原创边界和章节方向后，系统执行一键章节生成。内部仍可拆分 Scene、Beat 或 Section 进行 Critic、Humanizer 和 Quality Gate，但界面只在阻塞问题、质量风险和最终批准处打断 Creator。审核结果进入 Feedback Loop，用于持续优化 Prompt、Pattern、质量阈值和生成策略。

# 3. Core Modules

## 3.1 Creator Workspace

目标：为个人创作者提供从上传参考作品到生成原创章节的统一入口。

核心功能：最近项目、运行任务、待处理阻塞项、继续生成、章节批准和反馈摘要。

## 3.2 Source Library

目标：存放所有用于拆书分析的原始作品。

基础字段：id、title、author、platform、genre、tags、word_count、completion_status、rating、source、download_url。

核心功能：上传作品、填写来源信息、分类、标签管理、搜索、去重和自动分析。

## 3.3 Auto Book Analysis Engine

目标：自动把一本小说拆成 AI 可学习、可追踪、可落库的数据。

拆分维度：世界观、人物、势力、地图、修炼体系、剧情、节奏、爽点、反转、伏笔、悬念、战斗、感情线、日常剧情。

章节级输出：chapter、scene、event、conflict、emotion、reward、hook、climax。

Creator 默认不逐项审核拆书结果。系统只在低置信度、冲突、证据缺失或解析失败时打断 Creator。

## 3.4 Knowledge Base

目标：按知识分类，而不是按书分类。

知识库至少包含 Character Library、Worldview Library、Faction Library、Location Library、Pattern Library、Rhythm Profile Library 和 Asset Library。

## 3.5 Story Bible Engine

目标：基于 Creator 输入、原创边界、已批准知识包和题材目标，生成新书世界观与设定草稿。

输出至少包含 world rules、power system、factions、protagonist、core cast、main conflict、volume direction、style target 和 forbidden similarities。

Creator 负责确认设定方向和原创边界，不需要从零手写完整世界观。

## 3.6 Pattern Library

目标：把常见网文套路抽象成可参数化流程。

所有 Pattern 必须支持参数化、组合、替换角色、替换地点和替换目标。

## 3.7 Rhythm Engine

目标：量化小说节奏。

每章统计 climax_index、conflict_index、dialogue_ratio、description_ratio、battle_ratio、information_density、suspense_index 和 reward_count。

## 3.8 Prompt Engine

目标：管理 Prompt 模板并支持动态拼接。

模板类型包括人物 Prompt、世界 Prompt、剧情 Prompt、章节 Prompt、对白 Prompt、战斗 Prompt 和结尾 Prompt。

## 3.9 One-Click Chapter Engine

目标：让 Creator 通过一个主操作生成约 3000 字章节草稿。

系统内部可以使用 chapter_plan、scene_plan、beat_plan、memory_package、prompt_package、critic_report、humanizer_report 和 quality_report，但默认不要求 Creator 逐 Beat 推进。

## 3.10 Asset Library

目标：存放最小创作单位。

素材类型包括动作、心理、环境、天气、物品和台词片段。

## 3.11 Feedback Loop

目标：持续优化 AI 生成质量。

记录 Prompt 效果、章节评分、AI 错误、人工修改、重复率、读者反馈和热门章节。

输出 Prompt Ranking、Pattern Ranking 和 Knowledge Ranking。

## 3.12 Rule Engine

目标：保证长篇小说一致性。

规则类型包括人物规则、时间规则、地图规则、境界规则、法宝规则、年龄规则、势力规则、世界规则和伏笔规则。

示例规则：境界不能倒退、法宝唯一、人物不能瞬移、时间线必须连续、已死亡角色不能再次出现。

# 4. Story Graph

Story Graph 是 Novel Factory 的核心数据结构和辅助查看界面。

在 MVP 中，Story Graph 主要用于检索、解释、证据追踪和关系查看，不作为 Creator 的默认重编辑画布。关系修正应优先通过异常处理、重新抽取或知识包修订完成。

## 4.1 Node Types

节点类型：

- Character
- Location
- Event
- Artifact
- Faction
- Rule
- Resource
- Foreshadowing

## 4.2 Relationship Types

关系类型：

- Character belongs_to Faction
- Character owns Artifact
- Event occurs_at Location
- Character hates Character
- Event causes Event
- Foreshadowing resolves_at Chapter

## 4.3 Query Requirement

所有节点必须支持 AI 实时查询，并在 NF-NKS 系列文档中获得稳定定义。Creator-facing 图谱界面必须支持搜索节点、查看节点详情、查看关系来源、查看 evidence_refs 和跳转原文证据。

# 5. AI Generation Pipeline

```text
Step 1: 创建原创项目
↓
Step 2: 选择题材、风格和原创边界
↓
Step 3: 选择可用知识包
↓
Step 4: AI 生成 Story Bible 草稿
↓
Step 5: Creator 确认世界观和禁用相似点
↓
Step 6: 输入或确认章节方向
↓
Step 7: 一键生成约 3000 字章节
↓
Step 8: Critic / Humanizer / Quality Gate
↓
Step 9: 处理阻塞问题
↓
Step 10: Approve Chapter
↓
反馈进入后续策略
```

生成流水线必须把知识库、Story Graph、Prompt Engine、Chapter Engine 和 Consistency Engine 串联起来。

系统内部可以将章节拆成 Scene、Beat 或 Section 执行生成和审查，但 Creator-facing 主操作应是一键生成章节。人工介入集中在 Story Bible 确认、章节方向确认、阻塞问题处理、最终章节批准和策略建议审核。

人工确认结果必须回流到 Feedback Loop，用于后续优化。

# 6. Roadmap

## 6.1 V1

- Source upload
- 自动拆书和抽取
- 知识包摘要和异常处理
- AI 生成 Story Bible 草稿
- 一键生成单章
- 质量报告和章节批准

## 6.2 V2

- Story Graph 辅助查看增强
- 多知识包选择
- 章节方向模板
- 质量门禁策略配置
- 反馈建议审核

## 6.3 V3

- RAG 和长上下文增强
- Agent 协作
- 卷纲和多章连续生成
- 自动维护人物和世界状态
- 章节级策略自适应

## 6.4 V4

- 多题材支持
- 多平台支持
- 多项目并行生成
- 自动优化
- 自动学习
- 形成个人创作者可持续使用的 AI 生书平台

# 7. Boundaries, References, and Change Log

## 7.1 Document Boundaries

本文档只定义产品总览和产品级边界。

以下内容由后续文档定义：

- NF-NKS-000：术语与领域模型
- NF-NKS-100：拆书与知识抽取规范
- NF-ARCH-001：系统架构
- NF-DBS-001：数据库与 Schema
- NF-AGENT-001：Agent 协作模型
- NF-PROMPT-001：Prompt 模板规范
- NF-UX-001：Creator Interaction Flow Specification

## 7.2 References

- NFES-000
- prod.md

## 7.3 Approval

Document Status: Draft

Next Review: NF-PRD-001 Review

Next Document: NF-NKS-000 Glossary & Domain Model v2.0

## 7.4 Change Log

| Version | Date       | Author                     | Change                                                           |
| ------- | ---------- | -------------------------- | ---------------------------------------------------------------- |
| 2.1.0   | 2026-07-11 | Novel Factory Product Team | Repositioned as a personal creator AI novel-generation platform. |
| 2.0.0   | 2026-07-09 | Novel Factory Product Team | Rewritten from product draft into NFES-compliant PRD format.     |
