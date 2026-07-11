# 3. Backend Service Boundaries

## 3.1 Service Map

第一阶段后端包含以下微服务或粗粒度服务边界：

| Service Boundary        | Preferred Stack       | Responsibility                                             |
| ----------------------- | --------------------- | ---------------------------------------------------------- |
| API Gateway / BFF       | NestJS or FastAPI     | 前端 API 聚合、认证上下文、轻量编排和请求路由              |
| Book Service            | NestJS or FastAPI     | 管理书籍、章节、来源、导入状态和文本引用                   |
| Ingestion Service       | Python FastAPI/Worker | 清洗、去重、章节识别、文本标准化和 object storage 写入     |
| Extraction Orchestrator | Python Worker         | 编排 NF-NKS-100 拆书流水线和抽取任务状态                   |
| Knowledge Service       | Python FastAPI        | 管理 knowledge_objects、aliases、versions、review states   |
| Story Graph Service     | Python FastAPI        | 管理 graph_nodes、graph_edges、snapshots 和图查询          |
| Retrieval Service       | Python FastAPI        | 组合结构化查询、向量召回、证据召回和上下文裁剪             |
| Planning Service        | Python FastAPI        | 基于知识、Pattern、Rhythm 和 Rule 生成大纲、卷纲和章节计划 |
| Prompt Assembly Service | Python FastAPI        | 根据 NF-PROMPT-001 组装 Prompt Package                     |
| Generation Service      | Python Worker         | 管理章节生成、改写、润色和候选版本                         |
| Consistency Service     | Python FastAPI/Worker | 检查人物、世界、时间线、规则、伏笔和生成结果一致性         |
| Review Service          | NestJS or FastAPI     | 管理 AI Review、人审、批准、驳回和修正记录                 |
| Feedback Service        | Python FastAPI        | 接收评分、人工修改、读者反馈并更新 ranking signals         |

## 3.2 Ownership Rule

每个服务只能直接写入自己拥有的数据表族。跨服务变更必须通过 API、command、domain event 或 outbox event 完成。

示例：Generation Service 不得直接修改 knowledge_objects。它只能提交 review item 或 feedback record，由 Knowledge Service 或 Review Service 处理状态变更。

## 3.3 Interface Style

服务内部接口优先使用 application service 函数或 class，而不是直接暴露 ORM model。服务之间接口必须通过 HTTP API、async event 或 queue command 表达，不得共享 ORM model。

推荐接口形态：

```text
command input -> application service -> transaction -> domain result/event
```

该风格可以让服务拆分、独立部署和独立测试时保留清晰边界。

## 3.4 Repository and Package Boundary

建议第一阶段使用 monorepo 管理多服务代码，但每个服务必须有独立 package、Dockerfile、依赖声明和启动命令。

建议代码结构：

```text
apps/
├── web/                    # React + TypeScript + pnpm + shadcn/ui
├── api-gateway/            # NestJS or FastAPI
├── book-service/
├── knowledge-service/
├── generation-service/
├── review-service/
└── worker-services/
packages/
├── contracts/
├── shared-types/
└── ui/
infra/
├── docker-compose.yml
├── postgres/
├── redis/
└── minio/
```

Frontend package management must use pnpm. shadcn/ui is the preferred component source for common UI primitives.
