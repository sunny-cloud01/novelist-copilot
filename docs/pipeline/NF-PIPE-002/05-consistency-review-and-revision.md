# 5. Consistency Review and Revision

## 5.1 Consistency Review

Consistency Service 必须检查 Draft Candidate 是否违反已批准知识。

检查域：

- Character continuity
- relationship state
- timeline continuity
- location continuity
- power system constraints
- artifact uniqueness
- faction relationship state
- unresolved hook state
- rule and foreshadowing constraints

## 5.2 AI Quality Review

AI Quality Review 检查文本质量。

评估指标：

- instruction_following
- knowledge_consistency
- character_consistency
- plot_coherence
- rhythm_match
- rule_compliance
- repetition_signal
- AI_flavor_signal
- revision_efficiency

Review Prompt 必须输出可执行问题列表，不得只输出笼统评价。

## 5.3 Revision Run

Revision Run 根据 consistency_report、quality_report 和 human_review_notes 生成修订稿。

修订必须遵守：

- 不改写已批准事实。
- 不引入未审核关键设定。
- 不破坏章节目标。
- 修复问题必须可追踪到 issue_id。
- 每次修订必须生成 revision_diff 或 revision_summary。

## 5.4 Revision Loop Limit

自动修订必须有循环上限。

建议默认：

- max_revision_rounds: 3
- max_provider_retry: 2
- max_consistency_blocker: 0 for auto approval

超过上限必须进入 Human Review Gate。

## 5.5 Approval Criteria

Draft 可以进入 Approved Draft 状态，至少需要满足：

- no blocking consistency violation
- no high severity rule violation
- review_status approved or explicit auto_approval_policy matched
- output_ref persisted
- prompt_package_ref persisted
- quality_report persisted
