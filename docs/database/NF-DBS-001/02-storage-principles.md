# 2. Storage Principles

## 2.1 Source Traceability

所有从小说文本抽取出的对象、关系和规则必须可追踪到 Evidence。

## 2.2 Logical Stability

逻辑 Schema 必须优先保持稳定。物理存储可以随技术选型演进，但跨模块数据语义不得随意变化。

## 2.3 Separation of Concerns

来源数据、规范化对象、图关系、证据、审查、反馈和运行日志必须分别建模。

## 2.4 Lifecycle Awareness

数据库必须保存对象生命周期状态。允许状态引用 NF-NKS-000：Extracted、Normalized、Reviewed、Approved、Deprecated。

## 2.5 Append-Friendly Audit

审计、抽取运行、人工审核和反馈数据应优先采用 append-friendly 记录方式，避免覆盖历史证据。

## 2.6 Implementation Neutrality

本文档定义逻辑数据库规范，不绑定 PostgreSQL、Neo4j、MongoDB、Elastic、Milvus 或其他具体产品。
