# P1 打通线2真实生成（RAG 注入 + 默认写作链真 LLM + 质量分去写死）Design

**Goal:** 让用户选定的拆书知识源真正进入新书章节生成上下文（RAG），默认写作链在配 key 时真调 LLM、无 key 时确定性 fallback，质量分从真实信号计算而非写死常量 —— 使"用拆书成果和 AI 共建生成章节正文"真正成立。

**背景（当前真实状态，三份审计 + 自读确认）**
- RAG 断链：`_build_memory_package_payload`（writing.py:304）只拼 `object://` ref 字符串，不加载知识内容；`project['allowed_knowledge_source_refs']` 在 worker 侧零引用；writer prompt（provider_executor.py）只含 chapter summary + section beats，无知识注入槽。
- 默认写作链是模板：`AnthropicWritingAdapter` 三方法纯 f-string 零 HTTP（provider_executor.py:47-111）。`OpenAICompatibleWritingAdapter` 继承它并 override 为真调 `_chat`（有 key 真 HTTP、无 key 回退 `user[:320]`）。
- 质量分写死：`ai_flavor_score=0.34/0.52`、`mobile_readability=0.74+节数*0.03`、`originality=0.91`（writing.py:412-414）。critic 默认硬编码一条"斗之气三段"issue（provider_executor.py:77-90）。
- 可复用数据源：core getter `list_knowledge_sources`/`list_knowledge_objects_for_run`/`get_graph_summary`/`list_evidence_for_book` 齐全；worker 经 `load_phase_two_store()` 拿同一 STORE 单例可直接调。

**决策（已确认）**
1. 范围：只做 RAG 注入 + 默认写作链真 LLM + 质量分去写死。真规划/story bible 真生成/多章 manuscript state 回灌留待 P2。
2. 默认 provider 改法：把真调逻辑（含无 key 确定性模板 fallback）下移到 `AnthropicWritingAdapter` 基类，让默认 anthropic 也能真调；不改默认 provider 名，向后兼容。

---

## Task 1: RAG — build_knowledge_context 检索器（core-service）

**Files**
- Modify `apps/core-service/app/core/phase_two_store.py`（在 `list_knowledge_sources` :3286 附近新增函数）
- Test `apps/core-service/tests/test_phase_two_api.py`

**Interfaces**
- Produces `build_knowledge_context(allowed_knowledge_source_refs: list[str], max_objects: int = 12, max_evidence: int = 6) -> dict`：从每个 `object://source-books/{book_id}` ref 解析 book_id → 找 latest run → 聚合 `list_knowledge_objects_for_run`（取 canonical_name/object_type/aliases/summary）+ `get_graph_summary`（nodes/edges 概要）+ `list_evidence_for_book`（excerpt 片段）。返回 `{"summary": str, "objects": [...], "graph": {...}, "evidence": [...], "context_text": str}`，其中 `context_text` 是拼好的可直接进 prompt 的中文知识块（含人物/势力清单、关系、证据摘录）。

**做法**
- 解析 ref：`book_id = ref.rsplit("/", 1)[-1]`；用 `_latest_extraction_run_for_book(book_id)` 拿 run_id。
- objects：每对象取 `canonical_name·object_type·aliases·payload.summary`。
- graph：`get_graph_summary(book_id)` 的 nodes label + 从 graph_node_details/neighbors 取若干关系（若无则跳过）。
- evidence：`list_evidence_for_book(book_id)[:max_evidence]` 的 excerpt。
- `context_text` 拼成分段中文：`【可用知识源】...【人物与势力】...【关系】...【原文摘录】...`；空源时返回空 context_text 与空列表，不报错。

**验收**
- 传 demo book 的 source_ref → context_text 含该书真实对象名与证据摘录，非空。
- 传空 list → 返回空 context_text 不崩。

## Task 2: memory package 载入真实知识（worker）

**Files**
- Modify `apps/ai-worker/worker/writing.py`（`_build_memory_package_payload` :304；`run_create_writing_run` :361 调用点）
- Test `apps/ai-worker/tests/test_writing.py`（或新建 test_writing_rag.py，避开 dramatiq 依赖：直接测 `_build_memory_package_payload`）

**Interfaces**
- Consumes `build_knowledge_context`（Task 1，经 store 调用）。
- Produces `_build_memory_package_payload` 返回增加 `knowledge_context: str` 与 `knowledge_object_count: int`；`run_create_writing_run` 把该 context 传入 pipeline。

**做法**
- `_build_memory_package_payload` 读 `project.get("allowed_knowledge_source_refs", [])`；调 `store.build_knowledge_context(refs)`；把 `context["context_text"]` 放进返回的 `knowledge_context`，source_refs 补上真实 source refs（现有 story-bible/chapter-plan/section-plan ref 保留，删除"取第一个 graph_summary"的 hack 改为按项目知识源）。
- `run_create_writing_run` 把 `memory_package["knowledge_context"]` 通过 `execute_writing_provider_pipeline(..., knowledge_context=...)` 传下去（Task 3 接收）。

**验收**
- project 有 allowed_knowledge_source_refs 时 memory_package.knowledge_context 含真实知识文本。
- 无知识源时 knowledge_context 为空串，链路不崩。

## Task 3: 默认 adapter 真调 LLM + 注入知识（worker）

**Files**
- Modify `apps/ai-worker/worker/provider_executor.py`（`_chat` 下移到基类 `AnthropicWritingAdapter`；三方法接收 `knowledge_context`；`execute_writing_provider_pipeline` 签名加 `knowledge_context` 并透传）
- Test `apps/ai-worker/tests/test_provider_executor.py`（新建，避开 dramatiq）

**做法**
- 把 `_chat` 从 `OpenAICompatibleWritingAdapter` 上移到 `AnthropicWritingAdapter`（无 key 时 fallback 从 `user[:320]` 改为返回确定性模板：复用原 f-string 结构，保证无 key 也出可读中文而非截断）。`OpenAICompatibleWritingAdapter` 保留为语义别名（继承即可，未来可覆盖 anthropic 专用 endpoint）。
- `draft_section` / `humanize_section` 新增可选参数 `knowledge_context: str = ""`；把它拼进 user prompt 的"【世界观与知识】"段（有内容才加）。system prompt 增加"必须遵循给定世界观与已确立设定，不得引入矛盾"。
- `review_sections` 的默认硬编码"斗之气三段" issue：改为无 key/无真实模型时返回空 issue（PASS），有真实模型时走 `_chat` 判定——去掉写死的境界 issue（它对新书无意义）。
- `execute_writing_provider_pipeline` 签名加 `knowledge_context: str = ""`，`draft_section`/`humanize_section` 调用点透传。

**验收**
- mock `NOVELIST_LLM_BASE_URL`/`API_KEY` + fake HTTP → draft user prompt 含 knowledge_context 段。
- 无 key → 返回确定性模板（非硬编码斗破苍穹 issue），review 返回空 issue。

## Task 4: 质量分去写死（worker）

**Files**
- Modify `apps/ai-worker/worker/writing.py`（:412-414 质量分）
- Test `apps/ai-worker/tests/test_writing.py`（新增单元测试直接测打分 helper）

**做法**
- 抽出 `_compute_quality_scores(section_runs, blocking_issue_count) -> dict`：
  - `ai_flavor_score`：基于真实文本信号（句长方差、重复率、beat 覆盖）而非二值常量。给一个确定性但内容相关的启发式（如：重复短语比例低→分高），范围 0-1。
  - `mobile_readability_score`：基于平均段落/句长的启发式（不再是纯节数线性）。
  - `originality_safety_score`：基于 knowledge_context 命中禁用相似点检查的启发式（无则给保守默认）。
- 保留 blocking_issue_count 影响，但分数与真实草稿内容相关。

**验收**
- 不同草稿内容 → 分数不同（不再恒 0.34/0.52/0.91）。
- 现有 writing 测试仍绿（放宽精确值断言为范围/单调性）。

---

## Global Constraints
- 不硬编码任何真实 API 密钥。
- 无 key 时确定性 fallback，绝不崩、不静默 file fallback。
- 保持 HTTP API shape 不变；现有 demo（CHAPTER_PLAN_ID/WRITING_RUN_ID seed）相关测试仍绿。
- worker 经 `load_phase_two_store()` 调 core getter，不新增跨服务 HTTP。
- 每任务 ≤2 迭代 / ~15 分钟。命令用 `rtk` 前缀；core-service 测试用其 `.venv`（有 fastapi/pytest），worker 无 dramatiq 依赖的测试用 rtk python3。

## Verification
```
cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_two_api.py -q
cd apps/ai-worker && rtk python3 -m pytest tests/test_provider_executor.py tests/test_writing_rag.py -q   # 新建、无 dramatiq 依赖
rtk pnpm --filter @novel-factory/web test --run
```
浏览器手验：给项目选知识源 → 配 NOVELIST_LLM_BASE_URL/API_KEY → 生成章节 → 写作工作台的草稿/记忆包体现该书知识；不配 key 走确定性 fallback 不崩。

## Done bar
- 拆书知识经 build_knowledge_context 真正进入 writer prompt。
- 默认写作链配 key 真调 LLM、无 key 确定性 fallback。
- critic 不再对新书返回写死斗破苍穹 issue。
- 质量分与真实草稿内容相关，非写死常量。
- 全量测试绿；现有 demo 测试仍绿。
- P2 待办（不在本 tranche）：真章节/分节 LLM 规划、story bible 真生成候选、多章 manuscript state 回灌下一章。
