# 8. Evolution, Boundaries and Change Log

## 8.1 Evolution Path

系统架构演进分三阶段：

| Phase   | Architecture                                                                               |
| ------- | ------------------------------------------------------------------------------------------ |
| Phase 1 | Docker Compose microservice baseline, PostgreSQL + pgvector, Redis, Object Storage         |
| Phase 2 | Extract heavy workers and add graph/vector/search projections as independent services      |
| Phase 3 | Split high-load domains into independently scalable services with hardened event contracts |

## 8.2 Service Split Gate

满足以下条件之一时，可以进一步拆分或独立扩缩服务：

- 单模块负载明显影响其他模块延迟。
- 独立扩缩容收益超过部署复杂度。
- 模块有稳定 API 和事件契约。
- 模块内部依赖已经不需要共享事务。

优先候选：Extraction Worker、Generation Worker、Retrieval Service、Consistency Service、API Gateway / BFF。

## 8.3 Boundaries

NF-ARCH-002 定义后端技术架构。

NF-ARCH-002 不定义数据库物理 Schema、API 端点细节、Prompt 模板正文、Agent 角色细节或运维 runbook。

## 8.4 References

- NFES-000
- NF-PRD-001
- NF-NKS-000
- NF-NKS-001
- NF-NKS-100
- NF-NKS-200
- NF-NKS-210
- NF-NKS-220
- NF-NKS-230
- NF-NKS-240
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270
- NF-ARCH-001
- NF-DBS-001
- NF-DBS-002
- NF-AGENT-001
- NF-PROMPT-001

## 8.5 Approval

Document Status: Draft

Next Review: Backend implementation planning review

Next Document: NF-PIPE-001 Book Ingestion and Extraction Pipeline

## 8.6 Change Log

| Version | Date       | Author                          | Change                                                |
| ------- | ---------- | ------------------------------- | ----------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Architecture Team | Initial backend technical architecture specification. |
