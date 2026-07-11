# 5. Lifecycle and Contracts

## 5.1 Agent Lifecycle

```text
Created
↓
Assigned
↓
Running
↓
WaitingForTool
↓
ReviewRequired
↓
Completed
```

Failure lifecycle:

```text
Running
↓
Failed
↓
RetryScheduled 或 NeedsHumanReview 或 Blocked
```

## 5.2 Input Contract

Every Agent task must include task_id, agent_type, input_refs, allowed_tools, constraints, expected_outputs and trace_id.

## 5.3 Output Contract

Every Agent output must include task_id, agent_type, output_refs, confidence, evidence_refs, status, errors and created_at.
