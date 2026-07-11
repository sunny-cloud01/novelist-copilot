# 4. Learning Targets and Governance

## 4.1 Learning Targets

Feedback Knowledge 可用于优化：

- Model Router 权重。
- Prompt Template 版本。
- Retrieval 策略。
- Memory Package 组装规则。
- Style Profile。
- Expression Taxonomy。
- Forbidden Phrase Rule。
- Genre Playbook。
- Beat Planning 策略。

## 4.2 Governance Rule

反馈不得直接覆盖权威知识。

反馈只能产生：

- ranking_signal
- update_suggestion
- review_item
- change_request
- experiment_config
- rollback_request

## 4.3 Promotion Rule

反馈进入正式策略前必须满足：

- 有足够样本量。
- 有明确目标对象。
- 质量收益可解释。
- 不破坏一致性规则。
- 可回滚。

## 4.4 Rollback Rule

任何由反馈驱动的策略更新必须记录 previous_version、new_version、reason、approval_record 和 rollback_strategy。
