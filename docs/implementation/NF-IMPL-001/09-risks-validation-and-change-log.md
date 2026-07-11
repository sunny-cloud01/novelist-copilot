# 9. Risks, Validation and Change Log

## 9.1 Key Risks

| Risk                            | Mitigation                                                                             |
| ------------------------------- | -------------------------------------------------------------------------------------- |
| Microservice overhead too early | Use service boundaries first; deploy coarse-grained services until load requires split |
| Quality score instability       | Start with rule checks, LLM judge and human sampling; calibrate thresholds per genre   |
| AI flavor remains high          | Keep Style Analyzer before Writer; Humanizer is only a micro-pass                      |
| Knowledge drift                 | Use source_snapshot_id, dynamic state override and stale context blocking              |
| Human review overload           | Use severity, confidence, retry budget and blocking-only handoff                       |
| Copyright and originality risk  | Use authorized sources, abstract style features and originality safety gate            |
| Cost explosion                  | Track token, retry, accepted_output_ratio and model_cost_quality_ratio                 |

## 9.2 Validation Strategy

产品级验证分为：

- Documentation validation: build_docs check must pass。
- Contract validation: API envelope、task model、output package schema 可校验。
- Pipeline validation: sample book can move through extraction, review, planning and writing。
- Trace validation: selected generated Beat can trace back to source knowledge, prompt, memory and quality report。
- Cost validation: every model call has model_profile_id and token metrics。
- Labor validation: review queue volume and human_edit_distance remain within configured threshold。

## 9.3 Implementation Readiness Checklist

进入代码实现前必须确认：

- MVP scope locked。
- Service ownership table accepted。
- Table family draft created。
- API endpoint families selected。
- Writing Studio first workflow accepted。
- Model provider adapter interface accepted。
- Human review thresholds configured。

## 9.4 Boundaries

NF-IMPL-001 是产品级实现蓝图，不替代 PRD、ARCH、DBS、API、PIPE、RAG、QA、AGENT、PROMPT 或 NKS 文档。

当具体实现细节与本蓝图冲突时，应优先更新对应权威规范，再同步更新 NF-IMPL-001。

## 9.5 References

- NF-PRD-001
- NF-ARCH-001
- NF-ARCH-002
- NF-DBS-002
- NF-API-001
- NF-AGENT-001
- NF-PROMPT-001
- NF-PROMPT-002
- NF-PIPE-001
- NF-PIPE-002
- NF-PIPE-003
- NF-RAG-001
- NF-QA-001
- NF-NKS-290
- NF-IMPL-002

## 9.6 Approval

Document Status: Draft

Next Review: Product implementation blueprint review

Next Document: NF-IMPL-002 MVP Delivery Plan

## 9.7 Change Log

| Version | Date       | Author                            | Change                                          |
| ------- | ---------- | --------------------------------- | ----------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Implementation Team | Initial product-level implementation blueprint. |
