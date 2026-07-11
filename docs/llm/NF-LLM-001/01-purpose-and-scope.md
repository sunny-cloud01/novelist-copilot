# 1. Purpose and Scope

本文档定义 Novel Factory 的大模型接入、Provider Adapter、Model Profile、Agent Model Assignment、模型路由、降级、成本记录和 MVP 演进策略。

Novel Factory 的中间 Pipeline 会调度多个 Agent 分工完成自动拆书、知识抽取、归一化、图谱构建、Story Bible 生成、一键章节生成、Critic、Humanizer、Quality Gate 和 Feedback。MVP 阶段可以只接入一个模型跑通闭环，但架构必须允许不同 Agent 配置不同模型。

## 1.1 Goals

目标：

- 业务代码不直接依赖具体模型供应商 SDK。
- Agent 不硬编码模型名称。
- MVP 可以使用 single default model profile。
- 后续可以按 Agent role、task_type、genre、成本、质量和上下文长度切换模型。
- 所有模型调用都可追踪、可计费、可回放、可降级。

## 1.2 Non-Goals

本文档不定义：

- 具体供应商商业合同。
- API key 或密钥内容。
- Prompt 正文。
- 模型 benchmark 结果。
- 线上生产配额采购策略。

## 1.3 Core Principle

模型选择必须由配置和路由策略决定，而不是散落在 Agent 代码、Prompt 文本或前端参数中。

```text
Agent Task
↓
Agent Model Assignment
↓
Model Router
↓
Model Profile
↓
Provider Adapter
↓
Provider API
```
