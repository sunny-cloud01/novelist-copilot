# 4. Narration Style and Genre Expression

## 4.1 Narration Expression Types

叙述表达类型描述非对白文本的功能。

允许初始类型：

- scene_opening
- sensory_anchor
- tension_building
- emotional_interiority
- action_continuity
- information_reveal
- setting_exposition
- reward_delivery
- aftermath_reflection
- transition_bridge
- cliffhanger_close
- hook_reinforcement

## 4.2 Genre Expression Scope

genre_expression 用于记录题材表达习惯。

允许初始 genre_scope：

- xuanhuan
- xianxia
- urban
- sci_fi
- suspense
- historical
- romance
- game_system

每个 genre_expression 必须说明适用题材、禁用题材和典型使用场景。

## 4.3 Style Constraint Types

Style Constraint 表示生成文本的风格约束。

允许初始类型：

- plain_direct
- fast_paced
- restrained_emotional
- vivid_sensory
- ancient_formal
- modern_colloquial
- comedic_light
- brutal_fast
- lyrical_reflective
- dense_information

## 4.4 Rhythm Compatibility

Expression Type 必须能与 Rhythm Profile 协同使用。

示例：

- 高 climax_index 场景优先使用 action_continuity、reward_delivery 和 tension_building。
- 低 information_density 缓冲段落可以使用 aftermath_reflection 和 sensory_anchor。
- 高 suspense_index 章节结尾可以使用 cliffhanger_close 和 hook_reinforcement。

## 4.5 Genre Boundary Rules

- 题材表达不得替代 Worldview、Power System 或 Rule。
- 题材表达不得引入未经审核的新设定。
- style_tags 必须来自受控词表或已批准 Expression Type。
- 同一作品内的 genre_expression 应保持稳定，除非 generation_request 明确要求风格切换。
