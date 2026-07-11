# 3. Composition, Validation and Change Log

## 3.1 Composition Rules

Pattern 可以组合，但必须满足：

- 前一个 Pattern 的结果可作为后一个 Pattern 的前置条件。
- Slot 类型必须兼容。
- Rhythm Profile 不得连续堆叠高峰值而无缓冲。
- 同一章节内不得重复使用语义相同的 Reward，除非目标是强化同一爽点。

## 3.2 Validation Rules

Pattern 必须满足：

- 每个 Pattern 至少包含三个 Step。
- 每个 required slot 必须被填充。
- 每个 Step 必须绑定预期 Event、Conflict、Hook 或 Reward。
- Pattern 来源必须有 evidence 或人工定义记录。

## 3.3 Boundaries

NF-NKS-240 定义 Pattern 语义，不定义 Prompt 拼接格式。Prompt 拼接由 NF-PROMPT 文档负责。

## 3.4 Change Log

| Version | Date       | Author                                   | Change                                 |
| ------- | ---------- | ---------------------------------------- | -------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial Pattern Library specification. |
