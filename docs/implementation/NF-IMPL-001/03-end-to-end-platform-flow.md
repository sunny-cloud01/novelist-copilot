# 3. End-to-End Platform Flow

## 3.1 Source to Knowledge Flow

```text
Book Upload
↓
Ingestion Task
↓
Chapter Segmentation
↓
Scene Segmentation
↓
Knowledge Extraction
↓
Normalization and Alias Merge
↓
Story Graph Build
↓
Knowledge Review
↓
Approved Knowledge Base
```

每个抽取对象必须保留 evidence_refs。未审核对象只能作为 candidate 使用，不得进入正式写作上下文。

## 3.2 Knowledge to Original Project Flow

原创项目不是简单复制来源作品。

系统必须将 Approved Knowledge 抽象为可复用知识资产：Pattern、Rhythm Profile、Asset、Rule、Expression Type、Genre Playbook 和 Feedback Knowledge。

原创项目创建时，用户选择或配置：

- genre_scope
- target_reader_profile
- originality_boundary
- allowed_knowledge_sources
- style_profile_seed
- forbidden_changes
- quality_gate_profile

## 3.3 Project Planning Flow

```text
Project Setting
↓
Story Bible
↓
Volume Plan
↓
Chapter Plan
↓
Scene Plan
↓
Beat Plan
```

Planner 输出必须引用 Knowledge Base、Pattern、Rhythm Profile、Rule 和项目自有设定。新增关键设定必须进入 review 状态。

## 3.4 Writing Flow

写作阶段执行 NF-PIPE-003 的 Creator-facing 一键章节生成流程。Beat、Scene 或 Section 仍作为系统内部编排单元存在，但不要求 Creator 默认逐项推进：

```text
Memory Package
↓
Style Profile
↓
Generate Chapter Draft
↓
Critic Report
↓
Auto Rewrite Blocked Sections
↓
Humanizer Pass
↓
Chapter Assembly
↓
Quality Gate
↓
Human Review or Accept
```

## 3.5 Feedback Flow

完成章节后必须采集：

- writer_model_profile_id
- critic_model_profile_id
- humanizer_model_profile_id
- prompt_package_id
- memory_package_id
- quality_report_id
- human_edit_distance
- accepted_output_ratio
- ai_flavor_issue_category
- reader_reward_signal
- model_cost_quality_ratio

反馈进入 NF-NKS-290 定义的 Feedback Knowledge，不得直接覆盖正式策略。
