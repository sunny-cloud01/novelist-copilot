# 4. Database Migration Plan

## 4.1 Migration Order

MVP migrations should land in this order:

1. identity and workspace tables.
2. task and audit tables.
3. source and object storage metadata tables.
4. evidence tables.
5. knowledge and review tables.
6. graph tables.
7. project planning tables.
8. prompt and memory tables.
9. generation and quality tables.
10. feedback and config tables.

Physical table names, schema ownership, ULID rules, embedding table rules and migration boundaries are defined by NF-DBS-003.

This order allows early slices to run without waiting for writing-specific tables.

## 4.2 Required Table Families

MVP table families must match NF-IMPL-002:

- identity
- source
- task
- evidence
- knowledge
- graph
- review
- project
- prompt
- memory
- generation
- quality
- feedback
- config
- audit

## 4.3 Universal Columns

Persistent tables should include:

- id
- workspace_id when scoped
- lifecycle_status or status when applicable
- created_at
- updated_at
- created_by or actor_id when user initiated
- trace_id for mutation lineage

Versioned or review-sensitive tables should include:

- version
- review_status
- source_snapshot_id when reading knowledge state

## 4.4 Object Reference Rule

Tables that reference large text, reports or diff payloads must store object_ref instead of inline large payloads.

object_ref metadata must include checksum, byte_size, mime_type, owner_ref, access_policy and created_at.

## 4.5 Seed Data

MVP seed data must include:

- local admin user.
- default workspace.
- default model profiles.
- default agent model assignments.
- default quality thresholds.
- default config rules.
- minimal prompt templates.

Seed data must be safe for local development and must not include secrets.
