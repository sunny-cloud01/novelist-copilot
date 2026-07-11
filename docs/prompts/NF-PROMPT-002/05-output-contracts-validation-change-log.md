# 5. Output Contracts, Validation and Change Log

## 5.1 Output Contract Rules

结构化 Prompt 输出必须包含：

- prompt_type
- input_refs
- output_refs or output_body
- status
- confidence
- validation_errors

## 5.2 Validation Rules

Writing Prompt Pack 必须满足：

- 每个 Prompt 有明确输入和输出。
- Writer Prompt 支持 Beat 级生成。
- Critic Prompt 输出 failed_check_ids。
- Humanizer Prompt 输出 revision_diff。
- Style Prompt 不保存未授权长样例。
- 所有 Prompt 引用 NF-RAG-001 Memory Package 和 NF-QA-001 Quality Gate。

## 5.3 Boundaries

NF-PROMPT-002 定义写作 Prompt 契约，不定义供应商参数、模型选择策略或具体版权样本。

## 5.4 References

- NF-PROMPT-001
- NF-NKS-280
- NF-NKS-290
- NF-RAG-001
- NF-PIPE-003
- NF-QA-001

## 5.5 Approval

Document Status: Draft

Next Review: Writing prompt pack implementation review

Next Document: NF-QA-001 Writing Quality Gate Specification

## 5.6 Change Log

| Version | Date       | Author                                | Change                                     |
| ------- | ---------- | ------------------------------------- | ------------------------------------------ |
| 1.0.0   | 2026-07-10 | Novel Factory Prompt Engineering Team | Initial writing prompt pack specification. |
