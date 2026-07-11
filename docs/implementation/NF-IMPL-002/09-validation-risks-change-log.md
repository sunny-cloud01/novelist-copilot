# 9. Validation, Risks and Change Log

## 9.1 MVP Validation Plan

验证必须覆盖：

- Documentation: build_docs check passes。
- Local runtime: Docker Compose can start dependencies。
- API: required endpoint families return standard envelope。
- Task model: long tasks persist status in PostgreSQL。
- Storage: uploaded text and generated reports have object_ref and checksum。
- Traceability: accepted chapter traces to source evidence, memory, prompt, model and quality report。
- Human review: blocking issue can be routed to review action。
- Cost: model call metrics are recorded。

## 9.2 MVP Demo Script

MVP 演示必须按以下脚本执行：

1. 创建 workspace。
2. 上传一本参考作品文本。
3. 启动 ingestion 和 extraction。
4. 批准主要知识对象。
5. 创建原创小说项目。
6. 生成 chapter plan 和 section plan；内部 beat plan 作为 section payload 保存。
7. 逐 Beat 生成并通过 Critic 和 Humanizer。
8. 组章并运行 Quality Gate。
9. 接受章节进入 manuscript。
10. 打开 trace 和 feedback dashboard。

## 9.3 Key MVP Risks

| Risk                                 | Mitigation                                                |
| ------------------------------------ | --------------------------------------------------------- |
| MVP scope expands into full platform | Freeze non-goals and slice acceptance before coding       |
| LLM output instability               | Use structured output contracts, retries and human review |
| Review queue too large               | Only route blocking and low-confidence issues to humans   |
| Traceability gaps                    | Enforce input_refs and output_refs at task boundary       |
| Local infrastructure complexity      | Keep Phase 1 storage to PostgreSQL, Redis and MinIO       |
| Cost spikes                          | Enforce retry budgets and model cost metrics              |

## 9.4 Boundaries

NF-IMPL-002 定义 MVP 交付计划，不替代 NF-IMPL-001 的产品级蓝图，也不定义最终代码实现细节。

具体代码任务应由 NF-IMPL-003 Service Build Plan 或后续 implementation plan 管理。

## 9.5 References

- NF-IMPL-001
- NF-ARCH-002
- NF-DBS-002
- NF-API-001
- NF-PIPE-003
- NF-RAG-001
- NF-PROMPT-002
- NF-QA-001
- NF-NKS-290
- NF-IMPL-003

## 9.6 Approval

Document Status: Draft

Next Review: MVP scope review

Next Document: NF-IMPL-003 Service Build Plan

## 9.7 Change Log

| Version | Date       | Author                            | Change                           |
| ------- | ---------- | --------------------------------- | -------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Implementation Team | Initial MVP delivery plan draft. |
