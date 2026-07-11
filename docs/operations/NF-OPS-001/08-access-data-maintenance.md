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
