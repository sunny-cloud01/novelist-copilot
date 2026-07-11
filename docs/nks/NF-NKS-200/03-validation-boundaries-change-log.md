# 3. Validation, Boundaries and Change Log

## 3.1 Validation Rules

Story Graph 必须满足：

- 每个 node.object_id 指向已存在对象。
- 每条 edge 的 source_object_id 和 target_object_id 均存在。
- 每条关系必须绑定至少一条 evidence 或 review record。
- 关系变化不得覆盖历史关系。
- Deprecated 对象不得进入新的 generation context，除非用于历史回溯。

## 3.2 Boundaries

NF-NKS-200 定义图语义，不定义图数据库 Schema。数据库落地由 NF-DBS 文档负责。

## 3.3 References

- NF-NKS-000
- NF-NKS-001
- NF-NKS-100
- NF-DBS-001

## 3.4 Change Log

| Version | Date       | Author                                   | Change                                   |
| ------- | ---------- | ---------------------------------------- | ---------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial Story Graph model specification. |
