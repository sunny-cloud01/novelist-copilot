# 5. Validation, Boundaries and Change Log

## 5.1 Quality Report Contract

Quality Report 至少包含：

- quality_report_id
- target_scope
- score_summary
- blocking_issues
- revision_required
- human_review_required
- feedback_records
- evidence_refs

## 5.2 Validation Rules

Quality Gate 必须满足：

- 每个 score 必须有取值范围。
- blocking issue 必须给出 affected_text_ref。
- 质量失败必须能转化为 Critic rewrite request 或 Humanizer revision guidance。
- 通过阈值变更必须记录版本。

## 5.3 Boundaries

NF-QA-001 定义写作质量门禁，不定义具体评分模型实现、人工审稿界面或模型供应商参数。

## 5.4 References

- NF-NKS-230
- NF-NKS-250
- NF-NKS-270
- NF-NKS-280
- NF-NKS-290
- NF-RAG-001
- NF-PROMPT-002
- NF-PIPE-003

## 5.5 Approval

Document Status: Draft

Next Review: Writing quality gate implementation review

Next Document: Writing Studio Workflow Specification

## 5.6 Change Log

| Version | Date       | Author                                 | Change                                      |
| ------- | ---------- | -------------------------------------- | ------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Quality Engineering Team | Initial writing quality gate specification. |
