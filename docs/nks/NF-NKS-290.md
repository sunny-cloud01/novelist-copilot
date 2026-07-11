---
document_id: NF-NKS-290
title: Feedback Knowledge Specification
version: 1.0.0
status: Draft
category: Novel Knowledge Specification
owner: Novel Factory Knowledge Engineering Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-230
  - NF-NKS-240
  - NF-NKS-250
  - NF-NKS-260
  - NF-NKS-270
  - NF-NKS-280
  - NF-PIPE-003
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-240.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-260.md
  - docs/nks/NF-NKS-270.md
  - docs/nks/NF-NKS-280.md
  - docs/pipeline/NF-PIPE-003.md
---

# NF-NKS-290

# Feedback Knowledge Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 的 Feedback Knowledge。

Feedback Knowledge 将人工修改、AI Review、Critic 报告、Humanizer 改动、读者信号、模型成本和质量结果转化为可治理、可检索、可回放的知识对象。

本文档的目标是让写作流水线不只记录结果，而能从每次生成、审查、重写和人工编辑中学习，反向优化 Prompt、Model Router、Retrieval、Style Profile、Expression Taxonomy、Genre Playbook 和 Rule。

本文档覆盖：

- Feedback Record 对象模型。
- Human Edit、Review Signal、Reader Signal 和 Cost Quality Signal。
- 反馈分类、严重级别和目标对象。
- 反馈如何进入学习目标和治理流程。
- 反馈验证、回滚和边界。

本文档不定义具体推荐算法、在线学习模型或读者平台埋点实现。

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

# 3. Feedback Signal Taxonomy

## 3.1 Feedback Types

允许初始 feedback_type：

- prompt_effectiveness
- model_cost_quality
- retrieval_relevance
- memory_consistency
- style_fit
- voice_drift
- ai_flavor_issue
- forbidden_phrase_hit
- beat_goal_failure
- rhythm_mismatch
- reward_under_delivery
- hook_failure
- genre_playbook_mismatch
- human_edit_pattern
- reader_interest_signal

## 3.2 Target Types

反馈可作用于：

- prompt_template
- prompt_package
- model_profile
- retrieval_strategy
- memory_package_rule
- style_profile
- expression_type
- asset
- pattern
- rhythm_profile
- rule
- genre_playbook
- beat_plan
- chapter_plan

## 3.3 Severity

允许 severity：

- info
- low
- medium
- high
- blocking

blocking 反馈不得自动修改 Approved Knowledge，只能创建 review item、rule update request 或 prompt update request。

## 3.4 Signal Value Rules

signal_value 可以是数值、枚举或结构化对象。

数值型反馈必须声明取值范围。枚举型反馈必须来自受控词表。结构化反馈必须保存 schema_version。

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

# 5. Validation, Boundaries and Change Log

## 5.1 Validation Rules

Feedback Knowledge 必须满足：

- 每条 Feedback Record 必须有 source 和 target。
- blocking 反馈必须进入 Review Service。
- Human Edit 必须保存 before_ref 和 after_ref。
- Cost Quality Signal 必须绑定 model_profile_id。
- Reader Signal 必须记录来源和置信度。
- 反馈驱动的策略变更必须可回滚。

## 5.2 Boundaries

NF-NKS-290 定义反馈知识模型，不定义推荐算法、A/B 测试平台或读者数据采集 SDK。

## 5.3 References

- NF-NKS-000
- NF-NKS-230
- NF-NKS-240
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270
- NF-NKS-280
- NF-PIPE-003

## 5.4 Approval

Document Status: Draft

Next Review: Feedback learning implementation review

Next Document: NF-RAG-001 Knowledge Retrieval and Memory Context Specification

## 5.5 Change Log

| Version | Date       | Author                                   | Change                                    |
| ------- | ---------- | ---------------------------------------- | ----------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial feedback knowledge specification. |
