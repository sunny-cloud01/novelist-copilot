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
