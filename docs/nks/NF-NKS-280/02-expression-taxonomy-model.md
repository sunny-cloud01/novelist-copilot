# 2. Expression Taxonomy Model

## 2.1 Expression Type

Expression Type 表示一个可复用、可检索、可组合的表达分类。

最小字段：

- expression_type_id
- canonical_name
- display_name
- parent_expression_type_id
- expression_domain
- function_tags
- genre_scope
- style_scope
- compatible_character_roles
- compatible_emotion_types
- compatible_rhythm_range
- risk_tags
- example_asset_refs
- forbidden_asset_refs
- evidence_refs
- lifecycle_status

## 2.2 Expression Domain

允许初始 expression_domain：

- dialogue_expression
- narration_expression
- emotion_expression
- action_expression
- sensory_expression
- transition_expression
- reward_expression
- hook_expression
- conflict_expression
- genre_expression
- style_constraint
- anti_ai_expression

## 2.3 Function Tags

function_tags 用于说明表达在章节中的叙事功能。

允许初始值：

- threat
- mockery
- provocation
- concealment
- confession
- negotiation
- command
- refusal
- realization
- suspicion
- tension_building
- suspense_opening
- reward_delivery
- reversal_signal
- cliffhanger
- aftermath
- scene_transition
- pacing_buffer

## 2.4 Relationship to Asset

Expression Type 是分类和约束，Asset 是具体素材实例。

示例：

```text
Expression Type: mockery_dialogue
Asset: "就凭你？"
Asset: "你也配？"
Asset: "这点本事，也敢站出来？"
```

Asset 必须引用 Expression Type，Expression Type 不直接保存大段可复制文本。

## 2.5 Relationship to Rule

当表达分类用于禁止、限制或强制时，必须通过 NF-NKS-270 Rule 或 Consistency Constraint 承载可检查规则。

示例：

```text
Expression Type: mechanical_transition
Rule: 同一章节不得连续使用三个语义相同的机械转场句。
```
