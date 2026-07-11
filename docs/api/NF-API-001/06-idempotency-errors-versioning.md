# 6. Idempotency, Errors, and Versioning

## 6.1 Idempotency and Concurrency

Mutation endpoints that create extraction runs, agent tasks, prompt packages or generation requests must support idempotency_key.

Concurrent updates to review-sensitive resources must use version, etag or lifecycle-aware conflict checks.

## 6.2 Error Model

Standard error categories:

- validation_error
- authentication_error
- authorization_error
- not_found
- conflict
- lifecycle_violation
- rate_limited
- dependency_error
- internal_error

Error records must include code, message, target and recovery_hint when possible.

## 6.3 Versioning and Compatibility

API version must be present in URL path or explicit version header.

Breaking changes require a new Major API version.

Backward-compatible changes include adding optional fields, adding new endpoints and adding new enum values when clients are documented to tolerate unknown values.
