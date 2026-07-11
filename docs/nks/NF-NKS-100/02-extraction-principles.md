# 2. Extraction Principles

## 2.1 Evidence First

所有抽取结果必须保留证据来源。证据来源至少包含 book_id、chapter_id、scene_id 或 text_range、source_text_excerpt 和 extraction_method。

## 2.2 Object Before Relationship

必须先抽取并归一化对象，再建立对象之间的关系。禁止创建指向不存在对象的 Story Graph Relationship。

## 2.3 Stable Identity

同一实体在不同章节中重复出现时，必须归并到同一稳定 ID。当身份不确定时，必须创建候选对象并标记 resolution_state。

## 2.4 Separation of Fact and Inference

事实抽取与推理结论必须分开记录。

示例：

- Fact：角色在第 12 章拔剑攻击对手。
- Inference：角色倾向于冲动型战斗风格。

## 2.5 Incremental Extraction

抽取流程必须支持按 Book、Chapter、Scene 增量执行，并能在后续章节中修正前序对象的别名、关系和状态。
