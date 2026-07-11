# 2. Agent Principles

## 2.1 Specification Bound

Agent 必须遵守正式规范文档。领域对象引用 NF-NKS-000，抽取流程引用 NF-NKS-100，存储边界引用 NF-DBS-001，架构边界引用 NF-ARCH-001。

## 2.2 Tool-Constrained Execution

Agent 只能使用被授权的工具和数据范围。

## 2.3 Evidence Preservation

抽取类 Agent 必须保留 evidence，不得只输出无来源判断。

## 2.4 Human Review Compatibility

Agent 输出必须可被人工审核者理解、追溯和修正。

## 2.5 Fail Closed

当 Agent 无法确认结果可靠性时，必须进入 NeedsHumanReview 或 Blocked 状态，而不是继续传播不确定结果。
