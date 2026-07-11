# 3. Template Types

## 3.1 Extraction Prompt

用于从原文中抽取对象、关系、证据和规则。

## 3.2 Normalization Prompt

用于归一化别名、合并候选对象、识别重复对象。

## 3.3 Planning Prompt

用于生成大纲、卷纲、章节计划和剧情阶段。

## 3.3.1 Scene Planning Prompt

用于将章节计划拆解为 Scene 和 Beat，并输出 POV、冲突压力、爽点、悬念、节奏目标和每个 Beat 的写作目标。

## 3.3.2 Style Analysis Prompt

用于生成 Style Profile。输出必须引用 NF-NKS-280 的 Expression Type、Speaker Voice Profile、Style Constraint 和 anti_ai_expression。

## 3.4 Character Prompt

用于表达角色状态、动机、能力、口吻和行为约束。

角色口吻必须优先引用 NF-NKS-280 的 Speaker Voice Profile 或 Expression Type，不得在 Prompt 模板中临时发明口吻分类。

## 3.5 World Prompt

用于表达世界观、地点、势力、资源和力量体系规则。

## 3.6 Chapter Prompt

用于生成章节草稿。

Chapter Prompt 在 Creator-facing 交互中应支持一键生成约 3000 字章节。Prompt 结构内部仍应携带 Scene、Beat 或 Section 计划，以便模型按受控结构生成、检查和重写；当上下文或质量风险较高时，可降级为分段输出。

## 3.7 Dialogue Prompt

用于生成或修订对白。

Dialogue Prompt 必须使用 NF-NKS-280 定义的 dialogue_expression、tone_tags 和 anti_ai_expression 作为受控分类。

## 3.8 Battle Prompt

用于生成战斗、冲突和动作段落。

## 3.9 Review Prompt

用于质量检测、一致性检查、重复率检查和问题总结。

## 3.9.1 Critic Prompt

用于对 Beat Draft 执行结构化反向检查。输出必须包含 failed_check_ids、severity、affected_text_refs、required_changes 和 retry_guidance。

## 3.10 Revision Prompt

用于根据 Review Report 和人工意见进行局部修订。

## 3.11 Humanizer Prompt

用于在不改变事实和剧情目标的前提下，执行句式长短重组、段落切碎、口语化拟真、机械转场削减和 AI 味降低。
