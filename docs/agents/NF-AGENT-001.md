---
document_id: NF-AGENT-001
title: Agent Collaboration Model
version: 1.0.0
status: Draft
category: AI Agent Specification
owner: Novel Factory Agent Architecture Team
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
  - NF-NKS-290
  - NF-ARCH-001
  - NF-DBS-001
  - NF-RAG-001
  - NF-PROMPT-002
  - NF-QA-001
  - NF-PIPE-003
  - NF-LLM-001
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
  - docs/nks/NF-NKS-290.md
  - docs/architecture/NF-ARCH-001.md
  - docs/database/NF-DBS-001.md
  - docs/rag/NF-RAG-001.md
  - docs/prompts/NF-PROMPT-002.md
  - docs/quality/NF-QA-001.md
  - docs/pipeline/NF-PIPE-003.md
  - docs/llm/NF-LLM-001.md
---

# NF-AGENT-001

# Agent Collaboration Model

# 1. Purpose and Scope

本文档定义 Novel Factory 的 Agent 协作模型。

Agent Collaboration Model 描述各类 AI Agent 在拆书、知识抽取、审核、规划、生成、一致性检测和反馈学习中的职责边界、输入输出、生命周期、工具使用和失败处理方式。

本文档覆盖 Agent 类型与职责、Agent 协作拓扑、Agent 生命周期、输入输出契约、工具调用边界、人工审核交接、失败处理与重试、观测与审计要求。

本文档不覆盖 Prompt 模板正文、数据库物理 Schema、API 路径和响应结构或具体模型供应商参数。

# 2. Agent Principles

## 2.1 Specification Bound

Agent 必须遵守正式规范文档。领域对象引用 NF-NKS-000，抽取流程引用 NF-NKS-100，存储边界引用 NF-DBS-001，架构边界引用 NF-ARCH-001。

## 2.2 Tool-Constrained Execution

Agent 只能使用被授权的工具和数据范围。

## 2.3 Evidence Preservation

抽取类 Agent 必须保留 evidence，不得只输出无来源判断。

## 2.4 Human Review Compatibility

Agent 输出必须可被人工审核者理解、追溯和修正。

## 2.5 Fail Closed

当 Agent 无法确认结果可靠性时，必须进入 NeedsHumanReview 或 Blocked 状态，而不是继续传播不确定结果。

# 3. Agent Roles

## 3.1 Ingestion Agent

职责：导入原始作品、执行基础清洗、生成章节候选和预处理报告。

## 3.2 Extraction Agent

职责：按 NF-NKS-100 抽取 Scene、Entity、Event、Relationship、Pattern、Rhythm Profile 和 Rule。

## 3.3 Normalization Agent

职责：执行别名归一化、对象合并、ID 分配和候选冲突标记。

## 3.4 Graph Agent

职责：建立和验证 Story Graph 节点与关系。

## 3.5 Consistency Agent

职责：检查人物、时间线、地点、境界、法宝、势力、伏笔和世界规则一致性。

## 3.6 Planning Agent

职责：基于知识库、Story Graph、Pattern 和 Rhythm Profile 生成大纲、卷纲和章节计划。

## 3.7 Scene Planning Agent

职责：将章节计划拆分为 Scene 和 Beat，标记 POV、冲突压力、爽点、悬念、节奏目标和参与角色心理位置。

## 3.8 Style Analyzer Agent

职责：在 Writer 之前生成 Style Profile，分析句长分布、段落长度、POV 纯度、修辞偏好、对白比例和 NF-NKS-280 表达分类约束。

## 3.9 Writer Agent

职责：生成章节草稿或内部 Section/Beat 初稿。Creator-facing 交互可以是一键生成章节，但 Writer Agent 必须遵守系统内部的 Scene、Beat、Section、Memory Package 和 forbidden_changes，不得改写已批准设定。

## 3.10 Critic Agent

职责：对每个 Beat 执行结构化反向检查，输出 failed_check_ids、严重级别、问题位置和重写要求。

## 3.11 Memory Agent

职责：按 NF-RAG-001 为 Writer 和 Critic 提供结构化 Memory Package，包含角色动态状态、关系、物品、战力、地点、伏笔和前文摘要。

## 3.12 Humanizer Agent

职责：在不改变事实和剧情目标的前提下，执行句式长短重组、段落切碎、口语化拟真、去机械转场和低 AI 味改写。

## 3.13 Generation Agent

职责：生成章节草稿、局部改写和润色候选。

Generation Agent 是通用生成角色；写作流水线中的具体成稿职责优先由 Writer Agent、Critic Agent 和 Humanizer Agent 承担。

## 3.14 Review Agent

职责：按 NF-QA-001 执行写作质量门禁、AI 味检查、人味检查和人工审核辅助。

## 3.15 Feedback Agent

职责：按 NF-NKS-290 分析人工修改、读者反馈、评分和质量信号，并更新反馈知识和排名建议。

## 3.16 Model Assignment Rule

Agent role 不得在代码或 Prompt 中硬编码具体供应商模型。

每个 Agent task 必须通过 NF-LLM-001 定义的 Agent Model Assignment 和 Model Router 解析 model_profile_id。MVP 阶段允许所有 Agent 共享一个 default model_profile；后续可以按 Agent role、task_type、output_mode、genre 和质量/成本策略拆分为不同模型。

# 4. Collaboration Flows

## 4.1 Knowledge Extraction Flow

```text
Ingestion Agent
↓
Extraction Agent
↓
Normalization Agent
↓
Graph Agent
↓
Review Agent
↓
Human Reviewer
↓
Knowledge Base
```

## 4.2 Generation Flow

```text
Planning Agent
↓
Prompt Engine
↓
Generation Agent
↓
Consistency Agent
↓
Review Agent
↓
Human Reviewer
↓
Feedback Agent
```

## 4.3 Novel Writing Flow

```text
Planning Agent
↓
Scene Planning Agent
↓
Memory Agent + Style Analyzer Agent
↓
Writer Agent
↓
Critic Agent
↓ failed: Writer Agent rewrite same Beat
↓ passed
Humanizer Agent
↓
Review Agent
↓
Human Reviewer
↓
Feedback Agent
```

## 4.4 Feedback Learning Flow

```text
Human Edits + Reader Feedback + Quality Metrics
↓
Feedback Agent
↓
Ranking Suggestions
↓
Human Approval
↓
Rule Configuration Center + Knowledge Base
```

# 5. Lifecycle and Contracts

## 5.1 Agent Lifecycle

```text
Created
↓
Assigned
↓
Running
↓
WaitingForTool
↓
ReviewRequired
↓
Completed
```

Failure lifecycle:

```text
Running
↓
Failed
↓
RetryScheduled 或 NeedsHumanReview 或 Blocked
```

## 5.2 Input Contract

Every Agent task must include task_id, agent_type, input_refs, allowed_tools, constraints, expected_outputs and trace_id.

## 5.3 Output Contract

Every Agent output must include task_id, agent_type, output_refs, confidence, evidence_refs, status, errors and created_at.

# 6. Tool Boundary

Tool access must be scoped by Agent role.

- Ingestion Agent may access source import and preprocessing tools.
- Extraction Agent may access text analysis and knowledge extraction tools.
- Graph Agent may access graph validation tools.
- Generation Agent may access LLM generation tools and Prompt Engine output.
- Review Agent may access quality checks and consistency reports.
- Feedback Agent may access feedback analytics and ranking tools.

No Agent may directly modify Approved or Frozen knowledge without review workflow.

# 7. Human Review and Errors

## 7.1 Human Review Handoff

Agent must hand off to human review when confidence is below configured threshold, entity identity conflicts remain unresolved, graph validation fails, generated content violates blocking rules, policy-sensitive uncertainty exists, or data correction affects Approved objects.

Handoff package must include issue_summary, affected_objects, evidence_refs, recommended_actions and blocking_status.

## 7.2 Error Categories

Agent errors must use categories compatible with NF-NKS-100 and NF-DBS-001:

- input_error
- tool_error
- extraction_error
- normalization_error
- graph_error
- generation_error
- validation_error
- review_error

## 7.3 Retry Policy

Transient tool errors may retry. Semantic conflicts require review. Repeated failure must become Blocked.

# 8. Observability, Boundaries, and Change Log

## 8.1 Observability

Agent runs must emit run_id, task_id, agent_type, input_refs, output_refs, tool_calls, status, duration and error_id.

Agent outputs must be auditable through NF-DBS-001 audit_events or equivalent runtime logs.

## 8.2 Boundary Rules

NF-AGENT-001 defines Agent roles, lifecycle, orchestration boundaries and error handling.

NF-AGENT-001 must not define Prompt template content, database physical schemas, API request schemas or product goals.

## 8.3 References

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
- NF-NKS-290
- NF-ARCH-001
- NF-DBS-001
- NF-RAG-001
- NF-PROMPT-002
- NF-QA-001
- NF-PIPE-003

## 8.4 Approval

Document Status: Draft

Next Review: NF-AGENT-001 Review

Next Document: NF-PROMPT-001 Prompt Template Specification

## 8.5 Change Log

| Version | Date       | Author                                | Change                                       |
| ------- | ---------- | ------------------------------------- | -------------------------------------------- |
| 1.0.0   | 2026-07-09 | Novel Factory Agent Architecture Team | Initial Draft for Agent collaboration model. |
