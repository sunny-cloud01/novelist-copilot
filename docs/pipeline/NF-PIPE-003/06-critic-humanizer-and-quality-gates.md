# 6. Critic, Humanizer and Quality Gates

## 6.1 Critic Quality Gates

Critic 必须输出结构化报告。

检查项：

- knowledge_consistency
- character_consistency
- memory_consistency
- plot_progress
- beat_goal_completion
- pov_purity
- rhythm_match
- reward_delivery
- hook_integrity
- expression_quality
- ai_flavor_signal
- genre_fit

任何 blocking issue 必须打回 Writer。

## 6.2 AI Flavor Rules

必须检查以下高风险模式：

- however_style_transition
- empty_adverb
- cliche_webnovel_phrase
- theme_summary_ending
- action_psychology_summary_sandwich
- excessive_parallelism
- abstract_motivation_statement
- dialogue_without_position
- emotion_without_action
- thick_paragraph_for_mobile_reading

## 6.3 Forbidden Phrase Policy

Forbidden Phrase List 应由 NF-NKS-280 Expression Type 和 NF-NKS-270 Rule 维护。

初始高风险表达包括：

- 不由得
- 刹那间
- 某种意义上
- 一时间
- 仿佛……一般
- 值得一提的是
- 说时迟那时快
- 嘴角微微上扬
- 倒吸一口凉气
- 眼神中闪过一丝复杂
- 如割麦子般倒下
- 这不仅是……更是……
- ……的序幕正缓缓拉开

这些表达不是永久绝对禁用词，但默认不得进入正式生成结果。确需使用时必须有人工批准或特定风格规则允许。

## 6.4 Humanizer Scope

Humanizer 不做大改。

Humanizer 只处理：

- 句式长短重组。
- 段落切碎和手机阅读节奏。
- 去除书面腔对白。
- 降低机械转场。
- 替换泛化表达。
- 保留角色动作和感官剪影。

Humanizer 不得改变事实、剧情目标、伏笔状态、战力结果或角色关系。

## 6.5 Humanized Output Gate

Humanized Beat 必须满足：

- no blocking consistency issue
- ai_flavor_signal below threshold
- voice_drift_signal below threshold
- paragraph_mobile_readability accepted
- no unauthorized fact change
- revision_diff persisted

## 6.6 Human Review Gate

以下情况必须进入人工审核：

- Critic 与 Humanizer 评分冲突。
- 同一 Beat 多次重写失败。
- 关键设定需要新增或变更。
- AI flavor risk 无法自动降低。
- Genre playbook 与用户指定风格冲突。
