# 1. Purpose and Scope

本文档定义 Novel Factory 第一阶段后端技术实现架构。

NF-ARCH-001 定义系统级逻辑架构。NF-ARCH-002 在该架构之上定义可落地的后端模块、运行进程、任务编排、LLM 调用边界、数据一致性和演进路线。

本文档的核心目标是支持从拆书到 AI 生成的完整工程链路：

```text
Book Ingestion
↓
Knowledge Extraction
↓
Knowledge Storage and Review
↓
Retrieval and Planning
↓
Prompt Assembly
↓
Chapter Generation and Revision
↓
Consistency Review
↓
Human Feedback
```

本文档覆盖：

- 后端技术栈建议。
- API、Worker 和后台任务边界。
- 服务模块职责。
- LLM、Agent 和生成流水线边界。
- 数据流、一致性、幂等和错误处理。
- 部署、安全和可观测性要求。

本文档不定义数据库物理 Schema、Prompt 模板正文、前端交互设计或具体云厂商基础设施脚本。
