# 5. Configuration Lifecycle and Change Log

## 5.1 Configuration Ownership

模型配置由 Config Module 拥有。

允许操作：

- create_model_profile
- update_model_profile
- disable_model_profile
- create_agent_model_assignment
- update_agent_model_assignment
- test_model_profile
- review_model_performance

Feedback Agent 可以生成模型策略建议，但不得自动修改正式 assignment。策略建议必须进入 review 状态，并由 Creator 或 Operator 明确批准。

## 5.2 Environment Separation

不同环境必须使用独立配置：

- local
- test
- staging
- production

环境之间不得共享 provider secret。Markdown 文档、测试夹具和示例配置不得包含真实密钥。

## 5.3 Rollout Strategy

从 MVP 单模型到多模型的演进：

1. Single default model profile: 所有 Agent 走同一个 model_profile_id。
2. Split embedding/rerank: 检索类模型与生成类模型分离。
3. Split Writer/Critic: Writer 使用中文长文本模型，Critic 使用结构化审查模型。
4. Split Extraction/Planning/Humanizer: 按任务能力进一步配置。
5. Feedback-driven routing: 基于成本、质量、重试率和人工编辑距离调整 assignment。

## 5.4 Validation

每次新增或修改 model_profile / assignment 后，必须验证：

- Provider Adapter 可以连通。
- structured output 能通过 schema 校验。
- token usage 和 cost 能记录。
- fallback 能按预期触发。
- 禁用 profile 后不会被 Router 选择。

## 5.5 Change Log

| Version | Date       | Changes                                                     |
| ------- | ---------- | ----------------------------------------------------------- |
| 1.0.0   | 2026-07-11 | Initial LLM provider and agent model routing specification. |
