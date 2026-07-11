# 3. AI Flavor and Humanity Gates

## 3.1 AI Flavor Indicators

AI 味检查指标：

- forbidden_phrase_hit_count
- repeated_sentence_shape_count
- mechanical_transition_count
- theme_summary_ending_count
- empty_emotion_label_count
- over_explanation_count
- dialogue_without_position_count
- thick_paragraph_count

## 3.2 Humanity Indicators

人味检查指标：

- concrete_action_density
- sensory_anchor_presence
- character_intent_clarity
- emotional_residue_presence
- consequence_visibility
- voice_specificity
- sentence_rhythm_variance

## 3.3 Humanizer Acceptance

Humanizer 输出必须满足：

- ai_flavor_score 下降。
- humanity_score 不下降。
- knowledge_consistency_score 不下降。
- revision_diff 可解释。
- 不改变事实和剧情目标。

## 3.4 Forbidden Phrase Handling

Forbidden phrase hit 不必一律删除，但必须解释保留理由。

默认策略：

- high severity: rewrite required
- medium severity: Humanizer revision
- low severity: allow with reason
