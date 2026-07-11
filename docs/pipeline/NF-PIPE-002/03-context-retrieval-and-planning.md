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
