# 4. Logical Architecture

Novel Factory 的逻辑架构分为八层：

```text
Frontend Experience Layer
↓
Source Layer
↓
Ingestion Layer
↓
Knowledge Extraction Layer
↓
Knowledge Storage Layer
↓
Planning and Prompt Layer
↓
Generation and Consistency Layer
↓
Review and Feedback Layer
```

## 4.1 Frontend Experience Layer

Frontend Experience Layer 提供人工导入、拆书审核、知识管理、章节生成、质量评审和运营配置界面。

前端技术基线：React、TypeScript、pnpm。组件库优先使用 shadcn/ui；仅当 shadcn/ui 无法满足复杂编辑器、图谱或可视化场景时，才引入专项组件或可视化库。

## 4.2 Source Layer

Source Layer 管理原始小说文本、平台元数据、人工素材和外部参考数据。

## 4.3 Ingestion Layer

Ingestion Layer 负责导入、清洗、去重、章节识别和基础预处理。

## 4.4 Knowledge Extraction Layer

Knowledge Extraction Layer 按 NF-NKS-100 将 Book、Chapter、Scene 抽取为对象、关系、Pattern、Rhythm Profile 和 Rule。

## 4.5 Knowledge Storage Layer

Knowledge Storage Layer 存储结构化数据库、Knowledge Base、Story Graph、Evidence 和 Review Report。

## 4.6 Planning and Prompt Layer

Planning and Prompt Layer 基于知识对象、套路、节奏和生成目标构造大纲、卷纲、章节计划和 Prompt。

## 4.7 Generation and Consistency Layer

Generation and Consistency Layer 负责章节生成、润色、一致性检测和规则校验。

## 4.8 Review and Feedback Layer

Review and Feedback Layer 收集人工审核、AI 质量检测、读者反馈和生成效果指标，并回流到知识系统。
