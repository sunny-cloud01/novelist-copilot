# 3. Documentation Principles

## 3.1 Specification First

正式文档的核心目标不是记录讨论过程，而是定义系统行为、数据结构、约束条件、标准流程和可执行依据。

## 3.2 Single Source of Truth

每个领域概念必须存在唯一权威定义。例如，Character 的定义必须来源于 NF-NKS-000。其他文档只能引用该定义，不得重复定义。

## 3.3 Traceability

所有重要设计决策必须可追踪。重大架构决策必须创建 ADR。

## 3.4 AI Readability

所有正式文档必须结构清晰、章节稳定、定义明确、避免歧义，并支持机器解析。

## 3.5 Document as Source

Novel Factory 文档应按照源码工程方式维护。长文档应拆分为章节源文件，最终可构建为完整 Markdown、PDF、JSON 或 YAML 资产。
