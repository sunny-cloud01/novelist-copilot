# 2. Repository and Runtime Structure

## 2.1 Monorepo Structure

MVP 代码仓库推荐结构：

```text
apps/
├── web/
├── api-gateway/
├── core-service/
├── ai-worker/
└── scheduler/
packages/
├── contracts/
│   ├── openapi/
│   ├── schemas/
│   └── fixtures/
├── shared-types/
├── prompt-schemas/
├── config/
└── ui/
infra/
├── docker-compose.yml
├── postgres/
├── redis/
└── minio/
scripts/
└── dev/
```

## 2.2 Package Responsibilities

| Path                    | Responsibility                                                                     |
| ----------------------- | ---------------------------------------------------------------------------------- |
| apps/web                | React + TypeScript + pnpm + shadcn/ui frontend                                     |
| apps/api-gateway        | Frontend-facing BFF, auth context, envelope, trace propagation                     |
| apps/core-service       | MVP domain modules and PostgreSQL writes                                           |
| apps/ai-worker          | LLM, extraction, retrieval, planning, generation, critic, humanizer, quality tasks |
| apps/scheduler          | retries, timeout scan, stale projection scan, periodic maintenance                 |
| packages/contracts      | OpenAPI 3.1, JSON Schema, task contracts, review action enums, response envelopes  |
| packages/shared-types   | cross-app TypeScript types generated from contracts where possible                 |
| packages/prompt-schemas | prompt package, memory package and structured output schemas                       |
| packages/config         | model profile, provider config, quality threshold defaults                         |
| packages/ui             | shared shadcn/ui wrappers and project UI primitives                                |

## 2.3 Runtime Processes

Local MVP runtime:

```text
web -> api-gateway -> core-service
api-gateway -> ai-worker command queue
ai-worker -> postgres / redis / minio / provider adapter
scheduler -> postgres / redis
```

API Gateway may call core-service synchronously for reads and simple mutations. Long-running operations must create tasks and be executed by ai-worker.

## 2.4 Development Commands

Expected developer commands:

```sh
pnpm install
pnpm contracts:lint
pnpm contracts:generate
pnpm dev
pnpm test
pnpm lint
docker compose up -d postgres redis minio
```

Python worker dependencies may be managed inside apps/ai-worker with a dedicated environment tool, but local orchestration must remain documented in one root developer guide.
