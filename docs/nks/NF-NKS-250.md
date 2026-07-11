---
document_id: NF-NKS-250
title: Rhythm Profile Specification
version: 1.0.0
status: Draft
category: Novel Knowledge Specification
owner: Novel Factory Knowledge Engineering Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-230
  - NF-NKS-240
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-240.md
---

# NF-NKS-250

# Rhythm Profile Specification

# 1. Purpose and Scope

本文档定义 Rhythm Profile 的模块级规范。

Rhythm Profile 用于量化章节、场景、卷或剧情段落的叙事节奏，使系统能够比较作品风格、规划章节强度、控制生成节奏并进行质量评估。

本文档覆盖：

- Rhythm Profile model
- Rhythm metrics
- 聚合规则
- 生成约束
- 验证规则

本文档不定义具体可视化界面或模型评分实现。

# 2. Rhythm Model

## 2.1 Rhythm Profile

Rhythm Profile 表示某个范围内的节奏画像。

最小字段：

- rhythm_profile_id
- scope_type
- scope_id
- climax_index
- conflict_index
- dialogue_ratio
- description_ratio
- battle_ratio
- information_density
- suspense_index
- reward_count
- emotion_curve
- evidence_refs

## 2.2 Metric Definitions

初始指标定义：

| Metric              | Meaning                    |
| ------------------- | -------------------------- |
| climax_index        | 当前范围内叙事峰值强度     |
| conflict_index      | 冲突密度和冲突强度         |
| dialogue_ratio      | 对白占比                   |
| description_ratio   | 描写占比                   |
| battle_ratio        | 战斗或动作场景占比         |
| information_density | 新设定、新关系、新线索密度 |
| suspense_index      | 未解决 Hook 和威胁强度     |
| reward_count        | 明确爽点或正反馈节点数量   |

## 2.3 Emotion Curve

Emotion Curve 表示读者或角色体验随段落推进的变化。

最小字段：

- points
- dominant_emotion
- peak_position
- release_position
- unresolved_tension

Emotion Curve 应引用 Event、Conflict、Reward、Hook 或 Climax 对象。

# 3. Aggregation, Validation and Change Log

## 3.1 Aggregation Rules

Rhythm Profile 可按以下范围聚合：

- Scene
- Chapter
- Volume
- Book
- Pattern
- Generation Plan

聚合时必须保留来源范围，禁止将 Book 级指标直接替代 Chapter 级指标。

## 3.2 Generation Constraints

生成系统使用 Rhythm Profile 时必须满足：

- 高 climax_index 后必须允许缓冲段落，除非目标风格要求连续高压。
- reward_count 不得与 Hook resolution 完全脱节。
- information_density 过高时必须降低新设定引入速度。
- battle_ratio 必须符合题材和章节目标。

## 3.3 Validation Rules

Rhythm Profile 必须满足：

- scope_type 和 scope_id 必须存在。
- 指标必须有稳定取值范围。
- 高强度指标必须能追溯到 Event、Conflict、Reward、Hook 或 Climax。
- 自动计算结果必须记录 extractor 或 evaluator 版本。

## 3.4 Change Log

| Version | Date       | Author                                   | Change                                |
| ------- | ---------- | ---------------------------------------- | ------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial Rhythm Profile specification. |
