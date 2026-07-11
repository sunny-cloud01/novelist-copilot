# 1. Purpose and Scope

本文档定义 Novel Factory 的 Knowledge Retrieval and Memory Context 规范。

该规范负责把 Knowledge Base、Story Graph、结构化状态、向量召回、长上下文和前文摘要组织成可用于写作的 Memory Package。

本文档覆盖：

- Memory Context 对象模型。
- 召回策略和优先级。
- 动态状态覆盖静态描述的规则。
- stale context 检测。
- 长上下文使用策略。
- 生成前一致性验证。

本文档不定义向量数据库产品选型、具体 embedding 模型或 Prompt 模板正文。
