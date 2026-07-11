# 6. Usage, Validation, Boundaries and Change Log

## 6.1 Usage Context

Speech Expression and Style Taxonomy 可用于：

- Prompt assembly
- Chapter drafting
- Dialogue revision
- Character voice control
- Style review
- AI flavor review
- Asset tagging
- Pattern slot enrichment
- Feedback signal classification
- Writing quality gate classification

## 6.2 Validation Rules

Expression Taxonomy 必须满足：

- 每个 Expression Type 必须有 canonical_name。
- expression_domain 必须来自受控词表。
- Asset 的 style_tags 和 expression_type_refs 必须引用已批准分类。
- Speaker Voice Profile 必须引用有效 Character、role_type 或 archetype。
- anti_ai_expression 不得直接删除文本，只能生成 review issue 或 revision guidance。
- Deprecated Expression Type 不得进入新的 generation_request。

## 6.3 Boundaries

NF-NKS-280 定义表达分类、话术分类和风格约束。

NF-NKS-280 不保存大段素材实例；Asset 实例由 NF-NKS-260 管理。

NF-NKS-280 不定义 Prompt 模板正文；Prompt 模板由 NF-PROMPT-001 管理。

NF-NKS-280 不定义反馈知识对象；Feedback Record 和学习信号由 NF-NKS-290 管理。

NF-NKS-280 不定义一致性执行算法；可检查规则由 NF-NKS-270 和后端 Consistency Service 管理。

## 6.4 References

- NF-NKS-000
- NF-NKS-001
- NF-NKS-100
- NF-NKS-210
- NF-NKS-230
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270
- NF-NKS-290
- NF-PROMPT-001
- NF-PIPE-002
- NF-PIPE-003
- NF-QA-001

## 6.5 Approval

Document Status: Draft

Next Review: Expression taxonomy and anti AI flavor review

Next Document: NF-NKS-290 Feedback Knowledge Specification

## 6.6 Change Log

| Version | Date       | Author                                   | Change                                                            |
| ------- | ---------- | ---------------------------------------- | ----------------------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial speech expression and style taxonomy specification draft. |
