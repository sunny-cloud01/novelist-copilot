---
document_id: NF-NKS-270
title: Rule and Consistency Knowledge Specification
version: 1.0.0
status: Draft
category: Novel Knowledge Specification
owner: Novel Factory Knowledge Engineering Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-200
  - NF-NKS-220
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-200.md
  - docs/nks/NF-NKS-220.md
---

# NF-NKS-270

# Rule and Consistency Knowledge Specification

# 1. Purpose and Scope

本文档定义 Rule Knowledge 与 Consistency Knowledge 的模块级规范。

Rule 是影响世界运行、角色能力、时间线、空间移动、资源消耗、伏笔兑现和生成约束的知识对象。Consistency Knowledge 用于检查生成内容是否违反已批准知识。

本文档覆盖：

- Rule model
- Rule type
- Consistency constraint
- Violation record
- 修正建议边界

本文档不定义具体模型推理算法，也不定义运维告警策略。

# 2. Rule Model

## 2.1 Rule Profile

Rule Profile 表示一条可被检查或引用的规则。

最小字段：

- rule_id
- rule_type
- scope_type
- scope_id
- statement
- condition
- constraint
- severity
- lifecycle_status
- evidence_refs

## 2.2 Rule Types

允许初始类型：

- character_rule
- timeline_rule
- location_rule
- power_system_rule
- artifact_rule
- age_rule
- faction_rule
- worldview_rule
- foreshadowing_rule
- generation_constraint

## 2.3 Consistency Constraint

Consistency Constraint 表示一条可检查的约束。

最小字段：

- constraint_id
- rule_id
- target_object_type
- target_object_id
- check_type
- expected_condition
- violation_severity
- recovery_guidance

## 2.4 Violation Record

Violation Record 表示一次检测到的不一致。

最小字段：

- violation_id
- constraint_id
- detected_scope
- violated_text_ref
- violated_object_refs
- severity
- explanation
- recommended_action
- review_status

# 3. Consistency, Validation and Change Log

## 3.1 Consistency Examples

系统必须支持检查：

- 已死亡角色不能无解释再次出现。
- Character 不能使用超过 capability_state 的能力。
- Artifact 的唯一性不能被破坏。
- Location 移动必须符合时间线和空间规则。
- Foreshadowing 必须在合理范围内兑现、延迟或明确保留。
- Faction 关系变化必须有事件解释。

## 3.2 Validation Rules

Rule Knowledge 必须满足：

- 每条 Rule 必须有 scope。
- 每条 Constraint 必须能被人工或系统解释。
- Violation Record 不得直接修改源知识，只能提出 recommended_action。
- 高严重级别 violation 必须进入人工审核。

## 3.3 Boundaries

NF-NKS-270 定义规则和一致性知识语义。Consistency Engine 的运行架构由 NF-ARCH 文档定义，数据库存储由 NF-DBS 文档定义。

## 3.4 Change Log

| Version | Date       | Author                                   | Change                                                |
| ------- | ---------- | ---------------------------------------- | ----------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial rule and consistency knowledge specification. |
