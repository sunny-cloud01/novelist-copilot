# 1. Purpose and Scope

本文档定义 Novel Factory 的 Story Graph 模型规范。

Story Graph 用于表达 Character、Faction、Location、Event、Artifact、Rule、Foreshadowing、Pattern、Reward 和 Hook 等对象之间的结构化关系，使系统能够进行一致性检查、上下文召回、剧情规划和生成约束。

本文档覆盖：

- 图节点语义
- 图边语义
- 关系方向和证据要求
- 图快照
- 查询边界

本文档不覆盖数据库物理实现、图数据库产品选型、API 查询语法或具体 Prompt 模板。
