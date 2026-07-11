# 3. Core Modules

## 3.1 Creator Workspace

目标：为个人创作者提供从上传参考作品到生成原创章节的统一入口。

核心功能：最近项目、运行任务、待处理阻塞项、继续生成、章节批准和反馈摘要。

## 3.2 Source Library

目标：存放所有用于拆书分析的原始作品。

基础字段：id、title、author、platform、genre、tags、word_count、completion_status、rating、source、download_url。

核心功能：上传作品、填写来源信息、分类、标签管理、搜索、去重和自动分析。

## 3.3 Auto Book Analysis Engine

目标：自动把一本小说拆成 AI 可学习、可追踪、可落库的数据。

拆分维度：世界观、人物、势力、地图、修炼体系、剧情、节奏、爽点、反转、伏笔、悬念、战斗、感情线、日常剧情。

章节级输出：chapter、scene、event、conflict、emotion、reward、hook、climax。

Creator 默认不逐项审核拆书结果。系统只在低置信度、冲突、证据缺失或解析失败时打断 Creator。

## 3.4 Knowledge Base

目标：按知识分类，而不是按书分类。

知识库至少包含 Character Library、Worldview Library、Faction Library、Location Library、Pattern Library、Rhythm Profile Library 和 Asset Library。

## 3.5 Story Bible Engine

目标：基于 Creator 输入、原创边界、已批准知识包和题材目标，生成新书世界观与设定草稿。

输出至少包含 world rules、power system、factions、protagonist、core cast、main conflict、volume direction、style target 和 forbidden similarities。

Creator 负责确认设定方向和原创边界，不需要从零手写完整世界观。

## 3.6 Pattern Library

目标：把常见网文套路抽象成可参数化流程。

所有 Pattern 必须支持参数化、组合、替换角色、替换地点和替换目标。

## 3.7 Rhythm Engine

目标：量化小说节奏。

每章统计 climax_index、conflict_index、dialogue_ratio、description_ratio、battle_ratio、information_density、suspense_index 和 reward_count。

## 3.8 Prompt Engine

目标：管理 Prompt 模板并支持动态拼接。

模板类型包括人物 Prompt、世界 Prompt、剧情 Prompt、章节 Prompt、对白 Prompt、战斗 Prompt 和结尾 Prompt。

## 3.9 One-Click Chapter Engine

目标：让 Creator 通过一个主操作生成约 3000 字章节草稿。

系统内部可以使用 chapter_plan、scene_plan、beat_plan、memory_package、prompt_package、critic_report、humanizer_report 和 quality_report，但默认不要求 Creator 逐 Beat 推进。

## 3.10 Asset Library

目标：存放最小创作单位。

素材类型包括动作、心理、环境、天气、物品和台词片段。

## 3.11 Feedback Loop

目标：持续优化 AI 生成质量。

记录 Prompt 效果、章节评分、AI 错误、人工修改、重复率、读者反馈和热门章节。

输出 Prompt Ranking、Pattern Ranking 和 Knowledge Ranking。

## 3.12 Rule Engine

目标：保证长篇小说一致性。

规则类型包括人物规则、时间规则、地图规则、境界规则、法宝规则、年龄规则、势力规则、世界规则和伏笔规则。

示例规则：境界不能倒退、法宝唯一、人物不能瞬移、时间线必须连续、已死亡角色不能再次出现。
