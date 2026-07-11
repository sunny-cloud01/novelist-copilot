# 7. Evidence and Review Model

## 7.1 Evidence Requirement

The following records must be evidence-backed:

- knowledge_objects created from source text
- graph_edges
- extracted config_rules
- pattern records
- rhythm profile records
- contradiction candidates

## 7.2 Evidence Storage

Short excerpts may be stored inline when allowed by storage policy. Long excerpts and raw text must be stored in Object Store and referenced by source_text_excerpt_ref.

## 7.3 Review Status

Review status values:

- Pending
- Approved
- Rejected
- NeedsHumanReview
- Blocked

## 7.4 Blocking Issues

Blocking issues from NF-NKS-100 must be persisted in review_reports and linked to extraction_runs when applicable.
