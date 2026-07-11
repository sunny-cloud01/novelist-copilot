# 4. Extraction Stages

## 4.1 Scene Segmentation

Scene Segmentation 将 Chapter 切分为 Scene candidate。

切分依据：

- 时间变化。
- 地点变化。
- 参与角色变化。
- 叙事目标变化。
- 冲突状态变化。

输出：scene_candidates、scene_boundaries 和 segmentation_confidence。

## 4.2 Entity Extraction

Entity Extraction 抽取 Character、Faction、Location、Worldview、Power System、Artifact、Resource 和其他 NF-NKS 对象候选。

每个候选对象必须绑定 evidence_refs。

## 4.3 Event and Relationship Extraction

Event Extraction 抽取 Event、Conflict、Hook、Reward 和 Climax。

Relationship Extraction 基于已存在对象创建 Story Graph Relationship candidate。

禁止创建指向不存在对象的关系。

## 4.4 Pattern, Rhythm and Rule Extraction

Pipeline 必须抽取：

- Pattern candidate。
- Rhythm Profile。
- Rule candidate。
- Consistency constraint。
- Contradiction candidate。

这些输出分别引用 NF-NKS-240、NF-NKS-250 和 NF-NKS-270。

## 4.5 Evidence Binding

所有对象、关系、Pattern、Rhythm Profile、Rule 和抽取判断必须绑定 Evidence。

Evidence 至少包含：

- source_type
- source_id
- text_range
- source_text_excerpt_ref
- extraction_method
- confidence

## 4.6 Object Normalization

Object Normalization 负责：

- alias 合并。
- object_id 分配。
- duplicate candidate 归并。
- unresolved object 标记。
- lifecycle_status 初始化。

不确定对象不得直接进入 Approved 状态。
