# 2. MVP User Workflows

## 2.1 Workflow A: Source to Approved Knowledge

用户路径：

```text
Create Workspace
↓
Upload Source Book
↓
Run Ingestion
↓
Auto Segment Chapters and Scenes
↓
Run Basic Extraction
↓
Auto Normalize and Score Knowledge Candidates
↓
Review Exceptions or Low Confidence Items
↓
Commit Approved Knowledge Package
↓
Browse Story Graph
```

验收：系统可以自动完成章节切分、基础抽取、候选归一化和知识包提交。用户可以查看 evidence_refs、抽取报告和低置信度问题，并只对 exception item 执行 approve、reject、merge_alias 或 request_reextract。Story Graph 作为辅助查看界面，不作为 MVP 的重编辑入口。

## 2.2 Workflow B: Original Project Setup

用户路径：

```text
Create Novel Project
↓
Select Genre Scope
↓
Configure Originality Boundary
↓
Generate Story Bible Draft
↓
Review and Confirm Story Bible
↓
Select Allowed Knowledge Sources
↓
Configure Quality Gate Profile
```

验收：项目必须生成 project_id、story_bible_id、quality_gate_profile_id 和 allowed_knowledge_source_refs。Story Bible 默认由 AI 生成草稿，Creator 负责确认方向、禁用相似点和最终设定边界。

## 2.3 Workflow C: Plan One Chapter

用户路径：

```text
Open Project
↓
Create Chapter Goal
↓
Generate Chapter Plan Draft
↓
Generate Scene and Beat Plan Internally
↓
Confirm Chapter Direction
```

验收：Creator 只需要确认章目标、核心冲突、爽点、禁用变化和预估字数。系统内部仍需生成 Scene 和 Beat 计划；每个 Beat 必须包含 beat_goal、pov_character、active_characters、conflict_pressure、reward_or_hook、required_knowledge_refs 和 estimated_word_count，但不要求 Creator 默认逐项审批。

## 2.4 Workflow D: Generate One Chapter

用户路径：

```text
Assemble Memory Package
↓
Assemble Prompt Package
↓
Generate Full Chapter Draft
↓
Run Critic
↓
Auto Rewrite Blocked Sections
↓
Run Humanizer
↓
Assemble Chapter
↓
Run Quality Gate
↓
Human Review
↓
Accept Chapter
```

验收：Creator-facing 主操作是“一键生成本章”。章节被接受前必须有 writing_run、section_runs、critic_reports、humanizer_reports、quality_report 和 feedback_records。内部 Beat 可作为 section payload 的计划细节保存。只有 blocking issue、低一致性、原创性风险或 AI 味超阈值时，界面才要求 Creator 局部处理。

## 2.5 Workflow E: Review Feedback and Cost

用户路径：

```text
Open Feedback Dashboard
↓
Review AI Flavor Issues
↓
Review Human Edit Distance
↓
Review Model Cost Quality Ratio
↓
Create Strategy Suggestion
↓
Approve or Reject Suggestion
```

验收：反馈建议不得自动修改正式策略，必须进入 review 状态。
