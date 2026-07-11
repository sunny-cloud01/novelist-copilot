# 1. Purpose and Scope

本文档定义 Novel Factory 的 Feedback Knowledge。

Feedback Knowledge 将人工修改、AI Review、Critic 报告、Humanizer 改动、读者信号、模型成本和质量结果转化为可治理、可检索、可回放的知识对象。

本文档的目标是让写作流水线不只记录结果，而能从每次生成、审查、重写和人工编辑中学习，反向优化 Prompt、Model Router、Retrieval、Style Profile、Expression Taxonomy、Genre Playbook 和 Rule。

本文档覆盖：

- Feedback Record 对象模型。
- Human Edit、Review Signal、Reader Signal 和 Cost Quality Signal。
- 反馈分类、严重级别和目标对象。
- 反馈如何进入学习目标和治理流程。
- 反馈验证、回滚和边界。

本文档不定义具体推荐算法、在线学习模型或读者平台埋点实现。
