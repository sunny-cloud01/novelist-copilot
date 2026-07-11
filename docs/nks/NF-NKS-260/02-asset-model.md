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
