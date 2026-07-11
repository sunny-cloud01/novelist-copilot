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
