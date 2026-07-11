# 3. Usage, Validation and Change Log

## 3.1 Usage Context

Asset 可用于：

- Prompt assembly
- Chapter drafting
- Style reference
- Scene enrichment
- Pattern slot filling
- Revision suggestion

## 3.2 Validation Rules

Asset 必须满足：

- asset_type 必须来自受控词表。
- expression_type_refs 必须引用 NF-NKS-280 中已批准的 Expression Type。
- content_summary 必须说明素材用途。
- source_refs 必须可追踪。
- quality_score 必须由人工审核、模型评估或使用反馈产生。
- Deprecated Asset 不得进入新生成请求。

## 3.3 Boundaries

NF-NKS-260 定义素材知识语义，不定义 Prompt 模板、数据库字段类型或具体改写算法。

## 3.4 Change Log

| Version | Date       | Author                                   | Change                               |
| ------- | ---------- | ---------------------------------------- | ------------------------------------ |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial Asset Library specification. |
