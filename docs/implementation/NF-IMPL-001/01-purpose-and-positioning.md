# 1. Purpose and Positioning

本文档定义 Novel Factory 的产品级实现蓝图。

NF-PRD-001 定义产品愿景，NF-ARCH-001 和 NF-ARCH-002 定义系统架构与后端技术架构，NF-PIPE-003 定义写作编排流水线。NF-IMPL-001 在这些规范之上，回答产品落地时如何从用户开始使用，一直走到形成自己的小说，并保证过程可追踪、可审核、可回滚、不过度消耗人力。

## 1.1 Implementation Goal

产品级实现目标：

- 支持用户导入作品或自有素材。
- 支持自动拆书和知识结构化。
- 支持人审形成 Approved Knowledge Base。
- 支持创建原创小说项目、设定目标题材和写作策略。
- 支持规划卷纲、章纲、Scene 和 Beat。
- 支持按 Beat 生成、检查、重写、人类化和组章。
- 支持质量门禁、证据追踪和反馈学习。
- 支持用较少人力维护高质量长篇写作流程。

## 1.2 Product Boundary

NF-IMPL-001 覆盖产品实现蓝图、用户路径、服务协作、运行态、数据追踪、人力与成本控制、MVP 阶段和演进路线。

本文档不定义具体 UI 视觉稿、数据库字段 DDL、完整 API schema、模型供应商商业配置或发布平台接入。

## 1.3 Implementation Principle

实现必须遵守：

- Specification first: 所有对象和流程必须引用既有规范。
- Human decision at key points: 人工处理关键审核和审美选择，不承担批量机械修改。
- Trace by default: 每次导入、抽取、生成、审查、编辑和反馈都必须有 trace_id 或等价引用链。
- Progressive automation: 第一阶段先让流程可控，再逐步自动化低风险环节。
- Cost aware: 每个模型调用、重写次数、人工编辑距离和质量收益都必须可统计。
