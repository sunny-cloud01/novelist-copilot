# 1. Purpose and Scope

本文档定义 Novel Factory 的 Book Ingestion and Extraction Pipeline。

该 Pipeline 将原始小说输入转化为可审核、可追踪、可检索、可用于后续生成的 BookKnowledgePackage。它是从拆书到 AI 写作的第一条工程流水线。

本文档覆盖：

- 书籍导入和文件接收。
- 文本清洗、去重、章节识别和标准化。
- Chapter 和 Scene 切分。
- NF-NKS-100 定义的对象、关系、Pattern、Rhythm、Rule 和 Evidence 抽取。
- 任务状态、幂等、重试和失败恢复。
- 人工审核、导出和反馈回流。
- 可观测性和错误分类。

本文档不定义章节生成流水线、Prompt 模板正文、数据库物理表结构或具体 LLM Prompt。
