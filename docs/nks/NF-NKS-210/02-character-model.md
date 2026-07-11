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
