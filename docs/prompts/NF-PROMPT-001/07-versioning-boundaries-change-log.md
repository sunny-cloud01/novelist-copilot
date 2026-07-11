# 7. Versioning, Boundaries, and Change Log

## 7.1 Versioning

Prompt Template 使用 Semantic Versioning。

Major：变量结构或输出契约不兼容变更。

Minor：新增变量、规则或可选章节。

Patch：措辞、格式或示例修正。

Prompt Package 必须记录 template_version。

## 7.2 Safety and Boundary Rules

Prompt 不得要求模型忽略系统规范、绕过人工审核或改写已批准事实。

Prompt 不得在模板中重新定义 NF-NKS-000 对象语义或 NF-NKS-200 到 NF-NKS-270 的模块语义。

写作流水线的具体 Prompt Pack 由 NF-PROMPT-002 管理。

Prompt 不得把数据库物理字段当作唯一业务定义。

## 7.3 References

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
- NF-AGENT-001
- NF-PIPE-003
- NF-PROMPT-002

## 7.4 Approval

Document Status: Draft

Next Review: NF-PROMPT-001 Review

Next Document: NF-PROMPT-002 Writing Prompt Pack Specification

## 7.5 Change Log

| Version | Date       | Author                                | Change                                           |
| ------- | ---------- | ------------------------------------- | ------------------------------------------------ |
| 1.0.0   | 2026-07-09 | Novel Factory Prompt Engineering Team | Initial Draft for Prompt template specification. |
