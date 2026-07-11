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
