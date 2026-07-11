# 8. Observability, Boundaries, and Change Log

## 8.1 Observability

Agent runs must emit run_id, task_id, agent_type, input_refs, output_refs, tool_calls, status, duration and error_id.

Agent outputs must be auditable through NF-DBS-001 audit_events or equivalent runtime logs.

## 8.2 Boundary Rules

NF-AGENT-001 defines Agent roles, lifecycle, orchestration boundaries and error handling.

NF-AGENT-001 must not define Prompt template content, database physical schemas, API request schemas or product goals.

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
- NF-NKS-280
- NF-NKS-290
- NF-ARCH-001
- NF-DBS-001
- NF-RAG-001
- NF-PROMPT-002
- NF-QA-001
- NF-PIPE-003

## 8.4 Approval

Document Status: Draft

Next Review: NF-AGENT-001 Review

Next Document: NF-PROMPT-001 Prompt Template Specification

## 8.5 Change Log

| Version | Date       | Author                                | Change                                       |
| ------- | ---------- | ------------------------------------- | -------------------------------------------- |
| 1.0.0   | 2026-07-09 | Novel Factory Agent Architecture Team | Initial Draft for Agent collaboration model. |
