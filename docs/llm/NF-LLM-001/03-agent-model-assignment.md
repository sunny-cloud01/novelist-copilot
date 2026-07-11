# 3. Agent Model Assignment

## 3.1 Assignment Purpose

`agent_model_assignment` 定义某类 Agent 在某类任务中优先使用哪些模型。

一个 Agent role 可以有多个 assignment，用于区分：

- task_type。
- genre。
- structured 或 text 输出。
- normal 或 high_quality 模式。
- 成本优先或质量优先。

## 3.2 Assignment Fields

必须包含：

- assignment_id
- agent_role
- task_type
- output_mode: text, structured, embedding, rerank
- primary_model_profile_id
- fallback_model_profile_ids
- selection_policy
- max_retry
- max_cost
- enabled
- created_at
- updated_at

可选包含：

- genre_scope
- quality_floor
- latency_target_ms
- context_window_required
- temperature_override
- prompt_pack_scope

## 3.3 Recommended Agent Mapping

MVP 后的推荐映射：

| Agent Role           | Preferred Model Capability               | Notes                                  |
| -------------------- | ---------------------------------------- | -------------------------------------- |
| Ingestion Agent      | low_cost, structured_json                | 文件清洗、章节识别不应使用最贵模型     |
| Extraction Agent     | structured_json, long_context, reasoning | 需要稳定抽取对象、证据和关系           |
| Normalization Agent  | structured_json, reasoning               | 别名合并和冲突判断需要一致性           |
| Graph Agent          | structured_json, reasoning               | 图谱边必须指向已存在对象               |
| Planning Agent       | reasoning, structured_json, long_context | 生成章方向、世界观和剧情结构           |
| Scene Planning Agent | reasoning, structured_json               | 内部 Scene/Beat 拆分                   |
| Style Analyzer Agent | long_context, structured_json            | 输出抽象风格特征，不仿写作者           |
| Memory Agent         | long_context, reasoning                  | 动态状态和规则召回                     |
| Writer Agent         | cn_webnovel, long_context, low_cost      | 一键章节主草稿，重视中文网文表达和成本 |
| Critic Agent         | critique, structured_json, reasoning     | 输出问题位置、严重级别和修复建议       |
| Humanizer Agent      | rewriting, cn_webnovel                   | 去机械感、人味化，不改变事实           |
| Review Agent         | critique, structured_json                | 质量门禁和阻塞项判断                   |
| Feedback Agent       | structured_json, reasoning               | 生成策略建议，不自动改配置             |

## 3.4 Assignment Resolution

Model Router 解析顺序：

1. exact match: agent_role + task_type + output_mode + genre_scope
2. agent_role + task_type + output_mode
3. agent_role + output_mode
4. workspace default profile
5. system default profile

找不到 assignment 时，任务不得直接调用 provider，必须进入 configuration_error 或使用显式配置的 system default profile。
