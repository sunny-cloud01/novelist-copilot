# 1. Purpose and Scope

本文档定义 Novel Factory 的 AI Generation and Revision Pipeline。

该 Pipeline 将已审核的知识资产、Story Graph、Pattern、Rhythm Profile、Asset、Rule 和人工目标转化为章节计划、Prompt Package、章节草稿、修订稿、质量报告和反馈信号。

本文档的核心目标是让 AI 生成不只是一次性 Prompt 输出，而是一个可追踪、可检查、可修订、可反馈的创作流水线。

本文档覆盖：

- generation request 输入契约。
- 知识召回和上下文组装。
- 章节计划和叙事压力设计。
- Prompt Package 组装。
- 章节草稿生成。
- 一致性检查、AI 味检查和修订循环。
- 人工审核和反馈回流。
- 任务状态、失败恢复和可观测性。

本文档不定义具体 Prompt 模板正文、LLM provider 私有参数、前端编辑器交互或发布渠道流程。
