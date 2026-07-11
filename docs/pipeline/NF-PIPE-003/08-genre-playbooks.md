# 8. Genre Playbooks

## 8.1 Purpose

Genre Playbook 定义不同类型小说的章节结构、读者期待、爽点节奏和禁忌表达。

Planner、Scene Planner、Writer、Critic 和 Humanizer 都必须读取当前 genre_playbook。

## 8.2 Xuanhuan Playbook

玄幻类默认要求：

- 明确 power_level_state。
- 明确主角金手指、功法、法宝或资源变化。
- 明确本章升级进度或战力收益。
- 战斗结果必须符合 Power System。
- 围观者震惊可以作为 reward_expression，但不得机械重复。
- 秘境、宗门、天骄、长老、传承等 Pattern 必须引用 NF-NKS-240。

## 8.3 Urban Power Fantasy Playbook

都市爽文默认要求：

- 反派挑衅。
- 主角隐藏身份或隐藏实力。
- 侧面烘托。
- 打脸反转。
- 围观者震惊或关系反转。
- 余韵中留下下一章钩子。

章节不得在打脸后强行升华主题。主角可以直接收束利益、资源或关系优势。

## 8.4 Scene Planner Social Pressure

Scene Planner 必须标注：

- 谁轻视主角。
- 谁嫉妒主角。
- 谁误判局势。
- 谁被迫改变态度。
- 谁承担冲突后果。
- 谁提供读者代入视角。

## 8.5 Mobile Reading Style

中文网文章节应优先适配手机阅读。

默认段落策略：

- 一到两句一段。
- 高压冲突段落更短。
- 战斗动作拆成清晰连续动作。
- 对白独立成段。
- 避免厚重说明段。

## 8.6 Playbook Validation

Critic 必须检查章节是否满足 genre_playbook。

当 genre_playbook 与用户明确要求冲突时，以用户项目设定为准，并记录 playbook_override。
