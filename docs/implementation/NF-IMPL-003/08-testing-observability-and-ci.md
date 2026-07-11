# 8. Testing, Observability and CI

## 8.1 Test Layers

MVP must include:

- unit tests for contracts and schema validation.
- service tests for core module commands.
- worker tests for task lifecycle and retry budget.
- API tests for envelope, errors and idempotency.
- frontend tests for key workflow states.
- end-to-end smoke test for MVP demo script.

## 8.2 Contract Tests

Contract tests must validate:

- response envelope shape.
- task status enum.
- review action enum.
- provider adapter result shape.
- quality report shape.
- feedback record shape.

## 8.3 Observability Fields

Every request, task and model call must include or propagate:

- request_id
- trace_id
- workspace_id
- actor_id or agent_role
- status
- latency
- error_code

Model calls also require prompt_tokens, completion_tokens, retry_count and cost_estimate.

## 8.4 Audit Tests

Audit tests must verify audit_event creation for:

- approving knowledge object.
- accepting chapter into manuscript.
- changing model profile.
- changing quality threshold.
- promoting feedback suggestion.

## 8.5 CI Minimum Gate

MVP CI should run:

```sh
pnpm lint
pnpm contracts:lint
pnpm contracts:test
pnpm test
python scripts/build_docs.py --check
```

If Python worker has its own test command, it must be added to CI before ai-worker tasks become production-critical.
