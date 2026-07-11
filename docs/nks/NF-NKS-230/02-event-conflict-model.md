# 2. Event and Conflict Model

## 2.1 Event Model

Event 表示推动故事状态变化的叙事事件。

最小字段：

- event_id
- event_type
- participants
- location_id
- temporal_scope
- cause
- action
- result
- consequence
- affected_objects
- evidence_refs

## 2.2 Event Type

允许初始类型：

- encounter
- discovery
- battle
- negotiation
- betrayal
- rescue
- revelation
- breakthrough
- travel
- transaction
- punishment
- reward_delivery

## 2.3 Conflict Model

Conflict 表示角色、势力、规则或目标之间的冲突关系。

最小字段：

- conflict_id
- conflict_type
- parties
- objective
- pressure
- escalation_level
- resolution_state
- trigger_event_id
- evidence_refs

## 2.4 Conflict Lifecycle

Conflict 生命周期：

```text
introduced -> escalated -> confrontation -> resolved
```

未解决的 Conflict 必须保留为 open 状态，并可作为 Hook 或后续 Pattern 输入。
