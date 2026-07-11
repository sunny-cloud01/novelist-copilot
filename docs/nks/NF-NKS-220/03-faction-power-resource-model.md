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
