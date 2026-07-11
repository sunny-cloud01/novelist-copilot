# 4. Validation, Boundaries and Change Log

## 4.1 Validation Rules

World knowledge 必须满足：

- 每个 Location 必须属于一个 Worldview 或上级 Location。
- Power System 的 level_sequence 必须有稳定顺序。
- Character 的 capability_state 不得跳过不可跳过等级。
- Faction 的成员和敌友关系必须引用存在对象。
- Resource 的 scarcity 和 usage_rule 必须可解释。

## 4.2 Boundaries

NF-NKS-220 定义世界、地点、势力、力量和资源语义，不定义存储引擎或界面展示。

## 4.3 References

- NF-NKS-000
- NF-NKS-100
- NF-NKS-200
- NF-NKS-210

## 4.4 Change Log

| Version | Date       | Author                                   | Change                                        |
| ------- | ---------- | ---------------------------------------- | --------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial world knowledge module specification. |
