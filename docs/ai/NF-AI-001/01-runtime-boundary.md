# 1. Runtime Boundary

本文档定义 AI Worker 的实现级运行边界，包括 provider adapter、model router、structured output、streaming、prompt/object storage、质量评分和成本记录。

## 1.1 Runtime Modules

AI Worker MVP 模块：

| Module            | Responsibility                                   |
| ----------------- | ------------------------------------------------ |
| model_router      | resolve agent_model_assignment and model_profile |
| provider_adapter  | provider-neutral model calls                     |
| prompt_runtime    | load prompt_package_ref and redact logs          |
| structured_output | schema validation and repair budget              |
| retrieval_runtime | assemble Memory Package                          |
| writing_runtime   | run chapter/section generation steps             |
| quality_runtime   | run Critic, Humanizer and Quality Gate           |
| cost_runtime      | estimate and record token cost                   |

## 1.2 Call Path

Every model call follows：

```text
task handler
↓
load task + workspace config
↓
resolve agent_model_assignment
↓
resolve model_profile + provider_account.secret_ref
↓
load prompt package from object_ref
↓
call provider adapter
↓
validate output
↓
persist output_ref + llm_call_record
```

No task handler may call provider SDK directly.

## 1.3 Streaming Decision

MVP Provider Adapter must support non-streaming calls.

Streaming is optional for MVP UI. If implemented, streaming chunks are transient UI events and are not system of record. Final generated text must still be persisted to Object Storage and referenced by output_ref.
