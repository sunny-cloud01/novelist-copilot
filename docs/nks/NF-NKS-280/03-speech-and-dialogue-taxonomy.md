# 3. Speech and Dialogue Taxonomy

## 3.1 Dialogue Expression Types

对白表达类型描述角色说话的功能，而不是具体句子。

允许初始类型：

- threat_dialogue
- mockery_dialogue
- provocation_dialogue
- command_dialogue
- refusal_dialogue
- confession_dialogue
- concealment_dialogue
- negotiation_dialogue
- bargaining_dialogue
- apology_dialogue
- warning_dialogue
- oath_dialogue
- interrogation_dialogue
- revelation_dialogue
- farewell_dialogue

## 3.2 Speaker Voice Profile

Speaker Voice Profile 表示某类角色或某个角色的稳定口吻约束。

最小字段：

- voice_profile_id
- target_type
- target_id
- tone_tags
- diction_level
- sentence_shape
- directness
- emotional_leakage
- taboo_expressions
- preferred_expression_type_refs
- forbidden_expression_type_refs
- evidence_refs

## 3.3 Tone Tags

允许初始 tone_tags：

- cold
- restrained
- arrogant
- playful
- sincere
- cautious
- ruthless
- scholarly
- vulgar
- formal
- ancient_formal
- plain_direct
- comedic
- threatening
- compassionate

## 3.4 Dialogue Compatibility Rules

对白分类必须满足：

- Dialogue Asset 必须引用至少一个 dialogue_expression。
- Speaker Voice Profile 必须引用 Character、role_type 或 archetype。
- 高傲角色可以使用 mockery_dialogue，但不得默认使用 vulgar 语气。
- 克制型角色的 emotional_leakage 应低于冲动型角色，除非场景目标要求情绪破防。
- 同一场景中不同角色的 dialogue_expression 应体现立场差异。

## 3.5 Dialogue Review Signals

Review Service 应记录：

- voice_drift_signal
- generic_dialogue_signal
- repeated_mockery_signal
- character_position_mismatch
- excessive_explanation_signal
- dialogue_without_intent_signal
