---
document_id: NFES-000
title: Novel Factory Documentation Standard
version: 1.0.0
status: Draft
category: Engineering Standard
owner: Novel Factory Architecture Team
created: 2026-07-09
updated: 2026-07-09
dependencies:
  - none
references:
  - prod.md
---

# NFES-000

# Novel Factory Documentation Standard

# 1. Purpose

本文档定义 Novel Factory 项目的统一工程文档规范。

目标是建立一套类似 RFC、IEEE Software Standard 的文档体系，使所有项目文档具备：

- 统一结构
- 明确版本
- 可追踪变更
- 可被 AI 理解
- 可作为开发依据

本规范适用于产品设计、技术架构、Knowledge Engineering、AI Agent、数据模型、Prompt Engineering、API 和运维流程。

# 2. Scope

本文档规范以下内容：

- 文档分类
- 文档编号
- 生命周期
- 版本控制
- 变更流程
- 引用规则
- 审核流程
- AI 知识库要求
- 文档工程目录结构

本规范不记录具体产品功能、数据库字段、Agent 行为或 Prompt 模板。上述内容应分别进入 PRD、DBS、AGENT 或 PROMPT 文档。

# 3. Documentation Principles

## 3.1 Specification First

正式文档的核心目标不是记录讨论过程，而是定义系统行为、数据结构、约束条件、标准流程和可执行依据。

## 3.2 Single Source of Truth

每个领域概念必须存在唯一权威定义。例如，Character 的定义必须来源于 NF-NKS-000。其他文档只能引用该定义，不得重复定义。

## 3.3 Traceability

所有重要设计决策必须可追踪。重大架构决策必须创建 ADR。

## 3.4 AI Readability

所有正式文档必须结构清晰、章节稳定、定义明确、避免歧义，并支持机器解析。

## 3.5 Document as Source

Novel Factory 文档应按照源码工程方式维护。长文档应拆分为章节源文件，最终可构建为完整 Markdown、PDF、JSON 或 YAML 资产。

# 4. Document Classification

Novel Factory 文档分类如下：

```text
NF
├── PRD
├── NKS
├── ADR
├── ARCH
├── DBS
├── API
├── AGENT
├── PROMPT
├── PIPE
├── RAG
├── QA
├── IMPL
└── OPS
```

## 4.1 PRD

Product Requirement Document。用于定义产品目标、用户需求、产品边界和功能规划。

## 4.2 NKS

Novel Knowledge Specification。用于定义小说知识模型、数据对象、知识抽取规范和 Story Graph 模型。

## 4.3 ADR

Architecture Decision Record。用于记录架构问题、决策方案、技术取舍和影响范围。

## 4.4 ARCH

Architecture Document。用于描述系统架构、模块关系、数据流和部署拓扑。

## 4.5 DBS

Database Specification。用于定义数据库结构、Schema、Index、Migration 和数据约束。

## 4.6 API

API Specification。用于定义接口路径、请求响应、错误码、鉴权规则和兼容性约束。

## 4.7 AGENT

AI Agent Specification。用于定义 Agent 职责、输入输出、工具调用、生命周期和失败处理。

## 4.8 PROMPT

Prompt Engineering Specification。用于定义 Prompt 模板、参数、约束、评估方式和版本演化。

## 4.9 PIPE

Pipeline Specification。用于定义拆书、抽取、生成、改写、审核、反馈和写作编排流程。

## 4.10 RAG

Retrieval Augmented Generation Specification。用于定义检索策略、Memory Package、上下文预算、staleness 和一致性预检。

## 4.11 QA

Quality Assurance Specification。用于定义质量评分、写作质量门禁、低 AI 味检查、人味检查和审核阈值。

## 4.12 IMPL

Implementation Blueprint。用于定义产品级落地方案、阶段路线、服务协作、用户路径、人力成本控制和实现验收边界。

## 4.13 OPS

Operations Specification。用于定义运行流程、发布流程、监控告警、备份恢复和事故处理。

# 5. Lifecycle and Versioning

## 5.1 Lifecycle

所有正式文档必须经历：

```text
Draft
↓
Review
↓
Approved
↓
Frozen
↓
Deprecated
```

Draft 表示设计阶段，允许修改，不可作为生产依据。

Review 表示完成初稿，等待评审。

Approved 表示正式版本，可以被其他文档和开发任务引用。

Frozen 表示稳定版本，修改必须提交 Change Request。

Deprecated 表示废弃版本，保留历史记录，不再作为新开发依据。

## 5.2 Versioning

采用 Semantic Versioning：

```text
Major.Minor.Patch
```

Major 用于重大架构变化或不兼容修改。

Minor 用于新增功能、章节或向后兼容扩展。

Patch 用于错误修正、措辞修正或格式修正。

# 6. Authoring Rules

## 6.1 Front Matter

所有规范级文档必须包含 YAML Front Matter：

```yaml
document_id:
title:
version:
status:
category:
owner:
created:
updated:
dependencies:
references:
```

## 6.2 Formal Content Only

正式 Markdown 文档不得包含聊天说明、模型自述、下载提示、临时计划、未确认假设或页面渲染残留。

正式 Markdown 文档可以包含 Front Matter、正文规范、表格、图示代码块、References、Change Log 和 Approval 信息。

## 6.3 Cross References

禁止复制其他文档中的权威定义。

正确引用方式：

```text
See NF-NKS-000 Character Definition.
```

错误方式：重新定义 Character。

## 6.4 AI Knowledge Base

进入 AI Knowledge Base 的文档必须使用 Markdown 格式、UTF-8 编码、稳定 ID、明确章节，并且可被机器按标题、Front Matter 和稳定 ID 切片。

# 7. Repository Structure

推荐目录：

```text
NovelFactory-Docs/
├── docs/
│   ├── zh-CN/
│   ├── en-US/
│   ├── i18n/
│   ├── standards/
│   ├── prd/
│   ├── nks/
│   ├── adr/
│   ├── architecture/
│   ├── database/
│   ├── pipeline/
│   ├── agents/
│   ├── prompts/
│   ├── rag/
│   ├── quality/
│   ├── implementation/
│   └── operations/
├── schemas/
├── templates/
├── examples/
├── assets/
├── scripts/
└── build/
```

规范文件命名：

```text
NF-{CATEGORY}-{NUMBER}-{NAME}.md
```

在文档工程中，推荐同时维护：

```text
docs/{category}/{document-id}.md
docs/{category}/{document-id}/README.md
docs/{category}/{document-id}/{chapter}.md
```

双语文档入口推荐维护：

```text
docs/zh-CN/README.md
docs/en-US/README.md
docs/i18n/README.md
docs/i18n/document-map.md
```

`docs/{category}/{document-id}.md` 仍是 canonical reading version。`docs/zh-CN/` 和 `docs/en-US/` 用于阅读入口、摘要、术语对齐和协作导航，不替代 source chapters。

完整翻译版本只有在对应 canonical 文档稳定后再创建。创建完整翻译时，必须在 `docs/i18n/document-map.md` 记录路径、状态和更新责任。

# 8. Approval and Change Log

Document Status: Draft

Next Review: NFES-000 Review

Next Document: NF-PRD-001 Product Overview v2.0

## Change Log

| Version | Date       | Author                          | Change                                        |
| ------- | ---------- | ------------------------------- | --------------------------------------------- |
| 1.0.0   | 2026-07-09 | Novel Factory Architecture Team | Initial Draft for documentation project mode. |
