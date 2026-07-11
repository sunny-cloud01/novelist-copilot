# 2. Memory Context Model

## 2.1 Memory Package

Memory Package 是写作任务的上下文包。

最小字段：

- memory_package_id
- generation_request_id
- target_chapter_id
- target_section_id
- source_snapshot_id
- character_state_pack
- world_rule_pack
- relationship_state_pack
- location_timeline_pack
- inventory_artifact_pack
- power_level_pack
- unresolved_hook_pack
- prior_summary_pack
- forbidden_change_pack
- evidence_refs
- freshness_report

## 2.2 Current Story State

Current Story State 表示目标章节开始前的故事状态。

必须包含：

- current_chapter_index
- timeline_position
- active_location_refs
- active_character_refs
- active_conflict_refs
- unresolved_hook_refs
- open_rule_constraints

## 2.3 Character Dynamic State

Character Dynamic State 必须优先于 Character Static Profile。

最小字段：

- character_id
- latest_location_id
- health_state
- relationship_state_refs
- inventory_refs
- power_level_state
- known_information
- active_goal
- emotional_residue

## 2.4 Context Evidence

每个关键上下文必须绑定 evidence_refs 或 review_record。

Memory Package 不得只保存模型推测结论。
