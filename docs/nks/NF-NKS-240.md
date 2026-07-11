---
document_id: NF-NKS-240
title: Pattern Library Specification
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
  - NF-NKS-230
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-230.md
---

# NF-NKS-240

# Pattern Library Specification

# 1. Purpose and Scope

本文档定义 Pattern Library 的模块级规范。

Pattern 是可复用、可参数化、可组合的叙事流程，用于从已抽取作品中沉淀网文套路，并为章节计划、Prompt Engine 和生成约束提供结构化输入。

本文档覆盖：

- Pattern model
- Pattern step
- Slot and parameter
- Pattern composition
- Pattern validation

本文档不定义具体 Prompt 模板，也不保证某个 Pattern 适用于所有题材。

# 2. Pattern Model

## 2.1 Pattern Profile

Pattern Profile 表示一个可复用套路。

最小字段：

- pattern_id
- canonical_name
- pattern_type
- genre_scope
- intent
- preconditions
- steps
- slots
- expected_reader_effect
- compatible_rhythm_profile
- evidence_refs

## 2.2 Pattern Step

Pattern Step 表示套路中的一个阶段。

最小字段：

- step_id
- order_index
- step_type
- required_objects
- optional_objects
- expected_event_type
- expected_reward_type
- transition_condition

## 2.3 Slot Model

Slot 表示可替换参数。

常见 Slot：

- protagonist
- antagonist
- location
- faction
- artifact
- resource
- hidden_identity
- threat
- reward

Slot 必须声明类型约束，禁止将 Faction 填入 Character Slot。

## 2.4 Initial Pattern Types

允许初始 Pattern 类型：

- underdog_rise
- auction_house
- secret_realm_competition
- sect_assessment
- identity_reveal
- counterattack
- revenge_arc
- rescue_arc
- tournament_arc
- inheritance_discovery

# 3. Composition, Validation and Change Log

## 3.1 Composition Rules

Pattern 可以组合，但必须满足：

- 前一个 Pattern 的结果可作为后一个 Pattern 的前置条件。
- Slot 类型必须兼容。
- Rhythm Profile 不得连续堆叠高峰值而无缓冲。
- 同一章节内不得重复使用语义相同的 Reward，除非目标是强化同一爽点。

## 3.2 Validation Rules

Pattern 必须满足：

- 每个 Pattern 至少包含三个 Step。
- 每个 required slot 必须被填充。
- 每个 Step 必须绑定预期 Event、Conflict、Hook 或 Reward。
- Pattern 来源必须有 evidence 或人工定义记录。

## 3.3 Boundaries

NF-NKS-240 定义 Pattern 语义，不定义 Prompt 拼接格式。Prompt 拼接由 NF-PROMPT 文档负责。

## 3.4 Change Log

| Version | Date       | Author                                   | Change                                 |
| ------- | ---------- | ---------------------------------------- | -------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial Pattern Library specification. |
