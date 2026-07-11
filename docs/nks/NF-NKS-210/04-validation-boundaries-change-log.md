# 4. Validation, Boundaries and Change Log

## 4.1 Validation Rules

Character 知识必须满足：

- 每个 Character 必须有稳定 character_id。
- 每个 Alias 必须指向一个 Character 或 unresolved candidate。
- Character State 必须绑定 temporal_scope。
- Relationship 的 source 和 target 必须存在。
- 关系变化必须绑定 evidence 或 trigger_event_id。

## 4.2 Boundaries

NF-NKS-210 定义角色与关系知识模型，不定义数据库字段类型或 Prompt 文案。

## 4.3 References

- NF-NKS-000
- NF-NKS-100
- NF-NKS-200

## 4.4 Change Log

| Version | Date       | Author                                   | Change                                            |
| ------- | ---------- | ---------------------------------------- | ------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial Character and Relationship specification. |
