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
