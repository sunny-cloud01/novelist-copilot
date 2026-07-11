# 7. Model Router, Cost and Token Policy

## 7.1 Model Router Purpose

Novel Writing Pipeline 支持 Multi-Model Router。

不同 Agent 可以选择不同模型，依据是任务能力、成本、上下文长度、中文网文表现、结构化输出稳定性和延迟。

MVP 阶段允许所有 Agent 指向同一个 default model_profile，但调用路径仍必须经过 Model Router。这样后续可以通过配置拆分模型，而不是改写 Pipeline 代码。

## 7.2 Capability Profiles

模型选择应使用 capability profile，而不是在业务逻辑中硬编码供应商。

初始 capability profile：

| Agent Role    | Required Capability                            |
| ------------- | ---------------------------------------------- |
| Planner       | 结构化规划、JSON 稳定输出、长线逻辑            |
| Scene Planner | 情绪曲线、Beat 拆分、爽点安排                  |
| Writer        | 中文网文表达、低成本长文本生成、类型套路熟悉度 |
| Memory / RAG  | 长上下文、一致性检查、设定追踪                 |
| Critic        | 指令遵循、问题定位、结构化审查                 |
| Humanizer     | 句式重组、口语化、去 AI 味                     |

## 7.3 Example Provider Mapping

可选初始映射：

- Writer: 优先中文网文表现好、成本低、长文本稳定的模型。
- Planner / Critic: 优先结构化输出、逻辑规划和严格指令遵循强的模型。
- Memory / RAG: 优先长上下文和跨章节一致性检查强的模型。
- Humanizer: 可使用 Writer 同类模型或结构化改写模型。

供应商可配置为 DeepSeek、OpenAI、Gemini 或其他兼容 provider adapter。正式实现必须通过 Model Profile 配置，不得散落在 Prompt 文本中。

## 7.3.1 Agent Model Assignment

每个 Agent task 在调用模型前必须解析 agent_model_assignment。

解析输入：

- agent_role
- task_type
- output_mode
- genre_scope
- quality_mode
- workspace_id

解析输出：

- assignment_id
- primary_model_profile_id
- fallback_model_profile_ids
- selection_policy
- max_retry
- max_cost

assignment 解析失败时，任务不得直接调用 provider。系统必须使用显式配置的 system default profile，或进入 configuration_error。

## 7.4 Token Budget Policy

Token 预算优先级：

1. hard rules
2. Memory Package
3. current Beat Plan
4. current Scene Plan
5. previous approved Beat
6. Style Profile
7. few-shot guidance
8. broader chapter context

当预算不足时，优先摘要 broader context，不得裁剪 hard rules、Memory Package 或 forbidden_changes。

## 7.5 Cost Control

系统必须记录：

- model_profile_id
- agent_role
- prompt_tokens
- completion_tokens
- retry_count
- accepted_output_ratio
- rewrite_count
- human_edit_distance
- quality_score
- assignment_id
- fallback_from_call_id

低质量高成本模型路线必须进入 Feedback Loop 降权。

## 7.6 Feedback-Driven Routing

Feedback Agent 可以根据 accepted_output_ratio、rewrite_count、human_edit_distance、quality_score、latency 和 cost_estimate 生成模型路由建议。

路由建议不得自动修改正式 assignment，必须进入 review 状态。批准后由 Config Module 更新 agent_model_assignment。
