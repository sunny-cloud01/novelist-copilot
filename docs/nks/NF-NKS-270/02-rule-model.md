# 2. Rule Model

## 2.1 Rule Profile

Rule Profile 表示一条可被检查或引用的规则。

最小字段：

- rule_id
- rule_type
- scope_type
- scope_id
- statement
- condition
- constraint
- severity
- lifecycle_status
- evidence_refs

## 2.2 Rule Types

允许初始类型：

- character_rule
- timeline_rule
- location_rule
- power_system_rule
- artifact_rule
- age_rule
- faction_rule
- worldview_rule
- foreshadowing_rule
- generation_constraint

## 2.3 Consistency Constraint

Consistency Constraint 表示一条可检查的约束。

最小字段：

- constraint_id
- rule_id
- target_object_type
- target_object_id
- check_type
- expected_condition
- violation_severity
- recovery_guidance

## 2.4 Violation Record

Violation Record 表示一次检测到的不一致。

最小字段：

- violation_id
- constraint_id
- detected_scope
- violated_text_ref
- violated_object_refs
- severity
- explanation
- recommended_action
- review_status
