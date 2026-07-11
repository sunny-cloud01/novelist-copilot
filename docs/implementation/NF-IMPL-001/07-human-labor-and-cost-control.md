# 7. Human Labor and Cost Control

## 7.1 Labor Control Principle

产品目标不是完全无人写作，而是把人工集中在高价值判断上。

人工负责：

- 审核关键知识和冲突合并。
- 决定原创项目方向、题材、人物关系和风格边界。
- 处理 blocking quality issue。
- 审核反馈驱动的策略变更。
- 把少量关键章节调到最终审美标准。

系统负责：

- 批量抽取、归一化和证据绑定。
- 结构化规划和 Beat 拆分。
- 生成、Critic、Humanizer 和质量报告。
- 一致性检查、AI 味检查和手机阅读检查。
- 成本统计、反馈归因和策略建议。

## 7.2 Human Review Budget

第一阶段建议目标：

| Stage                | Human Review Target                        |
| -------------------- | ------------------------------------------ |
| Knowledge extraction | 只审高置信冲突、主角、核心规则和高影响对象 |
| Chapter planning     | 审核章纲和关键 Beat，不逐句改写计划        |
| Beat drafting        | 只处理自动重写失败或 blocking issue        |
| Chapter approval     | 重点审开头、高潮、结尾和一致性报告         |
| Feedback promotion   | 人工批准策略变更，不人工处理每条低风险反馈 |

## 7.3 Cost Control

必须记录：

- prompt_tokens
- completion_tokens
- retry_count
- rewrite_count
- model_profile_id
- accepted_output_ratio
- human_edit_distance
- quality_score
- model_cost_quality_ratio

低质量高成本路线必须自动降权或进入人工配置审查。

## 7.4 Automation Safety

可以自动执行：

- 低风险重写。
- forbidden phrase 替换建议。
- Memory Package 重新组装。
- stale context 拦截。
- 质量报告生成。

不得自动执行：

- 覆盖 Approved Knowledge。
- 改变核心设定。
- 发布章节。
- promotion blocking feedback。
- 大规模改变项目风格。
