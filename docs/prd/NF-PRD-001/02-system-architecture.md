# 2. System Architecture

```text
                 Novel Factory
                       │
              Creator Workspace
                       │
              Upload Source Book
                       │
                 Auto Analyze Book
                       │
          ┌────────────┴────────────┐
          │                         │
   Knowledge Package           Story Graph View
          │                         │
          └────────────┬────────────┘
                       │
             AI Story Bible Draft
                       │
          Confirm Worldview and Boundary
                       │
              One-Click Chapter Run
                       │
        Critic / Humanizer / Quality Gate
                       │
        Blocking Issue Review / Chapter Approval
                       │
                 Feedback Loop
                       │
              Strategy Optimization
```

系统以 Creator Workspace 为入口。Creator 上传参考作品后，系统自动完成文件接收、文本标准化、章节切分、知识抽取、证据绑定、候选归一化和知识包落库。Story Graph 是辅助查看和检索视图，不作为 MVP 的重编辑入口。

新书创作从 AI Story Bible Draft 开始，Creator 确认世界观、原创边界和章节方向后，系统执行一键章节生成。内部仍可拆分 Scene、Beat 或 Section 进行 Critic、Humanizer 和 Quality Gate，但界面只在阻塞问题、质量风险和最终批准处打断 Creator。审核结果进入 Feedback Loop，用于持续优化 Prompt、Pattern、质量阈值和生成策略。
