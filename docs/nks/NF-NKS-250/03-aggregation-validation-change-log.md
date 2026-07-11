# 3. Aggregation, Validation and Change Log

## 3.1 Aggregation Rules

Rhythm Profile 可按以下范围聚合：

- Scene
- Chapter
- Volume
- Book
- Pattern
- Generation Plan

聚合时必须保留来源范围，禁止将 Book 级指标直接替代 Chapter 级指标。

## 3.2 Generation Constraints

生成系统使用 Rhythm Profile 时必须满足：

- 高 climax_index 后必须允许缓冲段落，除非目标风格要求连续高压。
- reward_count 不得与 Hook resolution 完全脱节。
- information_density 过高时必须降低新设定引入速度。
- battle_ratio 必须符合题材和章节目标。

## 3.3 Validation Rules

Rhythm Profile 必须满足：

- scope_type 和 scope_id 必须存在。
- 指标必须有稳定取值范围。
- 高强度指标必须能追溯到 Event、Conflict、Reward、Hook 或 Climax。
- 自动计算结果必须记录 extractor 或 evaluator 版本。

## 3.4 Change Log

| Version | Date       | Author                                   | Change                                |
| ------- | ---------- | ---------------------------------------- | ------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Knowledge Engineering Team | Initial Rhythm Profile specification. |
