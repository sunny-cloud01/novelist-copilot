---
document_id: NF-NKS-100
title: Book Knowledge Extraction Specification
version: 1.0.0
status: Draft
category: Novel Knowledge Specification
owner: Novel Factory Knowledge Engineering Team
created: 2026-07-09
updated: 2026-07-09
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-200
  - NF-NKS-210
  - NF-NKS-220
  - NF-NKS-230
  - NF-NKS-240
  - NF-NKS-250
  - NF-NKS-260
  - NF-NKS-270
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-200.md
  - docs/nks/NF-NKS-210.md
  - docs/nks/NF-NKS-220.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-240.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-260.md
  - docs/nks/NF-NKS-270.md
---

# NF-NKS-100

# Book Knowledge Extraction Specification

# 1. Purpose and Scope

本文档定义 Novel Factory 的 Book Knowledge Extraction 标准流程。

Book Knowledge Extraction 是将小说文本从 Book、Chapter、Scene 等来源边界中抽取为结构化知识对象、Story Graph 节点、关系、规则、节奏画像和可复用创作资产的过程。

本文档必须引用 NF-NKS-000 中的对象定义，不得重新定义 Character、Event、Pattern、Rhythm Profile、Rule 或其他领域对象。

## 1.1 Scope

本文档覆盖输入文本与元数据要求、拆书抽取流水线、章节级抽取规则、场景级抽取规则、领域对象抽取规则、Story Graph 关系抽取规则、节奏与爽点抽取规则、输出包结构、证据与可追踪性要求、质量门禁与错误处理。

本文档不覆盖 NF-NKS-000 已定义对象的权威语义、数据库字段类型和索引、API 请求与响应结构、Prompt 模板正文或具体 Agent 工具调用实现。

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

# 3. Input Requirements

## 3.1 Book Input

Book 输入必须包含 book_id、title、author、platform、genre、tags、completion_status、source 和 chapters。

## 3.2 Chapter Input

Chapter 输入必须包含 chapter_id、book_id、chapter_index、title、raw_text 和 text_length。

## 3.3 Optional Metadata

可选元数据包括 platform_category、reader_rating、publish_time、author_notes、volume_name 和 source_url。

## 3.4 Text Preprocessing Requirement

抽取前必须完成基础预处理：

- 清理广告、页眉、页脚和重复水印。
- 保留章节标题。
- 保留原始段落顺序。
- 标记疑似 OCR 错误。
- 生成稳定 text_range。

# 4. Extraction Pipeline

标准抽取流水线：

```text
Step 1: Input Normalization
↓
Step 2: Chapter Segmentation
↓
Step 3: Scene Segmentation
↓
Step 4: Entity Extraction
↓
Step 5: Event Extraction
↓
Step 6: Relationship Extraction
↓
Step 7: Pattern Extraction
↓
Step 8: Rhythm Extraction
↓
Step 9: Rule and Consistency Extraction
↓
Step 10: Evidence Binding
↓
Step 11: Object Normalization
↓
Step 12: Quality Review
↓
Step 13: Knowledge Package Export
```

流水线必须支持 Book 级、Chapter 级和 Scene 级增量执行。

# 5. Stage Specifications

## 5.1 Input Normalization

目标：将来源文本转为稳定、可追踪的输入结构。

输出：normalized_book、normalized_chapters、preprocessing_report。

要求：不得改写正文语义，必须保留原始文本引用，所有清理动作必须可记录。

## 5.2 Chapter Segmentation

目标：确认章节边界并生成 Chapter 对象候选。

输出：chapter_candidates、chapter_order、missing_chapter_report。

要求：chapter_index 必须连续。章节标题缺失时允许使用生成标题，但必须标记 generated_title。

## 5.3 Scene Segmentation

目标：将 Chapter 切分为 Scene 候选。

切分依据：时间变化、地点变化、参与角色变化、叙事目标变化、冲突状态变化。

输出：scene_candidates、scene_boundaries、segmentation_confidence。

## 5.4 Entity Extraction

目标：抽取 Character、Faction、Location、Worldview、Power System、Artifact、Resource 等对象候选。

要求：每个对象必须绑定 evidence。Alias 必须归一化到 Canonical Name 或候选对象。不确定对象必须进入 candidate 状态。

输出：entity_candidates、alias_map、unresolved_entities。

## 5.5 Event Extraction

目标：抽取推动故事状态变化的 Event。

每个 Event 必须尽量回答 who、where、why、action、result、consequence。

输出：event_candidates、conflict_candidates、consequence_map。

## 5.6 Relationship Extraction

目标：基于已抽取对象建立 Story Graph Relationship。

要求：source_id 必须存在，target_id 必须存在，relation_type 必须来自受控词表，evidence 必须可追踪。

输出：relationship_candidates、relation_confidence_report。

## 5.7 Pattern Extraction

目标：识别可复用叙事套路或剧情流程。

示例 Pattern：废柴逆袭、拍卖会、秘境争夺、宗门考核、身份揭示、反杀打脸。

输出：pattern_candidates、pattern_steps、replaceable_slots。

## 5.8 Rhythm Extraction

目标：生成章节或场景的 Rhythm Profile。

统计指标：climax_index、conflict_index、dialogue_ratio、description_ratio、battle_ratio、information_density、suspense_index、reward_count。

输出：rhythm_profiles、chapter_rhythm_summary。

## 5.9 Rule and Consistency Extraction

目标：抽取影响世界运行、角色能力、时间线和生成约束的 Rule。

输出：rule_candidates、consistency_constraints、contradiction_candidates。

## 5.10 Evidence Binding

目标：将对象、关系、Pattern、Rhythm Profile 和 Rule 绑定到原文证据。

每条 evidence 必须包含 source_type、source_id、text_range、source_text_excerpt、confidence。

## 5.11 Object Normalization

目标：完成命名归一化、ID 分配、候选合并和对象生命周期更新。

输出：normalized_objects、merged_objects、duplicate_report、unresolved_report。

## 5.12 Quality Review

目标：在进入正式 Knowledge Base 前进行质量门禁。

输出：review_report、accepted_objects、rejected_objects、objects_requiring_human_review。

## 5.13 Knowledge Package Export

目标：导出可供数据库、Story Graph、RAG、Agent 和 Prompt Engine 使用的知识包。

输出：knowledge_package、graph_package、extraction_report、quality_report。

# 6. Output Package

## 6.1 Package Structure

Book Knowledge Extraction 的标准输出包包含：

```text
BookKnowledgePackage
├── metadata
├── source_book
├── chapters
├── scenes
├── objects
├── relationships
├── rhythm_profiles
├── patterns
├── rules
├── evidence
├── review_report
└── export_manifest
```

## 6.2 Metadata

metadata 必须包含 package_id、document_id、book_id、extraction_version、extraction_time、extractor 和 status。

## 6.3 Objects

objects 必须按 NF-NKS-000 对象类型组织。

允许对象类型包括 Book、Chapter、Scene、Character、Faction、Location、Worldview、Power System、Artifact、Resource、Event、Conflict、Emotion、Reward、Hook、Climax、Foreshadowing、Pattern、Rhythm Profile、Asset、Rule、Prompt Template。

## 6.4 Relationships

relationships 必须引用 NF-NKS-000 的 Relationship Model。

每条关系必须包含 source_id、relation_type、target_id、confidence、evidence_id。

## 6.5 Export Manifest

export_manifest 必须记录 exported_files、object_count、relationship_count、evidence_count、validation_status 和 review_status。

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

# 9. Error Handling

## 9.1 Error Categories

抽取错误分类：input_error、segmentation_error、extraction_error、normalization_error、relationship_error、validation_error、review_error。

## 9.2 Error Record

错误记录必须包含 error_id、error_category、source_id、severity、message、recovery_action、created_at。

## 9.3 Recovery Requirements

系统必须支持：

- 跳过单个失败 Scene 并继续处理后续 Scene。
- 标记失败章节并进入人工审核。
- 回滚单次抽取产生的候选对象。
- 在后续章节中补全缺失别名和关系。

# 10. Boundaries, References, and Change Log

## 10.1 Boundary Rules

NF-NKS-100 只定义抽取流程、输出结构、验证规则和质量门禁。

NF-NKS-100 不定义对象权威语义。对象定义必须引用 NF-NKS-000。

数据库字段类型、索引、迁移和物理存储由 NF-DBS 文档定义。

Agent 角色、工具调用、重试策略和任务编排由 NF-AGENT 文档定义。

Prompt 模板正文、变量结构和评估样例由 NF-PROMPT 文档定义。

## 10.2 References

- NFES-000
- NF-PRD-001
- NF-NKS-000
- NF-NKS-001
- NF-NKS-200
- NF-NKS-210
- NF-NKS-220
- NF-NKS-230
- NF-NKS-240
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270

## 10.3 Approval

Document Status: Draft

Next Review: NF-NKS-100 Review

Next Document: NF-ARCH-001 System Architecture or NF-DBS-001 Knowledge Database Specification

## 10.4 Change Log

| Version | Date       | Author                                   | Change                                               |
| ------- | ---------- | ---------------------------------------- | ---------------------------------------------------- |
| 1.0.0   | 2026-07-09 | Novel Factory Knowledge Engineering Team | Initial Draft for book knowledge extraction process. |
