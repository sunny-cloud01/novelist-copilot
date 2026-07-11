---
document_id: NF-NKS-260
title: Asset Library Specification
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
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-280
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-280.md
---

# NF-NKS-260

# Asset Library Specification

# 1. Purpose and Scope

本文档定义 Asset Library 的模块级规范。

Asset 是可复用的最小创作单位，可以被 Prompt Engine、Chapter Engine、Pattern Library 和人工创作流程引用。

本文档覆盖：

- Asset model
- Asset type
- Expression Type reference
- 组合规则
- 引用规则
- 质量和去重规则

本文档不保存原文长片段，也不定义版权处理流程。

统一话术、对白语气、叙述口吻、题材表达和反 AI 味分类由 NF-NKS-280 定义。Asset 只保存可复用素材实例，并通过 expression_type_refs 引用 NF-NKS-280 的分类。

# 2. Asset Model

## 2.1 Asset Profile

Asset Profile 表示一个可复用创作素材。

最小字段：

- asset_id
- asset_type
- canonical_name
- content_summary
- expression_type_refs
- style_tags
- genre_scope
- usage_context
- constraints
- source_refs
- evidence_refs
- quality_score

## 2.2 Asset Types

允许初始类型：

- action_phrase
- emotion_phrase
- environment_fragment
- weather_fragment
- object_description
- dialogue_fragment
- combat_move
- transition_sentence
- sensory_detail
- trope_expression

## 2.3 Source Boundary

Asset 必须是可复用的知识素材，而不是未经处理的大段原文。

如果 Asset 来源于已有作品，必须保存 source_refs 和 evidence_refs，并在导出给生成系统时遵守引用长度和改写规则。

## 2.4 Composition Rules

Asset 可以组合成章节生成素材包，但必须满足：

- 同一素材不得在短范围内重复使用。
- Asset 的 genre_scope 必须与目标题材兼容。
- dialogue_fragment 必须绑定 NF-NKS-280 定义的 dialogue_expression 或 Speaker Voice Profile。
- style_tags 必须来自 NF-NKS-280 的 Style Constraint 或已批准 Expression Type。
- combat_move 必须符合 Power System 和 Character capability_state。

# 3. Usage, Validation and Change Log

## 3.1 Usage Context

Asset 可用于：

- Prompt assembly
- Chapter drafting
- Style reference
- Scene enrichment
- Pattern slot filling
- Revision suggestion

## 3.2 Validation Rules

Asset 必须满足：

- asset_type 必须来自受控词表。
- expression_type_refs 必须引用 NF-NKS-280 中已批准的 Expression Type。
- content_summary 必须说明素材用途。
- source_refs 必须可追踪。
- quality_score 必须由人工审核、模型评估或使用反馈产生。
- Deprecated Asset 不得进入新生成请求。

## 3.3 Boundaries

NF-NKS-260 定义素材知识语义，不定义 Prompt 模板、数据库字段类型或具体改写算法。

## 3.4 Change Log

| Version | Date       | Author                                   | Change                               |
| ------- | ---------- | ---------------------------------------- | ------------------------------------ |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial Asset Library specification. |
