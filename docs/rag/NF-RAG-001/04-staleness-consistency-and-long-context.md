# 4. Staleness, Consistency and Long Context

## 4.1 Staleness Rule

如果召回对象的 source_version 落后于当前 story snapshot，则必须标记 stale。

stale context 不得进入 Writer Prompt，除非用于历史回顾并明确标记。

## 4.2 Dynamic Override Rule

动态状态覆盖静态状态。

示例：角色第 5 章失去法宝，则第 10 章不得从静态角色卡中召回该法宝作为当前持有物。

## 4.3 Long Context Policy

长上下文模型可用于 Memory / RAG 检查，但不得替代结构化状态。

长上下文输入必须记录：

- included_chapters
- included_summaries
- token_budget
- selection_reason
- omitted_ranges

## 4.4 Consistency Preflight

Writer 运行前必须检查：

- Memory Package 无 blocking stale item。
- 必要角色、地点、规则和 Beat 目标存在。
- forbidden_changes 已注入。
- unresolved hooks 与 beat_plan 不冲突。
