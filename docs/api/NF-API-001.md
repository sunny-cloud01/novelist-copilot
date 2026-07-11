---
document_id: NF-API-001
title: Platform API Specification
version: 1.0.0
status: Draft
category: API Specification
owner: Novel Factory API Architecture Team
created: 2026-07-09
updated: 2026-07-09
dependencies:
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
  - NF-AGENT-001
  - NF-PROMPT-001
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-200.md
  - docs/nks/NF-NKS-210.md
  - docs/nks/NF-NKS-220.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-240.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-260.md
  - docs/nks/NF-NKS-270.md
  - docs/architecture/NF-ARCH-001.md
  - docs/database/NF-DBS-001.md
  - docs/agents/NF-AGENT-001.md
  - docs/prompts/NF-PROMPT-001.md
---

# NF-API-001

# Platform API Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 平台 API 的设计规范。

Platform API Specification 用于约束资源命名、端点族、请求响应规则、鉴权、分页、幂等、错误码、版本和兼容性。

本文档覆盖 API 设计原则、资源域与端点族、请求与响应 envelope、鉴权与权限模型、分页、过滤和排序、幂等与并发控制、错误模型、版本与兼容性、API 观测要求。

本文档不覆盖数据库物理表结构、Agent 内部工具调用实现、Prompt 模板正文或前端页面设计。

# 2. API Principles

## 2.1 Resource-Oriented

API 应围绕稳定资源设计，而不是围绕 UI 页面或内部函数设计。

## 2.2 Spec-Backed Semantics

API 资源语义必须引用 PRD、NKS、ARCH 和 DBS 文档，不得在 API 文档中重新定义领域对象。

## 2.3 Traceable Operations

会改变知识对象、图关系、Prompt Package、Agent Task 或生成结果的 API 必须产生 trace_id 或 request_id。

## 2.4 Review-Safe Mutation

修改 Approved 或 Frozen 数据的 API 必须触发审核、审计或 Change Request 流程。

## 2.5 Backward Compatibility

API 必须显式声明版本，并尽量保持向后兼容。

# 3. Resource Domains

API 资源域：

- books
- chapters
- scenes
- knowledge-objects
- graph-nodes
- graph-edges
- evidence
- extraction-runs
- review-reports
- prompt-templates
- prompt-packages
- agent-tasks
- generation-requests
- generated-chapters
- feedback-records
- config-rules
- audit-events

# 4. Endpoint Families

## 4.1 Source API

负责 Book、Chapter、Scene 的导入、查询和预处理状态管理。

Representative endpoints: `POST /v1/books`, `GET /v1/books/{book_id}`, `GET /v1/books/{book_id}/chapters`, `GET /v1/chapters/{chapter_id}/scenes`。

## 4.2 Knowledge API

负责知识对象查询、候选对象管理、别名归一化和生命周期状态。

Representative endpoints: `GET /v1/knowledge-objects`, `GET /v1/knowledge-objects/{object_id}`, `POST /v1/knowledge-objects/{object_id}/review-actions`。

## 4.3 Graph API

负责 Story Graph 节点、关系和遍历查询。

Representative endpoints: `GET /v1/graph/nodes/{node_id}`, `GET /v1/graph/nodes/{node_id}/neighbors`, `POST /v1/graph/queries`。

## 4.4 Extraction API

负责抽取任务创建、状态查询、报告获取和错误记录。

Representative endpoints: `POST /v1/extraction-runs`, `GET /v1/extraction-runs/{run_id}`, `GET /v1/extraction-runs/{run_id}/report`。

## 4.5 Agent API

负责 Agent Task 创建、状态追踪、人工审核交接和结果读取。

Representative endpoints: `POST /v1/agent-tasks`, `GET /v1/agent-tasks/{task_id}`, `POST /v1/agent-tasks/{task_id}/review-actions`。

## 4.6 Prompt API

负责 Prompt Template、Prompt Package 和评估记录。

Representative endpoints: `GET /v1/prompt-templates`, `POST /v1/prompt-packages`, `GET /v1/prompt-packages/{package_id}`。

## 4.7 Generation API

负责生成请求、章节草稿、质量报告和修订请求。

Representative endpoints: `POST /v1/generation-requests`, `GET /v1/generation-requests/{request_id}`, `GET /v1/generated-chapters/{chapter_draft_id}`。

## 4.8 Feedback API

负责反馈记录、评分、排名建议和规则更新建议。

Representative endpoints: `POST /v1/feedback-records`, `GET /v1/feedback-records`, `GET /v1/rankings/prompt`。

# 5. Envelope, Authentication, and Pagination

## 5.1 Request and Response Envelope

Standard request metadata: request_id, actor_id, trace_id, idempotency_key。

Standard response envelope:

```json
{
  "data": {},
  "meta": {
    "request_id": "REQ-000001",
    "trace_id": "TRC-000001"
  },
  "errors": []
}
```

Error response envelope:

```json
{
  "data": null,
  "meta": {
    "request_id": "REQ-000001",
    "trace_id": "TRC-000001"
  },
  "errors": [
    {
      "code": "validation_error",
      "message": "Invalid input.",
      "target": "field_name"
    }
  ]
}
```

## 5.2 Authentication and Authorization

API must support authenticated actors: human_reviewer、system_agent、admin、service_account。

Authorization must be scoped by resource domain、action、lifecycle status、project or book scope。

Approved or Frozen data mutation requires elevated permission and audit logging.

## 5.3 Pagination, Filtering, and Sorting

List endpoints must support limit、cursor、sort、filter。

Cursor pagination is preferred for large result sets.

Filtering fields must be explicitly documented by each endpoint family.

# 6. Idempotency, Errors, and Versioning

## 6.1 Idempotency and Concurrency

Mutation endpoints that create extraction runs, agent tasks, prompt packages or generation requests must support idempotency_key.

Concurrent updates to review-sensitive resources must use version, etag or lifecycle-aware conflict checks.

## 6.2 Error Model

Standard error categories:

- validation_error
- authentication_error
- authorization_error
- not_found
- conflict
- lifecycle_violation
- rate_limited
- dependency_error
- internal_error

Error records must include code, message, target and recovery_hint when possible.

## 6.3 Versioning and Compatibility

API version must be present in URL path or explicit version header.

Breaking changes require a new Major API version.

Backward-compatible changes include adding optional fields, adding new endpoints and adding new enum values when clients are documented to tolerate unknown values.

# 7. Observability, Boundaries, and Change Log

## 7.1 Observability

Every API request must produce or propagate request_id, trace_id, actor_id, endpoint, status_code, latency and error_code.

Mutations must be traceable to audit_events when they affect persistent knowledge state.

## 7.2 Boundary Rules

NF-API-001 defines API resource boundaries and protocol rules.

NF-API-001 must not define database storage internals, Agent reasoning prompts, Prompt template content or operational runbooks.

## 7.3 References

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
- NF-AGENT-001
- NF-PROMPT-001

## 7.4 Approval

Document Status: Draft

Next Review: NF-API-001 Review

Next Document: NF-OPS-001 Operations Specification

## 7.5 Change Log

| Version | Date       | Author                              | Change                                        |
| ------- | ---------- | ----------------------------------- | --------------------------------------------- |
| 1.0.0   | 2026-07-09 | Novel Factory API Architecture Team | Initial Draft for platform API specification. |
