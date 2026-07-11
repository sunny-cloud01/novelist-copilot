# 1. Purpose and MVP Boundary

本文档定义 Novel Factory 第一版 MVP 的交付计划。

NF-IMPL-001 定义产品级实现蓝图。NF-IMPL-002 将蓝图中的 Phase 0、Phase 1 和 Phase 2 收敛为可开发、可验收、可演示的 MVP 范围。

## 1.1 MVP Goal

MVP 的目标不是一次性交付完整工业化写作平台，而是证明以下闭环可运行：

```text
导入一本参考作品
↓
完成基础拆书和知识审核
↓
创建一个原创小说项目
↓
生成一章可审稿章节
↓
查看证据链、质量报告、模型成本和反馈记录
```

## 1.2 MVP Must Include

MVP 必须包含：

- 用户工作区和基础权限。
- Source import 和章节管理。
- 基础抽取任务和知识候选审核。
- Approved Knowledge Base。
- 基础 Story Graph 浏览。
- Novel Project 创建和 Story Bible。
- Chapter Plan、Scene Plan、Beat Plan。
- Memory Package 和 Prompt Package 组装。
- Creator-facing one-click Chapter Generation，内部可拆分为 Beat、Scene、Critic 和 Humanizer 子任务。
- Chapter Assembly 和 Quality Gate。
- Feedback Record 和成本质量统计。

## 1.3 MVP Must Not Include

MVP 不包含：

- 多租户商业化计费。
- 发布平台接入。
- 完整移动端 App。
- 全自动长篇连载。
- 独立图数据库或专用向量数据库。
- 复杂读者平台埋点。
- 多语言完整翻译工作流。

## 1.4 Success Criteria

MVP 成功标准：

- 一名 Creator 可以在单个工作区完成从导入到生成单章。
- 每个正式章节都能追踪到 source、knowledge、memory、prompt、model、quality 和 feedback。
- 人工确认集中在来源导入、新书设定、章节最终批准和阻塞问题；拆书、抽取、图谱构建和章节生成默认自动运行。
- 本地 Docker Compose 可以启动核心依赖和服务。
