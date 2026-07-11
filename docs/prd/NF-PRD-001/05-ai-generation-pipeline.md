# 5. AI Generation Pipeline

```text
Step 1: 创建原创项目
↓
Step 2: 选择题材、风格和原创边界
↓
Step 3: 选择可用知识包
↓
Step 4: AI 生成 Story Bible 草稿
↓
Step 5: Creator 确认世界观和禁用相似点
↓
Step 6: 输入或确认章节方向
↓
Step 7: 一键生成约 3000 字章节
↓
Step 8: Critic / Humanizer / Quality Gate
↓
Step 9: 处理阻塞问题
↓
Step 10: Approve Chapter
↓
反馈进入后续策略
```

生成流水线必须把知识库、Story Graph、Prompt Engine、Chapter Engine 和 Consistency Engine 串联起来。

系统内部可以将章节拆成 Scene、Beat 或 Section 执行生成和审查，但 Creator-facing 主操作应是一键生成章节。人工介入集中在 Story Bible 确认、章节方向确认、阻塞问题处理、最终章节批准和策略建议审核。

人工确认结果必须回流到 Feedback Loop，用于后续优化。
