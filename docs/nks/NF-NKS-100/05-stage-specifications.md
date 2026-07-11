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
