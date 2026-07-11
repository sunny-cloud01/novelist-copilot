---
document_id: NF-SEC-001
title: Authentication, Authorization and Secret Management Specification
version: 1.0.0
status: Draft
category: Security Specification
owner: Novel Factory Security Architecture Team
created: 2026-07-11
updated: 2026-07-11
dependencies:
  - NFES-000
  - NF-API-001
  - NF-ARCH-002
  - NF-DBS-003
  - NF-LLM-001
references:
  - docs/standards/NFES-000.md
  - docs/api/NF-API-001.md
  - docs/architecture/NF-ARCH-002.md
  - docs/database/NF-DBS-003.md
  - docs/llm/NF-LLM-001.md
---

# NF-SEC-001

# Authentication, Authorization and Secret Management Specification

# 1. Identity and Roles

本文档定义 Novel Factory MVP 的身份、权限、服务账号、对象访问和密钥管理规则。

## 1.1 Product Assumption

Novel Factory MVP 是个人创作者平台，但仍保留 workspace 边界。workspace 用于隔离数据、配置、任务和后续可能的协作能力。

## 1.2 Actor Types

允许 actor：

| Actor           | Description                                   |
| --------------- | --------------------------------------------- |
| creator         | 个人创作者，拥有自己 workspace 的主要操作权限 |
| admin           | 本地或生产管理者，可处理配置和运维操作        |
| service_account | 服务间调用身份                                |
| system_agent    | 后台 Agent 任务身份                           |
| auditor         | 只读审计身份                                  |

## 1.3 Workspace Roles

MVP workspace role：

| Role     | Permissions                                    |
| -------- | ---------------------------------------------- |
| owner    | workspace 全权限，包括配置和删除请求           |
| creator  | 上传、生成、审核、批准章节                     |
| reviewer | 审核 knowledge、quality 和 feedback suggestion |
| viewer   | 只读查看项目、报告和图谱                       |
| service  | 后台任务执行和内部写入                         |

个人平台默认创建一个 owner 用户和一个 default workspace。

# 2. Authorization and Object Access

## 2.1 Authorization Rule

每个 API mutation 必须检查：

- actor authentication。
- workspace membership。
- resource ownership or scope。
- action permission。
- lifecycle permission。

Approved/Frozen knowledge、accepted chapter、model assignment 和 quality threshold 的修改必须写 audit_event。

## 2.2 Sensitive Resource Classes

敏感资源分类：

| Class          | Examples                         | Access Rule                                       |
| -------------- | -------------------------------- | ------------------------------------------------- |
| source_text    | uploaded source, normalized text | owner, creator, service                           |
| generated_text | drafts, humanized chapters       | owner, creator, reviewer, service                 |
| prompt_payload | prompt package object            | owner, service; reviewer can see redacted summary |
| llm_secret     | provider key                     | never returned by API                             |
| audit_log      | audit_events                     | owner, admin, auditor                             |
| model_config   | profiles, assignments            | owner, admin; service read-only                   |

## 2.3 Object Storage Access

Object Storage 不暴露永久公开 URL。

下载流程：

```text
client requests object_ref
↓
API checks workspace and permission
↓
API returns short-lived signed URL or streams object
```

Signed URL must expire. Default MVP expiration: 15 minutes.

## 2.4 Redaction Rule

日志、错误、task events 和 review summaries 不得包含：

- provider API key。
- full source text。
- full prompt body。
- raw credential。
- signed URL after expiration window。

允许记录：hash、checksum、byte_size、object_ref、excerpt range、token count、schema version。

# 3. Secret Management and Acceptance

## 3.1 Secret Storage

MVP local environment 使用 `.env.local` 或 Docker Compose env file 保存开发密钥。

生产环境必须使用 secret manager 或部署平台 secret storage。

禁止：

- 将 provider API key 写入 Markdown。
- 将 provider API key 写入 seed data。
- 将 provider API key 写入 PostgreSQL 明文字段。
- 在日志中打印 Authorization header。

## 3.2 Provider Account Rule

`config.provider_accounts.secret_ref` 指向外部 secret，不保存 secret 值。

AI Worker 调用 provider 前：

1. resolve model_profile。
2. resolve provider_account。
3. load secret by secret_ref。
4. call Provider Adapter。
5. record llm_call_record without secret。

## 3.3 Service Account Rule

服务间调用使用 service account token。

Token 必须包含：

- service_name
- allowed_scopes
- issued_at
- expires_at

长期运行 worker 不得使用 human creator token 执行后台写入。

## 3.4 Acceptance Checklist

安全层开工前必须确认：

- 本地 `.env.example` 只包含变量名和假值。
- provider secret 不进入 database seed。
- object_ref 下载需要授权检查。
- model assignment 修改写 audit_event。
- accepted chapter 删除或覆盖需要 elevated permission。

## 3.5 Change Log

| Version | Date       | Changes                                                                    |
| ------- | ---------- | -------------------------------------------------------------------------- |
| 1.0.0   | 2026-07-11 | Initial authentication, authorization and secret management specification. |
