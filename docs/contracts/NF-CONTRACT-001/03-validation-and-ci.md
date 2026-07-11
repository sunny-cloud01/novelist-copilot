# 3. Validation and CI

## 3.1 Contract Validation

CI must validate：

- OpenAPI file parses.
- all `$ref` targets resolve.
- generated TypeScript types are up to date.
- representative API responses match schemas.
- task command payloads match JSON Schema.
- Pydantic worker models can parse contract fixtures.

## 3.2 Compatibility Rule

Backward-compatible changes：

- add optional response field。
- add endpoint。
- add enum value only when clients are documented to tolerate unknown values。

Breaking changes：

- remove field。
- rename field。
- change type。
- make optional field required。
- change lifecycle semantics。

Breaking changes require `/v2` or explicit migration plan.

## 3.3 Fixture Rule

Each contract family must include at least one valid fixture and one invalid fixture.

Fixture path convention：

```text
packages/contracts/fixtures/{contract_family}/valid/*.json
packages/contracts/fixtures/{contract_family}/invalid/*.json
```

Fixtures must not contain provider secrets, full source book text or copyrighted samples.

## 3.4 Acceptance Checklist

Contract layer is ready when：

- `pnpm contracts:lint` validates OpenAPI and JSON Schema。
- `pnpm contracts:generate` regenerates TypeScript outputs。
- `pnpm contracts:test` validates fixtures。
- Python worker contract test loads task, prompt, memory and quality fixtures。

## 3.5 Change Log

| Version | Date       | Changes                                              |
| ------- | ---------- | ---------------------------------------------------- |
| 1.0.0   | 2026-07-11 | Initial API, DTO and OpenAPI contract specification. |
