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
