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
