# 11. Architecture Risks

## 11.1 Knowledge Drift

Risk: Knowledge Base and Story Graph may diverge from source evidence.

Mitigation: preserve evidence, review reports, object lifecycle, and traceable extraction runs.

## 11.2 Prompt Coupling

Risk: Prompt templates may depend on undocumented object fields.

Mitigation: Prompt variables must reference NF-NKS and NF-DBS definitions.

## 11.3 Graph Inconsistency

Risk: Story Graph relationships may reference missing or deprecated objects.

Mitigation: enforce referential integrity and lifecycle validation before package approval.

## 11.4 Automation Overtrust

Risk: AI extraction and generation results may be accepted without sufficient review.

Mitigation: keep human-in-the-loop review and blocking quality gates.

## 11.5 Distributed Service Complexity

Risk: Microservices increase integration, deployment, observability and data consistency complexity.

Mitigation: keep early services coarse grained, enforce ownership through APIs and events, run all local services through Docker Compose, and only add more service processes when a boundary has stable contracts.
