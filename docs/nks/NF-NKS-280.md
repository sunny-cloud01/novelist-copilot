---
document_id: NF-NKS-280
title: Speech Expression and Style Taxonomy Specification
version: 1.0.0
status: Draft
category: Novel Knowledge Specification
owner: Novel Factory Knowledge Engineering Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-210
  - NF-NKS-230
  - NF-NKS-250
  - NF-NKS-260
  - NF-NKS-270
  - NF-NKS-290
  - NF-PIPE-003
  - NF-QA-001
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-210.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-260.md
  - docs/nks/NF-NKS-270.md
  - docs/nks/NF-NKS-290.md
  - docs/pipeline/NF-PIPE-003.md
  - docs/quality/NF-QA-001.md
---

# NF-NKS-280

# Speech Expression and Style Taxonomy Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 的 Speech Expression and Style Taxonomy。

Speech Expression and Style Taxonomy 是统一话术、表达功能、对白语气、叙述口吻、题材表达和反 AI 味控制的权威分类规范。

该规范解决以下问题：

- Asset Library 只能保存素材实例，不能独立承担表达分类治理。
- Prompt Engine 需要稳定分类来选择表达策略，而不是随机拼接片段。
- Character Prompt 需要角色口吻约束，而不是只依赖自由文本描述。
- Review Service 需要识别重复句式、泛化表达和 AI 味风险。
- Feedback Loop 需要把人工修改反向归类到可学习的表达类型。

本文档覆盖：

- 表达分类模型。
- 对白与角色口吻分类。
- 叙述、题材和场景表达分类。
- 风格约束和反 AI 味分类。
- 与 Asset、Prompt、Rule、Rhythm 和 Review 的引用边界。

本文档不保存大段原文，不定义具体 Prompt 模板正文，不规定模型供应商参数，也不替代 NF-NKS-260 的 Asset 实例管理。

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

# 4. Narration Style and Genre Expression

## 4.1 Narration Expression Types

叙述表达类型描述非对白文本的功能。

允许初始类型：

- scene_opening
- sensory_anchor
- tension_building
- emotional_interiority
- action_continuity
- information_reveal
- setting_exposition
- reward_delivery
- aftermath_reflection
- transition_bridge
- cliffhanger_close
- hook_reinforcement

## 4.2 Genre Expression Scope

genre_expression 用于记录题材表达习惯。

允许初始 genre_scope：

- xuanhuan
- xianxia
- urban
- sci_fi
- suspense
- historical
- romance
- game_system

每个 genre_expression 必须说明适用题材、禁用题材和典型使用场景。

## 4.3 Style Constraint Types

Style Constraint 表示生成文本的风格约束。

允许初始类型：

- plain_direct
- fast_paced
- restrained_emotional
- vivid_sensory
- ancient_formal
- modern_colloquial
- comedic_light
- brutal_fast
- lyrical_reflective
- dense_information

## 4.4 Rhythm Compatibility

Expression Type 必须能与 Rhythm Profile 协同使用。

示例：

- 高 climax_index 场景优先使用 action_continuity、reward_delivery 和 tension_building。
- 低 information_density 缓冲段落可以使用 aftermath_reflection 和 sensory_anchor。
- 高 suspense_index 章节结尾可以使用 cliffhanger_close 和 hook_reinforcement。

## 4.5 Genre Boundary Rules

- 题材表达不得替代 Worldview、Power System 或 Rule。
- 题材表达不得引入未经审核的新设定。
- style_tags 必须来自受控词表或已批准 Expression Type。
- 同一作品内的 genre_expression 应保持稳定，除非 generation_request 明确要求风格切换。

# 5. Anti AI Expression and Repetition Control

## 5.1 Anti AI Expression Types

anti_ai_expression 用于标记容易产生 AI 味、模板感或机械重复的表达风险。

允许初始类型：

- generic_phrase
- empty_emotion_label
- over_explanation
- mechanical_transition
- repeated_sentence_shape
- excessive_summary
- abstract_motivation_statement
- emotion_without_action
- dialogue_without_position
- conflict_without_consequence
- sensory_cliche

## 5.2 Risk Tags

允许初始 risk_tags：

- high_repetition_risk
- high_ai_flavor_risk
- genre_mismatch_risk
- character_voice_drift_risk
- rhythm_break_risk
- overused_reward_expression
- low_specificity
- weak_scene_grounding

## 5.3 Repetition Control

系统必须支持以下重复检测：

- 同一章节内 expression_type 重复。
- 相邻章节内 dialogue_expression 重复。
- 同一角色的句式重复。
- 同一 Pattern 中 reward_expression 重复。
- transition_expression 机械串联。
- emotion_expression 只报情绪标签而无动作、选择或后果。

## 5.4 Review Outputs

Review Service 对表达问题应输出：

- issue_id
- expression_type_id
- affected_text_ref
- issue_category
- severity
- explanation
- suggested_expression_type_refs
- suggested_asset_refs
- revision_guidance

## 5.5 Revision Guidance

修订时不得只做同义词替换。

有效修订应优先改变：

- 角色立场。
- 动作承载。
- 场景感官锚点。
- 句式节奏。
- 信息释放顺序。
- 情绪外泄程度。
- 冲突后果。

# 6. Usage, Validation, Boundaries and Change Log

## 6.1 Usage Context

Speech Expression and Style Taxonomy 可用于：

- Prompt assembly
- Chapter drafting
- Dialogue revision
- Character voice control
- Style review
- AI flavor review
- Asset tagging
- Pattern slot enrichment
- Feedback signal classification
- Writing quality gate classification

## 6.2 Validation Rules

Expression Taxonomy 必须满足：

- 每个 Expression Type 必须有 canonical_name。
- expression_domain 必须来自受控词表。
- Asset 的 style_tags 和 expression_type_refs 必须引用已批准分类。
- Speaker Voice Profile 必须引用有效 Character、role_type 或 archetype。
- anti_ai_expression 不得直接删除文本，只能生成 review issue 或 revision guidance。
- Deprecated Expression Type 不得进入新的 generation_request。

## 6.3 Boundaries

NF-NKS-280 定义表达分类、话术分类和风格约束。

NF-NKS-280 不保存大段素材实例；Asset 实例由 NF-NKS-260 管理。

NF-NKS-280 不定义 Prompt 模板正文；Prompt 模板由 NF-PROMPT-001 管理。

NF-NKS-280 不定义反馈知识对象；Feedback Record 和学习信号由 NF-NKS-290 管理。

NF-NKS-280 不定义一致性执行算法；可检查规则由 NF-NKS-270 和后端 Consistency Service 管理。

## 6.4 References

- NF-NKS-000
- NF-NKS-001
- NF-NKS-100
- NF-NKS-210
- NF-NKS-230
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270
- NF-NKS-290
- NF-PROMPT-001
- NF-PIPE-002
- NF-PIPE-003
- NF-QA-001

## 6.5 Approval

Document Status: Draft

Next Review: Expression taxonomy and anti AI flavor review

Next Document: NF-NKS-290 Feedback Knowledge Specification

## 6.6 Change Log

| Version | Date       | Author                                   | Change                                                            |
| ------- | ---------- | ---------------------------------------- | ----------------------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial speech expression and style taxonomy specification draft. |
