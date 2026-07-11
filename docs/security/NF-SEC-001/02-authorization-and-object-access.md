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
