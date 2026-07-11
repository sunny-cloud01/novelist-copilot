---
document_id: NF-NKS-230
title: Event Conflict Hook Reward and Climax Specification
version: 1.0.0
status: Draft
category: Novel Knowledge Specification
owner: Novel Factory Knowledge Engineering Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-200
references:
  - docs/standards/NFES-000.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-200.md
---

# NF-NKS-230

# Event Conflict Hook Reward and Climax Specification

# 1. Purpose and Scope

本文档定义 Event、Conflict、Emotion、Hook、Reward 和 Climax 的模块级知识规范。

这些对象描述剧情推进、读者体验和章节结构，是 Story Graph、Pattern Library、Rhythm Profile 和生成计划的重要输入。

本文档覆盖：

- Event model
- Conflict model
- Hook model
- Reward model
- Climax model
- 读者体验节点验证规则

本文档不定义抽取流水线。抽取流程由 NF-NKS-100 定义。

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

# 3. Reader Experience Model

## 3.1 Hook Model

Hook 表示驱动继续阅读的悬念、问题、威胁或未完成承诺。

最小字段：

- hook_id
- hook_type
- open_question
- introduced_at
- expected_resolution_range
- linked_conflict_id
- linked_event_id
- evidence_refs

## 3.2 Reward Model

Reward 表示读者体验中的爽点、满足感或正反馈节点。

最小字段：

- reward_id
- reward_type
- trigger_event_id
- beneficiary_character_id
- reader_effect
- intensity
- payoff_target
- evidence_refs

## 3.3 Climax Model

Climax 表示章节、场景、卷或剧情段落中的强峰值事件。

最小字段：

- climax_id
- scope_type
- scope_id
- event_id
- conflict_id
- reward_refs
- hook_refs
- intensity
- aftermath
- evidence_refs

## 3.4 Experience Constraints

- Hook 必须有 open_question。
- Reward 必须说明 reader_effect。
- Climax 必须至少关联 Event、Conflict、Reward 或 Hook 中的一类对象。
- Reward 与 Climax 不等同。Reward 表示正反馈，Climax 表示叙事峰值。

# 4. Validation, Boundaries and Change Log

## 4.1 Validation Rules

剧情体验对象必须满足：

- Event 必须包含 cause、action、result 或明确标记缺失原因。
- Conflict 必须有 parties 和 objective。
- Hook 必须有预期解决范围。
- Reward 必须绑定触发事件或读者体验证据。
- Climax 必须绑定范围和峰值事件。

## 4.2 Boundaries

NF-NKS-230 定义剧情体验对象语义，不定义节奏指标计算公式。节奏指标由 NF-NKS-250 定义。

## 4.3 References

- NF-NKS-000
- NF-NKS-100
- NF-NKS-200

## 4.4 Change Log

| Version | Date       | Author                                   | Change                                             |
| ------- | ---------- | ---------------------------------------- | -------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial event and reader experience specification. |
