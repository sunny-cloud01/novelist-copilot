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
