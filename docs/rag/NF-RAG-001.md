---
document_id: NF-RAG-001
title: Knowledge Retrieval and Memory Context Specification
version: 1.0.0
status: Draft
category: Retrieval Augmented Generation Specification
owner: Novel Factory Retrieval Architecture Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-NKS-000
  - NF-NKS-200
  - NF-NKS-210
  - NF-NKS-220
  - NF-NKS-230
  - NF-NKS-250
  - NF-NKS-270
  - NF-NKS-290
  - NF-DBS-002
  - NF-PIPE-003
references:
  - docs/standards/NFES-000.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-200.md
  - docs/nks/NF-NKS-210.md
  - docs/nks/NF-NKS-220.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-270.md
  - docs/nks/NF-NKS-290.md
  - docs/database/NF-DBS-002.md
  - docs/pipeline/NF-PIPE-003.md
---

# NF-RAG-001

# Knowledge Retrieval and Memory Context Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 的 Knowledge Retrieval and Memory Context 规范。

该规范负责把 Knowledge Base、Story Graph、结构化状态、向量召回、长上下文和前文摘要组织成可用于写作的 Memory Package。

本文档覆盖：

- Memory Context 对象模型。
- 召回策略和优先级。
- 动态状态覆盖静态描述的规则。
- stale context 检测。
- 长上下文使用策略。
- 生成前一致性验证。

本文档不定义向量数据库产品选型、具体 embedding 模型或 Prompt 模板正文。

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

# 3. Retrieval Strategy and Priority

## 3.1 Retrieval Channels

Retrieval Service 必须组合：

- relational query
- Story Graph traversal
- vector retrieval
- evidence lookup
- rule lookup
- prior chapter summary
- long context pack

## 3.2 Priority Order

写作上下文优先级：

1. hard rules and forbidden changes
2. current character dynamic state
3. current relationship and conflict state
4. current location and timeline state
5. unresolved hooks and promised rewards
6. chapter and beat goal
7. genre playbook and rhythm target
8. style and expression constraints
9. supporting examples and evidence excerpts

## 3.3 Budget Trimming

上下文超限时，必须先压缩低优先级证据摘录，不得裁剪 hard rules、dynamic state 或 forbidden changes。

## 3.4 Retrieval Result Contract

每个召回结果至少包含：

- result_id
- object_id
- object_type
- relevance_reason
- confidence
- freshness
- evidence_refs
- source_channel

# 4. Staleness, Consistency and Long Context

## 4.1 Staleness Rule

如果召回对象的 source_version 落后于当前 story snapshot，则必须标记 stale。

stale context 不得进入 Writer Prompt，除非用于历史回顾并明确标记。

## 4.2 Dynamic Override Rule

动态状态覆盖静态状态。

示例：角色第 5 章失去法宝，则第 10 章不得从静态角色卡中召回该法宝作为当前持有物。

## 4.3 Long Context Policy

长上下文模型可用于 Memory / RAG 检查，但不得替代结构化状态。

长上下文输入必须记录：

- included_chapters
- included_summaries
- token_budget
- selection_reason
- omitted_ranges

## 4.4 Consistency Preflight

Writer 运行前必须检查：

- Memory Package 无 blocking stale item。
- 必要角色、地点、规则和 Beat 目标存在。
- forbidden_changes 已注入。
- unresolved hooks 与 beat_plan 不冲突。

# 5. Validation, Boundaries and Change Log

## 5.1 Validation Rules

Memory Context 必须满足：

- 每个 Memory Package 必须绑定 target_section_id 或 target_chapter_id。
- dynamic state 必须优先于 static profile。
- stale context 必须标记。
- Writer Prompt 不得接收未标记 stale 的过期上下文。
- 召回结果必须有 relevance_reason。

## 5.2 Boundaries

NF-RAG-001 定义检索和记忆上下文规范，不定义数据库产品选型、embedding 模型或 Prompt 模板正文。

## 5.3 References

- NF-NKS-000
- NF-NKS-200
- NF-NKS-210
- NF-NKS-220
- NF-NKS-230
- NF-NKS-250
- NF-NKS-270
- NF-NKS-290
- NF-DBS-002
- NF-PIPE-003

## 5.4 Approval

Document Status: Draft

Next Review: Retrieval implementation review

Next Document: NF-PROMPT-002 Writing Prompt Pack Specification

## 5.5 Change Log

| Version | Date       | Author                                    | Change                                              |
| ------- | ---------- | ----------------------------------------- | --------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Retrieval Architecture Team | Initial retrieval and memory context specification. |
