# 9. Delivery Order, Risks and Change Log

## 9.1 Recommended Build Order

Recommended build order:

1. Repository skeleton and local infrastructure.
2. API envelope, trace middleware and task model.
3. Source import and object storage metadata.
4. Knowledge extraction placeholder and review workflow.
5. Graph snapshot and basic graph browse.
6. Project, Story Bible and planning records.
7. Memory Package and Prompt Package contracts.
8. Provider adapter, model profile and agent assignment config.
9. Chapter generation, Critic and Humanizer tasks.
10. Chapter Assembly, Quality Gate and Feedback.
11. Writing Studio integration.
12. MVP demo script and CI smoke test.

## 9.2 Slice Review Gate

Each slice must pass:

- tests for touched contracts and modules.
- API envelope checks for new endpoints.
- task lifecycle check for long tasks.
- trace_id propagation check.
- documentation update when contract changes.

## 9.3 Key Build Risks

| Risk                                    | Mitigation                                               |
| --------------------------------------- | -------------------------------------------------------- |
| Contract drift between web and services | Put DTOs and enums in packages/contracts                 |
| Worker bypasses service ownership       | Require Core Service commands for persistent transitions |
| Provider SDK spreads across codebase    | Keep provider SDK only inside adapter module             |
| Migration order blocks early slices     | Create identity, task, source and audit first            |
| Writing Studio becomes too large        | Build state panels separately and compose page late      |
| Quality gate too vague for tests        | Start with explicit score fields and threshold fixtures  |

## 9.4 Boundaries

NF-IMPL-003 defines service build order and implementation contracts. It does not replace detailed code-level implementation plans, migrations or API OpenAPI schemas.

## 9.5 References

- NF-IMPL-001
- NF-IMPL-002
- NF-ARCH-002
- NF-DBS-002
- NF-API-001
- NF-AGENT-001
- NF-PROMPT-002
- NF-PIPE-003
- NF-RAG-001
- NF-QA-001

## 9.6 Approval

Document Status: Draft

Next Review: Service build plan review

Next Document: Repository Scaffold Implementation Plan

## 9.7 Change Log

| Version | Date       | Author                            | Change                            |
| ------- | ---------- | --------------------------------- | --------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Implementation Team | Initial service build plan draft. |
