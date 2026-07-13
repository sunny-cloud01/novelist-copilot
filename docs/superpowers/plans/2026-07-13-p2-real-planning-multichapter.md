# P2 打通线2真实生成 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** 章节/分节规划 LLM 生成（无 key 确定性派生），story bible regenerate 真生成候选，多章 manuscript state 反映真实草稿并回灌下一章。

**Architecture:** 新增 worker `generate_json` LLM helper（有 key 真调、无 key 返 None）；planning 两函数改为拉 story bible + build_knowledge_context 后生成真实章节标题/分节 beats；core story bible regenerate 无 explicit payload 时 LLM/确定性生成候选；`_build_manuscript_state` 从真实草稿派生、create_writing_run 把上一章 state 注入新章 memory。

**Tech Stack:** Python 3.11（ai-worker worker/、core-service app/），pytest，内存 CoreStore 单例（worker 经 load_phase_two_store 共享）。

## Global Constraints
- 不硬编码任何真实 API 密钥。
- 无 key 确定性 fallback，绝不崩、绝不回退乌坦城/三年之约/萧炎写死。
- HTTP API shape 不变；现有 demo（CHAPTER_PLAN_ID/WRITING_RUN_ID/STORY_BIBLE_ID seed）测试仍绿。
- 不碰多书隔离/deep_analysis（后台任务 task_62457d44 范围）：不改 apply_task_execution_result 的 deep_analysis 段、不加 _merge_book_scoped。
- worker 经 load_phase_two_store() 调 core getter，不新增跨服务 HTTP。
- 每任务 ≤2 迭代 / ~15 分钟。命令用 rtk；core-service 测试用其 .venv；worker 无 dramatiq 依赖的测试用 rtk python3。
- 跑测试时构建工具可能污染 pyproject.toml / uv.lock，提交前只 git add 真正改的文件，其余 git checkout/rm 还原。

---

### Task 1: worker LLM JSON helper

**Files:**
- Create: `apps/ai-worker/worker/llm_json.py`
- Test: `apps/ai-worker/tests/test_llm_json.py`

**Interfaces:**
- Produces: `generate_json(system: str, user: str, model_name: str = "deepseek-chat") -> dict | None`。

- [ ] **Step 1: 写失败测试**

新建 `apps/ai-worker/tests/test_llm_json.py`：

```python
import json
import worker.llm_json as llm_json
from worker.llm_json import generate_json


def test_generate_json_returns_none_without_key(monkeypatch):
    monkeypatch.delenv("NOVELIST_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("NOVELIST_LLM_API_KEY", raising=False)
    assert generate_json("s", "u") is None


def test_generate_json_parses_model_response(monkeypatch):
    monkeypatch.setenv("NOVELIST_LLM_BASE_URL", "http://fake")
    monkeypatch.setenv("NOVELIST_LLM_API_KEY", "k")

    class FakeResp:
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
        def read(self):
            return json.dumps({"choices": [{"message": {"content": '{"title": "开端"}'}}]}).encode("utf-8")

    monkeypatch.setattr(llm_json, "urlopen", lambda *a, **k: FakeResp())
    result = generate_json("s", "u")
    assert result == {"title": "开端"}


def test_generate_json_returns_none_on_bad_json(monkeypatch):
    monkeypatch.setenv("NOVELIST_LLM_BASE_URL", "http://fake")
    monkeypatch.setenv("NOVELIST_LLM_API_KEY", "k")

    class FakeResp:
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
        def read(self):
            return json.dumps({"choices": [{"message": {"content": "not json"}}]}).encode("utf-8")

    monkeypatch.setattr(llm_json, "urlopen", lambda *a, **k: FakeResp())
    assert generate_json("s", "u") is None
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_llm_json.py -q`
Expected: FAIL — 找不到 `worker.llm_json`

- [ ] **Step 3: 实现 helper**

新建 `apps/ai-worker/worker/llm_json.py`：

```python
from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _strip_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def generate_json(system: str, user: str, model_name: str = "deepseek-chat") -> dict[str, Any] | None:
    base_url = os.getenv("NOVELIST_LLM_BASE_URL")
    api_key = os.getenv("NOVELIST_LLM_API_KEY")
    if not base_url or not api_key:
        return None
    endpoint = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": model_name,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.5,
        "max_tokens": 1200,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")
    request = Request(
        endpoint,
        data=body,
        headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = payload["choices"][0]["message"]["content"]
        parsed = json.loads(_strip_fence(content))
        return parsed if isinstance(parsed, dict) else None
    except (HTTPError, URLError, TimeoutError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        return None
```

- [ ] **Step 4: 运行确认通过**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_llm_json.py -q`
Expected: PASS (3 passed)

- [ ] **Step 5: 提交**

```bash
git add apps/ai-worker/worker/llm_json.py apps/ai-worker/tests/test_llm_json.py
git commit -m "feat: add worker generate_json LLM helper with none fallback"
```

---

### Task 2: 真章节规划

**Files:**
- Modify: `apps/ai-worker/worker/planning.py`（`run_create_chapter_plan` :241，前面新增 helper）
- Test: `apps/ai-worker/tests/test_planning_generation.py`（新建）

**Interfaces:**
- Consumes: `generate_json`（Task 1）。
- Produces: `_generate_chapter_plan(story_bible: dict | None, chapter_index: int, knowledge_context: str) -> dict` → `{"title": str, "summary": str}`。

- [ ] **Step 1: 写失败测试**

新建 `apps/ai-worker/tests/test_planning_generation.py`：

```python
from worker.planning import _generate_chapter_plan


def test_chapter_plan_deterministic_without_key(monkeypatch):
    monkeypatch.delenv("NOVELIST_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("NOVELIST_LLM_API_KEY", raising=False)
    bible = {"payload": {"premise": "少年林澈踏入修行界", "protagonist": "林澈", "core_conflict": "底层修士与宗门规则"}}
    plan = _generate_chapter_plan(bible, 2, "【人物与势力】- 云岚宗[faction]")
    assert plan["title"] and plan["summary"]
    assert "乌坦城" not in plan["title"]
    assert "林澈" in plan["summary"] or "林澈" in plan["title"]


def test_chapter_plan_varies_by_index(monkeypatch):
    monkeypatch.delenv("NOVELIST_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("NOVELIST_LLM_API_KEY", raising=False)
    bible = {"payload": {"premise": "p", "protagonist": "林澈", "core_conflict": "c"}}
    assert _generate_chapter_plan(bible, 1, "")["summary"] != _generate_chapter_plan(bible, 3, "")["summary"]
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_planning_generation.py -q`
Expected: FAIL — `cannot import name '_generate_chapter_plan'`

- [ ] **Step 3: 实现 helper + 接入**

在 `apps/ai-worker/worker/planning.py` 顶部 import 加：

```python
from worker.llm_json import generate_json
```

在 `run_create_chapter_plan`（:241）之前插入：

```python
def _generate_chapter_plan(story_bible: dict[str, Any] | None, chapter_index: int, knowledge_context: str) -> dict[str, Any]:
    bible_payload = (story_bible or {}).get("payload", {})
    premise = bible_payload.get("premise", "")
    protagonist = bible_payload.get("protagonist", "主角")
    core_conflict = bible_payload.get("core_conflict", "")
    knowledge_block = f"\n【可用拆书知识】\n{knowledge_context}\n" if knowledge_context.strip() else ""
    generated = generate_json(
        system="你是中文网文章节规划师。基于故事圣经与已确立设定，为指定章节输出规划。只输出 JSON：{\"title\":\"章节标题\",\"summary\":\"本章推进摘要\"}，不要解释。",
        user=f"故事前提：{premise}\n主角：{protagonist}\n核心冲突：{core_conflict}\n当前章节：第{chapter_index}章{knowledge_block}",
    )
    if generated and isinstance(generated.get("title"), str) and generated.get("title").strip():
        return {"title": generated["title"].strip(), "summary": str(generated.get("summary", "")).strip() or f"{protagonist}在第{chapter_index}章推进{core_conflict or premise}。"}
    # 确定性 fallback：从 story bible 派生，非乌坦城写死
    stage = ["铺垫", "冲突", "转折", "推进", "高潮"][min(chapter_index - 1, 4)]
    return {
        "title": f"{protagonist}·第{chapter_index}章·{stage}",
        "summary": f"{protagonist}在第{chapter_index}章围绕「{core_conflict or premise}」展开{stage}，推进主线。",
    }
```

将 `run_create_chapter_plan` 的 chapter_plan payload 回填段（:252-259）替换为：

```python
    if chapter_plan:
        project = store.STORE.novel_projects.get(command["project_id"])
        story_bible = store.STORE.story_bibles.get(project["story_bible_id"]) if project else None
        allowed_refs = project.get("allowed_knowledge_source_refs", []) if project else []
        knowledge = store.build_knowledge_context(allowed_refs)
        generated = _generate_chapter_plan(story_bible, command["chapter_index"], knowledge["context_text"])
        chapter_plan["payload"] = {
            **chapter_plan.get("payload", {}),
            "title": generated["title"],
            "summary": generated["summary"],
            "planning_stages": PLANNING_STAGES,
            "current_stage": "quality_review",
        }
```

- [ ] **Step 4: 运行确认通过**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_planning_generation.py -q`
Expected: PASS (2 passed)

- [ ] **Step 5: 提交**

```bash
git add apps/ai-worker/worker/planning.py apps/ai-worker/tests/test_planning_generation.py
git commit -m "feat: generate real chapter plan from story bible and knowledge"
```

---

### Task 3: 真分节规划

**Files:**
- Modify: `apps/ai-worker/worker/planning.py`（`run_create_section_plans` :279，前面新增 helper）
- Test: `apps/ai-worker/tests/test_planning_generation.py`（追加）

**Interfaces:**
- Consumes: `generate_json`、`_generate_chapter_plan` 同上下文。
- Produces: `_generate_section_plans(chapter_plan: dict, story_bible: dict | None, knowledge_context: str, section_count: int, workspace_id: str) -> list[dict]`。

- [ ] **Step 1: 写失败测试**

追加到 `apps/ai-worker/tests/test_planning_generation.py`：

```python
from worker.planning import _generate_section_plans


def test_section_plans_deterministic_without_key(monkeypatch):
    monkeypatch.delenv("NOVELIST_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("NOVELIST_LLM_API_KEY", raising=False)
    chapter_plan = {"chapter_plan_id": "CP9", "chapter_index": 2, "payload": {"title": "林澈·第2章·冲突", "summary": "林澈推进冲突"}}
    bible = {"payload": {"protagonist": "林澈", "core_conflict": "宗门规则"}}
    sections = _generate_section_plans(chapter_plan, bible, "", 3, "WS1")
    assert len(sections) == 3
    assert sections[0]["section_plan_id"].startswith("CP9SEC")
    assert all(s["payload"]["scene_goal"] for s in sections)
    assert all(s["payload"]["beats"] for s in sections)
    joined = "".join(s["payload"]["scene_goal"] for s in sections)
    assert "乌坦城" not in joined
    assert {s["planning_role"] for s in sections} == {"setup", "conflict", "turn"}
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_planning_generation.py::test_section_plans_deterministic_without_key -q`
Expected: FAIL — `cannot import name '_generate_section_plans'`

- [ ] **Step 3: 实现 helper + 接入**

在 `run_create_section_plans`（:279）之前插入：

```python
def _generate_section_plans(chapter_plan: dict[str, Any], story_bible: dict[str, Any] | None, knowledge_context: str, section_count: int, workspace_id: str) -> list[dict[str, Any]]:
    chapter_plan_id = chapter_plan["chapter_plan_id"]
    chapter_summary = chapter_plan.get("payload", {}).get("summary", "")
    protagonist = (story_bible or {}).get("payload", {}).get("protagonist", "主角")
    core_conflict = (story_bible or {}).get("payload", {}).get("core_conflict", "")
    roles = ["setup", "conflict", "turn"]
    knowledge_block = f"\n【可用拆书知识】\n{knowledge_context}\n" if knowledge_context.strip() else ""
    generated = generate_json(
        system="你是中文网文分节规划师。为本章输出 setup/conflict/turn 三段分节，每段含 scene_goal 与 2 个 beats。只输出 JSON：{\"sections\":[{\"scene_goal\":\"\",\"beats\":[\"\",\"\"]}]}，不要解释。",
        user=f"本章摘要：{chapter_summary}\n主角：{protagonist}\n核心冲突：{core_conflict}{knowledge_block}",
    )
    gen_sections = generated.get("sections") if isinstance(generated, dict) else None
    now = utc_now()
    items: list[dict[str, Any]] = []
    for index in range(1, section_count + 1):
        role = roles[min(index - 1, len(roles) - 1)]
        gen = gen_sections[index - 1] if isinstance(gen_sections, list) and len(gen_sections) >= index and isinstance(gen_sections[index - 1], dict) else None
        if gen and str(gen.get("scene_goal", "")).strip():
            scene_goal = str(gen["scene_goal"]).strip()
            raw_beats = gen.get("beats", []) if isinstance(gen.get("beats"), list) else []
            beats = [{"index": bi + 1, "summary": str(b).strip()} for bi, b in enumerate(raw_beats) if str(b).strip()] or [{"index": 1, "summary": scene_goal}]
        else:
            phase = {"setup": "铺垫", "conflict": "冲突升级", "turn": "转折"}[role]
            scene_goal = f"{protagonist}在本节推进{core_conflict or chapter_summary or '主线'}的{phase}"
            beats = [
                {"index": 1, "summary": f"{protagonist}面对{phase}情境"},
                {"index": 2, "summary": f"{phase}推动局势变化"},
            ]
        items.append({
            "schema_version": 1,
            "section_plan_id": f"{chapter_plan_id}SEC{index}",
            "workspace_id": workspace_id,
            "chapter_plan_id": chapter_plan_id,
            "section_index": index,
            "planning_role": role,
            "payload": {"scene_goal": scene_goal, "beats": beats},
            "created_at": now,
            "updated_at": now,
        })
    return items
```

将 `run_create_section_plans`（:279）的 `items = store.STORE.section_plans_by_chapter.get(chapter_plan_id, [])` 之后逻辑改为：若已有 seed section 则保留，否则生成：

```python
def run_create_section_plans(command: dict[str, Any]) -> dict[str, Any]:
    store = load_phase_two_store()
    chapter_plan_id = command["chapter_plan_id"]
    items = store.STORE.section_plans_by_chapter.get(chapter_plan_id, [])
    if not items:
        chapter_plan = store.STORE.chapter_plans.get(chapter_plan_id)
        if chapter_plan:
            project = store.STORE.novel_projects.get(chapter_plan.get("project_id"))
            story_bible = store.STORE.story_bibles.get(project["story_bible_id"]) if project else None
            allowed_refs = project.get("allowed_knowledge_source_refs", []) if project else []
            knowledge = store.build_knowledge_context(allowed_refs)
            items = _generate_section_plans(chapter_plan, story_bible, knowledge["context_text"], command.get("section_count", 3), command["workspace_id"])
            store.STORE.section_plans_by_chapter[chapter_plan_id] = items
    metrics = {
        "planning_stages": PLANNING_STAGES,
        "current_stage": "quality_review",
        "section_count": len(items),
        "generated_at": utc_now(),
    }
    task = store.apply_task_execution_result(
        command["task_id"],
        "succeeded",
        [f"object://section-plans/{item['section_plan_id']}" for item in items],
        metrics,
        trace_id=command["trace_id"],
        dispatch_token=command.get("dispatch_token"),
    )
    return {
        "schema_version": 1,
        "task_id": command["task_id"],
        "status": task["status"] if task else "succeeded",
        "output_refs": task["output_refs"] if task else [f"object://section-plans/{item['section_plan_id']}" for item in items],
        "metrics": metrics,
        "errors": [],
        "trace_id": command["trace_id"],
    }
```

- [ ] **Step 4: 运行确认通过 + demo 不回归**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_planning_generation.py tests/test_planning.py -q`
Expected: PASS（demo CHAPTER_PLAN_ID 已有 seed section，走保留分支不变）

- [ ] **Step 5: 提交**

```bash
git add apps/ai-worker/worker/planning.py apps/ai-worker/tests/test_planning_generation.py
git commit -m "feat: generate real section plans for new chapters"
```

---

### Task 4: story bible 真生成候选

**Files:**
- Modify: `apps/core-service/app/core/phase_two_store.py`（`apply_story_bible_action` regenerate 分支 :4181，前面新增 helper）
- Test: `apps/core-service/tests/test_phase_three_api.py`

**Interfaces:**
- Produces: `_llm_json(system: str, user: str) -> dict | None`（core 侧，同 env 模式）；`_generate_story_bible_candidate(current_payload: dict, note: str | None) -> dict | None`；`_deterministic_enhance_story_bible(current_payload: dict) -> dict`。

- [ ] **Step 1: 写失败测试**

追加到 `apps/core-service/tests/test_phase_three_api.py`：

```python
def test_story_bible_regenerate_without_payload_generates_candidate():
    from app.core import phase_two_store as store
    store.reset_store()
    sb_id = store.STORY_BIBLE_ID
    before = store.STORE.story_bibles[sb_id]["payload"]["world_rules"][:]
    result = store.apply_story_bible_action(sb_id, "regenerate", payload={"summary": "补强世界规则"})
    assert result["status"] == "pending_review"
    assert result["diff"]["changed_fields"]  # 有变化，非原样回写
    after = store.STORE.story_bibles[sb_id]["payload"]["world_rules"]
    assert after != before or result["diff"]["changed_fields"]
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_three_api.py::test_story_bible_regenerate_without_payload_generates_candidate -q`
Expected: FAIL — regenerate 无 payload 时 next_payload 归一化默认值，diff.changed_fields 为空

- [ ] **Step 3: 实现 helper + 接入**

在 `apps/core-service/app/core/phase_two_store.py` 顶部确认已有 `import json, os` 与 urllib（若无则加）。在 `apply_story_bible_action`（:4147）之前插入：

```python
def _llm_json(system: str, user: str) -> Optional[dict[str, Any]]:
    base_url = os.getenv("NOVELIST_LLM_BASE_URL")
    api_key = os.getenv("NOVELIST_LLM_API_KEY")
    if not base_url or not api_key:
        return None
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
    endpoint = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0.5,
        "max_tokens": 1200,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")
    request = Request(endpoint, data=body, headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        parsed = json.loads(payload["choices"][0]["message"]["content"])
        return parsed if isinstance(parsed, dict) else None
    except (HTTPError, URLError, TimeoutError, KeyError, IndexError, TypeError, ValueError):
        return None


def _deterministic_enhance_story_bible(current_payload: dict[str, Any]) -> dict[str, Any]:
    enhanced = deepcopy(current_payload) if isinstance(current_payload, dict) else {}
    protagonist = enhanced.get("protagonist", "主角")
    world_rules = list(enhanced.get("world_rules", []))
    new_rule = f"{protagonist}每次突破都需付出真实代价，力量提升与风险同步。"
    if new_rule not in world_rules:
        world_rules.append(new_rule)
    enhanced["world_rules"] = world_rules
    promises = list(enhanced.get("narrative_promises", []))
    new_promise = f"前三章内确立{protagonist}的核心动机与首个转折。"
    if new_promise not in promises:
        promises.append(new_promise)
    enhanced["narrative_promises"] = promises
    return enhanced


def _generate_story_bible_candidate(current_payload: dict[str, Any], note: Optional[str]) -> Optional[dict[str, Any]]:
    generated = _llm_json(
        system="你是中文小说故事圣经编辑。基于当前故事圣经补强世界规则与叙事承诺，保持前提与主角一致。只输出 JSON，键：premise, protagonist, core_conflict, style_target, forbidden_similarities, world_rules(数组), narrative_promises(数组)。",
        user=f"当前故事圣经：{json.dumps(current_payload, ensure_ascii=False)}\n补强方向：{note or '强化世界观与叙事承诺'}",
    )
    return generated
```

将 regenerate 分支（:4181-4196）的 `next_payload` 求值改为：

```python
    elif action == "regenerate":
        explicit = (payload or {}).get("story_bible_payload")
        if explicit:
            next_payload = _normalize_story_bible_payload(explicit, project.get("title") if project else None)
        else:
            candidate = _generate_story_bible_candidate(normalized_current, note) or _deterministic_enhance_story_bible(normalized_current)
            next_payload = _normalize_story_bible_payload(candidate, project.get("title") if project else None)
        previous_version = story_bible.get("version", 1)
        previous_payload = deepcopy(story_bible.get("payload"))
        story_bible["version"] = previous_version + 1
        story_bible["status"] = "pending_review"
        story_bible["payload"] = deepcopy(next_payload)
        story_bible["diff"] = _story_bible_diff(
            previous_version,
            story_bible["version"],
            previous_payload,
            next_payload,
            summary or "补强故事圣经候选版本。",
        )
        changed_fields = story_bible["diff"]["changed_fields"]
        final_summary = story_bible["diff"]["summary"]
```

- [ ] **Step 4: 运行确认通过**

Run: `cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_three_api.py::test_story_bible_regenerate_without_payload_generates_candidate -q`
Expected: PASS

- [ ] **Step 5: 运行相关回归**

Run: `cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_three_api.py -q`
Expected: PASS（提供 explicit payload 的现有 regenerate 测试仍绿）

- [ ] **Step 6: 提交**

```bash
git add apps/core-service/app/core/phase_two_store.py apps/core-service/tests/test_phase_three_api.py
git commit -m "feat: generate story bible candidate when no explicit payload"
```

---

### Task 5: 多章 manuscript state 真生成 + 回灌

**Files:**
- Modify: `apps/core-service/app/core/phase_two_store.py`（`_build_manuscript_state` :5336；`create_writing_run` :4394）
- Test: `apps/core-service/tests/test_phase_three_api.py`

**Interfaces:**
- Consumes: writing_run 的 assembled_chapter/section_runs、`STORE.manuscript_states_by_project`。
- Produces: `_build_manuscript_state(writing_run, chapter_plan, accepted_chapter_ref, updated_at)` 改为从真实草稿派生；create_writing_run 给新 writing_run 写 `prior_context` 字段。

- [ ] **Step 1: 写失败测试**

追加到 `apps/core-service/tests/test_phase_three_api.py`：

```python
def test_manuscript_state_reflects_real_draft(monkeypatch):
    from app.core import phase_two_store as store
    store.reset_store()
    wr = store.STORE.writing_runs[store.WRITING_RUN_ID]
    wr["assembled_chapter"] = "林澈站在宗门前，立誓要打破规则的桎梏。他知道前路艰险。"
    cp = store.STORE.chapter_plans[store.CHAPTER_PLAN_ID]
    state = store._build_manuscript_state(wr, cp, "object://chapters/c1", store.utc_now())
    # 摘要来自真实草稿/章节，不再硬编码萧炎/三年之约
    text = json.dumps(state, ensure_ascii=False)
    assert "萧炎" not in state["current_story_state"]["summary"] or "林澈" in text
    assert state["prior_summary_pack"]  # 非空
```

（文件顶部若无 `import json` 则加。）

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_three_api.py::test_manuscript_state_reflects_real_draft -q`
Expected: FAIL — 当前 summary 硬编码"三年之约"、character 硬编码萧炎

- [ ] **Step 3: 改 `_build_manuscript_state` 从真实草稿派生**

将 `_build_manuscript_state`（:5336）替换为：

```python
def _build_manuscript_state(writing_run: dict[str, Any], chapter_plan: Optional[dict[str, Any]], accepted_chapter_ref: str, updated_at: str) -> dict[str, Any]:
    manuscript_state_id = writing_run.get("manuscript_state_id") or f"manuscript-state:{writing_run['project_id']}"
    chapter_payload = chapter_plan.get("payload", {}) if chapter_plan else {}
    chapter_title = chapter_payload.get("title", "当前章节")
    chapter_summary = chapter_payload.get("summary") or ""
    assembled = writing_run.get("assembled_chapter") or ""
    project = STORE.novel_projects.get(writing_run["project_id"])
    story_bible = STORE.story_bibles.get(project["story_bible_id"]) if project else None
    protagonist = (story_bible or {}).get("payload", {}).get("protagonist", "主角")
    core_conflict = (story_bible or {}).get("payload", {}).get("core_conflict", "")
    # 前情摘要包：从真实组章文本分句派生
    sentences = [s.strip() for s in assembled.replace("。", "。\n").split("\n") if s.strip()]
    prior_pack = [{"summary_index": i + 1, "summary": s} for i, s in enumerate(sentences[:3])] or (
        [{"summary_index": 1, "summary": chapter_summary or f"{chapter_title}已进入 manuscript。"}]
    )
    state_summary = (
        f"第 {chapter_plan['chapter_index']} 章《{chapter_title}》已进入 manuscript：{chapter_summary or assembled[:60]}"
        if chapter_plan else f"《{chapter_title}》已进入 manuscript。"
    )
    return {
        "schema_version": 1,
        "manuscript_state_id": manuscript_state_id,
        "project_id": writing_run["project_id"],
        "writing_run_id": writing_run["writing_run_id"],
        "current_story_state": {
            "summary": state_summary,
            "accepted_chapter_ref": accepted_chapter_ref,
            "quality_gate_status": "passed",
        },
        "character_dynamic_state": [
            {"character_name": protagonist, "state_summary": f"在本章推进「{core_conflict or chapter_summary}」，动机与处境更新。"}
        ],
        "relationship_state": [
            {"subject": protagonist, "object": core_conflict or "核心冲突", "state_summary": "人物与核心冲突的关系随本章推进。"}
        ],
        "hook_state": [
            {"hook_key": "core_conflict", "status": "active", "summary": core_conflict or chapter_summary or "核心挂钩持续推进。"}
        ],
        "prior_summary_pack": prior_pack,
        "updated_at": updated_at,
    }
```

- [ ] **Step 4: create_writing_run 注入上一章 state**

在 `create_writing_run`（:4394）建新 writing_run 的 dict 里（找到构造 writing_run 记录、写各字段处），加入 prior_context。在 `now = utc_now()` 之后、构造 writing_run 记录前加：

```python
    prior_state = STORE.manuscript_states_by_project.get(project_id)
    prior_context = ""
    if prior_state:
        prior_lines = [item["summary"] for item in prior_state.get("prior_summary_pack", [])]
        prior_context = "【前情提要】\n" + "\n".join(prior_lines) + f"\n当前故事状态：{prior_state.get('current_story_state', {}).get('summary', '')}"
```

在真实新章 writing_run 记录 dict 里加一个字段 `"prior_context": prior_context,`（找到该 dict 字面量，与 memory_package_id 等字段并列添加）。

- [ ] **Step 5: worker 把 prior_context 拼进 knowledge_context**

在 `apps/ai-worker/worker/writing.py` 的 `_build_memory_package_payload` 里，把 writing_run 的 prior_context 前置到 knowledge_context：

```python
    knowledge = store.build_knowledge_context(allowed_refs)
    prior_context = writing_run.get("prior_context", "")
    combined_context = (prior_context + "\n" + knowledge["context_text"]).strip() if prior_context else knowledge["context_text"]
```

并把返回的 `"knowledge_context": knowledge["context_text"]` 改为 `"knowledge_context": combined_context`。

- [ ] **Step 6: 运行确认通过**

Run: `cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_three_api.py::test_manuscript_state_reflects_real_draft -q`
Expected: PASS

- [ ] **Step 7: worker RAG 测试仍绿**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_writing_rag.py -q`
Expected: PASS（FakeStore 的 writing_run 无 prior_context 时 combined_context = knowledge context，不变）

- [ ] **Step 8: 提交**

```bash
git add apps/core-service/app/core/phase_two_store.py apps/ai-worker/worker/writing.py apps/core-service/tests/test_phase_three_api.py
git commit -m "feat: build real manuscript state and inject prior chapter context"
```

---

## Verification（整批完成后）

```bash
cd apps/ai-worker && rtk python3 -m pytest tests -q
cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_three_api.py tests/test_phase_two_api.py tests/test_persistence.py -q
rtk pnpm --filter @novel-factory/web test --run
rtk pnpm --filter @novel-factory/contracts test
```
（跑前后清理构建工具污染：`git checkout -- apps/*/pyproject.toml; rm -f apps/*/uv.lock`）

浏览器手验：新项目选知识源 → regenerate story bible 出候选（有变化）→ planner 出真实章节/分节（非乌坦城）→ 生成第1章 accept → manuscript state 反映真实草稿 → 建第2章 memory 含第1章前情。

## Done bar
- 章节/分节规划 LLM 生成（无 key 确定性派生），非写死乌坦城/三年之约。
- story bible regenerate 无 explicit payload 时真生成候选（diff 非空）。
- manuscript state 反映真实草稿，非硬编码萧炎。
- 多章：上一章 state 注入下一章 memory 的前情段。
- 全量测试绿；现有 demo 测试仍绿；未碰多书隔离/deep_analysis。
