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
