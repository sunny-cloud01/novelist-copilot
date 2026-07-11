# 4. Style, Memory and Context Injection

## 4.1 Style Analyzer Position

Style Analyzer 必须在 Writer 之前运行。

Style 不应只作为事后润色，而应在 Writer 动笔前注入为 System Prompt、few-shot guidance、style constraints 和 negative constraints。

## 4.2 Style Profile

Style Profile 至少包含：

- sentence_length_distribution
- paragraph_length_distribution
- verb_noun_ratio
- dialogue_ratio_target
- action_description_ratio
- interiority_ratio
- pov_purity
- metaphor_density
- diction_level
- rhythm_pattern
- preferred_expression_type_refs
- forbidden_expression_type_refs
- anti_ai_expression_refs

## 4.3 Few Shot Selection

Few-shot 选择必须满足：

- 与当前 genre_scope 兼容。
- 与当前 scene_type 兼容。
- 与 pov_character 兼容。
- 与 beat_goal 兼容。
- 来源已授权、内部自有或可安全使用。
- 片段长度受控，不得作为复制对象。

Few-shot 的目的不是复制文本，而是帮助模型理解节奏、句式、POV 和表达功能。

## 4.4 Prompt Injection Order

Writer Prompt 的上下文注入顺序：

1. hard rules and forbidden changes
2. Memory Package
3. Beat Plan
4. Style Profile
5. Expression Taxonomy constraints
6. selected few-shot guidance
7. output contract

## 4.5 Negative Constraints

Writer Prompt 必须注入：

- 禁止总结性旁白。
- 禁止段落结尾升华主题。
- 禁止泛化情绪标签替代动作。
- 禁止机械转场。
- 禁止高频 AI 词和陈词滥调。
- 禁止角色说出不符合 voice_profile 的书面语。

Negative constraints 应引用 NF-NKS-280 的 anti_ai_expression 和 NF-NKS-270 的 Rule。
