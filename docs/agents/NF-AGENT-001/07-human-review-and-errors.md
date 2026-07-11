# 7. Human Review and Errors

## 7.1 Human Review Handoff

Agent must hand off to human review when confidence is below configured threshold, entity identity conflicts remain unresolved, graph validation fails, generated content violates blocking rules, policy-sensitive uncertainty exists, or data correction affects Approved objects.

Handoff package must include issue_summary, affected_objects, evidence_refs, recommended_actions and blocking_status.

## 7.2 Error Categories

Agent errors must use categories compatible with NF-NKS-100 and NF-DBS-001:

- input_error
- tool_error
- extraction_error
- normalization_error
- graph_error
- generation_error
- validation_error
- review_error

## 7.3 Retry Policy

Transient tool errors may retry. Semantic conflicts require review. Repeated failure must become Blocked.
