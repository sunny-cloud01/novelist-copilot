# 8. Quality Gates

## 8.1 Minimum Acceptance Criteria

一个 Book Knowledge Package 至少必须满足：

- Book 元数据完整。
- Chapter 顺序可恢复。
- 每个 Chapter 至少有一个 Scene 或明确的 segmentation_failure 记录。
- 核心 Character 候选可追踪。
- Event 候选可追踪。
- 所有 Relationship 通过引用完整性检查。
- review_report 无 blocking issue。

## 8.2 Blocking Issues

以下问题阻止输出包进入 Approved 状态：

- 缺少 book_id。
- 大量章节顺序不可恢复。
- 关系引用不存在对象。
- 关键对象无 evidence。
- 抽取过程改写原文语义且无记录。

## 8.3 Human Review Triggers

以下情况必须进入人工审核：

- 角色身份冲突。
- 同名角色无法自动归并。
- 关键剧情因果链断裂。
- 世界规则与事件明显冲突。
- Foreshadowing 无法判断是否回收。
- 抽取 confidence 低于后续 Schema 设定阈值。
