# 6. Story Graph Relationships

## 6.1 Relationship Definition

Relationship 表示两个节点之间的有向语义关系。

最小语义字段：source_id、relation_type、target_id、confidence、evidence。

## 6.2 Base Relationship Types

| Source        | Relation        | Target    |
| ------------- | --------------- | --------- |
| Character     | belongs_to      | Faction   |
| Character     | owns            | Artifact  |
| Event         | occurs_at       | Location  |
| Character     | hates           | Character |
| Event         | causes          | Event     |
| Foreshadowing | resolves_at     | Chapter   |
| Character     | participates_in | Event     |
| Faction       | controls        | Location  |
| Rule          | constrains      | Character |
| Pattern       | contains        | Event     |

## 6.3 Relationship Constraints

关系必须满足：

- source_id 和 target_id 必须引用已存在对象。
- relation_type 必须来自受控词表。
- evidence 必须能追溯到文本、人工标注或系统推理记录。
- confidence 必须在后续 Schema 中定义取值范围。
