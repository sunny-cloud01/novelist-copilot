# P2 打通线2真实生成（真规划 + story bible 真生成 + 多章 manuscript 回灌）Design

**Goal:** 让章节/分节规划由 LLM 基于 story bible + 拆书知识真实生成（无 key 确定性派生），story bible regenerate 在无前端 payload 时真调 LLM 生成候选，多章生成时上一章 manuscript state 真实回灌进下一章上下文 —— 使"AI 共建新书"从规划到多章连续成为真链路。

**背景（当前真实状态）**
- 规划是占位：`run_create_chapter_plan`（planning.py:241）只回填 `f"第{n}章规划"`/`f"第{n}章完成故事推进规划"`；`run_create_section_plans`（:279）只读回数量、完全不生成 section。都不调 LLM。section 全来自 seed fixture（写死乌坦城/三年之约）。
- story bible regenerate（phase_two_store.py:4181）：只把前端传入的 `story_bible_payload` 归一化回写，无 LLM 生成能力。
- manuscript state 硬编码：`_build_manuscript_state`（:5336）写死萧炎/三年之约，忽略真实草稿；`create_writing_run`（:4410）对 demo CHAPTER_PLAN_ID 短路，但对真实新章 plan 会真建 run（多章结构已支持）；memory package 不含上一章 state。
- 可复用基础设施：worker LLM 调用模式（extraction.py `_openai_json_completion`、provider_executor `_chat`）；P1 已建 `build_knowledge_context`（供规划注入拆书知识）；worker 经 `load_phase_two_store()` 调 core getter。

**决策（已确认）**
1. 三块全做：真规划（章节+分节 LLM 生成）、story bible 真生成候选、多章 manuscript state 真回灌下一章。
2. manuscript：accept 时从真实草稿+知识生成 state；下一章 create_writing_run 把上一章 state 注入 memory package 作前情。
3. 无 key：确定性从 story_bible/知识/章节号派生真实标题/beats/state，绝不回退乌坦城/三年之约写死。

**避开区域**：多书隔离/deep_analysis 由独立后台任务 task_62457d44 负责——本 tranche 不碰 `apply_task_execution_result` 的 deep_analysis 段与相关 merge helper。

---

## Task 1: worker LLM JSON helper（planning 复用）

**Files**
- Create `apps/ai-worker/worker/llm_json.py`
- Test `apps/ai-worker/tests/test_llm_json.py`

**Interfaces**
- Produces `generate_json(system: str, user: str, model_hint: str = "") -> dict | None`：读 `NOVELIST_LLM_BASE_URL`/`NOVELIST_LLM_API_KEY`，有则真调 `/chat/completions`（response_format json_object）返回解析 dict；无 key 或解析失败返回 None（调用方走确定性 fallback）。与 extraction._openai_json_completion 同模式但返回 None 而非抛异常，便于 fallback。

**验收**
- 无 key → 返回 None。
- mock HTTP 返回 JSON → 返回解析 dict。

## Task 2: 真章节规划（chapter plan LLM 生成）

**Files**
- Modify `apps/ai-worker/worker/planning.py`（`run_create_chapter_plan` :241）
- Test `apps/ai-worker/tests/test_planning_generation.py`（新建，避开 dramatiq：直接测生成 helper）

**Interfaces**
- Consumes `generate_json`（Task 1）、`store.build_knowledge_context`（P1）。
- Produces `_generate_chapter_plan(store, project, story_bible, chapter_index, knowledge_context) -> dict`：返回 `{"title": str, "summary": str}`。有 key 走 LLM（prompt 含 story bible premise/protagonist/core_conflict + knowledge_context + 章节号）；无 key 确定性派生（用 story bible premise + protagonist + 章节号拼出真实标题/摘要，非乌坦城）。

**做法**
- `run_create_chapter_plan` 从 store 拉 project → story_bible → `build_knowledge_context(project.allowed_knowledge_source_refs)`；调 `_generate_chapter_plan`；写入 chapter_plan.payload 的 title/summary（替换占位 fallback）。

**验收**
- 不同 story bible/章节号 → 不同真实标题（非"第N章规划"占位、非乌坦城）。
- 无 key 确定性、可复现。

## Task 3: 真分节规划（section plans LLM 生成）

**Files**
- Modify `apps/ai-worker/worker/planning.py`（`run_create_section_plans` :279）
- Test `apps/ai-worker/tests/test_planning_generation.py`（追加）

**Interfaces**
- Consumes `generate_json`、`build_knowledge_context`、`_generate_chapter_plan` 的上下文。
- Produces `_generate_section_plans(store, chapter_plan, story_bible, knowledge_context, section_count) -> list[dict]`：返回 section dict 列表，每个 `{section_index, planning_role, payload:{scene_goal, beats:[{index,summary}]}}`，section_plan_id 用稳定格式 `{chapter_plan_id}SEC{n}`。有 key LLM 生成 scene_goal+beats；无 key 确定性派生（setup/conflict/turn 三段式，scene_goal 从 chapter summary + knowledge 派生，非"建立乌坦城压抑氛围"写死）。

**做法**
- `run_create_section_plans` 若该 chapter 已有 seed section（demo CHAPTER_PLAN_ID）则保留（现有 demo 测试绿）；否则调 `_generate_section_plans` 写入 `STORE.section_plans_by_chapter[chapter_plan_id]`。

**验收**
- 真实新 chapter → 生成 section（非空、非乌坦城写死）。
- demo CHAPTER_PLAN_ID 行为不变。

## Task 4: story bible 真生成候选

**Files**
- Modify `apps/core-service/app/core/phase_two_store.py`（`apply_story_bible_action` regenerate 分支 :4181）
- Test `apps/core-service/tests/test_phase_three_api.py`

**Interfaces**
- Produces regenerate 分支：当 payload 未提供 `story_bible_payload` 时，用 LLM（经一个 core 侧 `_generate_story_bible_candidate(current_payload, note) -> dict | None` helper，同 generate_json 模式）从当前 payload + note 生成候选；无 key/无 LLM 时确定性增强当前 payload（如补强 world_rules/narrative_promises 而非原样回写）。提供了 story_bible_payload 时保持现有归一化回写行为。

**做法**
- core 侧新增轻量 `_llm_json(system, user)`（同 worker 模式，读同样 env），无 key 返回 None。
- regenerate：`explicit = (payload or {}).get("story_bible_payload")`；`next_payload = normalize(explicit)` if explicit else `normalize(_generate_story_bible_candidate(current) or _deterministic_enhance(current))`。

**验收**
- regenerate 无 explicit payload + 无 key → 候选与原版有差异（确定性增强），diff.changed_fields 非空。
- 提供 explicit payload → 行为不变（现有测试绿）。

## Task 5: 多章 manuscript state 真生成 + 回灌

**Files**
- Modify `apps/core-service/app/core/phase_two_store.py`（`_build_manuscript_state` :5336；`create_writing_run` :4394 memory 注入；`_build_memory_package` 或 writing 侧注入点）
- Test `apps/core-service/tests/test_phase_three_api.py`

**Interfaces**
- Produces `_build_manuscript_state`：从 writing_run 的真实 assembled_chapter/section_runs + chapter_plan + 项目知识生成 state（current_story_state.summary 用真实章节摘要，character/relationship/hook/prior_summary 从草稿与已确立设定派生），不再硬编码萧炎/三年之约。
- create_writing_run：查该 project 是否有已 accept 的上一章 manuscript state（`STORE.manuscript_states_by_project`），有则把其 prior_summary_pack + character/hook state 注入本次 memory package 的前情段（worker `_build_memory_package_payload` 已能读 project；此处在 core 侧把上一章 state ref 放进 writing_run 或 memory package 供 worker 读取）。

**做法**
- `_build_manuscript_state` 参数增加 writing_run 的真实输出；summary 用 `chapter_plan.payload.summary` + accepted ref；prior_summary_pack 从 assembled_chapter 分句摘要（确定性）或 LLM 摘要（有 key）。
- create_writing_run：`prior_state = STORE.manuscript_states_by_project.get(project_id)`；若存在，把 `prior_state.prior_summary_pack`/`current_story_state.summary` 写入新 writing_run 的一个 `prior_context` 字段；worker memory package 组装时读它拼进 knowledge_context 前情段。

**验收**
- accept 第1章后 manuscript state 反映真实章节（非萧炎写死）。
- 建第2章 writing_run → 其 memory/prior_context 含第1章 state 摘要。

---

## Global Constraints
- 不硬编码任何真实 API 密钥。
- 无 key 确定性 fallback，绝不崩、绝不回退乌坦城/三年之约/萧炎写死。
- HTTP API shape 不变；现有 demo（CHAPTER_PLAN_ID/WRITING_RUN_ID/STORY_BIBLE seed）测试仍绿。
- 不碰多书隔离/deep_analysis（后台任务 task_62457d44 范围）。
- worker 经 `load_phase_two_store()` 调 core getter，不新增跨服务 HTTP。
- 每任务 ≤2 迭代 / ~15 分钟。命令用 `rtk`；core-service 测试用其 `.venv`；worker 测试用 rtk python3（无 dramatiq 依赖的测试文件）。

## Verification
```
cd apps/ai-worker && rtk python3 -m pytest tests/test_llm_json.py tests/test_planning_generation.py -q
cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_three_api.py tests/test_phase_two_api.py tests/test_persistence.py -q
rtk pnpm --filter @novel-factory/web test --run
rtk pnpm --filter @novel-factory/contracts test
```
浏览器手验：新项目选知识源 → regenerate story bible 出候选 → planner 出真实章节/分节（非乌坦城）→ 生成第1章 accept → 建第2章 memory 含第1章前情。

## Done bar
- 章节/分节规划 LLM 生成（无 key 确定性派生），非写死乌坦城。
- story bible regenerate 无 explicit payload 时真生成候选。
- manuscript state 反映真实草稿，非硬编码萧炎。
- 多章：上一章 state 注入下一章上下文。
- 全量测试绿；现有 demo 测试仍绿。
