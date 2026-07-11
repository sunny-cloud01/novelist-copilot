---
document_id: NF-UX-001
title: Creator Interaction Flow Specification
version: 1.0.0
status: Draft
category: UX Specification
owner: Novel Factory Product Design Team
created: 2026-07-11
updated: 2026-07-11
dependencies:
  - NF-PRD-001
  - NF-IMPL-002
  - NF-IMPL-003
  - NF-PIPE-001
  - NF-PIPE-003
  - NF-PROMPT-001
  - NF-QA-001
references:
  - docs/prd/NF-PRD-001.md
  - docs/implementation/NF-IMPL-002.md
  - docs/implementation/NF-IMPL-003.md
  - docs/pipeline/NF-PIPE-001.md
  - docs/pipeline/NF-PIPE-003.md
  - docs/prompts/NF-PROMPT-001.md
  - docs/quality/NF-QA-001.md
---

# NF-UX-001

# Creator Interaction Flow Specification

# 1. Purpose and Product Position

本文档定义 Novel Factory 面向个人创作者的核心交互流程。

Novel Factory 不是专业编辑团队使用的重审核后台，而是个人生书平台。系统必须替 Creator 承担拆书、抽取、落库、图谱构建、世界观草稿、章节生成、审查和修订的大部分机械工作。Creator 的主要职责是提供方向、确认关键设定、处理异常和批准最终内容。

## 1.1 UX Goal

交互目标：

```text
少输入
↓
自动运行
↓
异常打断
↓
关键确认
↓
可追踪批准
```

系统应避免把内部工程流水线直接暴露给 Creator。内部可以有 Chapter、Scene、Beat、Prompt、Critic、Humanizer、Quality Gate 等复杂结构；界面应以“上传一本书”“生成知识包”“创建新书设定”“生成本章”“处理阻塞问题”“批准章节”等 Creator 能理解的动作组织。

## 1.2 Primary User

Primary user 是个人创作者。

用户特征：

- 可能不熟悉被上传书籍的全部细节。
- 不希望逐章、逐对象、逐 Beat 进行人工审核。
- 需要 AI 自动拆解参考作品并生成可用知识资产。
- 需要 AI 帮助生成新书世界观、章节和场景。
- 需要看到证据链、风险和质量结果，但不想维护复杂图谱。

## 1.3 Design Principle

前端工作台保持简洁、克制、低装饰。

页面优先展示：

- 当前任务状态。
- 下一步可执行动作。
- 阻塞问题。
- 自动产物摘要。
- 必要证据和审查结果。

页面不应优先展示：

- 复杂动画。
- 装饰性图表。
- 需要专业编辑理解的大量中间对象。
- 默认展开的内部 Beat 级流水线。

# 2. End-to-End Creator Flow

## 2.1 High Level Flow

Creator-facing 主流程：

```text
Create Workspace
↓
Upload Source Book
↓
Auto Analyze Book
↓
Review Extraction Summary
↓
Commit Knowledge Package
↓
Inspect Story Graph
↓
Create Novel Project
↓
Generate Story Bible Draft
↓
Confirm Worldview and Boundaries
↓
Generate Chapter Direction
↓
One-Click Generate Chapter
↓
Review Quality and Blocking Issues
↓
Approve Chapter
↓
Record Feedback and Continue
```

## 2.2 Default Automation Rule

默认自动运行的步骤：

- 文件接收、去重和存储。
- 文本标准化。
- 章节和场景切分。
- 对象、关系、规则、节奏和证据抽取。
- 候选归一化和低置信度标记。
- Story Graph snapshot 构建。
- Story Bible 草稿生成。
- Chapter、Scene 和 Beat 内部计划。
- Memory Package 和 Prompt Package 装配。
- 约 3000 字章节草稿生成。
- Critic、Humanizer 和 Quality Gate。

默认不要求 Creator 逐项审核这些中间结果。

## 2.3 Human Confirmation Rule

必须让 Creator 确认的点：

| Confirmation Point               | Purpose                                  |
| -------------------------------- | ---------------------------------------- |
| Source upload metadata           | 确认来源、类型、用途边界                 |
| Extraction summary               | 让 Creator 知道系统形成了什么知识包      |
| Low confidence or conflict items | 只处理系统无法可靠判断的问题             |
| Story Bible draft                | 确认新书世界观、主角、风格、禁用相似点   |
| Chapter direction                | 确认本章目标、冲突、爽点、字数和禁用变化 |
| Blocking quality issues          | 处理一致性、原创性、AI 味或事实冲突      |
| Final chapter approval           | 批准进入正式 manuscript                  |
| Strategy suggestion              | 批准反馈是否影响后续生成策略             |

## 2.4 Interrupt-Only Review Rule

系统只在以下情况打断 Creator：

- 上传文件无法解析。
- 章节切分置信度低。
- 大量候选对象无法归一化。
- 证据引用缺失。
- 图谱出现指向不存在对象的关系。
- Story Bible 与原创边界冲突。
- 章节生成质量低于阈值。
- 原创性风险或相似表达风险超阈值。
- AI 味检测超阈值。
- 模型成本异常。

非阻塞信息进入报告和详情页，不应阻断主流程。

# 3. Page Model and Actions

## 3.1 Navigation Model

主导航保持简单：

```text
Home
Sources
Knowledge
Projects
Writing
Review
Reports
Settings
```

其中 Story Graph 不作为主入口强制暴露，可作为 Knowledge 或 Project 详情中的辅助视图。

## 3.2 Page Responsibilities

| Page               | Primary Job                          | Main Action              |
| ------------------ | ------------------------------------ | ------------------------ |
| Home               | 展示最近项目、运行任务和待处理阻塞项 | Continue                 |
| Sources            | 上传参考作品并查看导入状态           | Upload Source            |
| Source Detail      | 查看自动拆书结果和抽取摘要           | Commit Knowledge Package |
| Extraction Run     | 查看自动任务进度、错误和低置信度项   | Resolve Exceptions       |
| Knowledge Package  | 查看已落库知识、证据和摘要           | Use in Project           |
| Story Graph View   | 辅助查看人物、势力、地点和事件关系   | Inspect Node             |
| Project Home       | 管理新书目标、设定和章节             | Generate Story Bible     |
| Story Bible Review | 确认 AI 生成的世界观、规则和原创边界 | Confirm Bible            |
| Chapter Setup      | 输入本章目标、字数和禁用变化         | Generate Chapter         |
| Writing Run        | 查看一键生成进度和质量检查           | Review Result            |
| Quality Review     | 处理阻塞问题和局部修订               | Resolve Blocker          |
| Chapter Approval   | 批准最终章节进入 manuscript          | Approve Chapter          |
| Reports            | 查看成本、质量、反馈和策略建议       | Review Suggestion        |

## 3.3 Upload Interaction

Upload Source 应包含：

- 文件选择或文本粘贴。
- title、author、platform、genre、source_type。
- 用途边界确认。
- 自动重复检测结果。
- Upload and Analyze 按钮。

上传成功后，系统直接进入自动拆书任务，不要求 Creator 手动选择每个 pipeline stage。

## 3.4 Extraction Interaction

Extraction Run 页面显示：

- run_status。
- 当前阶段。
- 预计剩余时间。
- 已识别章节数、场景数、对象数、证据数。
- 阻塞错误。
- 低置信度项目列表。

主操作：

- Resolve Exception。
- Re-run Failed Step。
- Commit Knowledge Package。

不得默认要求 Creator 审核每一个 knowledge candidate。

## 3.5 Knowledge Graph Interaction

Story Graph 是辅助查看，不是 MVP 的重编辑工作台。

必须支持：

- 搜索节点。
- 查看节点详情。
- 查看关系来源。
- 查看 evidence_refs。
- 从节点跳转到原文证据。

MVP 不要求：

- 大规模画布编辑。
- 手动画边。
- 复杂布局调参。
- 图数据库级交互。

# 4. Writing Flow and Approval

## 4.1 Story Bible Generation

新书世界观默认由 AI 生成草稿。

Creator 输入：

- genre。
- desired_tone。
- protagonist preference。
- originality boundary。
- allowed knowledge sources。
- forbidden similarities。

系统输出 Story Bible Draft：

- world rules。
- power system。
- factions。
- protagonist and core cast。
- main conflict。
- volume direction。
- style target。
- forbidden changes。

Creator 操作：

- Confirm。
- Regenerate section。
- Edit key field。
- Reject and retry。

## 4.2 Chapter Setup

章节生成前，Creator 不需要设计完整 Scene 或 Beat。

Creator 只需确认：

- chapter_goal。
- target_word_count，默认约 3000。
- main_conflict。
- reward_or_hook。
- emotional direction。
- must_include。
- must_not_change。

系统内部生成 chapter_plan、scene_plan 和 beat_plan。

## 4.3 One-Click Chapter Generation

主按钮为 Generate Chapter。

系统内部执行：

```text
Assemble Memory Package
↓
Assemble Prompt Package
↓
Generate Chapter Draft by internal sections
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
```

UI 对 Creator 展示为一个 writing_run，而不是多个必须手动推进的 Beat run。

## 4.4 Quality Review

Quality Review 应将问题分为：

| Type       | UI Behavior             |
| ---------- | ----------------------- |
| blocking   | 必须处理后才能 approve  |
| warning    | 可忽略但记录到 approval |
| suggestion | 可选采纳                |
| passed     | 只展示摘要              |

Blocking issue 包括：

- 世界观冲突。
- 人物状态冲突。
- 关键证据缺失。
- 原创性风险。
- AI 味超阈值。
- 字数严重偏离。
- 章节目标未完成。

## 4.5 Approval

Final Chapter Approval 必须记录：

- actor_id。
- approved_at。
- chapter_version_id。
- writing_run_id。
- quality_report_id。
- unresolved warning count。
- feedback note。

Approve 后章节进入正式 manuscript。未批准的章节只能作为 draft version 保留。

# 5. States, Errors and Change Log

## 5.1 Core Status Vocabulary

通用状态：

```text
idle
queued
running
needs_attention
blocked
completed
approved
failed
cancelled
```

Creator-facing 文案应避免暴露过多内部状态。内部 task_events 可以更细，但页面状态应收敛到上述集合。

## 5.2 Action Vocabulary

主要按钮使用固定词汇：

| Action               | Meaning              |
| -------------------- | -------------------- |
| Upload Source        | 上传参考作品         |
| Analyze Book         | 自动拆书和抽取       |
| Resolve Exception    | 处理异常项           |
| Commit Knowledge     | 落库知识包           |
| Inspect Graph        | 辅助查看图谱         |
| Generate Story Bible | 生成新书设定草稿     |
| Confirm Bible        | 确认世界观和原创边界 |
| Generate Chapter     | 一键生成章节         |
| Fix Blocking Issue   | 修复阻塞问题         |
| Approve Chapter      | 批准章节             |
| Review Suggestion    | 审核策略建议         |

同一动作在按钮、Toast、任务记录和审计日志中必须使用一致名称。

## 5.3 Error Handling

错误提示必须说明：

- 哪一步失败。
- 影响什么产物。
- 用户是否必须处理。
- 可执行的下一步。

示例：

```text
Chapter generation blocked
The draft conflicts with the approved power-system rule "九曜纹残片不能直接开启秘境".
Fix the blocked section or regenerate the chapter with stricter world rules.
```

## 5.4 Audit and Trace

以下动作必须写入 audit_events：

- Upload Source。
- Commit Knowledge。
- Confirm Bible。
- Generate Chapter。
- Fix Blocking Issue。
- Approve Chapter。
- Review Suggestion。

每个正式章节必须可以追踪到 source、knowledge package、story bible、memory package、prompt package、writing run、quality report 和 approval record。

## 5.5 Change Log

| Version | Date       | Changes                                  |
| ------- | ---------- | ---------------------------------------- |
| 1.0.0   | 2026-07-11 | Initial Creator-facing interaction flow. |
