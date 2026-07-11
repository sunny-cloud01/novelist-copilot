# 3. Storage Domains

Novel Factory 推荐使用四类存储域：

```text
Relational Store
Graph Store
Object Store
Vector Index
```

## 3.1 Relational Store

Relational Store 负责保存强一致的核心对象、审查状态、运行记录、配置和引用关系。

适合数据：Book、Chapter、Scene、Canonical Objects、Evidence Metadata、Review Report、Extraction Run、Feedback Record。

## 3.2 Graph Store

Graph Store 负责保存 Story Graph 节点与关系，并支持多跳关系查询。

适合数据：Story Graph Node、Story Graph Edge、Relationship Confidence、Graph Snapshot。

## 3.3 Object Store

Object Store 负责保存大文本、原始文件、抽取包、导出包和质量报告。

适合数据：raw_text、normalized_text、BookKnowledgePackage、quality_report、generated_chapter_draft、long source excerpt。

## 3.4 Vector Index

Vector Index 负责支持语义检索、RAG、相似 Pattern 检索和素材召回。

适合数据：Chapter embedding、Scene embedding、Character profile embedding、Pattern embedding、Asset embedding、Evidence excerpt embedding。
