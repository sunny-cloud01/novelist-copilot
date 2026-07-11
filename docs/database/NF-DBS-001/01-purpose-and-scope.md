# 1. Purpose and Scope

本文档定义 Novel Factory 的 Knowledge Database 规范。

Knowledge Database 是承载 Book Library、Knowledge Base、Story Graph、Evidence、Review Report、Rule、Feedback 和运行审计数据的持久化基础。

本文档将 NF-NKS-000 的领域对象、NF-NKS-100 的 BookKnowledgePackage 和 NF-ARCH-001 的 Knowledge Storage Layer 转化为数据库级存储域、逻辑 Schema、约束、索引、迁移和备份规则。

## 1.1 Scope

本文档覆盖存储原则、存储域划分、逻辑 Schema 组、核心表或集合、Story Graph 存储模型、Evidence 与 Review 存储模型、索引与约束、数据生命周期、Migration 规则、备份与恢复要求。

本文档不覆盖 API 路径、请求体或响应体，Agent 工具调用流程，Prompt 模板正文，具体数据库产品选型或云厂商部署配置。
