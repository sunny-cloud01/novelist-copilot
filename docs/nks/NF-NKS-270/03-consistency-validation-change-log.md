# 3. Consistency, Validation and Change Log

## 3.1 Consistency Examples

系统必须支持检查：

- 已死亡角色不能无解释再次出现。
- Character 不能使用超过 capability_state 的能力。
- Artifact 的唯一性不能被破坏。
- Location 移动必须符合时间线和空间规则。
- Foreshadowing 必须在合理范围内兑现、延迟或明确保留。
- Faction 关系变化必须有事件解释。

## 3.2 Validation Rules

Rule Knowledge 必须满足：

- 每条 Rule 必须有 scope。
- 每条 Constraint 必须能被人工或系统解释。
- Violation Record 不得直接修改源知识，只能提出 recommended_action。
- 高严重级别 violation 必须进入人工审核。

## 3.3 Boundaries

NF-NKS-270 定义规则和一致性知识语义。Consistency Engine 的运行架构由 NF-ARCH 文档定义，数据库存储由 NF-DBS 文档定义。

## 3.4 Change Log

| Version | Date       | Author                                   | Change                                                |
| ------- | ---------- | ---------------------------------------- | ----------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial rule and consistency knowledge specification. |
