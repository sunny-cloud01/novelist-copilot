---
document_id: NF-NKS-001
title: Novel Knowledge Specification Map
version: 1.0.0
status: Draft
category: Novel Knowledge Specification
owner: Novel Factory Knowledge Engineering Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-100
  - NF-NKS-280
  - NF-NKS-290
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-280.md
  - docs/nks/NF-NKS-290.md
---

# NF-NKS-001

# Novel Knowledge Specification Map

# 1. Purpose and Scope

本文档定义 Novel Factory 的 NKS 文档地图，用于说明 NKS 系列中每份规范的职责、依赖关系和演进边界。

当前 NKS 系列采用分层结构：

- NF-NKS-000 定义全局术语、领域对象和基础关系。
- NF-NKS-100 定义从小说文本抽取知识对象的流程。
- NF-NKS-200 到 NF-NKS-290 定义模块级知识规范和反馈知识规范。

本文档不重新定义领域对象，不描述数据库字段类型，不定义 API 请求响应，也不包含 Prompt 模板正文。

# 2. NKS Document Map

## 2.1 Foundation Documents

| Document ID | Responsibility                                                                  |
| ----------- | ------------------------------------------------------------------------------- |
| NF-NKS-000  | Glossary, domain objects, base Story Graph relationships and lifecycle rules    |
| NF-NKS-001  | NKS document map and module ownership boundaries                                |
| NF-NKS-100  | Book knowledge extraction process, output package, validation and quality gates |

## 2.2 Module Specifications

| Document ID | Responsibility                                                                 |
| ----------- | ------------------------------------------------------------------------------ |
| NF-NKS-200  | Story Graph node, edge, traversal and snapshot model                           |
| NF-NKS-210  | Character profile, role semantics, relationship state and character continuity |
| NF-NKS-220  | Worldview, location, faction, power system and resource knowledge              |
| NF-NKS-230  | Event, conflict, hook, reward and climax knowledge                             |
| NF-NKS-240  | Pattern Library and reusable narrative flow model                              |
| NF-NKS-250  | Rhythm Profile metrics, aggregation and generation constraints                 |
| NF-NKS-260  | Asset Library and reusable creative atom model                                 |
| NF-NKS-270  | Rule and consistency knowledge model                                           |
| NF-NKS-280  | Speech expression, dialogue voice, style taxonomy and anti AI expression model |
| NF-NKS-290  | Feedback knowledge, learning signal, human edit and review signal model        |

## 2.3 Numbering Convention

- `000-099` 表示 NKS 基础和索引文档。
- `100-199` 表示抽取流程和知识生产流程文档。
- `200-299` 表示模块级知识规范和反馈知识规范。

模块文档必须引用 NF-NKS-000 的对象定义，不得重新定义同名对象的权威语义。

# 3. Boundaries, References and Change Log

## 3.1 Boundaries

NF-NKS-001 只维护 NKS 系列地图和模块边界。

模块细节必须落在对应的模块规范中。跨模块概念必须优先回到 NF-NKS-000 定义。

## 3.2 References

- NFES-000
- NF-PRD-001
- NF-NKS-000
- NF-NKS-100
- NF-NKS-280

## 3.3 Approval

Document Status: Draft

Next Review: NKS module coverage review

## 3.4 Change Log

| Version | Date       | Author                                   | Change                          |
| ------- | ---------- | ---------------------------------------- | ------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial NKS document map draft. |
