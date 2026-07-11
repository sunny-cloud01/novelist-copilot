# 5. Validation, Boundaries and Change Log

## 5.1 Validation Rules

Feedback Knowledge 必须满足：

- 每条 Feedback Record 必须有 source 和 target。
- blocking 反馈必须进入 Review Service。
- Human Edit 必须保存 before_ref 和 after_ref。
- Cost Quality Signal 必须绑定 model_profile_id。
- Reader Signal 必须记录来源和置信度。
- 反馈驱动的策略变更必须可回滚。

## 5.2 Boundaries

NF-NKS-290 定义反馈知识模型，不定义推荐算法、A/B 测试平台或读者数据采集 SDK。

## 5.3 References

- NF-NKS-000
- NF-NKS-230
- NF-NKS-240
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270
- NF-NKS-280
- NF-PIPE-003

## 5.4 Approval

Document Status: Draft

Next Review: Feedback learning implementation review

Next Document: NF-RAG-001 Knowledge Retrieval and Memory Context Specification

## 5.5 Change Log

| Version | Date       | Author                                   | Change                                    |
| ------- | ---------- | ---------------------------------------- | ----------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial feedback knowledge specification. |
