# 6. Human Review and Feedback

## 6.1 Human Review Gate

以下情况必须进入人工审核：

- 高严重级别一致性违规。
- 角色行为明显偏离已批准状态。
- 章节目标完成但文本 AI 味过重。
- 自动修订超过上限。
- 生成引入新关键设定。
- 审核策略要求人工批准。

## 6.2 Review Actions

人工审核者可以执行：

- approve_draft
- request_revision
- reject_draft
- edit_draft
- mark_issue_resolved
- create_feedback_record
- create_rule_update_request
- create_pattern_update_request

所有操作必须写入 audit_events。

## 6.3 Feedback Signals

Feedback Service 必须保存：

- prompt_effectiveness
- pattern_fit
- rhythm_fit
- character_consistency_score
- world_consistency_score
- reader_interest_signal
- repetition_signal
- human_edit_distance
- issue_category

## 6.4 Feedback Targets

反馈可以作用于：

- Prompt Template
- Pattern
- Rhythm Profile
- Asset
- Rule
- Character State
- Generation Strategy
- Retrieval Strategy

反馈不得直接覆盖 Approved Knowledge。需要修改知识时必须进入 Review Service 或 Knowledge Service 的受控流程。

## 6.5 Learning Loop

反馈回流后，系统可以更新 ranking_signals、quality_thresholds、prompt evaluation results 和 retrieval weights。

任何影响正式生成策略的变更必须可追踪到 feedback_record 或 review_report。
