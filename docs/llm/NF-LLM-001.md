---
document_id: NF-LLM-001
title: LLM Provider and Agent Model Routing Specification
version: 1.0.0
status: Draft
category: LLM Integration Specification
owner: Novel Factory AI Platform Team
created: 2026-07-11
updated: 2026-07-11
dependencies:
  - NFES-000
  - NF-AGENT-001
  - NF-ARCH-002
  - NF-DBS-002
  - NF-IMPL-003
  - NF-PIPE-003
  - NF-PROMPT-001
references:
  - docs/standards/NFES-000.md
  - docs/agents/NF-AGENT-001.md
  - docs/architecture/NF-ARCH-002.md
  - docs/database/NF-DBS-002.md
  - docs/implementation/NF-IMPL-003.md
  - docs/pipeline/NF-PIPE-003.md
  - docs/prompts/NF-PROMPT-001.md
---

# NF-LLM-001

# LLM Provider and Agent Model Routing Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 的大模型接入、Provider Adapter、Model Profile、Agent Model Assignment、模型路由、降级、成本记录和 MVP 演进策略。

Novel Factory 的中间 Pipeline 会调度多个 Agent 分工完成自动拆书、知识抽取、归一化、图谱构建、Story Bible 生成、一键章节生成、Critic、Humanizer、Quality Gate 和 Feedback。MVP 阶段可以只接入一个模型跑通闭环，但架构必须允许不同 Agent 配置不同模型。

## 1.1 Goals

目标：

- 业务代码不直接依赖具体模型供应商 SDK。
- Agent 不硬编码模型名称。
- MVP 可以使用 single default model profile。
- 后续可以按 Agent role、task_type、genre、成本、质量和上下文长度切换模型。
- 所有模型调用都可追踪、可计费、可回放、可降级。

## 1.2 Non-Goals

本文档不定义：

- 具体供应商商业合同。
- API key 或密钥内容。
- Prompt 正文。
- 模型 benchmark 结果。
- 线上生产配额采购策略。

## 1.3 Core Principle

模型选择必须由配置和路由策略决定，而不是散落在 Agent 代码、Prompt 文本或前端参数中。

```text
Agent Task
↓
Agent Model Assignment
↓
Model Router
↓
Model Profile
↓
Provider Adapter
↓
Provider API
```

# 2. Provider Adapter and Model Profile

## 2.1 Provider Adapter Boundary

所有模型调用必须通过 Provider Adapter。

Adapter 至少暴露：

```text
generate_text(model_profile_id, prompt_package_ref, trace_id)
generate_structured(model_profile_id, prompt_package_ref, output_schema_ref, trace_id)
embed_text(model_profile_id, text_ref, trace_id)
rerank(model_profile_id, query_ref, candidate_refs, trace_id)
```

Adapter 负责：

- 供应商请求格式转换。
- 响应归一化。
- 超时和重试。
- token usage 捕获。
- provider error 映射。
- model version 记录。
- cost_estimate 计算。
- structured output validation 前置或后置配合。

## 2.2 Model Profile

`model_profile` 是可被路由选择的模型配置单元。

必须包含：

- model_profile_id
- provider_name
- provider_model_name
- display_name
- capability_tags
- supported_call_types: text, structured, embedding, rerank
- max_context_tokens
- max_output_tokens
- default_temperature
- cost_weight
- quality_weight
- latency_weight
- enabled
- fallback_profile_ids
- version

不得包含：

- API key。
- 私有密钥。
- 供应商账户密码。
- 不可提交的商业敏感配置。

## 2.3 Capability Tags

初始 capability_tags：

| Tag             | Meaning                      |
| --------------- | ---------------------------- |
| cn_webnovel     | 中文网文表达稳定             |
| long_context    | 长上下文处理能力强           |
| structured_json | 结构化 JSON 输出稳定         |
| reasoning       | 规划和逻辑推理强             |
| low_cost        | 单位 token 成本低            |
| low_latency     | 响应延迟低                   |
| rewriting       | 改写、人味化、句式重组能力强 |
| critique        | 审查、问题定位、规则遵循强   |
| embedding       | 向量生成模型                 |
| rerank          | 检索重排模型                 |

## 2.4 MVP Single Model Mode

MVP 可以配置一个 `default_llm_profile` 覆盖所有 text 和 structured generation Agent。

即使只有一个模型，也必须通过 model_profile_id 调用，不允许业务代码直接写 provider_model_name。这样后续从单模型切换到多模型时，只需要新增 profile 和 assignment，而不需要重写 Agent 代码。

# 3. Agent Model Assignment

## 3.1 Assignment Purpose

`agent_model_assignment` 定义某类 Agent 在某类任务中优先使用哪些模型。

一个 Agent role 可以有多个 assignment，用于区分：

- task_type。
- genre。
- structured 或 text 输出。
- normal 或 high_quality 模式。
- 成本优先或质量优先。

## 3.2 Assignment Fields

必须包含：

- assignment_id
- agent_role
- task_type
- output_mode: text, structured, embedding, rerank
- primary_model_profile_id
- fallback_model_profile_ids
- selection_policy
- max_retry
- max_cost
- enabled
- created_at
- updated_at

可选包含：

- genre_scope
- quality_floor
- latency_target_ms
- context_window_required
- temperature_override
- prompt_pack_scope

## 3.3 Recommended Agent Mapping

MVP 后的推荐映射：

| Agent Role           | Preferred Model Capability               | Notes                                  |
| -------------------- | ---------------------------------------- | -------------------------------------- |
| Ingestion Agent      | low_cost, structured_json                | 文件清洗、章节识别不应使用最贵模型     |
| Extraction Agent     | structured_json, long_context, reasoning | 需要稳定抽取对象、证据和关系           |
| Normalization Agent  | structured_json, reasoning               | 别名合并和冲突判断需要一致性           |
| Graph Agent          | structured_json, reasoning               | 图谱边必须指向已存在对象               |
| Planning Agent       | reasoning, structured_json, long_context | 生成章方向、世界观和剧情结构           |
| Scene Planning Agent | reasoning, structured_json               | 内部 Scene/Beat 拆分                   |
| Style Analyzer Agent | long_context, structured_json            | 输出抽象风格特征，不仿写作者           |
| Memory Agent         | long_context, reasoning                  | 动态状态和规则召回                     |
| Writer Agent         | cn_webnovel, long_context, low_cost      | 一键章节主草稿，重视中文网文表达和成本 |
| Critic Agent         | critique, structured_json, reasoning     | 输出问题位置、严重级别和修复建议       |
| Humanizer Agent      | rewriting, cn_webnovel                   | 去机械感、人味化，不改变事实           |
| Review Agent         | critique, structured_json                | 质量门禁和阻塞项判断                   |
| Feedback Agent       | structured_json, reasoning               | 生成策略建议，不自动改配置             |

## 3.4 Assignment Resolution

Model Router 解析顺序：

1. exact match: agent_role + task_type + output_mode + genre_scope
2. agent_role + task_type + output_mode
3. agent_role + output_mode
4. workspace default profile
5. system default profile

找不到 assignment 时，任务不得直接调用 provider，必须进入 configuration_error 或使用显式配置的 system default profile。

# 4. Router Policy, Fallback and Cost

## 4.1 Selection Policy

selection_policy 初始类型：

| Policy             | Behavior                                        |
| ------------------ | ----------------------------------------------- |
| cost_first         | 优先低成本，质量低于阈值时升级模型              |
| quality_first      | 优先高质量，适合 Story Bible、Critic 和最终审查 |
| latency_first      | 优先低延迟，适合交互式预览                      |
| long_context_first | 优先上下文窗口，适合 Memory 和 Style Analyzer   |
| structured_first   | 优先 JSON 稳定性，适合抽取和质量报告            |
| fixed              | 固定使用 primary_model_profile_id               |

MVP 默认可以使用 fixed policy 指向同一个模型。

## 4.2 Fallback Rule

Fallback 触发条件：

- provider timeout。
- rate limit。
- lifecycle or policy unavailable。
- structured output validation 连续失败。
- context length exceeded。
- quality gate 判定初稿低于最低阈值且仍在预算内。

Fallback 不得改变任务语义。降级或升级模型后必须记录原始失败和 fallback_profile_id。

## 4.3 Cost Guardrail

每个 task_type 必须有预算边界：

- max_prompt_tokens
- max_completion_tokens
- max_retry
- max_cost
- max_fallback_depth

超过预算时，任务进入 blocked 或 needs_attention，不继续自动消耗模型调用。

## 4.4 Call Record

每次模型调用必须记录：

- llm_call_id
- trace_id
- task_id
- agent_role
- task_type
- assignment_id
- model_profile_id
- provider_name
- provider_model_name
- prompt_package_ref
- input_refs
- output_ref
- prompt_tokens
- completion_tokens
- latency_ms
- retry_count
- cost_estimate
- status
- error_code
- fallback_from_call_id
- created_at

这些记录用于成本分析、质量归因、模型降权和审计。

# 5. Configuration Lifecycle and Change Log

## 5.1 Configuration Ownership

模型配置由 Config Module 拥有。

允许操作：

- create_model_profile
- update_model_profile
- disable_model_profile
- create_agent_model_assignment
- update_agent_model_assignment
- test_model_profile
- review_model_performance

Feedback Agent 可以生成模型策略建议，但不得自动修改正式 assignment。策略建议必须进入 review 状态，并由 Creator 或 Operator 明确批准。

## 5.2 Environment Separation

不同环境必须使用独立配置：

- local
- test
- staging
- production

环境之间不得共享 provider secret。Markdown 文档、测试夹具和示例配置不得包含真实密钥。

## 5.3 Rollout Strategy

从 MVP 单模型到多模型的演进：

1. Single default model profile: 所有 Agent 走同一个 model_profile_id。
2. Split embedding/rerank: 检索类模型与生成类模型分离。
3. Split Writer/Critic: Writer 使用中文长文本模型，Critic 使用结构化审查模型。
4. Split Extraction/Planning/Humanizer: 按任务能力进一步配置。
5. Feedback-driven routing: 基于成本、质量、重试率和人工编辑距离调整 assignment。

## 5.4 Validation

每次新增或修改 model_profile / assignment 后，必须验证：

- Provider Adapter 可以连通。
- structured output 能通过 schema 校验。
- token usage 和 cost 能记录。
- fallback 能按预期触发。
- 禁用 profile 后不会被 Router 选择。

## 5.5 Change Log

| Version | Date       | Changes                                                     |
| ------- | ---------- | ----------------------------------------------------------- |
| 1.0.0   | 2026-07-11 | Initial LLM provider and agent model routing specification. |
