# 5. Validation, Boundaries and Change Log

## 5.1 Validation Rules

Memory Context 必须满足：

- 每个 Memory Package 必须绑定 target_section_id 或 target_chapter_id。
- dynamic state 必须优先于 static profile。
- stale context 必须标记。
- Writer Prompt 不得接收未标记 stale 的过期上下文。
- 召回结果必须有 relevance_reason。

## 5.2 Boundaries

NF-RAG-001 定义检索和记忆上下文规范，不定义数据库产品选型、embedding 模型或 Prompt 模板正文。

## 5.3 References

- NF-NKS-000
- NF-NKS-200
- NF-NKS-210
- NF-NKS-220
- NF-NKS-230
- NF-NKS-250
- NF-NKS-270
- NF-NKS-290
- NF-DBS-002
- NF-PIPE-003

## 5.4 Approval

Document Status: Draft

Next Review: Retrieval implementation review

Next Document: NF-PROMPT-002 Writing Prompt Pack Specification

## 5.5 Change Log

| Version | Date       | Author                                    | Change                                              |
| ------- | ---------- | ----------------------------------------- | --------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Retrieval Architecture Team | Initial retrieval and memory context specification. |
