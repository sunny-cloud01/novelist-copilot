---
document_id: NF-OPS-001
title: Operations Specification
version: 1.0.0
status: Draft
category: Operations Specification
owner: Novel Factory Operations Team
created: 2026-07-09
updated: 2026-07-09
dependencies:
  - NFES-000
  - NF-ARCH-001
  - NF-DBS-001
  - NF-API-001
references:
  - docs/standards/NFES-000.md
  - docs/architecture/NF-ARCH-001.md
  - docs/database/NF-DBS-001.md
  - docs/api/NF-API-001.md
---

# NF-OPS-001

# Operations Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 的运维规范。

Operations Specification 用于约束运行环境、发布流程、监控指标、备份恢复、事故处理、访问控制和运维审计。

本文档覆盖环境分层、发布流程、配置管理、监控与告警、备份与恢复、事故响应、访问控制、运行审计和维护窗口。

本文档不覆盖产品需求、数据库逻辑 Schema、API 资源设计或 Prompt 模板内容。

# 2. Operations Principles

## 2.1 Traceable Operations

所有生产环境变更必须可追踪到 operator、change_id、timestamp 和 rollback_strategy。

## 2.2 Backup Before Risky Change

高风险迁移、数据回填、批量删除、索引重建和模型切换前必须确认备份或恢复点。

## 2.3 Observability First

所有核心流水线必须具备基本指标、日志和错误追踪。

## 2.4 Human Approval for Production

生产发布、数据修正和 Approved/Frozen 文档相关变更必须有人审查。

## 2.5 Degraded Operation

外部 LLM、OCR、向量索引或图数据库异常时，系统应支持降级运行或停止高风险任务。

# 3. Environments and Release

## 3.1 Environment Model

环境分层：local、development、staging、production。

Production 必须限制直接写入权限。Staging 必须能复现核心发布、迁移和恢复流程。

## 3.2 Release Process

标准发布流程：

```text
Change Proposal
↓
Review
↓
Staging Validation
↓
Backup or Recovery Point Check
↓
Production Release
↓
Smoke Test
↓
Monitoring Window
↓
Release Closure
```

Release record 必须包含 release_id、version、change_summary、affected_modules、migration_required、rollback_strategy、approver、released_at。

# 4. Configuration Management

配置类型：

- environment_config
- model_config
- extraction_thresholds
- quality_gates
- feature_flags
- rate_limits
- access_policies

敏感配置不得写入 Markdown 文档或代码仓库。

配置变更必须记录 audit_event。

# 5. Monitoring and Alerts

Required metric groups:

- ingestion_metrics
- extraction_metrics
- validation_metrics
- generation_metrics
- consistency_metrics
- review_metrics
- feedback_metrics
- api_metrics
- database_metrics
- agent_metrics

Required alert categories:

- extraction_failure_spike
- generation_failure_spike
- graph_validation_failure
- database_latency_high
- backup_failed
- api_error_rate_high
- agent_task_backlog_high
- human_review_backlog_high

# 6. Backup and Recovery

Backups must cover:

- Relational Store
- Graph Store
- Object Store metadata
- Vector Index rebuild manifests
- migration records
- audit_events

Recovery procedures must exist for:

- source data recovery
- approved knowledge object recovery
- graph snapshot recovery
- extraction package recovery
- review report recovery
- vector index rebuild

# 7. Incident Response

Incident lifecycle:

```text
Detected
↓
Triaged
↓
Contained
↓
Mitigated
↓
Resolved
↓
Postmortem
```

Incident record must include incident_id、severity、detected_at、affected_modules、user_impact、root_cause、mitigation、follow_up_actions。

Severity levels:

- SEV1: production unavailable or data integrity at risk
- SEV2: core pipeline blocked
- SEV3: degraded function with workaround
- SEV4: minor issue or documentation correction

# 8. Access, Data Operations, and Maintenance

## 8.1 Access Control

Production access must be role-scoped.

Recommended roles: operator、reviewer、admin、service_account、auditor。

Access to raw source text, generated content and audit logs must be restricted by least privilege.

## 8.2 Data Operations

Data correction must create audit_events.

Bulk operations require dry_run result、affected_count、backup confirmation、approval、rollback strategy。

Approved or Frozen knowledge data must not be modified without review workflow.

## 8.3 Maintenance Windows

Scheduled maintenance must include maintenance_id、planned_start、planned_end、affected_modules、expected_impact、rollback_strategy、communication_plan。

# 9. Boundaries, References, and Change Log

## 9.1 Boundary Rules

NF-OPS-001 defines operational procedures, monitoring, backup, recovery and incident handling.

NF-OPS-001 must not define product behavior, database logical schema, Agent collaboration details or Prompt template content.

## 9.2 References

- NFES-000
- NF-ARCH-001
- NF-DBS-001
- NF-API-001

## 9.3 Approval

Document Status: Draft

Next Review: NF-OPS-001 Review

Next Document: NF-ADR-001 Document Project Architecture Decision

## 9.4 Change Log

| Version | Date       | Author                        | Change                                      |
| ------- | ---------- | ----------------------------- | ------------------------------------------- |
| 1.0.0   | 2026-07-09 | Novel Factory Operations Team | Initial Draft for operations specification. |
