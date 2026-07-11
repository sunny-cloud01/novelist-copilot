# 5. LLM, Agent and Generation Boundaries

## 5.1 Model Router and Provider Adapter

业务模块不得直接依赖具体 LLM provider SDK。

业务模块必须先向 AI Worker 提交 Agent Task，由 Model Router 解析 agent_model_assignment 和 model_profile_id，再通过 provider adapter 调用模型。

调用边界：

```text
Business Service
↓
AI Worker Agent Task
↓
Model Router
↓
Provider Adapter
↓
Provider API
```

Model Router 至少负责：

- 根据 agent_role、task_type、output_mode、genre_scope 选择 assignment。
- 将 assignment 解析为 primary model_profile_id。
- 判断 profile 是否 enabled。
- 处理 fallback_profile_ids。
- 应用 max_retry、max_cost 和 selection_policy。

Provider Adapter 至少负责：

- request normalization
- response normalization
- timeout handling
- retry policy
- token usage capture
- model version recording
- safety and policy error mapping

## 5.2 LLM Call Record

每次 LLM 调用必须记录：

- call_id
- trace_id
- task_id
- agent_role
- task_type
- assignment_id
- model_profile_id
- provider
- model
- prompt_ref
- input_refs
- output_ref
- token_usage
- latency
- retry_count
- cost_estimate
- fallback_from_call_id
- status
- error_code
- created_at

Prompt 正文可以进入 Object Storage，PostgreSQL 保存 prompt_ref 和元数据。

## 5.3 Agent Boundary

Agent 是任务执行角色，不是权威数据源。

Agent 输出必须进入 Review、Extraction 或 Generation 的受控流程。Agent 不得直接批准 knowledge object，不得绕过 Review Service 修改 Approved Knowledge Base。

## 5.4 Generation Pipeline

章节生成推荐流程：

```text
Generation Request
↓
Retrieve Character State + World Rules + Pattern + Rhythm + Assets
↓
Planning Service creates Chapter Plan
↓
Prompt Assembly Service creates Prompt Package
↓
Generation Service creates Draft Candidate
↓
Consistency Service checks Draft Candidate
↓
Revision Run improves Draft Candidate
↓
AI Review creates Quality Report
↓
Human Review approves or requests changes
↓
Feedback Service records signals
```

## 5.5 Human Flavor Principle

“人味”不是单次 Prompt 目标，而是后端上下文质量、角色连续性、节奏控制、素材选择、冲突压力和修订循环共同产生的结果。

生成系统必须优先召回：

- 当前角色的欲望、误解、秘密、恐惧和关系压力。
- 当前世界规则和不可违反约束。
- 章节目标、未兑现 Hook、预期 Reward 和节奏目标。
- 与题材和风格匹配的 Asset。
- 前文导致的情绪残留和后续承诺。

## 5.6 Revision Rule

第一稿不得直接视为最终章节。

每个章节草稿至少应经过：

- consistency check
- rhythm check
- repetition check
- AI flavor check
- human review or explicit auto-approval policy
