# 8. MVP and Phased Delivery

## 8.1 Phase 0 Documentation and Contracts

目标：把产品实现所需规范收敛到可开发状态。

交付物：

- NF-IMPL-001 Product-Level Implementation Blueprint。
- MVP API endpoint list。
- MVP database table family draft。
- Writing Studio interaction specification。
- model profile and provider adapter contract。

## 8.2 Phase 1 Knowledge MVP

目标：完成从导入到自动分析和知识包落库。

范围：

- Source import。
- Chapter segmentation。
- Basic extraction run。
- Extraction summary and exception review。
- Evidence binding。
- Knowledge Package commit。
- Basic Story Graph browse。

验收：用户可以导入一本书，系统自动抽取主要人物、地点、事件、伏笔和规则；用户只处理低置信度或冲突异常，并将知识包提交为可用于新书项目的 Knowledge Package。

## 8.3 Phase 2 Writing MVP

目标：完成从原创项目到单章成稿。

范围：

- Novel Project creation。
- Story Bible and chapter plan。
- Memory Package assembly。
- Prompt Pack assembly。
- Creator-facing one-click chapter generation with internal Scene/Beat orchestration。
- Critic and Humanizer loop。
- Chapter Assembly。
- Quality Gate。

验收：用户可以基于 Approved Knowledge 和自有设定生成一章可审稿章节，并查看证据链、质量报告和模型成本。

## 8.4 Phase 3 Feedback and Optimization

目标：让系统从写作过程学习。

范围：

- Human edit capture。
- Feedback Record。
- model_cost_quality dashboard。
- Prompt ranking suggestion。
- Retrieval strategy suggestion。
- Manual promotion and rollback。

验收：用户修改章节后，系统能归因修改原因，并生成可审核的策略优化建议。

## 8.5 Phase 4 Scale and Collaboration

目标：支持多项目、多角色和更长篇幅。

范围：

- Multi-project dashboard。
- Role-based permissions。
- Batch writing queue。
- Long-running manuscript state。
- Dedicated vector DB or graph DB upgrade when thresholds are met。
- Export and publication preparation。
