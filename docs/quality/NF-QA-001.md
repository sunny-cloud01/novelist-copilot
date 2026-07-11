---
document_id: NF-QA-001
title: Writing Quality Gate Specification
version: 1.0.0
status: Draft
category: Quality Assurance Specification
owner: Novel Factory Quality Engineering Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-NKS-230
  - NF-NKS-250
  - NF-NKS-270
  - NF-NKS-280
  - NF-NKS-290
  - NF-RAG-001
  - NF-PROMPT-002
  - NF-PIPE-003
references:
  - docs/standards/NFES-000.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-270.md
  - docs/nks/NF-NKS-280.md
  - docs/nks/NF-NKS-290.md
  - docs/rag/NF-RAG-001.md
  - docs/prompts/NF-PROMPT-002.md
  - docs/pipeline/NF-PIPE-003.md
---

# NF-QA-001

# Writing Quality Gate Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 的 Writing Quality Gate。

Writing Quality Gate 将“合理”“有人味”“少 AI 味”“爽点到位”“适合手机阅读”等目标转化为可检查、可评分、可回放的质量门禁。

本文档覆盖：

- 写作质量评分模型。
- AI 味和人味门禁。
- 叙事一致性门禁。
- Genre Playbook 门禁。
- 通过阈值、阻塞规则和反馈输出。

本文档不定义具体模型评分算法或人工审稿 UI。

# 2. Quality Score Model

## 2.1 Score Range

所有质量分默认使用 0 到 100。

建议解释：

- 90-100: excellent
- 75-89: pass
- 60-74: needs revision
- 0-59: blocked

## 2.2 Core Scores

写作质量至少包含：

- knowledge_consistency_score
- character_consistency_score
- plot_coherence_score
- beat_goal_completion_score
- rhythm_match_score
- reward_delivery_score
- hook_integrity_score
- ai_flavor_score
- humanity_score
- voice_fit_score
- mobile_readability_score
- originality_safety_score

## 2.3 Default Pass Thresholds

默认通过阈值：

| Score                       | Pass Threshold |
| --------------------------- | -------------- |
| knowledge_consistency_score | 90             |
| character_consistency_score | 85             |
| plot_coherence_score        | 80             |
| beat_goal_completion_score  | 80             |
| rhythm_match_score          | 75             |
| reward_delivery_score       | 75             |
| hook_integrity_score        | 80             |
| ai_flavor_score             | <= 25          |
| humanity_score              | 75             |
| voice_fit_score             | 80             |
| mobile_readability_score    | 75             |
| originality_safety_score    | 85             |

ai_flavor_score 越低越好。

## 2.4 Blocking Rules

以下情况直接 blocking：

- 已批准事实被改写。
- 角色战力或状态严重冲突。
- 未授权关键设定被引入。
- ai_flavor_score 高于 45。
- originality_safety_score 低于 70。
- Humanizer 改变剧情事实。

# 3. AI Flavor and Humanity Gates

## 3.1 AI Flavor Indicators

AI 味检查指标：

- forbidden_phrase_hit_count
- repeated_sentence_shape_count
- mechanical_transition_count
- theme_summary_ending_count
- empty_emotion_label_count
- over_explanation_count
- dialogue_without_position_count
- thick_paragraph_count

## 3.2 Humanity Indicators

人味检查指标：

- concrete_action_density
- sensory_anchor_presence
- character_intent_clarity
- emotional_residue_presence
- consequence_visibility
- voice_specificity
- sentence_rhythm_variance

## 3.3 Humanizer Acceptance

Humanizer 输出必须满足：

- ai_flavor_score 下降。
- humanity_score 不下降。
- knowledge_consistency_score 不下降。
- revision_diff 可解释。
- 不改变事实和剧情目标。

## 3.4 Forbidden Phrase Handling

Forbidden phrase hit 不必一律删除，但必须解释保留理由。

默认策略：

- high severity: rewrite required
- medium severity: Humanizer revision
- low severity: allow with reason

# 4. Narrative Consistency and Genre Gates

## 4.1 Narrative Consistency Gates

必须检查：

- Character 状态连续。
- Relationship 状态连续。
- Location 和 timeline 合理。
- Power System 不被破坏。
- Artifact 唯一性不被破坏。
- Hook 状态合理推进或保留。
- Beat 目标完成。

## 4.2 Genre Playbook Gates

Genre Playbook 检查：

- 玄幻章节必须检查 power_level_state、资源收益、战斗约束和围观者反馈是否过度重复。
- 都市爽文章节必须检查挑衅、压制、反转、打脸和余韵是否闭合。
- 悬疑章节必须检查线索释放、误导、公平性和悬念保留。

## 4.3 Mobile Readability Gates

手机阅读检查：

- 平均段落长度不应过长。
- 高压冲突段落应短。
- 对白应独立成段。
- 说明性段落不得连续堆叠。
- 章节结尾应停在动作、对白、感官剪影或悬念上。

## 4.4 Originality Safety Gates

原创性安全检查：

- 不复刻来源作品独特情节组合。
- 不复制受版权文本表达。
- 风格只抽象为节奏、句式和表达分类。
- similarity_risk 高时进入人工审核。

# 5. Validation, Boundaries and Change Log

## 5.1 Quality Report Contract

Quality Report 至少包含：

- quality_report_id
- target_scope
- score_summary
- blocking_issues
- revision_required
- human_review_required
- feedback_records
- evidence_refs

## 5.2 Validation Rules

Quality Gate 必须满足：

- 每个 score 必须有取值范围。
- blocking issue 必须给出 affected_text_ref。
- 质量失败必须能转化为 Critic rewrite request 或 Humanizer revision guidance。
- 通过阈值变更必须记录版本。

## 5.3 Boundaries

NF-QA-001 定义写作质量门禁，不定义具体评分模型实现、人工审稿界面或模型供应商参数。

## 5.4 References

- NF-NKS-230
- NF-NKS-250
- NF-NKS-270
- NF-NKS-280
- NF-NKS-290
- NF-RAG-001
- NF-PROMPT-002
- NF-PIPE-003

## 5.5 Approval

Document Status: Draft

Next Review: Writing quality gate implementation review

Next Document: Writing Studio Workflow Specification

## 5.6 Change Log

| Version | Date       | Author                                 | Change                                      |
| ------- | ---------- | -------------------------------------- | ------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Quality Engineering Team | Initial writing quality gate specification. |
