# 7. MVP AI Workflow and Quality

## 7.1 Provider Adapter Boundary

MVP 必须通过 provider adapter 调用模型。

业务代码不得直接依赖具体供应商 SDK。所有模型调用必须记录：

- model_profile_id
- provider_name
- agent_role
- prompt_tokens
- completion_tokens
- latency
- retry_count
- cost_estimate

即使 MVP 只使用一个模型，也必须通过 model_profile_id 和 agent_model_assignment 调用，不得在 Agent 代码或 Prompt 中硬编码 provider_model_name。

## 7.2 MVP Agent Roles

MVP 启用以下 Agent role：

- Extraction Agent
- Normalization Agent
- Planning Agent
- Memory Agent
- Style Analyzer Agent
- Writer Agent
- Critic Agent
- Humanizer Agent
- Review Agent
- Feedback Agent

MVP 必须为上述 Agent role 创建默认 model assignment。初始 assignment 可以全部指向同一个 default model_profile。后续可以按 Agent role 替换模型：Writer 使用中文长文本模型，Critic 使用结构化审查模型，Humanizer 使用改写模型，Memory Agent 使用长上下文模型。

## 7.3 MVP Writing Quality Gates

单章成稿必须检查：

- knowledge_consistency_score
- character_consistency_score
- beat_goal_completion_score
- rhythm_match_score
- ai_flavor_score
- humanity_score
- mobile_readability_score
- originality_safety_score

默认 blocking：

- Approved Knowledge 被改写。
- Humanizer 改变剧情事实。
- ai_flavor_score 高于配置阈值。
- originality_safety_score 低于配置阈值。

## 7.4 Retry Budget

MVP 默认重试预算：

| Stage                   | Retry Budget |
| ----------------------- | ------------ |
| extraction task         | 2            |
| memory package assembly | 1            |
| chapter generation      | 2            |
| critic review           | 1            |
| humanizer pass          | 1            |
| quality gate            | 1            |

超过预算后进入 requires_review 或 blocked，不继续自动消耗模型调用。

## 7.5 Humanizer Boundary

Humanizer 只做微改写：句式、段落、机械转场、泛化表达、手机阅读节奏。

Humanizer 不得改变事实、角色关系、战力结果、伏笔状态或章节目标。

## 7.6 Model Routing Acceptance

MVP AI workflow 验收必须包含：

- default model_profile 可用。
- 每个 MVP Agent role 都有 enabled assignment。
- Provider Adapter 记录 token、latency、retry 和 cost。
- 禁用 model_profile 后 Router 不再选择该 profile。
- structured output validation 失败会消耗 retry budget。
- fallback_profile_ids 可以为空，但字段和流程必须存在。
