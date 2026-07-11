# 9. Migration, Backup, and Retention

## 9.1 Migration Record

Every schema migration must create a migration record containing migration_id, version, description, applied_at, actor and rollback_strategy.

## 9.2 Backward Compatibility

Minor and Patch migrations should preserve backward compatibility for canonical documents and approved data packages.

## 9.3 Data Backfill

Data backfill must be traceable and must not overwrite source evidence.

## 9.4 Rollback

Rollback must preserve audit_events and migration records.

## 9.5 Backup Scope

Backups must cover Relational Store, Graph Store, Object Store metadata, Vector Index rebuild manifests, migration records and audit_events.

## 9.6 Recovery Point

The system must define recovery points for source data, approved knowledge objects, graph snapshots, extraction packages and review reports.

## 9.7 Vector Index Recovery

Vector Index may be rebuilt from canonical objects, text references and embedding manifests. The rebuild process must be documented by NF-OPS.

## 9.8 Raw Source Retention

Raw source retention policy must preserve enough text reference to support evidence audit and legal review.

## 9.9 Deprecated Object Retention

Deprecated objects must remain queryable for historical references but excluded from default generation retrieval.

## 9.10 Audit Retention

Audit records must not be deleted during normal data cleanup.
