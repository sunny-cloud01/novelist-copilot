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
