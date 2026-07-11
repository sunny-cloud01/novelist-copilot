---
document_id: NF-NKS-210
title: Character and Relationship Knowledge Specification
version: 1.0.0
status: Draft
category: Novel Knowledge Specification
owner: Novel Factory Knowledge Engineering Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-200
references:
  - docs/standards/NFES-000.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-200.md
---

# NF-NKS-210

# Character and Relationship Knowledge Specification

# 1. Purpose and Scope

本文档定义 Character Library 与 Character Relationship 的模块级知识规范。

Character 是长篇小说生成中最重要的连续性对象之一。系统必须稳定记录角色身份、动机、成长、能力、关系、状态变化和证据来源。

本文档覆盖：

- Character profile
- Character state
- Character relationship
- 角色连续性约束
- 角色关系验证规则

本文档不重新定义 Character 的基础语义。Character 的权威定义仍来源于 NF-NKS-000。

# 2. Character Model

## 2.1 Character Profile

Character Profile 表示角色的稳定画像。

最小字段：

- character_id
- canonical_name
- display_name
- aliases
- role_type
- archetype
- motivation
- personality_traits
- capability_profile
- growth_path
- faction_refs
- relationship_refs
- evidence_refs

## 2.2 Role Type

`role_type` 必须来自受控词表。

允许初始值：

- protagonist
- antagonist
- ally
- mentor
- rival
- love_interest
- family_member
- faction_leader
- background_character

## 2.3 Character State

Character State 表示角色在特定时间范围内的可变状态。

最小字段：

- state_id
- character_id
- temporal_scope
- location_id
- faction_id
- status
- capability_state
- emotional_state
- known_information
- active_goal
- evidence_refs

状态不得覆盖 Profile。Profile 表示稳定身份，State 表示阶段性状态。

## 2.4 Continuity Requirements

角色连续性必须满足：

- 同一角色的别名必须归并到稳定 character_id。
- 角色死亡、失踪、背叛、晋升等状态变化必须通过 Event 或 Review Record 解释。
- 能力成长不得违反 Power System 规则。
- 角色位置变化必须与时间线和 Location 关系兼容。

# 3. Relationship Model

## 3.1 Relationship Profile

Character Relationship 表示两个角色或角色与势力之间的阶段性关系。

最小字段：

- relationship_id
- source_character_id
- target_object_id
- relation_type
- relation_strength
- relation_status
- temporal_scope
- trigger_event_id
- evidence_refs

## 3.2 Relation Types

允许初始关系类型：

- ally_of
- enemy_of
- mentor_of
- disciple_of
- family_of
- rival_of
- loyal_to
- betrays
- protects
- owes_debt_to
- competes_with
- secretly_identity_linked_to

## 3.3 Relationship State Change

关系变化必须由 Event、Conflict、Reward、Hook 或 Review Record 驱动。

示例：

```text
ally_of -> suspicious_of -> enemy_of
```

此类变化必须保留 temporal_scope，禁止直接覆盖原始关系。

# 4. Validation, Boundaries and Change Log

## 4.1 Validation Rules

Character 知识必须满足：

- 每个 Character 必须有稳定 character_id。
- 每个 Alias 必须指向一个 Character 或 unresolved candidate。
- Character State 必须绑定 temporal_scope。
- Relationship 的 source 和 target 必须存在。
- 关系变化必须绑定 evidence 或 trigger_event_id。

## 4.2 Boundaries

NF-NKS-210 定义角色与关系知识模型，不定义数据库字段类型或 Prompt 文案。

## 4.3 References

- NF-NKS-000
- NF-NKS-100
- NF-NKS-200

## 4.4 Change Log

| Version | Date       | Author                                   | Change                                            |
| ------- | ---------- | ---------------------------------------- | ------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial Character and Relationship specification. |
