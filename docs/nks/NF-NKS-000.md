---
document_id: NF-NKS-000
title: Novel Knowledge Glossary and Domain Model
version: 2.0.0
status: Draft
category: Novel Knowledge Specification
owner: Novel Factory Knowledge Engineering Team
created: 2026-07-09
updated: 2026-07-09
dependencies:
  - NFES-000
  - NF-PRD-001
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
---

# NF-NKS-000

# Novel Knowledge Glossary and Domain Model

# 1. Purpose and Scope

本文档定义 Novel Factory 中所有核心术语、领域对象及其边界。

所有后续文档，包括 Schema、数据库、Story Graph、Agent、Prompt、RAG 和知识抽取规范，必须引用本规范，不允许重新定义相同概念。

## 1.1 Scope

本文档覆盖 Novel Factory 核心术语、Novel Knowledge Engineering 领域对象、Story Graph 基础节点类型、Story Graph 基础关系类型、对象命名规则、对象 ID 规则和跨文档引用边界。

本文档不覆盖具体数据库字段类型、API 请求与响应结构、Prompt 模板正文、Agent 执行流程或单本小说的实际抽取结果。

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

# 3. Naming and ID Conventions

## 3.1 Canonical Name

每个领域对象必须有唯一英文 Canonical Name。

| Chinese Name | Canonical Name        |
| ------------ | --------------------- |
| 角色         | Character             |
| 事件         | Event                 |
| 势力         | Faction               |
| 地点         | Location              |
| 伏笔         | Foreshadowing         |
| 爽点         | Reward                |
| 表达分类     | Expression Type       |
| 角色口吻     | Speaker Voice Profile |
| 风格约束     | Style Constraint      |

## 3.2 Display Name

Display Name 用于界面、人类阅读和本地化展示，不得替代 Canonical Name。

## 3.3 Alias

Alias 只用于检索、兼容旧数据或用户输入归一化。Alias 不得在正式 Schema、API 或 Prompt 参数中作为主字段使用。

## 3.4 ID Convention

推荐格式：

```text
{PREFIX}-{NUMBER}
```

Prefix 使用 3 到 6 位大写英文字母。Number 使用 6 位数字，不足补零。ID 一经发布不得复用。

| Object Type     | Prefix | Example    |
| --------------- | ------ | ---------- |
| Book            | BOK    | BOK-000001 |
| Chapter         | CHP    | CHP-000001 |
| Scene           | SCN    | SCN-000001 |
| Character       | CHR    | CHR-000001 |
| Faction         | FAC    | FAC-000001 |
| Location        | LOC    | LOC-000001 |
| Event           | EVT    | EVT-000001 |
| Pattern         | PAT    | PAT-000001 |
| Artifact        | ART    | ART-000001 |
| Foreshadowing   | FSH    | FSH-000001 |
| Rule            | RUL    | RUL-000001 |
| Prompt Template | PRM    | PRM-000001 |
| Expression Type | EXP    | EXP-000001 |
| Voice Profile   | VOI    | VOI-000001 |

# 4. Core Glossary

## 4.1 Novel Factory

Novel Factory 是一套以 AI 为核心的网文知识工程与内容生产系统。

## 4.2 Novel Knowledge Engineering

Novel Knowledge Engineering 是将小说文本拆解为结构化知识、关系、规则、节奏和可复用创作资产的工程方法。

## 4.3 Book Analysis

Book Analysis 是将一本小说拆解为章节、场景、事件、人物、世界观、节奏、套路和素材的过程。

## 4.4 Knowledge Base

Knowledge Base 是按知识类型组织的结构化知识集合，而不是按单本小说简单归档的文本集合。

## 4.5 Story Graph

Story Graph 是描述角色、地点、事件、势力、物品、规则、伏笔及其关系的图结构。

## 4.6 Prompt Engine

Prompt Engine 是根据知识、套路、节奏和生成目标动态组合 Prompt 的系统模块。

## 4.7 Consistency Engine

Consistency Engine 是检查长篇小说内部一致性的系统模块。

## 4.8 Feedback Loop

Feedback Loop 是将评分、错误、人工修改和读者反馈回流到知识库与 Prompt 系统的优化机制。

## 4.9 Expression Taxonomy

Expression Taxonomy 是统一话术、表达功能、对白语气、叙述口吻、题材表达和反 AI 味风险的受控分类体系。

## 4.10 Speaker Voice Profile

Speaker Voice Profile 是角色、角色类型或人设 archetype 的稳定说话方式约束，用于控制对白立场、语气、句式和情绪外泄程度。

## 4.11 Style Constraint

Style Constraint 是对生成文本的表达风格要求，例如 fast_paced、ancient_formal、plain_direct 或 restrained_emotional。

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

# 6. Story Graph Relationships

## 6.1 Relationship Definition

Relationship 表示两个节点之间的有向语义关系。

最小语义字段：source_id、relation_type、target_id、confidence、evidence。

## 6.2 Base Relationship Types

| Source        | Relation        | Target    |
| ------------- | --------------- | --------- |
| Character     | belongs_to      | Faction   |
| Character     | owns            | Artifact  |
| Event         | occurs_at       | Location  |
| Character     | hates           | Character |
| Event         | causes          | Event     |
| Foreshadowing | resolves_at     | Chapter   |
| Character     | participates_in | Event     |
| Faction       | controls        | Location  |
| Rule          | constrains      | Character |
| Pattern       | contains        | Event     |

## 6.3 Relationship Constraints

关系必须满足：

- source_id 和 target_id 必须引用已存在对象。
- relation_type 必须来自受控词表。
- evidence 必须能追溯到文本、人工标注或系统推理记录。
- confidence 必须在后续 Schema 中定义取值范围。

# 7. Object Lifecycle

知识对象生命周期：

```text
Extracted
↓
Normalized
↓
Reviewed
↓
Approved
↓
Deprecated
```

## 7.1 Extracted

对象由人工、规则、OCR、LLM 或 Agent 从来源文本中抽取。

## 7.2 Normalized

对象完成命名归一化、ID 分配和基础字段整理。

## 7.3 Reviewed

对象等待人工或高级 Agent 审核。

## 7.4 Approved

对象可以进入正式 Knowledge Base、Story Graph 或生成流程。

## 7.5 Deprecated

对象保留历史记录，但不再用于新生成任务。

# 8. Boundary Rules

## 8.1 NF-NKS-000 Boundary

NF-NKS-000 只定义术语和领域对象。

NF-NKS-000 不定义具体抽取流程、数据库类型、API 字段格式或 Prompt 模板正文。

## 8.2 NF-NKS-100 Boundary

NF-NKS-100 应引用本文档中的对象定义，并定义如何从 Book、Chapter 和 Scene 中抽取这些对象。

## 8.3 Database Boundary

数据库 Schema 必须引用本文档对象，但字段类型、索引、迁移和约束由 NF-DBS 文档定义。

## 8.4 Prompt Boundary

Prompt 文档必须引用本文档对象，但不得在 Prompt 文档中重新定义 Character、Event、Pattern 或 Rhythm Profile。

# 9. References, Approval, and Change Log

## 9.1 References

- NFES-000
- NF-PRD-001

## 9.2 Approval

Document Status: Draft

Next Review: NF-NKS-000 Review

Next Document: NF-NKS-100 Book Knowledge Extraction Specification

## 9.3 Change Log

| Version | Date       | Author                                   | Change                                                     |
| ------- | ---------- | ---------------------------------------- | ---------------------------------------------------------- |
| 2.0.0   | 2026-07-09 | Novel Factory Knowledge Engineering Team | Created NFES-compliant glossary and domain model baseline. |
