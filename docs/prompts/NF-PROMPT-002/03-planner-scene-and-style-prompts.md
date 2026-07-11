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
