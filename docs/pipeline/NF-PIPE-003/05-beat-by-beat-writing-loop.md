# 5. Beat by Beat Writing Loop

## 5.1 Beat Granularity

默认每个 Beat 生成 300 到 800 中文字。

Beat 不应过长。过长会增加上下文漂移、总结性表达、重复句式和 AI 味风险。

## 5.2 Writer Task

Writer 只负责当前 Beat 的初稿。

Writer 输入：

- beat_plan
- memory_package
- style_profile
- prompt_package
- previous_approved_beat
- forbidden_changes
- output_contract

Writer 输出：

- beat_draft
- self_report
- used_knowledge_refs
- uncertain_points

## 5.3 Writer Restrictions

Writer 不得：

- 改写已批准设定。
- 自行解决未授权伏笔。
- 引入未审核关键设定。
- 一次性跳过多个 Beat。
- 用旁白替代角色选择。
- 在段落末尾做哲理总结。

## 5.4 Critic Pairing

Critic 在每个 Beat 后立即执行。

Critic 检查：

- beat_goal 是否完成。
- POV 是否稳定。
- 角色动机是否合理。
- 战力、物品、地点和时间线是否一致。
- 是否出现 AI 高频句式。
- 是否缺乏动作、感官或具体后果。
- 是否符合 genre playbook。

## 5.5 Rewrite Rule

Critic 未通过时，不得直接进入下一 Beat。

Rewrite Request 必须包含：

- failed_check_ids
- severity
- exact_text_refs
- required_changes
- forbidden_changes
- retry_budget

同一 Beat 自动重写默认最多 2 次。超过上限进入人工审核或 Planner 回退。

## 5.6 Chapter Assembly

所有 Beat 通过后，Chapter Assembly 负责：

- 合并 Beat。
- 消除硬断裂。
- 保持手机阅读段落节奏。
- 检查章节开头、高潮和结尾。
- 生成 chapter_quality_report。

Chapter Assembly 不得大规模改写已通过 Beat。
