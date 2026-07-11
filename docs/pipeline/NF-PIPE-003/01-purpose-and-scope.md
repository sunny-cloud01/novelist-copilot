# 1. Purpose and Scope

本文档定义 Novel Factory 从“可生成章节”过渡到“可持续写出合理、有人味、低 AI 味小说”的写作编排流水线。

NF-PIPE-002 定义通用 AI Generation and Revision Pipeline。NF-PIPE-003 在此基础上定义更具体的小说成稿工作流：战略层负责设定、剧情、场景和节奏规划；执行层负责 Beat 级写作、检查、重写、人类化和反馈回流。

本文档覆盖：

- 双层循环写作模型。
- 设定库、Story Graph 和结构化 Memory 的检索方式。
- Style Analyzer 前置注入。
- Scene Planner 的内部 Beat/Section 拆分，以及 Creator-facing 一键章节生成入口。
- Writer 与 Critic 的局部闭环。
- Humanizer 的去 AI 味和口语化拟真任务。
- 多模型路由、Token 成本和失败降级策略。
- 玄幻、都市爽文等 genre playbook 的写作约束。
- 任务状态、输出包和反馈回流。

本文档不定义具体模型供应商合同、Prompt 模板正文、版权处理策略或最终发布渠道。

Style few-shot 和风格分析必须来自已授权、可使用或内部自有素材。系统不得要求模型直接仿写某个受版权保护作者的完整表达，只能抽象为句长、节奏、POV、修辞偏好和表达分类等可治理特征。
