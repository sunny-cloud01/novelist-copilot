# 5. States, Errors and Change Log

## 5.1 Core Status Vocabulary

通用状态：

```text
idle
queued
running
needs_attention
blocked
completed
approved
failed
cancelled
```

Creator-facing 文案应避免暴露过多内部状态。内部 task_events 可以更细，但页面状态应收敛到上述集合。

## 5.2 Action Vocabulary

主要按钮使用固定词汇：

| Action               | Meaning              |
| -------------------- | -------------------- |
| Upload Source        | 上传参考作品         |
| Analyze Book         | 自动拆书和抽取       |
| Resolve Exception    | 处理异常项           |
| Commit Knowledge     | 落库知识包           |
| Inspect Graph        | 辅助查看图谱         |
| Generate Story Bible | 生成新书设定草稿     |
| Confirm Bible        | 确认世界观和原创边界 |
| Generate Chapter     | 一键生成章节         |
| Fix Blocking Issue   | 修复阻塞问题         |
| Approve Chapter      | 批准章节             |
| Review Suggestion    | 审核策略建议         |

同一动作在按钮、Toast、任务记录和审计日志中必须使用一致名称。

## 5.3 Error Handling

错误提示必须说明：

- 哪一步失败。
- 影响什么产物。
- 用户是否必须处理。
- 可执行的下一步。

示例：

```text
Chapter generation blocked
The draft conflicts with the approved power-system rule "九曜纹残片不能直接开启秘境".
Fix the blocked section or regenerate the chapter with stricter world rules.
```

## 5.4 Audit and Trace

以下动作必须写入 audit_events：

- Upload Source。
- Commit Knowledge。
- Confirm Bible。
- Generate Chapter。
- Fix Blocking Issue。
- Approve Chapter。
- Review Suggestion。

每个正式章节必须可以追踪到 source、knowledge package、story bible、memory package、prompt package、writing run、quality report 和 approval record。

## 5.5 Change Log

| Version | Date       | Changes                                  |
| ------- | ---------- | ---------------------------------------- |
| 1.0.0   | 2026-07-11 | Initial Creator-facing interaction flow. |
