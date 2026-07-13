# P1 打通线2真实生成 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** 让拆书知识经 RAG 真正进入新书章节生成，默认写作链配 key 真调 LLM、无 key 确定性 fallback，质量分基于真实草稿信号。

**Architecture:** core-service 新增 `build_knowledge_context` 从 allowed_knowledge_source_refs 拉真实 objects/graph/evidence 拼中文知识块；worker `_build_memory_package_payload` 载入该 context；`_chat` 下移到 `AnthropicWritingAdapter` 基类使默认也真调，三段 prompt 注入 knowledge_context；质量分改真实启发式。

**Tech Stack:** Python 3.11（core-service app/、ai-worker worker/），pytest，内存 CoreStore 单例（worker 经 load_phase_two_store 共享）。

## Global Constraints
- 不硬编码任何真实 API 密钥。
- 无 key 时确定性 fallback，绝不崩、不静默 file fallback。
- HTTP API shape 不变；现有 demo（CHAPTER_PLAN_ID/WRITING_RUN_ID seed）测试仍绿。
- worker 经 `load_phase_two_store()` 调 core getter，不新增跨服务 HTTP。
- 每任务 ≤2 迭代 / ~15 分钟。命令用 `rtk`；core-service 测试用其 `.venv`（有 fastapi/pytest），worker 无 dramatiq 依赖测试用 rtk python3。

---

### Task 1: build_knowledge_context 检索器

**Files:**
- Modify: `apps/core-service/app/core/phase_two_store.py`（`list_knowledge_sources` :3286 之后新增）
- Test: `apps/core-service/tests/test_phase_two_api.py`

**Interfaces:**
- Consumes: `_latest_extraction_run_for_book`, `list_knowledge_objects_for_run`, `get_graph_summary`, `list_evidence_for_book`（均已存在）。
- Produces: `build_knowledge_context(allowed_knowledge_source_refs: list[str], max_objects: int = 12, max_evidence: int = 6) -> dict` → `{"summary": str, "objects": list, "graph": dict, "evidence": list, "context_text": str}`。

- [ ] **Step 1: 写失败测试**

追加到 `apps/core-service/tests/test_phase_two_api.py`：

```python
def test_build_knowledge_context_from_source_refs():
    from app.core import phase_two_store as store
    store.reset_store()
    book_id = store.BOOK_ID
    context = store.build_knowledge_context([f"object://source-books/{book_id}"])
    assert isinstance(context["context_text"], str)
    assert context["objects"]
    assert context["context_text"].strip()
    # 含真实对象名
    names = {o["canonical_name"] for o in context["objects"]}
    assert any(name in context["context_text"] for name in names)


def test_build_knowledge_context_empty_refs_safe():
    from app.core import phase_two_store as store
    store.reset_store()
    context = store.build_knowledge_context([])
    assert context["context_text"] == ""
    assert context["objects"] == []
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_two_api.py::test_build_knowledge_context_from_source_refs -q`
Expected: FAIL — `AttributeError: module ... has no attribute 'build_knowledge_context'`

- [ ] **Step 3: 实现函数**

在 `apps/core-service/app/core/phase_two_store.py` 的 `list_knowledge_sources` 函数之后插入：

```python
def build_knowledge_context(
    allowed_knowledge_source_refs: list[str],
    max_objects: int = 12,
    max_evidence: int = 6,
) -> dict[str, Any]:
    objects: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    graph_nodes: list[dict[str, Any]] = []
    source_labels: list[str] = []
    for ref in allowed_knowledge_source_refs or []:
        book_id = ref.rsplit("/", 1)[-1]
        book = STORE.books.get(book_id)
        if not book:
            continue
        source_labels.append(book.get("title", book_id))
        run = _latest_extraction_run_for_book(book_id)
        run_id = run.get("run_id") if run else None
        if run_id:
            for obj in list_knowledge_objects_for_run(run_id):
                objects.append({
                    "canonical_name": obj.get("canonical_name", ""),
                    "object_type": obj.get("object_type", ""),
                    "aliases": obj.get("payload", {}).get("aliases", []),
                    "summary": obj.get("payload", {}).get("summary", ""),
                })
        summary = get_graph_summary(book_id)
        graph_nodes.extend(summary.get("nodes", []))
        for item in list_evidence_for_book(book_id)[:max_evidence]:
            evidence.append({
                "excerpt": item.get("excerpt", ""),
                "chapter_index": item.get("chapter_index"),
            })
    objects = objects[:max_objects]
    evidence = evidence[:max_evidence]

    lines: list[str] = []
    if source_labels:
        lines.append("【可用知识源】" + "、".join(source_labels))
    if objects:
        lines.append("【人物与势力】")
        for obj in objects:
            alias_part = f"（别名：{'、'.join(obj['aliases'])}）" if obj["aliases"] else ""
            desc = f"·{obj['summary']}" if obj["summary"] else ""
            lines.append(f"- {obj['canonical_name']}[{obj['object_type']}]{alias_part}{desc}")
    if graph_nodes:
        lines.append("【图谱节点】" + "、".join(str(n.get("label", "")) for n in graph_nodes[:max_objects]))
    if evidence:
        lines.append("【原文摘录】")
        for item in evidence:
            chapter_hint = f"第{item['chapter_index']}章" if item.get("chapter_index") else ""
            lines.append(f"- {chapter_hint}「{item['excerpt']}」")
    context_text = "\n".join(lines)
    return {
        "summary": f"已汇总 {len(source_labels)} 个知识源、{len(objects)} 个对象、{len(evidence)} 条证据。" if source_labels else "",
        "objects": objects,
        "graph": {"nodes": graph_nodes[:max_objects]},
        "evidence": evidence,
        "context_text": context_text,
    }
```

- [ ] **Step 4: 运行确认通过**

Run: `cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_two_api.py::test_build_knowledge_context_from_source_refs tests/test_phase_two_api.py::test_build_knowledge_context_empty_refs_safe -q`
Expected: PASS (2 passed)

- [ ] **Step 5: 提交**

```bash
git add apps/core-service/app/core/phase_two_store.py apps/core-service/tests/test_phase_two_api.py
git commit -m "feat: add build_knowledge_context RAG retriever"
```

---

### Task 2: memory package 载入真实知识

**Files:**
- Modify: `apps/ai-worker/worker/writing.py`（`_build_memory_package_payload` :304）
- Test: `apps/ai-worker/tests/test_writing_rag.py`（新建，无 dramatiq 依赖）

**Interfaces:**
- Consumes: `build_knowledge_context`（Task 1，经 `store.build_knowledge_context`）。
- Produces: `_build_memory_package_payload` 返回增加 `knowledge_context: str`。

- [ ] **Step 1: 写失败测试**

新建 `apps/ai-worker/tests/test_writing_rag.py`：

```python
from worker.writing import _build_memory_package_payload


class FakeStore:
    def __init__(self, refs, context_text):
        self._refs = refs
        self._context_text = context_text
        self.STORE = self
        self.novel_projects = {"P1": {"story_bible_id": "SB1", "allowed_knowledge_source_refs": refs}}

    def build_knowledge_context(self, refs, **kwargs):
        assert refs == self._refs
        return {"summary": "s", "objects": [], "graph": {}, "evidence": [], "context_text": self._context_text}


def test_memory_package_includes_knowledge_context():
    store = FakeStore(["object://source-books/B1"], "【人物与势力】- 林澈[character]")
    writing_run = {"project_id": "P1", "chapter_plan_id": "CP1"}
    chapter_plan = {"chapter_index": 1, "payload": {"title": "开端"}}
    section_plans = [{"section_plan_id": "SP1"}]
    payload = _build_memory_package_payload(store, writing_run, chapter_plan, section_plans)
    assert "knowledge_context" in payload
    assert "林澈" in payload["knowledge_context"]


def test_memory_package_empty_knowledge_safe():
    store = FakeStore([], "")
    store.STORE.novel_projects["P1"]["allowed_knowledge_source_refs"] = []
    writing_run = {"project_id": "P1", "chapter_plan_id": "CP1"}
    chapter_plan = {"chapter_index": 1, "payload": {"title": "开端"}}
    payload = _build_memory_package_payload(store, writing_run, chapter_plan, [{"section_plan_id": "SP1"}])
    assert payload["knowledge_context"] == ""
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_writing_rag.py -q`
Expected: FAIL — `KeyError: 'knowledge_context'`

- [ ] **Step 3: 修改 `_build_memory_package_payload`**

将 `apps/ai-worker/worker/writing.py` 的 `_build_memory_package_payload`（:304）替换为：

```python
def _build_memory_package_payload(store: Any, writing_run: dict[str, Any], chapter_plan: dict[str, Any], section_plans: list[dict[str, Any]]) -> dict[str, Any]:
    project = store.STORE.novel_projects[writing_run["project_id"]]
    allowed_refs = project.get("allowed_knowledge_source_refs", [])
    source_refs = [
        f"object://story-bibles/{project['story_bible_id']}",
        f"object://chapter-plans/{writing_run['chapter_plan_id']}",
        *[f"object://section-plans/{item['section_plan_id']}" for item in section_plans],
        *allowed_refs,
    ]
    knowledge = store.build_knowledge_context(allowed_refs)
    chapter_title = chapter_plan.get("payload", {}).get("title") or f"第{chapter_plan['chapter_index']}章"
    summary_suffix = f"，已载入 {len(knowledge['objects'])} 个知识对象" if knowledge["objects"] else ""
    return {
        "summary": f"已汇总 {chapter_title} 的故事圣经、章节目标、分节 beats{summary_suffix}。",
        "source_refs": source_refs,
        "knowledge_context": knowledge["context_text"],
    }
```

- [ ] **Step 4: 运行确认通过**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_writing_rag.py -q`
Expected: PASS (2 passed)

- [ ] **Step 5: 把 knowledge_context 传入 pipeline**

在 `run_create_writing_run`（:361-371）把 memory_package 的 knowledge_context 传给 pipeline。将调用改为：

```python
    memory_package = _build_memory_package_payload(store, writing_run, chapter_plan, section_plans)
    prompt_package = _build_prompt_package_payload(store)
    try:
        provider_execution = execute_writing_provider_pipeline(
            store=store,
            writing_run=writing_run,
            chapter_plan=chapter_plan,
            section_plans=section_plans,
            section_runs=section_runs,
            prompt_package=prompt_package,
            knowledge_context=memory_package.get("knowledge_context", ""),
        )
```

（`execute_writing_provider_pipeline` 的 `knowledge_context` 参数由 Task 3 添加；本步先传，Task 3 接收。若 Task 3 未完成会 TypeError——因此本步的验证放在 Task 3 之后的联跑；本任务 Step 4 的单元测试不经过 pipeline，不受影响。）

- [ ] **Step 6: 提交**

```bash
git add apps/ai-worker/worker/writing.py apps/ai-worker/tests/test_writing_rag.py
git commit -m "feat: load real knowledge context into memory package"
```

---

### Task 3: 默认 adapter 真调 LLM + 注入知识

**Files:**
- Modify: `apps/ai-worker/worker/provider_executor.py`（`_chat` 上移基类、三方法加 knowledge_context、pipeline 签名+透传）
- Test: `apps/ai-worker/tests/test_provider_executor.py`（新建，无 dramatiq 依赖）

**Interfaces:**
- Consumes: `knowledge_context: str`（Task 2 传入）。
- Produces: `AnthropicWritingAdapter._chat`；`draft_section`/`humanize_section` 新增 `knowledge_context: str = ""`；`execute_writing_provider_pipeline(..., knowledge_context: str = "")`。

- [ ] **Step 1: 写失败测试**

新建 `apps/ai-worker/tests/test_provider_executor.py`：

```python
import worker.provider_executor as pe
from worker.provider_executor import AnthropicWritingAdapter


def test_base_adapter_has_chat_with_fallback(monkeypatch):
    monkeypatch.delenv("NOVELIST_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("NOVELIST_LLM_API_KEY", raising=False)
    adapter = AnthropicWritingAdapter()
    # 无 key → 确定性 fallback，非 user[:320] 裸截断，含可读中文
    out = adapter._chat(model_profile={"provider_model_name": "m"}, system="s", user="写一段")
    assert isinstance(out, str) and out


def test_draft_injects_knowledge_context(monkeypatch):
    captured = {}

    def fake_chat(self, *, model_profile, system, user):
        captured["user"] = user
        captured["system"] = system
        return "草稿正文"

    monkeypatch.setattr(AnthropicWritingAdapter, "_chat", fake_chat)
    adapter = AnthropicWritingAdapter()
    result = adapter.draft_section(
        chapter_plan={"payload": {"summary": "章节目标"}},
        section_plan={"payload": {"scene_goal": "出场", "beats": [{"summary": "b1", "index": 1}]}},
        section_index=1,
        model_profile={"provider_model_name": "m"},
        knowledge_context="【人物与势力】- 林澈[character]",
    )
    assert result["writer_output"] == "草稿正文"
    assert "林澈" in captured["user"]


def test_review_no_hardcoded_issue_without_model(monkeypatch):
    monkeypatch.delenv("NOVELIST_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("NOVELIST_LLM_API_KEY", raising=False)
    adapter = AnthropicWritingAdapter()
    issues = adapter.review_sections(
        section_runs=[{"draft_object_ref": "object://d1"}, {"draft_object_ref": "object://d2"}],
        drafts=[{"writer_output": "a"}, {"writer_output": "b"}],
        consistency_report_id="CR1",
        model_profile={"provider_model_name": "m"},
    )
    assert issues == []
    assert all("斗之气" not in str(i) for i in issues)
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_provider_executor.py -q`
Expected: FAIL — `AnthropicWritingAdapter` 无 `_chat`；draft_section 不接受 `knowledge_context`；review 返回硬编码 issue。

- [ ] **Step 3: 把 `_chat` 上移基类 + 无 key 确定性 fallback**

将 `AnthropicWritingAdapter`（provider_executor.py:46）改为包含 `_chat`（从 OpenAICompatibleWritingAdapter :114 剪切上移），无 key 分支改为返回确定性模板：

```python
class AnthropicWritingAdapter:
    def _chat(self, *, model_profile: dict[str, Any], system: str, user: str) -> str:
        base_url = os.getenv("NOVELIST_LLM_BASE_URL")
        api_key = os.getenv("NOVELIST_LLM_API_KEY")
        if not base_url or not api_key:
            # 确定性 fallback：无 LLM 时用 user 前缀构造可读中文，而非裸截断
            return f"（离线草稿）{user.strip()[:280]}"
        endpoint = base_url.rstrip("/") + "/chat/completions"
        body = json.dumps(
            {
                "model": model_profile["provider_model_name"],
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": 0.4,
                "max_tokens": 600,
            }
        ).encode("utf-8")
        request = Request(
            endpoint,
            data=body,
            headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise ProviderExecutionError("provider_http_error", f"provider request failed: {exc.code}") from exc
        except URLError as exc:
            raise ProviderExecutionError("provider_network_error", "provider request failed") from exc
        except TimeoutError as exc:
            raise ProviderExecutionError("provider_timeout", "provider request timed out") from exc
        try:
            return payload["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderExecutionError("provider_response_invalid", "provider response missing message content") from exc

    def draft_section(self, *, chapter_plan: dict[str, Any], section_plan: dict[str, Any], section_index: int, model_profile: dict[str, Any], knowledge_context: str = "") -> dict[str, Any]:
        payload = section_plan.get("payload", {})
        scene_goal = payload.get("scene_goal") or f"推进第 {section_index} 节剧情"
        beats = payload.get("beats", [])
        beat_phrase = "，".join(beat.get("summary", f"beat {beat.get('index', i + 1)}") for i, beat in enumerate(beats)) or scene_goal
        knowledge_block = f"\n【世界观与知识】\n{knowledge_context}\n" if knowledge_context.strip() else ""
        user = (
            f"章节目标：{chapter_plan.get('payload', {}).get('summary', scene_goal)}\n"
            f"本节目标：{scene_goal}\nbeats：{beat_phrase}\n{knowledge_block}"
        )
        text = self._chat(
            model_profile=model_profile,
            system="你是中文网文章节写手。必须遵循给定世界观与已确立设定，不得引入矛盾。输出一段可直接进入章节草稿的中文正文，不要解释。",
            user=user,
        )
        return {"writer_output": text, "scene_goal": scene_goal, "beat_phrase": beat_phrase, "provider_model_name": model_profile["provider_model_name"]}

    def review_sections(self, *, section_runs: list[dict[str, Any]], drafts: list[dict[str, Any]], consistency_report_id: str, model_profile: dict[str, Any]) -> list[dict[str, Any]]:
        base_url = os.getenv("NOVELIST_LLM_BASE_URL")
        api_key = os.getenv("NOVELIST_LLM_API_KEY")
        if not base_url or not api_key:
            return []
        combined = "\n".join(draft["writer_output"] for draft in drafts)
        review = self._chat(
            model_profile=model_profile,
            system="你是中文小说一致性审稿人。若没有严重阻断，只输出 PASS；若有阻断，用一句中文说明。",
            user=combined,
        )
        if review.upper().startswith("PASS"):
            return []
        section_run = section_runs[min(1, len(section_runs) - 1)]
        return [
            {
                "issue_id": "01JZCONSISTISSUE000000001",
                "category": "llm_consistency_review",
                "severity": "warning",
                "summary": review[:160],
                "affected_text_ref": f"{section_run['draft_object_ref']}#p1",
                "rule_id": "rule-01JZPOWER000000000000001",
                "resolution_status": "open",
                "input_refs": ["object://rules/rule-01JZPOWER000000000000001"],
                "output_refs": [f"object://consistency-reports/{consistency_report_id}/issues/1"],
                "note": model_profile["provider_model_name"],
            }
        ]

    def humanize_section(self, *, section_plan: dict[str, Any], section_index: int, draft_text: str, critic_issues: list[dict[str, Any]], model_profile: dict[str, Any], knowledge_context: str = "") -> dict[str, Any]:
        knowledge_block = f"\n【需保持一致的设定】\n{knowledge_context}\n" if knowledge_context.strip() else ""
        text = self._chat(
            model_profile=model_profile,
            system="你是中文小说润色师。保留剧情事实与给定设定，降低机械感，输出润色正文，不要解释。",
            user=f"{draft_text}\n{knowledge_block}",
        )
        return {"humanized_text": text, "provider_model_name": model_profile["provider_model_name"], "had_critic_issues": bool(critic_issues)}
```

并把 `OpenAICompatibleWritingAdapter` 简化为继承别名（删除其重复的 `_chat`/`draft_section`/`review_sections`/`humanize_section`，因已全部上移）：

```python
class OpenAICompatibleWritingAdapter(AnthropicWritingAdapter):
    pass
```

- [ ] **Step 4: pipeline 签名加 knowledge_context 并透传**

在 `execute_writing_provider_pipeline`（约 :221）签名加 `knowledge_context: str = ""`；把 draft/humanize 调用点透传：

```python
    drafts = [
        writer_adapter.draft_section(
            chapter_plan=chapter_plan,
            section_plan=section_plan,
            section_index=index,
            model_profile=writer_profile,
            knowledge_context=knowledge_context,
        )
        for index, section_plan in enumerate(section_plans, start=1)
    ]
```

humanize 调用点同样加 `knowledge_context=knowledge_context`（找到 `humanize_section(` 调用处补参）。

- [ ] **Step 5: 运行确认通过**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_provider_executor.py -q`
Expected: PASS (3 passed)

- [ ] **Step 6: 提交**

```bash
git add apps/ai-worker/worker/provider_executor.py apps/ai-worker/tests/test_provider_executor.py
git commit -m "feat: default adapter calls LLM and injects knowledge context"
```

---

### Task 4: 质量分去写死

**Files:**
- Modify: `apps/ai-worker/worker/writing.py`（:412-414）
- Test: `apps/ai-worker/tests/test_writing_rag.py`（追加）

**Interfaces:**
- Produces: `_compute_quality_scores(section_runs: list[dict], blocking_issue_count: int) -> dict`（`ai_flavor_score`/`mobile_readability_score`/`originality_safety_score`）。

- [ ] **Step 1: 写失败测试**

追加到 `apps/ai-worker/tests/test_writing_rag.py`：

```python
from worker.writing import _compute_quality_scores


def test_quality_scores_vary_with_content():
    rich = [{"humanized_text": "他缓步走入议事堂，众人目光聚焦，空气仿佛凝固。少年抬眼，语气平静。"}]
    poor = [{"humanized_text": "好好好好好好好好好好好好好好好好"}]
    s_rich = _compute_quality_scores(rich, 0)
    s_poor = _compute_quality_scores(poor, 0)
    assert 0.0 <= s_rich["ai_flavor_score"] <= 1.0
    assert 0.0 <= s_poor["ai_flavor_score"] <= 1.0
    # 高重复文本 ai_flavor 更差
    assert s_poor["ai_flavor_score"] < s_rich["ai_flavor_score"]
    assert s_rich["ai_flavor_score"] != 0.52
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_writing_rag.py::test_quality_scores_vary_with_content -q`
Expected: FAIL — `cannot import name '_compute_quality_scores'`

- [ ] **Step 3: 实现打分 helper**

在 `apps/ai-worker/worker/writing.py` 的 `run_create_writing_run` 之前插入：

```python
def _compute_quality_scores(section_runs: list[dict[str, Any]], blocking_issue_count: int) -> dict[str, Any]:
    texts = [sr.get("humanized_text") or sr.get("writer_output") or "" for sr in section_runs]
    joined = "".join(texts)
    total_chars = len(joined) or 1
    unique_chars = len(set(joined))
    diversity = unique_chars / total_chars  # 重复越多越低
    # ai_flavor：内容多样性驱动，blocking 时封顶
    base_flavor = min(0.95, 0.35 + diversity * 0.6)
    ai_flavor_score = round(min(base_flavor, 0.45) if blocking_issue_count else base_flavor, 2)
    # mobile_readability：按平均句长（句号/逗号分段）
    segments = [seg for seg in joined.replace("。", "，").split("，") if seg.strip()]
    avg_len = (sum(len(s) for s in segments) / len(segments)) if segments else 0
    readability = 0.9 - min(0.4, abs(avg_len - 18) * 0.02)  # 句长约18字最佳
    mobile_readability_score = round(max(0.5, min(0.95, readability)), 2)
    # originality：多样性 + 无阻断
    originality_safety_score = round(min(0.95, 0.6 + diversity * 0.35), 2)
    return {
        "ai_flavor_score": ai_flavor_score,
        "mobile_readability_score": mobile_readability_score,
        "originality_safety_score": originality_safety_score,
    }
```

- [ ] **Step 4: 接入 run_create_writing_run**

将 :412-414 三行替换为：

```python
    _quality_scores = _compute_quality_scores(section_runs, blocking_issue_count)
    ai_flavor_score = _quality_scores["ai_flavor_score"]
    mobile_readability_score = _quality_scores["mobile_readability_score"]
    originality_safety_score = _quality_scores["originality_safety_score"]
```

- [ ] **Step 5: 运行确认通过**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_writing_rag.py -q`
Expected: PASS

- [ ] **Step 6: 提交**

```bash
git add apps/ai-worker/worker/writing.py apps/ai-worker/tests/test_writing_rag.py
git commit -m "feat: compute quality scores from real draft signals"
```

---

## Verification（整批完成后）

```bash
cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_two_api.py tests/test_persistence.py -q
cd apps/ai-worker && rtk python3 -m pytest tests/test_provider_executor.py tests/test_writing_rag.py tests/test_extraction_entities.py -q
rtk pnpm --filter @novel-factory/web test --run
rtk pnpm --filter @novel-factory/contracts test
```

浏览器手验：项目选知识源 → 配 NOVELIST_LLM_BASE_URL/API_KEY → 生成章节 → 记忆包/草稿体现该书知识；不配 key 走确定性 fallback 不崩。

## Done bar
- 拆书知识经 build_knowledge_context 进入 writer prompt。
- 默认写作链配 key 真调 LLM、无 key 确定性 fallback。
- critic 不再对新书返回写死斗破苍穹 issue。
- 质量分与真实草稿内容相关。
- 全量测试绿；现有 demo 测试仍绿。
