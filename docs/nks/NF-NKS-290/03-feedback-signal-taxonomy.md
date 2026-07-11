# 3. Feedback Signal Taxonomy

## 3.1 Feedback Types

允许初始 feedback_type：

- prompt_effectiveness
- model_cost_quality
- retrieval_relevance
- memory_consistency
- style_fit
- voice_drift
- ai_flavor_issue
- forbidden_phrase_hit
- beat_goal_failure
- rhythm_mismatch
- reward_under_delivery
- hook_failure
- genre_playbook_mismatch
- human_edit_pattern
- reader_interest_signal

## 3.2 Target Types

反馈可作用于：

- prompt_template
- prompt_package
- model_profile
- retrieval_strategy
- memory_package_rule
- style_profile
- expression_type
- asset
- pattern
- rhythm_profile
- rule
- genre_playbook
- beat_plan
- chapter_plan

## 3.3 Severity

允许 severity：

- info
- low
- medium
- high
- blocking

blocking 反馈不得自动修改 Approved Knowledge，只能创建 review item、rule update request 或 prompt update request。

## 3.4 Signal Value Rules

signal_value 可以是数值、枚举或结构化对象。

数值型反馈必须声明取值范围。枚举型反馈必须来自受控词表。结构化反馈必须保存 schema_version。
