# 6. Data Flow and Consistency

## 6.1 Extraction Data Flow

```text
Book Service
↓
Ingestion Service
↓
Object Storage raw_text / normalized_text
↓
Extraction Orchestrator
↓
Knowledge Service + Story Graph Service
↓
Review Service
↓
Approved Knowledge Base
```

所有从原文抽取出的对象必须绑定 evidence_refs。

## 6.2 Retrieval Data Flow

```text
Generation Request
↓
Retrieval Service
├── relational filters
├── vector search
├── Story Graph traversal
├── evidence retrieval
└── context budget trimming
↓
Planning Service
```

Retrieval Service 必须同时考虑 lifecycle_status、review_status、genre_scope、book_scope 和 permission。

## 6.3 Generation Data Flow

```text
Planning Service
↓
Prompt Assembly Service
↓
LLM Provider Adapter
↓
Generation Service
↓
Consistency Service
↓
Review Service
↓
Feedback Service
```

每个中间产物必须有 output_ref 或 database record，便于回放、审计和质量分析。

## 6.4 Consistency Layers

一致性分为三层：

| Layer                   | Responsibility                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------- |
| Transaction Consistency | PostgreSQL transaction, idempotency and ownership boundaries                          |
| Knowledge Consistency   | NKS object identity, evidence, lifecycle and review states                            |
| Narrative Consistency   | Character continuity, timeline, location, power system, rule and foreshadowing checks |

## 6.5 Outbox Rule

跨 projection 更新使用 outbox pattern。

业务事务写入 PostgreSQL 和 outbox event。后台 worker 更新 embedding、graph projection、search projection 或 object package。Projection 失败不得回滚已完成的权威业务事务，但必须留下 retryable failure record。

## 6.6 Error Taxonomy

后端错误至少分为：

- validation_error
- permission_error
- dependency_error
- llm_provider_error
- extraction_error
- consistency_violation
- review_required
- storage_error
- projection_error
- unknown_error

错误必须可追踪到 task_id、run_id、request_id 或 affected_object_id。
