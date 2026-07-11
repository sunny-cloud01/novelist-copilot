# 2. Product Experience Map

## 2.1 Primary User Roles

产品第一阶段支持以下角色：

| Role               | Responsibility                                       |
| ------------------ | ---------------------------------------------------- |
| Creator            | 创建原创小说项目、选择题材、审核方向、接受或修改章节 |
| Knowledge Reviewer | 审核拆书结果、合并对象、批准知识和规则               |
| Writing Reviewer   | 审核章节质量、处理阻塞问题、批准重要改写             |
| Operator           | 管理模型配置、质量阈值、任务队列和成本报表           |
| Service Account    | 执行 Agent、Worker、Scheduler 和系统内部任务         |

## 2.2 User Journey

从开始使用到形成自己的小说，产品路径如下：

```text
Create Workspace
↓
Import Source Books or Materials
↓
Run Ingestion and Book Analysis
↓
Review Extraction Summary and Exceptions
↓
Commit Knowledge Package and Inspect Story Graph
↓
Create Original Novel Project
↓
Configure Genre, Rules, Style and Constraints
↓
Confirm AI-Generated Story Bible and Chapter Direction
↓
Generate Chapter in One Click
↓
Critic Review and Humanizer Pass
↓
Assemble Chapter
↓
Quality Gate and Human Review
↓
Accept Chapter into Project Manuscript
↓
Capture Feedback and Improve Strategy
```

## 2.3 Frontend Workspaces

第一阶段前端应拆为以下工作区：

- Source Workspace: 导入、清洗状态、章节预览。
- Knowledge Workspace: 自动抽取摘要、证据、低置信度异常和知识包落库。
- Story Graph View: 图谱辅助查看、关系来源、伏笔状态，不作为默认重编辑入口。
- Novel Project Workspace: 原创项目设定、卷纲、章纲、角色和规则。
- Writing Studio: 一键章节生成、内部 Scene/Beat 编排状态、Critic、Humanizer、组章和质量报告。
- Feedback and Analytics Workspace: 模型成本、质量趋势、人工编辑模式和策略建议。
- Configuration Workspace: 模型路由、规则、质量阈值、Prompt 版本和权限。

## 2.4 UX Rule

用户不应被要求理解所有底层服务。

界面必须把复杂流水线压缩为可操作状态：queued、running、requires_review、blocked、approved、failed。详细证据、模型调用、质量项和反馈记录可以展开查看，但默认页面应围绕下一步决策呈现。
