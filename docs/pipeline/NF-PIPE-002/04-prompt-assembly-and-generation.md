# 4. Prompt Assembly and Generation

## 4.1 Prompt Assembly

Prompt Assembly Service 根据 NF-PROMPT-001 创建 Prompt Package。

Prompt Package 必须包含：

- metadata
- template_ref
- variables
- knowledge_refs
- graph_refs
- constraints
- output_contract
- evaluation_rules
- assembly_log

Prompt Package 必须保存 prompt_package_id 和 prompt_ref，便于复现生成结果。

## 4.2 Prompt Budget Rule

Prompt Assembly 必须控制上下文预算。

优先级顺序：

1. hard constraints and forbidden changes
2. character state and active relationship pressure
3. chapter goal and scene goals
4. unresolved hooks and expected rewards
5. world rules and consistency constraints
6. rhythm target
7. relevant pattern steps
8. supporting assets and style references

当上下文超限时，低优先级内容必须被摘要、裁剪或转为 retrieval hint。

## 4.3 Draft Generation

Draft Generation 调用 LLM provider adapter，生成 Draft Candidate。

每个 Draft Candidate 必须记录：

- draft_id
- generation_request_id
- prompt_package_id
- provider
- model
- model_version
- output_ref
- token_usage
- latency
- status

## 4.4 Human Flavor Requirements

生成任务必须明确避免机械 AI 味。

Prompt Package 应提供：

- 角色当下的欲望、误解、秘密和压力。
- 场景内的具体动作和感官锚点。
- 对白的角色立场差异。
- 情绪推进，而不是只给剧情说明。
- 章节节奏目标和必要留白。
- 需要回避的套路化表达或重复句式。

## 4.5 Draft Versioning

同一个 generation_request 可以产生多个 draft candidate。

Draft 不得覆盖，必须通过 version 或 parent_draft_id 形成修订链。
