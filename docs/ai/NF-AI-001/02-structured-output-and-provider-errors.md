# 2. Structured Output and Provider Errors

## 2.1 Structured Output Strategy

MVP structured output uses JSON Schema validation after provider response.

Preferred provider features：

1. native JSON schema or structured output mode when available。
2. JSON mode when schema mode is unavailable。
3. plain text JSON extraction only as fallback。

Validation flow：

```text
raw provider response
↓
parse JSON
↓
validate JSON Schema
↓
if invalid and retry budget remains: retry with validation error summary
↓
if still invalid: requires_review
```

Schema repair counts against retry budget.

## 2.2 Provider Error Taxonomy

Provider errors normalize to：

| Error Code                 | Task Result                 |
| -------------------------- | --------------------------- |
| provider_timeout           | retrying                    |
| provider_rate_limited      | retrying                    |
| provider_auth_failed       | blocked                     |
| provider_model_unavailable | fallback or retrying        |
| provider_policy_block      | blocked                     |
| provider_context_exceeded  | fallback or requires_review |
| provider_invalid_response  | retrying or requires_review |
| provider_unknown_error     | retrying then failed        |

## 2.3 Safety and Lifecycle Errors

Policy or lifecycle violations do not silently fallback to a weaker model.

If provider blocks content because of safety policy, task status becomes `blocked` and a task_event records sanitized reason.

If task attempts to alter Approved Knowledge outside review flow, task status becomes `blocked` with `lifecycle_violation`.
