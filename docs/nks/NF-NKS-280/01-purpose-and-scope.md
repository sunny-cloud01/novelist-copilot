# 1. Purpose and Scope

本文档定义 Novel Factory 的 Speech Expression and Style Taxonomy。

Speech Expression and Style Taxonomy 是统一话术、表达功能、对白语气、叙述口吻、题材表达和反 AI 味控制的权威分类规范。

该规范解决以下问题：

- Asset Library 只能保存素材实例，不能独立承担表达分类治理。
- Prompt Engine 需要稳定分类来选择表达策略，而不是随机拼接片段。
- Character Prompt 需要角色口吻约束，而不是只依赖自由文本描述。
- Review Service 需要识别重复句式、泛化表达和 AI 味风险。
- Feedback Loop 需要把人工修改反向归类到可学习的表达类型。

本文档覆盖：

- 表达分类模型。
- 对白与角色口吻分类。
- 叙述、题材和场景表达分类。
- 风格约束和反 AI 味分类。
- 与 Asset、Prompt、Rule、Rhythm 和 Review 的引用边界。

本文档不保存大段原文，不定义具体 Prompt 模板正文，不规定模型供应商参数，也不替代 NF-NKS-260 的 Asset 实例管理。
