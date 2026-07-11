# 5. Domain Object Model

## 5.1 Book

Book 表示一部用于拆书、分析或生成参考的小说作品。Book 是来源对象，Knowledge Base 是抽取后的结构化知识集合。

最小语义字段：id、title、author、platform、genre、tags、word_count、completion_status、source。

## 5.2 Chapter

Chapter 表示 Book 中的章节单位，是拆书分析的基本文本边界之一。

最小语义字段：id、book_id、chapter_index、title、text_range。

## 5.3 Scene

Scene 表示 Chapter 内具有相对完整时间、地点、参与者和事件目标的叙事片段。一个 Chapter 可以包含多个 Scene。

最小语义字段：id、chapter_id、location_id、participants、primary_event_id。

## 5.4 Character

Character 表示小说中的角色。Character 可以属于 Faction，可以拥有 Artifact，可以参与 Event。

Character 不得用于表示势力、身份标签或抽象人设模板。

最小语义字段：id、name、aliases、role_type、motivation、personality_traits、capability_profile、growth_path。

## 5.5 Faction

Faction 表示具有组织结构、利益目标和成员关系的势力。

示例：宗门、皇朝、家族、学院、魔教、商会。

最小语义字段：id、name、faction_type、hierarchy、resources、relationship_profile。

## 5.6 Location

Location 表示事件发生或角色活动的空间节点。

示例：新手村、秘境、皇城、禁地、战场、拍卖会。

最小语义字段：id、name、location_type、parent_location_id、rules、resources。

## 5.7 Worldview

Worldview 表示作品或题材的世界观规则集合。Worldview 不等同于 Location。

最小语义字段：id、genre、core_rules、power_system_id、social_structure、resource_rules。

## 5.8 Power System

Power System 表示力量、修炼、等级或能力成长体系。

示例：修仙境界、高武等级、异能等级、科技文明等级。

最小语义字段：id、name、level_sequence、advancement_rules、constraints。

## 5.9 Artifact

Artifact 表示对剧情、战斗、身份或资源产生影响的重要物品。

示例：法宝、神器、令牌、秘籍、装备、特殊资源。

最小语义字段：id、name、artifact_type、owner_character_id、capability、uniqueness_rule。

## 5.10 Resource

Resource 表示可被角色、势力或世界规则消耗、争夺或分配的资源。

最小语义字段：id、name、resource_type、scarcity、usage_rule。

## 5.11 Event

Event 表示推动故事状态变化的叙事事件。Event 必须能够回答：谁、在何处、因为什么、做了什么、导致什么变化。

最小语义字段：id、event_type、participants、location_id、cause、action、result、consequence。

## 5.12 Conflict

Conflict 表示角色、势力、规则或目标之间的冲突关系。Conflict 可以驱动 Event，也可以由 Event 升级或解决。

最小语义字段：id、conflict_type、parties、objective、pressure、resolution_state。

## 5.13 Emotion

Emotion 表示场景或角色在叙事中的情绪状态，用于节奏分析、读者体验建模和生成控制。

最小语义字段：id、subject_id、emotion_type、intensity、trigger_event_id。

## 5.14 Reward

Reward 表示读者体验中的爽点、满足感或正反馈节点。Reward 不等同于物质奖励。

最小语义字段：id、reward_type、trigger_event_id、beneficiary_character_id、reader_effect。

## 5.15 Hook

Hook 表示用于驱动继续阅读的悬念、问题、威胁或未完成承诺。

最小语义字段：id、hook_type、open_question、introduced_at、expected_resolution_range。

## 5.16 Climax

Climax 表示章节、场景、卷或剧情段落中的强峰值事件。Climax 必须与 Conflict、Reward 或 Hook 至少一种对象存在关系。

最小语义字段：id、climax_type、event_id、intensity、narrative_scope。

## 5.17 Foreshadowing

Foreshadowing 表示伏笔，必须记录埋设位置、承诺内容、回收位置和回收状态。

最小语义字段：id、seed_location、promise、payoff_location、status。

## 5.18 Pattern

Pattern 表示可复用的叙事套路或剧情流程。Pattern 必须支持参数化、组合、替换角色、替换地点和替换目标。

最小语义字段：id、name、pattern_type、steps、required_roles、replaceable_slots。

## 5.19 Rhythm Profile

Rhythm Profile 表示章节或剧情段落的节奏画像。

最小语义字段：id、target_id、climax_index、conflict_index、dialogue_ratio、description_ratio、battle_ratio、information_density、suspense_index、reward_count。

## 5.20 Asset

Asset 表示最小创作素材单位。

示例：动作、心理、环境、天气、物品、台词片段。

最小语义字段：id、asset_type、content、applicable_context、expression_type_refs、constraints。

## 5.21 Expression Type

Expression Type 表示统一话术、表达功能、对白语气、叙述口吻或反 AI 味风险的可复用分类。Expression Type 是分类和约束，不等同于具体素材文本。

最小语义字段：id、canonical_name、expression_domain、function_tags、genre_scope、style_scope、risk_tags、example_asset_refs。

## 5.22 Speaker Voice Profile

Speaker Voice Profile 表示某个角色、角色类型或 archetype 的稳定口吻约束。

最小语义字段：id、target_type、target_id、tone_tags、diction_level、sentence_shape、directness、preferred_expression_type_refs、forbidden_expression_type_refs。

## 5.23 Rule

Rule 表示约束故事一致性、世界运行或生成行为的规则。

示例：境界不能倒退、法宝唯一、人物不能瞬移、时间线必须连续、已死亡角色不能再次出现。

最小语义字段：id、rule_type、statement、scope、severity、validation_method。

## 5.24 Prompt Template

Prompt Template 表示可参数化的 Prompt 模板。Prompt Template 不等同于一次实际 Prompt。

最小语义字段：id、name、template_type、parameters、constraints、evaluation_metric。
