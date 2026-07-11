# 3. MVP Frontend Scope

## 3.1 Technical Baseline

Frontend 使用 React + TypeScript + pnpm。通用组件优先使用 shadcn/ui。

MVP 前端只实现 Web 管理和创作工作台，不实现移动端 App。

## 3.2 Required Pages

MVP 页面范围：

| Page                  | Purpose                                                     |
| --------------------- | ----------------------------------------------------------- |
| Workspace Home        | 工作区入口、最近任务、待审核项                              |
| Source Library        | 上传作品、查看书籍、章节和导入状态                          |
| Extraction Run Detail | 查看抽取任务进度、错误和报告                                |
| Knowledge Review      | 审核 candidate knowledge、证据、冲突和别名                  |
| Story Graph Viewer    | 基础图谱浏览、节点详情、关系查看                            |
| Novel Project Home    | 项目设定、Story Bible、章节列表                             |
| Chapter Planner       | 章纲、Scene 和 Beat 计划审核                                |
| Writing Studio        | 章节生成、Section 级恢复、Critic、Humanizer、组章、质量报告 |
| Feedback Dashboard    | 模型成本、AI 味、人工编辑距离和策略建议                     |
| Configuration         | 模型 profile、质量阈值、Prompt 版本和规则配置               |

## 3.3 MVP UI States

所有长任务页面必须支持：

- queued
- running
- succeeded
- failed
- requires_review
- blocked

状态必须来自后端 task 或 run，不得只由前端本地推断。

## 3.4 Writing Studio MVP Layout

Writing Studio 第一版必须展示：

- 左侧：chapter plan、scene list、section list，并可折叠查看内部 beat plan。
- 中间：当前 section draft、humanized section、assembled chapter。
- 右侧：Memory Package 摘要、Critic issues、Quality Gate、trace refs。
- 底部：model cost、retry_count、human actions。

## 3.5 Frontend Non-Goals

MVP 不实现：

- 高级协同编辑。
- 自定义可视化图谱布局编辑器。
- 发布排期。
- 商业化计费页面。
- 复杂主题系统。
