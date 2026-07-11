---
document_id: NF-ADR-001
title: Adopt Documentation Project Architecture
version: 1.0.0
status: Draft
category: Architecture Decision Record
owner: Novel Factory Architecture Team
created: 2026-07-09
updated: 2026-07-09
dependencies:
  - NFES-000
references:
  - docs/standards/NFES-000.md
---

# NF-ADR-001

# Adopt Documentation Project Architecture

# 1. Status and Context

## 1.1 Status

Draft

## 1.2 Context

Novel Factory 文档体系预计包含产品、知识工程、架构、数据库、Agent、Prompt、API、运维和决策记录等多个文档类别。

其中 NF-NKS-100 等知识工程文档可能持续增长。如果只维护单个超长 Markdown 文件，会出现页面渲染混乱、单文件审阅成本高、局部修改影响无关章节、AI/RAG 切片不稳定、后续导出缺少构建边界等问题。

# 2. Decision

Novel Factory 采用 Documentation Project Architecture。

每个正式文档同时维护：

```text
docs/{category}/{document-id}.md
docs/{category}/{document-id}/README.md
docs/{category}/{document-id}/{chapter}.md
```

语义约定：

- `{document-id}.md` 是 canonical 汇总文档和正式阅读版。
- `{document-id}/` 下的章节文件是 source chapters，用于局部维护和后续自动构建。
- 当前阶段允许人工同步 canonical 与 source chapters。
- 后续应引入 build script，使 source chapters 成为自动生成 canonical 文档的来源。

# 3. Consequences

## 3.1 Positive Consequences

- 长文档可以逐章维护。
- 文档结构适合 Git diff 和 Review。
- AI/RAG 可以按章节稳定切片。
- 后续可自动生成 Markdown、PDF、JSON、YAML 和网站。
- 每个文档可拥有独立章节索引。

## 3.2 Negative Consequences

- 当前没有自动构建脚本时，canonical 文件和章节源文件可能漂移。
- 文档数量增加，目录结构更复杂。
- 作者必须理解 canonical 与 source chapters 的关系。

## 3.3 Mitigations

- README 必须登记 canonical 文档。
- 每个章节目录必须包含 README.md。
- 后续应创建构建脚本，将 source chapters 合并成 canonical 文档。
- Validation 应检查 Front Matter、document_id、占位符和章节完整性。

# 4. Alternatives Considered

## 4.1 Single Markdown File per Document

Rejected.

原因：不适合超长 NKS 文档，也不利于局部审阅和后续构建。

## 4.2 Chat-Only Documentation

Rejected.

原因：聊天记录不可作为稳定工程文档来源，容易混入解释性文字和渲染残留。

## 4.3 External Wiki Only

Rejected for current phase.

原因：当前阶段需要 Git 友好的本地文档工程，Wiki 可以作为后续发布目标。

# 5. Implementation, Review, and Change Log

## 5.1 Implementation Notes

当前已采用该结构维护 NFES-000、NF-PRD-001、NF-NKS-000、NF-NKS-001、NF-NKS-100、NF-NKS-200、NF-NKS-210、NF-NKS-220、NF-NKS-230、NF-NKS-240、NF-NKS-250、NF-NKS-260、NF-NKS-270、NF-NKS-280、NF-NKS-290、NF-ARCH-001、NF-ARCH-002、NF-DBS-001、NF-DBS-002、NF-PIPE-001、NF-PIPE-002、NF-PIPE-003、NF-AGENT-001、NF-PROMPT-001、NF-PROMPT-002、NF-RAG-001、NF-QA-001、NF-IMPL-001、NF-IMPL-002、NF-IMPL-003、NF-API-001、NF-OPS-001 和 NF-ADR-001。

当前已引入 `scripts/build_docs.py`，用于列出、检查和生成 canonical 文档。

## 5.2 Review Criteria

本 ADR 进入 Approved 前，需要确认 canonical 文档是否继续允许手工编辑、source chapters 是否成为唯一 source of truth、是否需要在 CI 中验证章节合并结果。

## 5.3 References

- NFES-000

## 5.4 Approval

Document Status: Draft

Next Review: NF-ADR-001 Review

Next Document: Build Process Specification or NFES-001 Build Standard

## 5.5 Change Log

| Version | Date       | Author                          | Change                                                         |
| ------- | ---------- | ------------------------------- | -------------------------------------------------------------- |
| 1.0.0   | 2026-07-09 | Novel Factory Architecture Team | Initial Draft for documentation project architecture decision. |
