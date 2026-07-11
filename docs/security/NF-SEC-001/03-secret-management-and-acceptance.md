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
