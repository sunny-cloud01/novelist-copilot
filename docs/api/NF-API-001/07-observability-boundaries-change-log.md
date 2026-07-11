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
