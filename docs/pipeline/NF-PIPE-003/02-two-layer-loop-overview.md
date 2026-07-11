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
