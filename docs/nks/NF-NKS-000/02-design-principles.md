# 2. Design Principles

## 2.1 Single Source of Truth

一个概念只能有一个官方名称。正确：Event。禁止：Action、Occurrence、Story Event 混用。

## 2.2 Atomic Meaning

每个对象只表达一种语义。Character 只表示角色，不得同时表示人物、势力和身份的混合对象。

## 2.3 Referenceable

所有可进入知识库、Story Graph 或数据库的对象必须具有唯一 ID。

## 2.4 AI First

术语定义必须清晰、稳定、可机器解析，并可被 RAG、Agent 和 Prompt Engine 引用。

## 2.5 Separation of Knowledge and Instance

知识模型与具体实例必须分离。Character 是领域对象类型，`CHR-000001` 是某个具体角色实例。

## 2.6 Cross-Document Stability

一旦对象名称进入 Approved 或 Frozen 文档，其他文档不得随意改名。需要改名时必须创建 Change Request。
