# 1. Contract Source of Truth

本文档定义 Novel Factory 的 API、DTO、OpenAPI、JSON Schema 和前后端 SDK 契约规则。

## 1.1 Decision

MVP 使用 OpenAPI 3.1 作为 HTTP API source of truth，JSON Schema 2020-12 作为结构化 payload source of truth。

约定：

- `packages/contracts/openapi/novel-factory.v1.yaml` 保存 HTTP API 契约。
- `packages/contracts/schemas/` 保存 JSON Schema。
- TypeScript client 和 server DTO 从 OpenAPI/JSON Schema 生成。
- Python ai-worker 使用 Pydantic model 从 JSON Schema 对齐或手写后由 contract test 校验。

## 1.2 Contract Ownership

| Contract                | Owner                    | Consumer                                |
| ----------------------- | ------------------------ | --------------------------------------- |
| OpenAPI HTTP endpoints  | api-gateway              | web, tests, external tools              |
| Task command schemas    | ai-worker + core-service | scheduler, worker modules               |
| Prompt package schemas  | ai-worker                | prompt assembly, provider adapter       |
| Quality report schemas  | quality module           | review UI, feedback module              |
| LLM call record schemas | ai-worker                | observability, feedback, cost dashboard |

## 1.3 Versioning

API version path：`/v1`。

Schema version fields：

- every JSONB payload must include `schema_version`。
- breaking schema changes increment major version。
- additive optional fields increment minor version。

## 1.4 Generated Artifacts

Generated artifacts may be committed only if the repo build requires them. If committed, generated files must include a generated marker and must not be manually edited.

Recommended generated outputs：

- `packages/shared-types/src/api.ts`
- `packages/shared-types/src/schemas.ts`
- `apps/web/src/api/client.ts`
- `apps/api-gateway/src/generated/contracts.ts`
