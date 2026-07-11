# 3. System Context

Novel Factory 位于原始小说来源、知识工程系统、AI 生成系统和人工审核流程之间。

```text
External Book Sources
        │
        ▼
Novel Factory
        │
        ├── Knowledge Engineering
        ├── Story Graph
        ├── Prompt and Generation
        ├── Consistency Checking
        └── Feedback Learning
        │
        ▼
Generated Novel Assets
```

外部参与方：

- 内容来源：小说文本、平台元数据、人工整理素材。
- 人工审核者：评审抽取结果、生成章节和质量报告。
- AI 模型：执行抽取、推理、生成、评估和润色。
- 下游系统：数据库、RAG、Agent Orchestrator、Prompt Engine、发布工具。
