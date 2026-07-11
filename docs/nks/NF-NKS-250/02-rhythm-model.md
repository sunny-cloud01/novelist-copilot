# 2. Rhythm Model

## 2.1 Rhythm Profile

Rhythm Profile 表示某个范围内的节奏画像。

最小字段：

- rhythm_profile_id
- scope_type
- scope_id
- climax_index
- conflict_index
- dialogue_ratio
- description_ratio
- battle_ratio
- information_density
- suspense_index
- reward_count
- emotion_curve
- evidence_refs

## 2.2 Metric Definitions

初始指标定义：

| Metric              | Meaning                    |
| ------------------- | -------------------------- |
| climax_index        | 当前范围内叙事峰值强度     |
| conflict_index      | 冲突密度和冲突强度         |
| dialogue_ratio      | 对白占比                   |
| description_ratio   | 描写占比                   |
| battle_ratio        | 战斗或动作场景占比         |
| information_density | 新设定、新关系、新线索密度 |
| suspense_index      | 未解决 Hook 和威胁强度     |
| reward_count        | 明确爽点或正反馈节点数量   |

## 2.3 Emotion Curve

Emotion Curve 表示读者或角色体验随段落推进的变化。

最小字段：

- points
- dominant_emotion
- peak_position
- release_position
- unresolved_tension

Emotion Curve 应引用 Event、Conflict、Reward、Hook 或 Climax 对象。
