# 3. Agent Roles

## 3.1 Ingestion Agent

职责：导入原始作品、执行基础清洗、生成章节候选和预处理报告。

## 3.2 Extraction Agent

职责：按 NF-NKS-100 抽取 Scene、Entity、Event、Relationship、Pattern、Rhythm Profile 和 Rule。

## 3.3 Normalization Agent

职责：执行别名归一化、对象合并、ID 分配和候选冲突标记。

## 3.4 Graph Agent

职责：建立和验证 Story Graph 节点与关系。

## 3.5 Consistency Agent

职责：检查人物、时间线、地点、境界、法宝、势力、伏笔和世界规则一致性。

## 3.6 Planning Agent

职责：基于知识库、Story Graph、Pattern 和 Rhythm Profile 生成大纲、卷纲和章节计划。

## 3.7 Scene Planning Agent

职责：将章节计划拆分为 Scene 和 Beat，标记 POV、冲突压力、爽点、悬念、节奏目标和参与角色心理位置。

## 3.8 Style Analyzer Agent

职责：在 Writer 之前生成 Style Profile，分析句长分布、段落长度、POV 纯度、修辞偏好、对白比例和 NF-NKS-280 表达分类约束。

## 3.9 Writer Agent

职责：生成章节草稿或内部 Section/Beat 初稿。Creator-facing 交互可以是一键生成章节，但 Writer Agent 必须遵守系统内部的 Scene、Beat、Section、Memory Package 和 forbidden_changes，不得改写已批准设定。

## 3.10 Critic Agent

职责：对每个 Beat 执行结构化反向检查，输出 failed_check_ids、严重级别、问题位置和重写要求。

## 3.11 Memory Agent

职责：按 NF-RAG-001 为 Writer 和 Critic 提供结构化 Memory Package，包含角色动态状态、关系、物品、战力、地点、伏笔和前文摘要。

## 3.12 Humanizer Agent

职责：在不改变事实和剧情目标的前提下，执行句式长短重组、段落切碎、口语化拟真、去机械转场和低 AI 味改写。

## 3.13 Generation Agent

职责：生成章节草稿、局部改写和润色候选。

Generation Agent 是通用生成角色；写作流水线中的具体成稿职责优先由 Writer Agent、Critic Agent 和 Humanizer Agent 承担。

## 3.14 Review Agent

职责：按 NF-QA-001 执行写作质量门禁、AI 味检查、人味检查和人工审核辅助。

## 3.15 Feedback Agent

职责：按 NF-NKS-290 分析人工修改、读者反馈、评分和质量信号，并更新反馈知识和排名建议。

## 3.16 Model Assignment Rule

Agent role 不得在代码或 Prompt 中硬编码具体供应商模型。

每个 Agent task 必须通过 NF-LLM-001 定义的 Agent Model Assignment 和 Model Router 解析 model_profile_id。MVP 阶段允许所有 Agent 共享一个 default model_profile；后续可以按 Agent role、task_type、output_mode、genre 和质量/成本策略拆分为不同模型。
