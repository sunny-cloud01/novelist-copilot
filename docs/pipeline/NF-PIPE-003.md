---
document_id: NF-PIPE-003
title: Novel Writing Orchestration and Humanization Pipeline
version: 1.0.0
status: Draft
category: Pipeline Specification
owner: Novel Factory Writing Pipeline Team
created: 2026-07-10
updated: 2026-07-10
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
  - NF-NKS-280
  - NF-NKS-290
  - NF-RAG-001
  - NF-ARCH-001
  - NF-ARCH-002
  - NF-DBS-002
  - NF-PIPE-001
  - NF-PIPE-002
  - NF-AGENT-001
  - NF-PROMPT-001
  - NF-PROMPT-002
  - NF-QA-001
  - NF-LLM-001
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
  - docs/nks/NF-NKS-280.md
  - docs/nks/NF-NKS-290.md
  - docs/rag/NF-RAG-001.md
  - docs/architecture/NF-ARCH-001.md
  - docs/architecture/NF-ARCH-002.md
  - docs/database/NF-DBS-002.md
  - docs/pipeline/NF-PIPE-001.md
  - docs/pipeline/NF-PIPE-002.md
  - docs/agents/NF-AGENT-001.md
  - docs/prompts/NF-PROMPT-001.md
  - docs/prompts/NF-PROMPT-002.md
  - docs/quality/NF-QA-001.md
  - docs/llm/NF-LLM-001.md
---

# NF-PIPE-003

# Novel Writing Orchestration and Humanization Pipeline

# 1. Purpose and Scope

本文档定义 Novel Factory 从“可生成章节”过渡到“可持续写出合理、有人味、低 AI 味小说”的写作编排流水线。

NF-PIPE-002 定义通用 AI Generation and Revision Pipeline。NF-PIPE-003 在此基础上定义更具体的小说成稿工作流：战略层负责设定、剧情、场景和节奏规划；执行层负责 Beat 级写作、检查、重写、人类化和反馈回流。

本文档覆盖：

- 双层循环写作模型。
- 设定库、Story Graph 和结构化 Memory 的检索方式。
- Style Analyzer 前置注入。
- Scene Planner 的内部 Beat/Section 拆分，以及 Creator-facing 一键章节生成入口。
- Writer 与 Critic 的局部闭环。
- Humanizer 的去 AI 味和口语化拟真任务。
- 多模型路由、Token 成本和失败降级策略。
- 玄幻、都市爽文等 genre playbook 的写作约束。
- 任务状态、输出包和反馈回流。

本文档不定义具体模型供应商合同、Prompt 模板正文、版权处理策略或最终发布渠道。

Style few-shot 和风格分析必须来自已授权、可使用或内部自有素材。系统不得要求模型直接仿写某个受版权保护作者的完整表达，只能抽象为句长、节奏、POV、修辞偏好和表达分类等可治理特征。

# 2. Two Layer Loop Overview

## 2.1 Core Model

Novel Writing Pipeline 采用双层循环模型：

```text
Strategic Layer
├── Setting Retrieval
├── Plot Planning
├── Volume and Chapter Planning
├── Scene Planning
└── Beat Planning
        ↓
Execution Layer
├── Style Injection
├── Writer Draft Beat
├── Critic Review Beat
├── Rewrite Beat when blocked
├── Humanizer Pass
└── Chapter Assembly
        ↓
Feedback Loop
```

## 2.2 Strategic Layer

战略层决定“这一章为什么存在”。

核心输出：

- story_context_package
- volume_plan
- chapter_plan
- scene_plan
- beat_plan
- rhythm_target
- reward_curve
- hook_plan
- forbidden_changes

## 2.3 Execution Layer

执行层决定“这一段如何写出来”。

核心输出：

- style_profile
- prompt_package
- beat_draft
- critic_report
- rewrite_request
- humanized_beat
- assembled_chapter
- quality_report

## 2.4 Creator-Facing Generation Rule

产品界面默认允许 Creator 一键生成约 3000 字章节。

一键生成是交互入口，不代表系统跳过结构化编排。系统内部仍必须拆分 Scene、Beat 或 Section，并对每个内部单元执行上下文装配、生成、Critic、Rewrite 和 Humanizer 检查。

Creator 默认不逐 Beat 审核。只有当内部单元出现 blocking issue、知识冲突、原创性风险、AI 味超阈值、上下文不足或质量门禁失败时，界面才暴露局部修订入口。

默认内部流程：

```text
Chapter Direction
↓
Internal Scene and Beat Plan
↓
Writer drafts chapter sections
↓
Critic checks each section
↓
Failed: auto rewrite blocked section
↓
Passed: Humanizer pass
↓
Chapter Assembly
```

当章节类型、上下文长度或模型能力不支持稳定整章生成时，系统可以降级为分段生成，但 UI 仍应呈现为一个 chapter generation run，而不是要求 Creator 手动推进每个 Beat。

## 2.5 Approval Rule

章节只有在内部 Scene、Beat 或 Section 检查通过后，才可以进入 Chapter Assembly。

Chapter Assembly 后仍需执行章节级一致性检查、节奏检查和人工审核门禁。

# 3. Strategic Layer Planning and RAG

## 3.1 Retrieval Upgrade

写作阶段不得只依赖普通向量检索。

Context Retrieval 必须组合：

- structured JSON / relational query
- Story Graph traversal
- approved knowledge object lookup
- character state lookup
- world rule lookup
- timeline and location lookup
- vector retrieval for supporting evidence
- long context memory when available

## 3.2 Memory Package

Memory Package 至少包含：

- character_static_profile
- character_dynamic_state
- relationship_state
- inventory_and_artifact_state
- power_level_state
- location_state
- faction_state
- unresolved_conflicts
- unresolved_hooks
- prior_chapter_summary
- forbidden_changes

动态状态必须优先于早期静态描述。

示例：若第 5 章武器升级，则第 10 章生成时必须使用升级后的 weapon_state，不得只引用第 1 章初始描述。

## 3.3 Planner Outputs

Planner 必须输出：

- chapter_goal
- emotional_curve
- frustration_satisfaction_curve
- required_reward
- required_hook
- main_conflict
- reveal_plan
- protagonist_gain
- antagonist_pressure
- continuity_constraints

## 3.4 Scene Planner Outputs

Scene Planner 必须将章节拆成 Scene 和 Beat。

每个 Beat 至少包含：

- beat_id
- beat_goal
- pov_character
- active_characters
- conflict_pressure
- who_underestimates_whom
- who_is_jealous
- who_is_shocked
- reward_or_hook
- required_knowledge_refs
- rhythm_target
- estimated_word_count

## 3.5 Strategic Validation

进入 Writer 前必须检查：

- Beat 是否推进章节目标。
- Beat 是否引用有效角色和地点。
- 情绪曲线是否存在压抑、反转或释放。
- 爽点和悬念是否可追踪到 NF-NKS-230。
- 节奏目标是否可追踪到 NF-NKS-250。
- 表达风格是否可追踪到 NF-NKS-280。

# 4. Style, Memory and Context Injection

## 4.1 Style Analyzer Position

Style Analyzer 必须在 Writer 之前运行。

Style 不应只作为事后润色，而应在 Writer 动笔前注入为 System Prompt、few-shot guidance、style constraints 和 negative constraints。

## 4.2 Style Profile

Style Profile 至少包含：

- sentence_length_distribution
- paragraph_length_distribution
- verb_noun_ratio
- dialogue_ratio_target
- action_description_ratio
- interiority_ratio
- pov_purity
- metaphor_density
- diction_level
- rhythm_pattern
- preferred_expression_type_refs
- forbidden_expression_type_refs
- anti_ai_expression_refs

## 4.3 Few Shot Selection

Few-shot 选择必须满足：

- 与当前 genre_scope 兼容。
- 与当前 scene_type 兼容。
- 与 pov_character 兼容。
- 与 beat_goal 兼容。
- 来源已授权、内部自有或可安全使用。
- 片段长度受控，不得作为复制对象。

Few-shot 的目的不是复制文本，而是帮助模型理解节奏、句式、POV 和表达功能。

## 4.4 Prompt Injection Order

Writer Prompt 的上下文注入顺序：

1. hard rules and forbidden changes
2. Memory Package
3. Beat Plan
4. Style Profile
5. Expression Taxonomy constraints
6. selected few-shot guidance
7. output contract

## 4.5 Negative Constraints

Writer Prompt 必须注入：

- 禁止总结性旁白。
- 禁止段落结尾升华主题。
- 禁止泛化情绪标签替代动作。
- 禁止机械转场。
- 禁止高频 AI 词和陈词滥调。
- 禁止角色说出不符合 voice_profile 的书面语。

Negative constraints 应引用 NF-NKS-280 的 anti_ai_expression 和 NF-NKS-270 的 Rule。

# 5. Beat by Beat Writing Loop

## 5.1 Beat Granularity

默认每个 Beat 生成 300 到 800 中文字。

Beat 不应过长。过长会增加上下文漂移、总结性表达、重复句式和 AI 味风险。

## 5.2 Writer Task

Writer 只负责当前 Beat 的初稿。

Writer 输入：

- beat_plan
- memory_package
- style_profile
- prompt_package
- previous_approved_beat
- forbidden_changes
- output_contract

Writer 输出：

- beat_draft
- self_report
- used_knowledge_refs
- uncertain_points

## 5.3 Writer Restrictions

Writer 不得：

- 改写已批准设定。
- 自行解决未授权伏笔。
- 引入未审核关键设定。
- 一次性跳过多个 Beat。
- 用旁白替代角色选择。
- 在段落末尾做哲理总结。

## 5.4 Critic Pairing

Critic 在每个 Beat 后立即执行。

Critic 检查：

- beat_goal 是否完成。
- POV 是否稳定。
- 角色动机是否合理。
- 战力、物品、地点和时间线是否一致。
- 是否出现 AI 高频句式。
- 是否缺乏动作、感官或具体后果。
- 是否符合 genre playbook。

## 5.5 Rewrite Rule

Critic 未通过时，不得直接进入下一 Beat。

Rewrite Request 必须包含：

- failed_check_ids
- severity
- exact_text_refs
- required_changes
- forbidden_changes
- retry_budget

同一 Beat 自动重写默认最多 2 次。超过上限进入人工审核或 Planner 回退。

## 5.6 Chapter Assembly

所有 Beat 通过后，Chapter Assembly 负责：

- 合并 Beat。
- 消除硬断裂。
- 保持手机阅读段落节奏。
- 检查章节开头、高潮和结尾。
- 生成 chapter_quality_report。

Chapter Assembly 不得大规模改写已通过 Beat。

# 6. Critic, Humanizer and Quality Gates

## 6.1 Critic Quality Gates

Critic 必须输出结构化报告。

检查项：

- knowledge_consistency
- character_consistency
- memory_consistency
- plot_progress
- beat_goal_completion
- pov_purity
- rhythm_match
- reward_delivery
- hook_integrity
- expression_quality
- ai_flavor_signal
- genre_fit

任何 blocking issue 必须打回 Writer。

## 6.2 AI Flavor Rules

必须检查以下高风险模式：

- however_style_transition
- empty_adverb
- cliche_webnovel_phrase
- theme_summary_ending
- action_psychology_summary_sandwich
- excessive_parallelism
- abstract_motivation_statement
- dialogue_without_position
- emotion_without_action
- thick_paragraph_for_mobile_reading

## 6.3 Forbidden Phrase Policy

Forbidden Phrase List 应由 NF-NKS-280 Expression Type 和 NF-NKS-270 Rule 维护。

初始高风险表达包括：

- 不由得
- 刹那间
- 某种意义上
- 一时间
- 仿佛……一般
- 值得一提的是
- 说时迟那时快
- 嘴角微微上扬
- 倒吸一口凉气
- 眼神中闪过一丝复杂
- 如割麦子般倒下
- 这不仅是……更是……
- ……的序幕正缓缓拉开

这些表达不是永久绝对禁用词，但默认不得进入正式生成结果。确需使用时必须有人工批准或特定风格规则允许。

## 6.4 Humanizer Scope

Humanizer 不做大改。

Humanizer 只处理：

- 句式长短重组。
- 段落切碎和手机阅读节奏。
- 去除书面腔对白。
- 降低机械转场。
- 替换泛化表达。
- 保留角色动作和感官剪影。

Humanizer 不得改变事实、剧情目标、伏笔状态、战力结果或角色关系。

## 6.5 Humanized Output Gate

Humanized Beat 必须满足：

- no blocking consistency issue
- ai_flavor_signal below threshold
- voice_drift_signal below threshold
- paragraph_mobile_readability accepted
- no unauthorized fact change
- revision_diff persisted

## 6.6 Human Review Gate

以下情况必须进入人工审核：

- Critic 与 Humanizer 评分冲突。
- 同一 Beat 多次重写失败。
- 关键设定需要新增或变更。
- AI flavor risk 无法自动降低。
- Genre playbook 与用户指定风格冲突。

# 7. Model Router, Cost and Token Policy

## 7.1 Model Router Purpose

Novel Writing Pipeline 支持 Multi-Model Router。

不同 Agent 可以选择不同模型，依据是任务能力、成本、上下文长度、中文网文表现、结构化输出稳定性和延迟。

MVP 阶段允许所有 Agent 指向同一个 default model_profile，但调用路径仍必须经过 Model Router。这样后续可以通过配置拆分模型，而不是改写 Pipeline 代码。

## 7.2 Capability Profiles

模型选择应使用 capability profile，而不是在业务逻辑中硬编码供应商。

初始 capability profile：

| Agent Role    | Required Capability                            |
| ------------- | ---------------------------------------------- |
| Planner       | 结构化规划、JSON 稳定输出、长线逻辑            |
| Scene Planner | 情绪曲线、Beat 拆分、爽点安排                  |
| Writer        | 中文网文表达、低成本长文本生成、类型套路熟悉度 |
| Memory / RAG  | 长上下文、一致性检查、设定追踪                 |
| Critic        | 指令遵循、问题定位、结构化审查                 |
| Humanizer     | 句式重组、口语化、去 AI 味                     |

## 7.3 Example Provider Mapping

可选初始映射：

- Writer: 优先中文网文表现好、成本低、长文本稳定的模型。
- Planner / Critic: 优先结构化输出、逻辑规划和严格指令遵循强的模型。
- Memory / RAG: 优先长上下文和跨章节一致性检查强的模型。
- Humanizer: 可使用 Writer 同类模型或结构化改写模型。

供应商可配置为 DeepSeek、OpenAI、Gemini 或其他兼容 provider adapter。正式实现必须通过 Model Profile 配置，不得散落在 Prompt 文本中。

## 7.3.1 Agent Model Assignment

每个 Agent task 在调用模型前必须解析 agent_model_assignment。

解析输入：

- agent_role
- task_type
- output_mode
- genre_scope
- quality_mode
- workspace_id

解析输出：

- assignment_id
- primary_model_profile_id
- fallback_model_profile_ids
- selection_policy
- max_retry
- max_cost

assignment 解析失败时，任务不得直接调用 provider。系统必须使用显式配置的 system default profile，或进入 configuration_error。

## 7.4 Token Budget Policy

Token 预算优先级：

1. hard rules
2. Memory Package
3. current Beat Plan
4. current Scene Plan
5. previous approved Beat
6. Style Profile
7. few-shot guidance
8. broader chapter context

当预算不足时，优先摘要 broader context，不得裁剪 hard rules、Memory Package 或 forbidden_changes。

## 7.5 Cost Control

系统必须记录：

- model_profile_id
- agent_role
- prompt_tokens
- completion_tokens
- retry_count
- accepted_output_ratio
- rewrite_count
- human_edit_distance
- quality_score
- assignment_id
- fallback_from_call_id

低质量高成本模型路线必须进入 Feedback Loop 降权。

## 7.6 Feedback-Driven Routing

Feedback Agent 可以根据 accepted_output_ratio、rewrite_count、human_edit_distance、quality_score、latency 和 cost_estimate 生成模型路由建议。

路由建议不得自动修改正式 assignment，必须进入 review 状态。批准后由 Config Module 更新 agent_model_assignment。

# 8. Genre Playbooks

## 8.1 Purpose

Genre Playbook 定义不同类型小说的章节结构、读者期待、爽点节奏和禁忌表达。

Planner、Scene Planner、Writer、Critic 和 Humanizer 都必须读取当前 genre_playbook。

## 8.2 Xuanhuan Playbook

玄幻类默认要求：

- 明确 power_level_state。
- 明确主角金手指、功法、法宝或资源变化。
- 明确本章升级进度或战力收益。
- 战斗结果必须符合 Power System。
- 围观者震惊可以作为 reward_expression，但不得机械重复。
- 秘境、宗门、天骄、长老、传承等 Pattern 必须引用 NF-NKS-240。

## 8.3 Urban Power Fantasy Playbook

都市爽文默认要求：

- 反派挑衅。
- 主角隐藏身份或隐藏实力。
- 侧面烘托。
- 打脸反转。
- 围观者震惊或关系反转。
- 余韵中留下下一章钩子。

章节不得在打脸后强行升华主题。主角可以直接收束利益、资源或关系优势。

## 8.4 Scene Planner Social Pressure

Scene Planner 必须标注：

- 谁轻视主角。
- 谁嫉妒主角。
- 谁误判局势。
- 谁被迫改变态度。
- 谁承担冲突后果。
- 谁提供读者代入视角。

## 8.5 Mobile Reading Style

中文网文章节应优先适配手机阅读。

默认段落策略：

- 一到两句一段。
- 高压冲突段落更短。
- 战斗动作拆成清晰连续动作。
- 对白独立成段。
- 避免厚重说明段。

## 8.6 Playbook Validation

Critic 必须检查章节是否满足 genre_playbook。

当 genre_playbook 与用户明确要求冲突时，以用户项目设定为准，并记录 playbook_override。

# 9. Task State, Output and Feedback

## 9.1 Writing Run

每次写作任务必须创建 writing_run。

最小字段：

- writing_run_id
- generation_request_id
- target_project_id
- target_chapter_id
- genre_playbook_id
- model_router_profile_id
- status
- current_stage
- current_beat_id
- input_refs
- output_refs
- started_at
- finished_at

## 9.2 Beat Run

每个 Beat 必须创建 beat_run。

最小字段：

- section_run_id
- writing_run_id
- beat_id
- writer_model_profile_id
- critic_model_profile_id
- humanizer_model_profile_id
- status
- retry_count
- draft_ref
- critic_report_ref
- humanized_ref
- accepted_at

## 9.3 Status Model

状态流：

```text
planned
↓
style_ready
↓
writing_beat
↓
critic_review
↓
rewrite_required
↓
writing_beat
↓
humanizer_pass
↓
beat_approved
↓
chapter_assembly
↓
chapter_review
↓
approved or requires_human_review
```

## 9.4 Output Package

Writing Output Package：

```text
WritingOutputPackage
├── metadata
├── story_context_package
├── chapter_plan
├── scene_plan
├── beat_plans
├── style_profile
├── memory_package
├── beat_drafts
├── critic_reports
├── humanizer_reports
├── assembled_chapter
├── quality_report
├── feedback_records
└── export_manifest
```

## 9.5 Feedback Capture

Feedback Service 必须记录：

- beat_acceptance_rate
- rewrite_reason
- ai_flavor_issue_category
- forbidden_phrase_hit
- voice_drift_signal
- human_edit_distance
- reader_reward_signal
- genre_playbook_fit
- model_cost_quality_ratio

## 9.6 Learning Targets

反馈可用于优化：

- model router profile
- prompt template
- style profile
- expression taxonomy
- forbidden phrase rules
- genre playbook
- retrieval strategy
- beat planning strategy

任何影响正式生成策略的自动调整都必须可追踪并可回滚。

# 10. Boundaries, References and Change Log

## 10.1 Boundaries

NF-PIPE-003 定义 Novel Writing Orchestration and Humanization Pipeline。

NF-PIPE-003 不定义具体 Prompt 模板正文、检索上下文对象、写作质量评分算法、模型供应商商业配置、版权授权流程、前端编辑器交互或发布渠道。

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
- NF-NKS-280
- NF-NKS-290
- NF-RAG-001
- NF-ARCH-001
- NF-ARCH-002
- NF-DBS-002
- NF-PIPE-001
- NF-PIPE-002
- NF-AGENT-001
- NF-PROMPT-001
- NF-PROMPT-002
- NF-QA-001

## 10.3 Approval

Document Status: Draft

Next Review: Writing pipeline implementation review

Next Document: Writing Studio Workflow Specification

## 10.4 Change Log

| Version | Date       | Author                              | Change                                                         |
| ------- | ---------- | ----------------------------------- | -------------------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Writing Pipeline Team | Initial writing orchestration and humanization pipeline draft. |
