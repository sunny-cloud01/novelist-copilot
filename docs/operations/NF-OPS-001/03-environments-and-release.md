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
