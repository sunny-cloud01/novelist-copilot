# 5. Data Traceability and Audit

## 5.1 Traceability Goal

系统必须能够回答：

- 某个知识对象来自哪本书、哪一章、哪段证据。
- 某个章节计划引用了哪些 Pattern、Rule、Rhythm 和 Story Graph 状态。
- 某个 Beat 由哪个 Prompt Package、Memory Package 和模型生成。
- Critic 为什么打回，Humanizer 改了什么。
- 人工最终改了哪些文字，原因是什么。
- 哪些反馈影响了后续 Prompt、Model Router 或检索策略。

## 5.2 Core Trace Chain

最小追踪链：

```text
source_book
→ source_chapter
→ evidence_record
→ knowledge_object / graph_edge
→ memory_package
→ prompt_package
→ writing_run
→ beat_run
→ beat_draft
→ critic_report
→ humanizer_report
→ quality_report
→ approved_chapter
→ feedback_record
```

## 5.3 Required References

关键对象必须保存：

- request_id
- trace_id
- actor_id or agent_role
- input_refs
- output_refs
- evidence_refs
- model_profile_id when model is used
- prompt_package_id when prompt is used
- source_snapshot_id when knowledge is read
- quality_report_id when quality gate is executed

## 5.4 Audit Policy

以下操作必须产生 audit_event：

- 修改 Approved 或 Frozen knowledge。
- 批准或驳回知识对象。
- 修改质量阈值、模型路由、Prompt 版本或规则配置。
- 接受章节进入正式 manuscript。
- 反馈驱动策略 promotion 或 rollback。

## 5.5 Evidence and Storage Rule

大文本、草稿、报告、diff 和长证据片段进入 Object Storage。PostgreSQL 保存 object_ref、checksum、owner、version、review_status 和 access policy。

embedding、图数据库和搜索索引都是 projection，不得作为唯一事实来源。
