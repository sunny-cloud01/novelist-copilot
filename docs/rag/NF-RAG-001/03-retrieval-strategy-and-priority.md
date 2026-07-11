# 3. Retrieval Strategy and Priority

## 3.1 Retrieval Channels

Retrieval Service 必须组合：

- relational query
- Story Graph traversal
- vector retrieval
- evidence lookup
- rule lookup
- prior chapter summary
- long context pack

## 3.2 Priority Order

写作上下文优先级：

1. hard rules and forbidden changes
2. current character dynamic state
3. current relationship and conflict state
4. current location and timeline state
5. unresolved hooks and promised rewards
6. chapter and beat goal
7. genre playbook and rhythm target
8. style and expression constraints
9. supporting examples and evidence excerpts

## 3.3 Budget Trimming

上下文超限时，必须先压缩低优先级证据摘录，不得裁剪 hard rules、dynamic state 或 forbidden changes。

## 3.4 Retrieval Result Contract

每个召回结果至少包含：

- result_id
- object_id
- object_type
- relevance_reason
- confidence
- freshness
- evidence_refs
- source_channel
