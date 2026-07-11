---
document_id: NF-NKS-220
title: Worldview Location Faction and Power System Specification
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

# NF-NKS-220

# Worldview Location Faction and Power System Specification

# 1. Purpose and Scope

本文档定义 Worldview Library、Location Library、Faction Library、Power System 和 Resource Knowledge 的模块级规范。

这些对象共同描述小说世界如何运行：空间边界、势力结构、等级体系、资源规则、社会秩序和题材约束。

本文档覆盖：

- Worldview model
- Location hierarchy
- Faction model
- Power System model
- Resource model
- 世界一致性验证规则

本文档不定义数据库物理 Schema，也不定义具体生成 Prompt。

# 2. World and Location Model

## 2.1 Worldview Model

Worldview 表示作品或题材的世界规则集合。

最小字段：

- worldview_id
- genre
- core_rules
- social_structure
- power_system_refs
- faction_refs
- location_refs
- resource_rules
- taboo_rules
- evidence_refs

## 2.2 Location Model

Location 表示事件发生或角色活动的空间节点。

最小字段：

- location_id
- canonical_name
- location_type
- parent_location_id
- worldview_id
- access_rules
- resident_factions
- available_resources
- danger_level
- evidence_refs

## 2.3 Location Hierarchy

Location 必须支持层级结构。

示例：

```text
World
└── Continent
    └── Kingdom
        └── City
            └── Auction House
```

子 Location 必须继承上级 Location 的世界规则，除非存在明确例外规则。

# 3. Faction, Power and Resource Model

## 3.1 Faction Model

Faction 表示具有组织结构、利益目标和成员关系的势力。

最小字段：

- faction_id
- canonical_name
- faction_type
- hierarchy
- leader_character_id
- member_refs
- territory_refs
- resource_refs
- alliance_refs
- enemy_refs
- evidence_refs

## 3.2 Power System Model

Power System 表示力量、修炼、等级或能力成长体系。

最小字段：

- power_system_id
- canonical_name
- level_sequence
- advancement_rules
- constraints
- breakthrough_costs
- failure_consequences
- forbidden_transitions
- evidence_refs

## 3.3 Resource Model

Resource 表示可被角色、势力或世界规则消耗、争夺或分配的资源。

最小字段：

- resource_id
- canonical_name
- resource_type
- scarcity
- usage_rule
- production_rule
- owner_refs
- location_refs
- evidence_refs

## 3.4 Cross Object Constraints

- Character 的能力成长必须符合 Power System。
- Faction 的领地必须引用有效 Location。
- Resource 的使用必须符合 Worldview 和 Power System 规则。
- Faction 关系变化必须通过 Event、Conflict 或 Review Record 解释。

# 4. Validation, Boundaries and Change Log

## 4.1 Validation Rules

World knowledge 必须满足：

- 每个 Location 必须属于一个 Worldview 或上级 Location。
- Power System 的 level_sequence 必须有稳定顺序。
- Character 的 capability_state 不得跳过不可跳过等级。
- Faction 的成员和敌友关系必须引用存在对象。
- Resource 的 scarcity 和 usage_rule 必须可解释。

## 4.2 Boundaries

NF-NKS-220 定义世界、地点、势力、力量和资源语义，不定义存储引擎或界面展示。

## 4.3 References

- NF-NKS-000
- NF-NKS-100
- NF-NKS-200
- NF-NKS-210

## 4.4 Change Log

| Version | Date       | Author                                   | Change                                        |
| ------- | ---------- | ---------------------------------------- | --------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial world knowledge module specification. |
