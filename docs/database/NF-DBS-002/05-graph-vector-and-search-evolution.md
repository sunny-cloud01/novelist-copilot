# 5. Graph, Vector and Search Evolution

## 5.1 Story Graph Phase 1

第一阶段 Story Graph 使用 PostgreSQL 表保存 graph_nodes、graph_edges 和 graph_snapshots。

该方案适合：

- 单书或小规模跨书图谱。
- 审核友好的图边记录。
- 以 object_id、relation_type、chapter_scope、confidence 为主的查询。
- 生成前上下文召回。

## 5.2 Graph Database Upgrade Gate

满足以下条件之一时，可以引入 Neo4j 或 Memgraph：

- 多跳查询成为核心高频路径。
- PostgreSQL recursive query 无法满足交互式延迟要求。
- 需要图算法，例如 community detection、centrality、path ranking。
- 跨书知识图谱关系规模显著超过单库调优能力。

图数据库必须作为 projection store，不得替代 PostgreSQL 中的 canonical object identity。

## 5.3 Vector Search Phase 1

第一阶段使用 pgvector 支持：

- chapter embedding
- scene embedding
- character profile embedding
- pattern embedding
- asset embedding
- evidence excerpt embedding

pgvector 查询结果必须与 PostgreSQL 中的 lifecycle_status、review_status、genre_scope、source_scope 和 permission 过滤结合。

## 5.4 Dedicated Vector DB Upgrade Gate

满足以下条件之一时，可以引入 Qdrant、Milvus 或 Weaviate：

- embedding 数量达到 pgvector 维护成本明显上升的规模。
- 需要多 collection、多向量、多租户或复杂 ANN 调优。
- 需要高频在线召回并与生成流水线并发运行。
- embedding 实验迭代明显影响主库稳定性。

专用向量库必须保存 PostgreSQL object_id，不得生成新的知识对象身份。

## 5.5 Search Engine Upgrade Gate

满足以下条件之一时，可以引入 OpenSearch 或 Meilisearch：

- 后台运营需要复杂全文检索、模糊查询和聚合筛选。
- PostgreSQL full-text search 无法满足搜索体验。
- 需要跨字段、跨标签、跨题材的快速检索。

搜索引擎必须作为 read projection，不得成为写入入口。
