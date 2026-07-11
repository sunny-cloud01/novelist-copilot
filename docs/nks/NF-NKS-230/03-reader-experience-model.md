# 3. Reader Experience Model

## 3.1 Hook Model

Hook 表示驱动继续阅读的悬念、问题、威胁或未完成承诺。

最小字段：

- hook_id
- hook_type
- open_question
- introduced_at
- expected_resolution_range
- linked_conflict_id
- linked_event_id
- evidence_refs

## 3.2 Reward Model

Reward 表示读者体验中的爽点、满足感或正反馈节点。

最小字段：

- reward_id
- reward_type
- trigger_event_id
- beneficiary_character_id
- reader_effect
- intensity
- payoff_target
- evidence_refs

## 3.3 Climax Model

Climax 表示章节、场景、卷或剧情段落中的强峰值事件。

最小字段：

- climax_id
- scope_type
- scope_id
- event_id
- conflict_id
- reward_refs
- hook_refs
- intensity
- aftermath
- evidence_refs

## 3.4 Experience Constraints

- Hook 必须有 open_question。
- Reward 必须说明 reader_effect。
- Climax 必须至少关联 Event、Conflict、Reward 或 Hook 中的一类对象。
- Reward 与 Climax 不等同。Reward 表示正反馈，Climax 表示叙事峰值。
