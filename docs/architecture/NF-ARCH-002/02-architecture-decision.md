# 2. Architecture Decision

## 2.1 Phase 1 Architecture Style

Novel Factory 第一阶段采用 microservice-oriented architecture。

系统必须按前端应用、API Gateway / BFF、领域服务、Worker 服务、Scheduler 和基础设施服务拆分运行边界。第一阶段可以保持少量粗粒度服务，但不得弱化已定义的服务边界和所有权规则。

所有运行单元必须可容器化，本地开发默认通过 Docker Compose 或等价容器编排启动。

## 2.2 Recommended Stack

推荐第一阶段技术栈：

| Layer                        | Recommendation                                                           |
| ---------------------------- | ------------------------------------------------------------------------ |
| Frontend                     | React + TypeScript                                                       |
| Frontend Package Manager     | pnpm                                                                     |
| Frontend Component Library   | shadcn/ui preferred                                                      |
| API Gateway / BFF            | NestJS or FastAPI                                                        |
| AI / Knowledge Services      | Python FastAPI                                                           |
| Admin / Realtime Services    | NestJS when TypeScript integration is more valuable                      |
| Python Data Validation       | Pydantic                                                                 |
| TypeScript Validation        | Zod or class-validator                                                   |
| Python ORM / SQL             | SQLAlchemy Core or SQLAlchemy ORM                                        |
| TypeScript ORM / SQL         | Prisma or Drizzle when used by NestJS services                           |
| Migration                    | Alembic for Python-owned schemas; service-owned migration tool otherwise |
| Worker                       | Celery, Dramatiq, RQ, or service-specific worker                         |
| Queue / Runtime Coordination | Redis                                                                    |
| Database                     | PostgreSQL with pgvector                                                 |
| Object Storage               | MinIO locally, S3-compatible storage later                               |
| Local Infrastructure         | Docker Compose                                                           |
| LLM Provider Integration     | Provider adapter layer                                                   |

## 2.3 Service Technology Selection Rule

服务技术栈按职责选择，不要求所有后端服务使用同一种语言。

Python is recommended for text processing, LLM orchestration, embedding generation, extraction evaluation, retrieval, generation and consistency checking.

NestJS is recommended for API Gateway / BFF, admin APIs, authentication integration, realtime events, TypeScript SDK alignment and frontend-facing orchestration.

Service boundaries must be chosen by domain ownership and runtime profile, not by language preference alone.

## 2.4 Microservice Constraints

Microservices must obey:

- No cross-service database writes without ownership boundary.
- No direct dependency from business modules to specific LLM provider SDKs.
- No generation result enters approved knowledge without review state.
- No Redis state is treated as system of record.
- No object storage file is referenced without PostgreSQL metadata.
- No frontend service bypasses API Gateway / BFF for privileged operations.
