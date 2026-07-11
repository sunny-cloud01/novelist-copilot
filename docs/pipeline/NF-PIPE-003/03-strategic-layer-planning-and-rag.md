# 3. Strategic Layer Planning and RAG

## 3.1 Retrieval Upgrade

写作阶段不得只依赖普通向量检索。

Context Retrieval 必须组合：

- structured JSON / relational query
- Story Graph traversal
- approved knowledge object lookup
- character state lookup
- world rule lookup
- timeline and location lookup
- vector retrieval for supporting evidence
- long context memory when available

## 3.2 Memory Package

Memory Package 至少包含：

- character_static_profile
- character_dynamic_state
- relationship_state
- inventory_and_artifact_state
- power_level_state
- location_state
- faction_state
- unresolved_conflicts
- unresolved_hooks
- prior_chapter_summary
- forbidden_changes

动态状态必须优先于早期静态描述。

示例：若第 5 章武器升级，则第 10 章生成时必须使用升级后的 weapon_state，不得只引用第 1 章初始描述。

## 3.3 Planner Outputs

Planner 必须输出：

- chapter_goal
- emotional_curve
- frustration_satisfaction_curve
- required_reward
- required_hook
- main_conflict
- reveal_plan
- protagonist_gain
- antagonist_pressure
- continuity_constraints

## 3.4 Scene Planner Outputs

Scene Planner 必须将章节拆成 Scene 和 Beat。

每个 Beat 至少包含：

- beat_id
- beat_goal
- pov_character
- active_characters
- conflict_pressure
- who_underestimates_whom
- who_is_jealous
- who_is_shocked
- reward_or_hook
- required_knowledge_refs
- rhythm_target
- estimated_word_count

## 3.5 Strategic Validation

进入 Writer 前必须检查：

- Beat 是否推进章节目标。
- Beat 是否引用有效角色和地点。
- 情绪曲线是否存在压抑、反转或释放。
- 爽点和悬念是否可追踪到 NF-NKS-230。
- 节奏目标是否可追踪到 NF-NKS-250。
- 表达风格是否可追踪到 NF-NKS-280。
