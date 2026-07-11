---
document_id: NF-PROMPT-002
title: Writing Prompt Pack Specification
version: 1.0.0
status: Draft
category: Prompt Engineering Specification
owner: Novel Factory Prompt Engineering Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PROMPT-001
  - NF-NKS-280
  - NF-NKS-290
  - NF-RAG-001
  - NF-QA-001
  - NF-PIPE-003
  - NF-LLM-001
references:
  - docs/standards/NFES-000.md
  - docs/prompts/NF-PROMPT-001.md
  - docs/nks/NF-NKS-280.md
  - docs/nks/NF-NKS-290.md
  - docs/rag/NF-RAG-001.md
  - docs/quality/NF-QA-001.md
  - docs/pipeline/NF-PIPE-003.md
  - docs/llm/NF-LLM-001.md
---

# NF-PROMPT-002

# Writing Prompt Pack Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 写作流水线使用的 Writing Prompt Pack。

NF-PROMPT-001 定义 Prompt 模板通用规范。NF-PROMPT-002 定义 NF-PIPE-003 所需的 Planner、Scene Planner、Style Analyzer、Writer、Critic、Humanizer 和 Chapter Assembly Prompt 契约。

本文档覆盖：

- Prompt Pack 组成。
- 各写作 Prompt 的输入变量。
- 输出结构和失败格式。
- 禁止事项和质量检查。
- 与 Memory Package、Expression Taxonomy、Feedback Knowledge 和 Quality Gate 的关系。

本文档不保存具体供应商私有 Prompt，不定义模型参数，不包含受版权文本样例。

# 2. Prompt Pack Overview

## 2.1 Prompt Pack Components

Writing Prompt Pack 包含：

- planner_prompt
- scene_planner_prompt
- style_analyzer_prompt
- writer_beat_prompt
- critic_prompt
- humanizer_prompt
- chapter_assembly_prompt

## 2.2 Shared Inputs

所有写作 Prompt 必须支持：

- task_id
- generation_request_id
- target_project_id
- target_chapter_id
- target_section_id
- memory_package_ref
- genre_playbook_ref
- style_profile_ref
- expression_constraint_refs
- forbidden_changes
- output_contract

## 2.3 Shared Rules

所有写作 Prompt 必须遵守：

- 不改写 Approved Knowledge。
- 不引入未审核关键设定。
- 不要求模型绕过 Review。
- 不复制未授权风格样本文本。
- 输出必须可追踪到 input_refs。

## 2.4 Failure Format

失败输出必须包含：

- status: failed
- failure_reason
- missing_inputs
- blocking_constraints
- recommended_next_action

# 3. Planner, Scene and Style Prompts

## 3.1 Planner Prompt

输入：

- story_context_package
- current_story_state
- target_volume_goal
- genre_playbook
- unresolved_hooks
- rhythm_target

输出：

- chapter_goal
- emotional_curve
- frustration_satisfaction_curve
- required_reward
- required_hook
- main_conflict
- reveal_plan
- protagonist_gain
- continuity_constraints

## 3.2 Scene Planner Prompt

输入：

- chapter_plan
- memory_package
- genre_playbook
- rhythm_target

输出：

- scene_plan
- beat_plans
- pov_character
- active_characters
- conflict_pressure
- social_pressure_map
- estimated_word_count

## 3.3 Style Analyzer Prompt

输入：

- authorized_style_refs
- genre_scope
- scene_type
- pov_character
- expression_taxonomy_refs

输出：

- sentence_length_distribution
- paragraph_length_distribution
- verb_noun_ratio
- pov_purity
- diction_level
- preferred_expression_type_refs
- forbidden_expression_type_refs
- anti_ai_expression_refs

## 3.4 Style Boundary

Style Analyzer 不得要求模型模仿受版权作者。它只能输出抽象风格特征、节奏约束和表达分类。

# 4. Writer, Critic and Humanizer Prompts

## 4.1 Writer Chapter or Section Prompt

输入：

- chapter_plan
- scene_or_section_plan
- memory_package
- style_profile
- previous_approved_context
- expression_constraints
- forbidden_changes

输出：

- chapter_or_section_draft
- used_knowledge_refs
- self_report
- uncertain_points

约束：Writer 必须遵守当前 chapter_plan 和内部 scene_or_section_plan。Creator-facing 可以是一键生成整章，系统内部可以拆成 Section/Beat 执行；Writer 不得改写已批准设定，不得越过 forbidden_changes。

## 4.2 Critic Prompt

输入：

- chapter_or_section_draft
- chapter_plan
- scene_or_section_plan
- memory_package
- quality_gate_refs
- expression_taxonomy_refs

输出：

- pass_status
- failed_check_ids
- severity
- affected_text_refs
- required_changes
- retry_guidance

Critic 必须给可执行问题，不得只给笼统评价。

## 4.3 Humanizer Prompt

输入：

- critic_approved_chapter_or_section
- style_profile
- expression_constraints
- forbidden_phrase_rules
- mobile_readability_target

输出：

- humanized_chapter_or_section
- revision_diff
- humanizer_report

Humanizer 不得改变事实、剧情目标、角色关系、战力结果或伏笔状态。

## 4.4 Chapter Assembly Prompt

输入：

- approved_sections
- chapter_plan
- rhythm_target
- hook_plan

输出：

- assembled_chapter
- transition_fix_report
- chapter_quality_precheck

# 5. Output Contracts, Validation and Change Log

## 5.1 Output Contract Rules

结构化 Prompt 输出必须包含：

- prompt_type
- input_refs
- output_refs or output_body
- status
- confidence
- validation_errors

## 5.2 Validation Rules

Writing Prompt Pack 必须满足：

- 每个 Prompt 有明确输入和输出。
- Writer Prompt 支持 Beat 级生成。
- Critic Prompt 输出 failed_check_ids。
- Humanizer Prompt 输出 revision_diff。
- Style Prompt 不保存未授权长样例。
- 所有 Prompt 引用 NF-RAG-001 Memory Package 和 NF-QA-001 Quality Gate。

## 5.3 Boundaries

NF-PROMPT-002 定义写作 Prompt 契约，不定义供应商参数、模型选择策略或具体版权样本。

## 5.4 References

- NF-PROMPT-001
- NF-NKS-280
- NF-NKS-290
- NF-RAG-001
- NF-PIPE-003
- NF-QA-001

## 5.5 Approval

Document Status: Draft

Next Review: Writing prompt pack implementation review

Next Document: NF-QA-001 Writing Quality Gate Specification

## 5.6 Change Log

| Version | Date       | Author                                | Change                                     |
| ------- | ---------- | ------------------------------------- | ------------------------------------------ |
| 1.0.0   | 2026-07-10 | Novel Factory Prompt Engineering Team | Initial writing prompt pack specification. |
