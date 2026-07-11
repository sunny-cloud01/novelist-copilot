# 2. Storage Stack Decision

## 2.1 Phase 1 Storage Stack

Novel Factory 第一阶段采用以下存储组合：

```text
PostgreSQL + pgvector
Object Storage
Redis
```

其中 PostgreSQL 是 system of record，Object Storage 保存大文本和包文件，Redis 保存任务状态、短期缓存和队列协调状态。

## 2.2 Phase 1 Responsibilities

| Component      | Responsibility                                                                              |
| -------------- | ------------------------------------------------------------------------------------------- |
| PostgreSQL     | 核心业务数据、知识对象、图边注册、审核、反馈、任务元数据、JSONB payload、pgvector embedding |
| Object Storage | 原文、标准化文本、抽取包、生成草稿、质量报告、长证据片段                                    |
| Redis          | Worker 队列、任务锁、短期缓存、Agent 协调状态、限流计数                                     |

## 2.3 Evolution Principle

第一阶段不直接引入独立图数据库、专用向量数据库和全文搜索集群。

原因：当前最重要的风险是知识模型、对象生命周期、证据链和审核状态仍在快速演进。过早拆分存储会增加迁移、调试和一致性成本。

## 2.4 Upgrade Targets

当 PostgreSQL 内部能力无法满足特定负载时，允许引入：

- Neo4j 或 Memgraph：复杂多跳 Story Graph 查询。
- Qdrant、Milvus 或 Weaviate：大规模向量检索和 embedding 实验。
- OpenSearch 或 Meilisearch：后台全文检索、标签检索和运营检索体验。

升级必须以 NF-DBS-001 的逻辑 Schema 和 NF-NKS 系列语义为边界，不得改变 canonical 对象身份。
