# 8. Boundary Rules

## 8.1 NF-NKS-000 Boundary

NF-NKS-000 只定义术语和领域对象。

NF-NKS-000 不定义具体抽取流程、数据库类型、API 字段格式或 Prompt 模板正文。

## 8.2 NF-NKS-100 Boundary

NF-NKS-100 应引用本文档中的对象定义，并定义如何从 Book、Chapter 和 Scene 中抽取这些对象。

## 8.3 Database Boundary

数据库 Schema 必须引用本文档对象，但字段类型、索引、迁移和约束由 NF-DBS 文档定义。

## 8.4 Prompt Boundary

Prompt 文档必须引用本文档对象，但不得在 Prompt 文档中重新定义 Character、Event、Pattern 或 Rhythm Profile。
