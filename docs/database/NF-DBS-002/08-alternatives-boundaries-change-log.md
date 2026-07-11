# 8. Alternatives, Boundaries and Change Log

## 8.1 Alternatives Considered

### 8.1.1 Neo4j First

Rejected for Phase 1.

原因：Story Graph 语义和对象生命周期仍在演进。直接以图数据库为主库会增加迁移和审核复杂度。

### 8.1.2 Dedicated Vector DB First

Rejected for Phase 1.

原因：第一阶段 embedding 规模和召回策略尚未稳定。pgvector 足以支撑早期 RAG、相似 Pattern 和素材召回。

### 8.1.3 MongoDB First

Rejected for Phase 1.

原因：Novel Factory 需要强审计、强引用、审核状态和跨对象一致性。JSONB 已能覆盖半结构化 payload，而 PostgreSQL 提供更强事务边界。

### 8.1.4 Elasticsearch First

Rejected for Phase 1.

原因：全文检索不是第一阶段的权威存储核心。搜索引擎更适合作为后续 read projection。

## 8.2 Boundary Rules

NF-DBS-002 定义物理数据库与存储选型。

NF-DBS-002 不定义业务 API、Prompt 模板、Agent 推理策略、具体 ORM 代码或云厂商 Terraform 配置。

## 8.3 References

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

## 8.4 Approval

Document Status: Draft

Next Review: Backend technical architecture review

Next Document: NF-ARCH-002 Backend Technical Architecture

## 8.5 Change Log

| Version | Date       | Author                               | Change                                                 |
| ------- | ---------- | ------------------------------------ | ------------------------------------------------------ |
| 1.0.0   | 2026-07-10 | Novel Factory Data Architecture Team | Initial physical database and storage selection draft. |
