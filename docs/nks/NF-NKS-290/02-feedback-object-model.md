# 2. Feedback Object Model

## 2.1 Feedback Record

Feedback Record 表示一次可追踪的反馈事件。

最小字段：

- feedback_id
- feedback_type
- source_type
- source_id
- target_type
- target_id
- signal_value
- severity
- confidence
- evidence_refs
- created_by
- created_at
- lifecycle_status

## 2.2 Human Edit

Human Edit 表示人工对生成文本或知识对象的修改。

最小字段：

- human_edit_id
- target_text_ref
- before_ref
- after_ref
- edit_distance
- edit_category
- reason
- affected_expression_type_refs
- affected_prompt_refs
- reviewer_id

## 2.3 Review Signal

Review Signal 表示 Critic、Review Agent、Consistency Service 或 Humanizer 输出的质量信号。

最小字段：

- review_signal_id
- review_report_id
- signal_type
- score
- threshold
- pass_status
- affected_scope
- recommended_action

## 2.4 Reader Signal

Reader Signal 表示外部或模拟读者反馈。

最小字段：

- reader_signal_id
- source_channel
- chapter_id
- beat_id
- reward_signal
- retention_signal
- complaint_category
- comment_summary
- confidence

## 2.5 Cost Quality Signal

Cost Quality Signal 表示模型调用成本与质量结果。

最小字段：

- cost_quality_signal_id
- model_profile_id
- agent_role
- prompt_tokens
- completion_tokens
- latency
- retry_count
- accepted_output_ratio
- human_edit_distance
- quality_score
