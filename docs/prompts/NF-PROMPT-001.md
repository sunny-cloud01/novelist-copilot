---
document_id: NF-PROMPT-001
title: Prompt Template Specification
version: 1.0.0
status: Draft
category: Prompt Engineering Specification
owner: Novel Factory Prompt Engineering Team
created: 2026-07-09
updated: 2026-07-09
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-200
  - NF-NKS-210
  - NF-NKS-220
  - NF-NKS-230
  - NF-NKS-240
  - NF-NKS-250
  - NF-NKS-260
  - NF-NKS-270
  - NF-NKS-280
  - NF-PROMPT-002
  - NF-ARCH-001
  - NF-DBS-001
  - NF-AGENT-001
  - NF-PIPE-003
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-200.md
  - docs/nks/NF-NKS-210.md
  - docs/nks/NF-NKS-220.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-240.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-260.md
  - docs/nks/NF-NKS-270.md
  - docs/nks/NF-NKS-280.md
  - docs/prompts/NF-PROMPT-002.md
  - docs/architecture/NF-ARCH-001.md
  - docs/database/NF-DBS-001.md
  - docs/agents/NF-AGENT-001.md
  - docs/pipeline/NF-PIPE-003.md
---

# NF-PROMPT-001

# Prompt Template Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 的 Prompt Template 规范。

Prompt Template Specification 用于约束 Prompt 模板类型、变量结构、知识引用、装配流程、输出格式、评估指标和版本管理。

本文档覆盖 Prompt 模板分类、变量命名与来源、Prompt Package 结构、模板装配流程、输出格式要求、评估与回归测试、版本和变更管理、安全与边界规则。

本文档不覆盖 Agent 生命周期、数据库物理 Schema、API 路由或模型供应商私有参数。

# 2. Prompt Principles

## 2.1 Knowledge-Grounded

Prompt 必须引用 Knowledge Base、Story Graph、Rule、Pattern 或 Rhythm Profile 中的结构化知识，不得只依赖自由文本记忆。

## 2.2 Variable-Driven

Prompt 模板必须使用明确变量，不得把业务数据硬编码进模板正文。

## 2.3 Traceable Output

Prompt 输出必须能追溯到使用的模板版本、变量、知识引用和生成任务。

## 2.4 Constraint First

一致性规则、禁止事项、世界观规则和角色状态应在生成指令前明确给出。

## 2.5 Reviewable

Prompt Package 必须可被人工审核者阅读和复现。

# 3. Template Types

## 3.1 Extraction Prompt

用于从原文中抽取对象、关系、证据和规则。

## 3.2 Normalization Prompt

用于归一化别名、合并候选对象、识别重复对象。

## 3.3 Planning Prompt

用于生成大纲、卷纲、章节计划和剧情阶段。

## 3.3.1 Scene Planning Prompt

用于将章节计划拆解为 Scene 和 Beat，并输出 POV、冲突压力、爽点、悬念、节奏目标和每个 Beat 的写作目标。

## 3.3.2 Style Analysis Prompt

用于生成 Style Profile。输出必须引用 NF-NKS-280 的 Expression Type、Speaker Voice Profile、Style Constraint 和 anti_ai_expression。

## 3.4 Character Prompt

用于表达角色状态、动机、能力、口吻和行为约束。

角色口吻必须优先引用 NF-NKS-280 的 Speaker Voice Profile 或 Expression Type，不得在 Prompt 模板中临时发明口吻分类。

## 3.5 World Prompt

用于表达世界观、地点、势力、资源和力量体系规则。

## 3.6 Chapter Prompt

用于生成章节草稿。

Chapter Prompt 在 Creator-facing 交互中应支持一键生成约 3000 字章节。Prompt 结构内部仍应携带 Scene、Beat 或 Section 计划，以便模型按受控结构生成、检查和重写；当上下文或质量风险较高时，可降级为分段输出。

## 3.7 Dialogue Prompt

用于生成或修订对白。

Dialogue Prompt 必须使用 NF-NKS-280 定义的 dialogue_expression、tone_tags 和 anti_ai_expression 作为受控分类。

## 3.8 Battle Prompt

用于生成战斗、冲突和动作段落。

## 3.9 Review Prompt

用于质量检测、一致性检查、重复率检查和问题总结。

## 3.9.1 Critic Prompt

用于对 Beat Draft 执行结构化反向检查。输出必须包含 failed_check_ids、severity、affected_text_refs、required_changes 和 retry_guidance。

## 3.10 Revision Prompt

用于根据 Review Report 和人工意见进行局部修订。

## 3.11 Humanizer Prompt

用于在不改变事实和剧情目标的前提下，执行句式长短重组、段落切碎、口语化拟真、机械转场削减和 AI 味降低。

# 4. Prompt Variable Model

Prompt 变量必须包含以下元数据：

- variable_name
- source_document
- source_object_type
- source_id
- required
- default_value
- validation_rule

变量命名规则：

- 使用 snake_case。
- 不使用含糊名称。
- 引用 NKS 对象时必须保留 source_id。

示例变量：

- character_profile
- faction_context
- location_context
- active_rules
- unresolved_hooks
- rhythm_target
- chapter_goal
- forbidden_changes

# 5. Package and Assembly

## 5.1 Prompt Package

标准 Prompt Package：

```text
PromptPackage
├── metadata
├── template_ref
├── variables
├── knowledge_refs
├── graph_refs
├── constraints
├── output_contract
├── evaluation_rules
└── assembly_log
```

metadata 必须包含 prompt_package_id、template_id、template_version、task_id、agent_type 和 created_at。

## 5.2 Assembly Flow

Prompt 装配流程：

```text
Generation Goal
↓
Knowledge Query
↓
Story Graph Query
↓
Rule Selection
↓
Template Selection
↓
Variable Binding
↓
Constraint Injection
↓
Output Contract Binding
↓
Prompt Package Export
```

# 6. Output and Evaluation

## 6.1 Output Contract

Prompt 必须声明输出格式。

输出格式可以是 Markdown prose、JSON object、YAML object、structured checklist 或 review report。

结构化输出必须声明 required_fields、allowed_values、failure_format 和 evidence_required。

## 6.2 Evaluation Rules

Prompt 评估指标：

- instruction_following
- knowledge_consistency
- character_consistency
- plot_coherence
- rhythm_match
- rule_compliance
- originality_signal
- revision_efficiency
- ai_flavor_signal
- voice_drift_signal
- beat_goal_completion
- mobile_readability

Review Prompt 必须输出可执行问题列表，而不是笼统评价。

# 7. Versioning, Boundaries, and Change Log

## 7.1 Versioning

Prompt Template 使用 Semantic Versioning。

Major：变量结构或输出契约不兼容变更。

Minor：新增变量、规则或可选章节。

Patch：措辞、格式或示例修正。

Prompt Package 必须记录 template_version。

## 7.2 Safety and Boundary Rules

Prompt 不得要求模型忽略系统规范、绕过人工审核或改写已批准事实。

Prompt 不得在模板中重新定义 NF-NKS-000 对象语义或 NF-NKS-200 到 NF-NKS-270 的模块语义。

写作流水线的具体 Prompt Pack 由 NF-PROMPT-002 管理。

Prompt 不得把数据库物理字段当作唯一业务定义。

## 7.3 References

- NFES-000
- NF-PRD-001
- NF-NKS-000
- NF-NKS-001
- NF-NKS-100
- NF-NKS-200
- NF-NKS-210
- NF-NKS-220
- NF-NKS-230
- NF-NKS-240
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270
- NF-NKS-280
- NF-ARCH-001
- NF-DBS-001
- NF-AGENT-001
- NF-PIPE-003
- NF-PROMPT-002

## 7.4 Approval

Document Status: Draft

Next Review: NF-PROMPT-001 Review

Next Document: NF-PROMPT-002 Writing Prompt Pack Specification

## 7.5 Change Log

| Version | Date       | Author                                | Change                                           |
| ------- | ---------- | ------------------------------------- | ------------------------------------------------ |
| 1.0.0   | 2026-07-09 | Novel Factory Prompt Engineering Team | Initial Draft for Prompt template specification. |
