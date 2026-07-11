# 2. Quality Score Model

## 2.1 Score Range

所有质量分默认使用 0 到 100。

建议解释：

- 90-100: excellent
- 75-89: pass
- 60-74: needs revision
- 0-59: blocked

## 2.2 Core Scores

写作质量至少包含：

- knowledge_consistency_score
- character_consistency_score
- plot_coherence_score
- beat_goal_completion_score
- rhythm_match_score
- reward_delivery_score
- hook_integrity_score
- ai_flavor_score
- humanity_score
- voice_fit_score
- mobile_readability_score
- originality_safety_score

## 2.3 Default Pass Thresholds

默认通过阈值：

| Score                       | Pass Threshold |
| --------------------------- | -------------- |
| knowledge_consistency_score | 90             |
| character_consistency_score | 85             |
| plot_coherence_score        | 80             |
| beat_goal_completion_score  | 80             |
| rhythm_match_score          | 75             |
| reward_delivery_score       | 75             |
| hook_integrity_score        | 80             |
| ai_flavor_score             | <= 25          |
| humanity_score              | 75             |
| voice_fit_score             | 80             |
| mobile_readability_score    | 75             |
| originality_safety_score    | 85             |

ai_flavor_score 越低越好。

## 2.4 Blocking Rules

以下情况直接 blocking：

- 已批准事实被改写。
- 角色战力或状态严重冲突。
- 未授权关键设定被引入。
- ai_flavor_score 高于 45。
- originality_safety_score 低于 70。
- Humanizer 改变剧情事实。
