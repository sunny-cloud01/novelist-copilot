# 2. API Principles

## 2.1 Resource-Oriented

API 应围绕稳定资源设计，而不是围绕 UI 页面或内部函数设计。

## 2.2 Spec-Backed Semantics

API 资源语义必须引用 PRD、NKS、ARCH 和 DBS 文档，不得在 API 文档中重新定义领域对象。

## 2.3 Traceable Operations

会改变知识对象、图关系、Prompt Package、Agent Task 或生成结果的 API 必须产生 trace_id 或 request_id。

## 2.4 Review-Safe Mutation

修改 Approved 或 Frozen 数据的 API 必须触发审核、审计或 Change Request 流程。

## 2.5 Backward Compatibility

API 必须显式声明版本，并尽量保持向后兼容。
