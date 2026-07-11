---
document_id: NF-PIPE-002
title: AI Generation and Revision Pipeline
version: 1.0.0
status: Draft
category: Pipeline Specification
owner: Novel Factory Backend Architecture Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-200
  - NF-NKS-210
  - NF-NKS-220
  - NF-NKS-230
  - NF-NKS-240
  - NF-NKS-250
  - NF-NKS-260
  - NF-NKS-270
  - NF-NKS-280
  - NF-ARCH-001
  - NF-ARCH-002
  - NF-DBS-001
  - NF-DBS-002
  - NF-PIPE-001
  - NF-AGENT-001
  - NF-PROMPT-001
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-200.md
  - docs/nks/NF-NKS-210.md
  - docs/nks/NF-NKS-220.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-240.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-260.md
  - docs/nks/NF-NKS-270.md
  - docs/nks/NF-NKS-280.md
  - docs/architecture/NF-ARCH-001.md
  - docs/architecture/NF-ARCH-002.md
  - docs/database/NF-DBS-001.md
  - docs/database/NF-DBS-002.md
  - docs/pipeline/NF-PIPE-001.md
  - docs/agents/NF-AGENT-001.md
  - docs/prompts/NF-PROMPT-001.md
---

# NF-PIPE-002

# AI Generation and Revision Pipeline

# 1. Purpose and Scope

本文档定义 Novel Factory 的 AI Generation and Revision Pipeline。

该 Pipeline 将已审核的知识资产、Story Graph、Pattern、Rhythm Profile、Asset、Rule 和人工目标转化为章节计划、Prompt Package、章节草稿、修订稿、质量报告和反馈信号。

本文档的核心目标是让 AI 生成不只是一次性 Prompt 输出，而是一个可追踪、可检查、可修订、可反馈的创作流水线。

本文档覆盖：

- generation request 输入契约。
- 知识召回和上下文组装。
- 章节计划和叙事压力设计。
- Prompt Package 组装。
- 章节草稿生成。
- 一致性检查、AI 味检查和修订循环。
- 人工审核和反馈回流。
- 任务状态、失败恢复和可观测性。

本文档不定义具体 Prompt 模板正文、LLM provider 私有参数、前端编辑器交互或发布渠道流程。

# 2. Generation Pipeline Overview

## 2.1 High Level Flow

```text
Generation Request
↓
Context Retrieval
↓
Chapter Planning
↓
Prompt Assembly
↓
Draft Generation
↓
Consistency Review
↓
Revision Run
↓
AI Quality Review
↓
Human Review Gate
↓
Approved Draft or Revision Request
↓
Feedback Capture
```

## 2.2 Pipeline Owners

| Stage              | Owner Module            |
| ------------------ | ----------------------- |
| Generation Request | Generation Service      |
| Context Retrieval  | Retrieval Service       |
| Chapter Planning   | Planning Service        |
| Prompt Assembly    | Prompt Assembly Service |
| Draft Generation   | Generation Service      |
| Consistency Review | Consistency Service     |
| Revision Run       | Generation Service      |
| AI Quality Review  | Review Service          |
| Human Review Gate  | Review Service          |
| Feedback Capture   | Feedback Service        |

## 2.3 Input Contract

Generation Request 至少包含：

- request_id
- target_book_or_project_id
- generation_scope
- genre
- chapter_goal
- current_story_state_refs
- required_character_refs
- required_world_refs
- required_pattern_refs
- rhythm_target
- forbidden_changes
- requester

## 2.4 Output Contract

Pipeline 输出至少包含：

- chapter_plan
- prompt_package_ref
- draft_candidate_ref
- consistency_report
- revision_report
- quality_report
- human_review_report
- feedback_records
- final_draft_ref or rejection_reason

# 3. Context Retrieval and Planning

## 3.1 Retrieval Purpose

Context Retrieval 负责为生成任务收集足够但不过载的上下文。

召回目标不是把所有知识塞入 Prompt，而是筛选出本章真正影响人物行为、剧情推进、规则约束和读者体验的知识。

## 3.2 Retrieval Inputs

Retrieval Service 至少使用：

- generation_request
- current_story_state
- approved knowledge objects
- Story Graph snapshot
- active rules
- unresolved hooks
- target rhythm profile
- candidate patterns
- relevant assets
- previous chapter summaries

## 3.3 Retrieval Filters

召回必须过滤：

- lifecycle_status
- review_status
- genre_scope
- story_scope
- chapter_scope
- permission
- freshness or source_version

未审核 candidate 对象不得默认进入正式生成上下文。

## 3.4 Context Package

Context Package 至少包含：

- character_state_pack
- world_rule_pack
- faction_location_pack
- event_conflict_pack
- hook_reward_pack
- pattern_pack
- rhythm_pack
- asset_pack
- forbidden_change_pack
- evidence_refs

## 3.5 Chapter Planning

Planning Service 根据 Context Package 生成 Chapter Plan。

Chapter Plan 至少包含：

- chapter_goal
- scene_goals
- primary_conflict
- character_intent
- emotional_turn
- hook_to_advance
- reward_to_deliver
- rule_constraints
- rhythm_target
- revision_focus

Chapter Plan 必须先于 Prompt Package 生成，并作为后续审查对象保存。

# 4. Prompt Assembly and Generation

## 4.1 Prompt Assembly

Prompt Assembly Service 根据 NF-PROMPT-001 创建 Prompt Package。

Prompt Package 必须包含：

- metadata
- template_ref
- variables
- knowledge_refs
- graph_refs
- constraints
- output_contract
- evaluation_rules
- assembly_log

Prompt Package 必须保存 prompt_package_id 和 prompt_ref，便于复现生成结果。

## 4.2 Prompt Budget Rule

Prompt Assembly 必须控制上下文预算。

优先级顺序：

1. hard constraints and forbidden changes
2. character state and active relationship pressure
3. chapter goal and scene goals
4. unresolved hooks and expected rewards
5. world rules and consistency constraints
6. rhythm target
7. relevant pattern steps
8. supporting assets and style references

当上下文超限时，低优先级内容必须被摘要、裁剪或转为 retrieval hint。

## 4.3 Draft Generation

Draft Generation 调用 LLM provider adapter，生成 Draft Candidate。

每个 Draft Candidate 必须记录：

- draft_id
- generation_request_id
- prompt_package_id
- provider
- model
- model_version
- output_ref
- token_usage
- latency
- status

## 4.4 Human Flavor Requirements

生成任务必须明确避免机械 AI 味。

Prompt Package 应提供：

- 角色当下的欲望、误解、秘密和压力。
- 场景内的具体动作和感官锚点。
- 对白的角色立场差异。
- 情绪推进，而不是只给剧情说明。
- 章节节奏目标和必要留白。
- 需要回避的套路化表达或重复句式。

## 4.5 Draft Versioning

同一个 generation_request 可以产生多个 draft candidate。

Draft 不得覆盖，必须通过 version 或 parent_draft_id 形成修订链。

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

# 7. Task State, Observability and Recovery

## 7.1 Generation Run

每次生成流水线必须创建 generation_run。

最小字段：

- run_id
- generation_request_id
- pipeline_version
- status
- current_stage
- input_refs
- output_refs
- idempotency_key
- retry_count
- started_at
- finished_at

## 7.2 Stage Status

标准 stage status：

```text
pending -> running -> succeeded
pending -> skipped
running -> failed
running -> requires_review
running -> retrying -> running
```

## 7.3 Checkpoints

建议 checkpoint：

- context_retrieval_completed
- chapter_plan_created
- prompt_package_created
- draft_generated
- consistency_review_completed
- revision_completed
- ai_quality_review_completed
- human_review_completed
- feedback_captured

失败恢复必须从最近安全 checkpoint 继续。

## 7.4 Error Categories

生成流水线错误至少分为：

- retrieval_error
- prompt_assembly_error
- llm_provider_error
- output_validation_error
- consistency_violation
- revision_limit_exceeded
- review_required
- storage_error
- projection_error
- unknown_error

## 7.5 Observability Signals

必须记录：

- generation_latency
- retrieval_latency
- prompt_token_count
- completion_token_count
- revision_round_count
- consistency_violation_count
- AI_flavor_signal
- human_edit_distance
- approval_rate
- rejection_rate
- provider_error_rate

## 7.6 Recovery Rule

LLM provider transient failure 可以重试。

知识冲突、角色偏离、世界规则冲突和高 AI_flavor_signal 不应盲目重试，必须进入修订或人工审核。

# 8. Boundaries, References and Change Log

## 8.1 Boundaries

NF-PIPE-002 定义 AI Generation and Revision Pipeline。

NF-PIPE-002 不定义 Book ingestion、知识抽取、Prompt 模板正文、数据库物理表结构、前端编辑器交互或发布渠道流程。

## 8.2 References

- NFES-000
- NF-PRD-001
- NF-NKS-000
- NF-NKS-001
- NF-NKS-100
- NF-NKS-200
- NF-NKS-210
- NF-NKS-220
- NF-NKS-230
- NF-NKS-240
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270
- NF-NKS-280
- NF-ARCH-001
- NF-ARCH-002
- NF-DBS-001
- NF-DBS-002
- NF-PIPE-001
- NF-AGENT-001
- NF-PROMPT-001

## 8.3 Approval

Document Status: Draft

Next Review: AI generation implementation review

Next Document: NF-PIPE-003 Novel Writing Orchestration and Humanization Pipeline

## 8.4 Change Log

| Version | Date       | Author                                  | Change                                             |
| ------- | ---------- | --------------------------------------- | -------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Backend Architecture Team | Initial AI generation and revision pipeline draft. |
