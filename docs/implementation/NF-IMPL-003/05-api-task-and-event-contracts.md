# 5. API, Task and Event Contracts

## 5.1 API Envelope

All HTTP responses must follow NF-API-001 envelope:

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

Errors must include code, message, target and recovery_hint when possible.

## 5.2 Task Contract

Task record fields:

- task_id
- task_type
- workspace_id
- owner_module
- input_refs
- output_refs
- status
- progress
- idempotency_key
- retry_count
- error_code
- created_at
- started_at
- finished_at

Allowed status:

```text
queued
running
retrying
succeeded
failed
cancelled
requires_review
blocked
```

Task queue, lease, retry, scheduler recovery and idempotency semantics are defined by NF-TASK-001.

## 5.3 Task Event Contract

Task event fields:

- task_event_id
- task_id
- event_type
- message
- payload_ref or payload_json
- created_at

Required event_type:

- created
- started
- progress
- retry_scheduled
- review_required
- blocked
- failed
- succeeded

## 5.4 Command Contract

Worker command payload must include:

- command_id
- task_id
- task_type
- workspace_id
- input_refs
- idempotency_key
- trace_id
- requested_by

Worker result must include:

- task_id
- status
- output_refs
- metrics
- errors
- trace_id

## 5.5 Domain Event Contract

MVP domain events are internal and persisted through task_events or audit_events.

Allowed initial events:

- source_book_created
- ingestion_completed
- knowledge_candidate_created
- knowledge_object_approved
- graph_snapshot_created
- chapter_plan_created
- writing_run_created
- section_accepted
- chapter_accepted
- quality_gate_failed
- feedback_record_created
