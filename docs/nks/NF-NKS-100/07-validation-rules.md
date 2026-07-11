# 7. Validation Rules

## 7.1 Required Evidence

以下结果必须绑定 evidence：Character、Faction、Location、Event、Conflict、Relationship、Pattern、Rule。

## 7.2 Required IDs

进入 Knowledge Package 的对象必须具有稳定 ID 或 candidate_id。

## 7.3 Referential Integrity

所有 Relationship 的 source_id 和 target_id 必须引用同一输出包中存在的对象，或引用已批准 Knowledge Base 中的对象。

## 7.4 Chapter Order Integrity

Chapter 必须保持原始顺序。缺章、重复章节和顺序异常必须进入 review_report。

## 7.5 Scene Boundary Integrity

Scene 的 text_range 不得互相重叠，且必须属于对应 Chapter 的 text_range。

## 7.6 Object Lifecycle Integrity

输出对象必须处于 Extracted、Normalized、Reviewed、Approved 或 Deprecated 状态之一。
