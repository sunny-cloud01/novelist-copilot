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
