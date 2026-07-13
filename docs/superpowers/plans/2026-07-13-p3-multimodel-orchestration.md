# P3 做实多模型 Agent 编排 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** 不同 agent role 可指向不同真实 provider（profile env 引用驱动），provider_calls 记录真实 token/latency/cost（回读 API usage 替换写死 ROLE_CALL_METRICS），前端配置改动 POST 后端真落库，router 纳入 max_cost 路由；critic issue 去硬编码。

**Architecture:** model_profile 增 base_url_env/api_key_env 让 `_chat` 按 profile 读不同 env；`_chat` 返回 dict 带 usage/latency，pipeline 把真实指标写回 provider_calls；前端 toggle/update 有 API 时 POST configuration 端点（已 REAL）用返回快照刷新；resolve_model_profile 加 max_cost 过滤。

**Tech Stack:** Python 3.11（core-service app/、ai-worker worker/），React + Vite + vitest（apps/web），pytest。worker 经 load_phase_two_store 共享 CoreStore。

## Global Constraints
- 不硬编码任何真实 API 密钥（只存 env 引用名）。
- 无 key 时确定性 fallback，绝不崩。
- HTTP API shape 不变（新增字段向后兼容）；现有 demo 测试仍绿。
- **完全不碰 deep_analysis / apply_task_execution_result 的 extraction 落表段 / _merge_book_scoped / 多书隔离**（后台任务 task_62457d44 范围）。
- worker 经 load_phase_two_store() 调 core，不新增跨服务 HTTP。
- 每任务 ≤2 迭代 / ~15 分钟。命令用 rtk；core-service 测试用其 .venv；worker 用 rtk python3。跑前后清构建污染：`git checkout -- apps/*/pyproject.toml; rm -f apps/*/uv.lock`。

---

### Task 1: profile 携带 provider env 引用 + `_chat` 按 profile 读 env

**Files:**
- Modify: `apps/core-service/app/core/phase_two_store.py`（model_profile seed :1227-1248）
- Modify: `apps/ai-worker/worker/provider_executor.py`（`_chat` :50-86）
- Test: `apps/ai-worker/tests/test_provider_executor.py`（追加）

**Interfaces:**
- Produces: model_profile 新增可选字段 `base_url_env: str`、`api_key_env: str`；`_chat` 读 `model_profile.get("base_url_env", "NOVELIST_LLM_BASE_URL")` 对应 env。

- [ ] **Step 1: 写失败测试**

追加到 `apps/ai-worker/tests/test_provider_executor.py`：

```python
def test_chat_reads_profile_specific_env(monkeypatch):
    from worker.provider_executor import AnthropicWritingAdapter
    monkeypatch.delenv("NOVELIST_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("NOVELIST_LLM_API_KEY", raising=False)
    monkeypatch.setenv("NOVELIST_CRITIC_LLM_BASE_URL", "http://critic")
    monkeypatch.setenv("NOVELIST_CRITIC_LLM_API_KEY", "ck")
    captured = {}

    class FakeResp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self):
            import json
            return json.dumps({"choices": [{"message": {"content": "ok"}}], "usage": {"prompt_tokens": 5, "completion_tokens": 3}}).encode("utf-8")

    def fake_urlopen(request, timeout=60):
        captured["url"] = request.full_url
        captured["auth"] = request.headers.get("Authorization")
        return FakeResp()

    import worker.provider_executor as pe
    monkeypatch.setattr(pe, "urlopen", fake_urlopen)
    adapter = AnthropicWritingAdapter()
    result = adapter._chat(
        model_profile={"provider_model_name": "m", "base_url_env": "NOVELIST_CRITIC_LLM_BASE_URL", "api_key_env": "NOVELIST_CRITIC_LLM_API_KEY"},
        system="s", user="u",
    )
    assert "http://critic" in captured["url"]
    assert captured["auth"] == "Bearer ck"
    # _chat 现在返回 dict（Task 2 会用 usage；此步先确认 text 可取）
    text = result["text"] if isinstance(result, dict) else result
    assert text == "ok"
```

注意：本 Task 让 `_chat` 已返回 dict（含 text）；Task 2 补全 usage/latency 字段。若你想 Task 1 只改 env 读取、保持返回 str，则把上面断言改为 `assert result == "ok"`，并在 Task 2 再改 dict——但为减少反复，本计划让 Task 1 直接改为返回 dict（见 Step 3）。

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_provider_executor.py::test_chat_reads_profile_specific_env -q`
Expected: FAIL — `_chat` 读硬编码 NOVELIST_LLM_BASE_URL（critic env 读不到）且返回 str 无 text 键

- [ ] **Step 3: 改 `_chat` 读 profile env + 返回 dict**

将 `AnthropicWritingAdapter._chat`（provider_executor.py:50）替换为：

```python
    def _chat(self, *, model_profile: dict[str, Any], system: str, user: str) -> dict[str, Any]:
        import time
        base_env = model_profile.get("base_url_env", "NOVELIST_LLM_BASE_URL")
        key_env = model_profile.get("api_key_env", "NOVELIST_LLM_API_KEY")
        base_url = os.getenv(base_env)
        api_key = os.getenv(key_env)
        if not base_url or not api_key:
            text = f"（离线草稿）{user.strip()[:280]}"
            # 无 key 确定性估算指标（按字符长度派生，供 provider_calls 兜底）
            return {"text": text, "prompt_tokens": len(user) // 2, "completion_tokens": len(text) // 2, "latency_ms": 0}
        endpoint = base_url.rstrip("/") + "/chat/completions"
        body = json.dumps({
            "model": model_profile["provider_model_name"],
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "temperature": 0.4,
            "max_tokens": 600,
        }).encode("utf-8")
        request = Request(endpoint, data=body, headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"}, method="POST")
        started = time.monotonic()
        try:
            with urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise ProviderExecutionError("provider_http_error", f"provider request failed: {exc.code}") from exc
        except URLError as exc:
            raise ProviderExecutionError("provider_network_error", "provider request failed") from exc
        except TimeoutError as exc:
            raise ProviderExecutionError("provider_timeout", "provider request timed out") from exc
        latency_ms = int((time.monotonic() - started) * 1000)
        try:
            text = payload["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderExecutionError("provider_response_invalid", "provider response missing message content") from exc
        usage = payload.get("usage") or {}
        return {"text": text, "prompt_tokens": int(usage.get("prompt_tokens", 0)), "completion_tokens": int(usage.get("completion_tokens", 0)), "latency_ms": latency_ms}
```

同步更新三个调用 `_chat` 的方法（draft_section/review_sections/humanize_section）取 `result["text"]`：找到它们内 `text = self._chat(...)` 处，改为 `chat = self._chat(...)` 后用 `chat["text"]`，并把 `chat` 的指标透传到返回 dict（draft_section 返回加 `"prompt_tokens"/"completion_tokens"/"latency_ms"`）。review_sections 内 `review = self._chat(...)` 改为 `review = self._chat(...)["text"]`。humanize_section 同 draft。

- [ ] **Step 4: seed 加默认 env 字段**

在 model_profile seed（phase_two_store.py:1227-1248）两个 profile dict 各加：

```python
        "base_url_env": "NOVELIST_LLM_BASE_URL",
        "api_key_env": "NOVELIST_LLM_API_KEY",
```

- [ ] **Step 5: 运行确认通过**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_provider_executor.py -q`
Expected: PASS（现有 test_provider_executor 用例中调 draft/humanize 的断言仍绿——它们取 writer_output/humanized_text 不受 dict 化影响）

- [ ] **Step 6: 提交**

```bash
git add apps/ai-worker/worker/provider_executor.py apps/core-service/app/core/phase_two_store.py apps/ai-worker/tests/test_provider_executor.py
git commit -m "feat: drive provider credentials by per-profile env references"
```

---

### Task 2: 真实 provider_calls 指标（pipeline 写回真值）

**Files:**
- Modify: `apps/ai-worker/worker/provider_executor.py`（`execute_writing_provider_pipeline` :171-266）
- Test: `apps/ai-worker/tests/test_provider_executor.py`（追加）

**Interfaces:**
- Consumes: `_chat` 返回的 usage/latency（Task 1）。
- Produces: pipeline 把 writer/critic/humanizer 的真实 token/latency 写回对应 provider_calls 项，`cost_estimate` 由真实 token 算、`cost_estimate_status="measured"`。

- [ ] **Step 1: 写失败测试**

追加到 `apps/ai-worker/tests/test_provider_executor.py`：

```python
def test_pipeline_writes_real_metrics_to_provider_calls(monkeypatch):
    import worker.provider_executor as pe
    from worker.provider_executor import AnthropicWritingAdapter
    # mock _chat 返回真实 usage
    monkeypatch.setattr(AnthropicWritingAdapter, "_chat", lambda self, **k: {"text": "正文", "prompt_tokens": 111, "completion_tokens": 47, "latency_ms": 321})

    class FakeStore:
        class STORE:
            provider_calls_by_writing = {"WR1": [
                {"provider_call_id": "c-w", "agent_role": "writer", "model_profile_id": "p", "status": "succeeded", "prompt_tokens": 1800, "completion_tokens": 920, "latency_ms": 1430, "cost_estimate": 0.31, "cost_estimate_status": "estimated", "retry_count": 0},
                {"provider_call_id": "c-c", "agent_role": "critic", "model_profile_id": "p", "status": "succeeded", "prompt_tokens": 1400, "completion_tokens": 540, "latency_ms": 980, "cost_estimate": 0.22, "cost_estimate_status": "estimated", "retry_count": 0},
                {"provider_call_id": "c-h", "agent_role": "humanizer", "model_profile_id": "p", "status": "succeeded", "prompt_tokens": 1780, "completion_tokens": 850, "latency_ms": 1210, "cost_estimate": 0.33, "cost_estimate_status": "estimated", "retry_count": 0},
            ]}
            model_profiles = {"p": {"provider_name": "anthropic", "provider_model_name": "m"}}
        def _build_model_cost(self, calls, retry):
            return {"input_tokens": sum(c["prompt_tokens"] for c in calls), "output_tokens": sum(c["completion_tokens"] for c in calls), "estimated_total_cost": sum(c["cost_estimate"] for c in calls), "retry_count": retry}

    store = FakeStore()
    writing_run = {"writing_run_id": "WR1", "consistency_report_id": "CR1"}
    chapter_plan = {"payload": {"summary": "s"}}
    section_plans = [{"section_plan_id": "SP1", "payload": {"scene_goal": "g", "beats": [{"index": 1, "summary": "b"}]}}]
    section_runs = [{"section_run_id": "SR1", "draft_object_ref": "object://d1", "critic_report_ref": "cr", "humanized_object_ref": "hr", "beat_status": [{"index": 1}]}]
    result = pe.execute_writing_provider_pipeline(
        store=store, writing_run=writing_run, chapter_plan=chapter_plan,
        section_plans=section_plans, section_runs=section_runs, prompt_package={"template_refs": []},
        knowledge_context="",
    )
    writer_call = next(c for c in result["provider_calls"] if c["agent_role"] == "writer")
    assert writer_call["prompt_tokens"] == 111
    assert writer_call["completion_tokens"] == 47
    assert writer_call["latency_ms"] == 321
    assert writer_call["cost_estimate_status"] == "measured"
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_provider_executor.py::test_pipeline_writes_real_metrics_to_provider_calls -q`
Expected: FAIL — provider_calls 仍是写死 1800/920，status 仍 estimated

- [ ] **Step 3: pipeline 写回真实指标**

在 `execute_writing_provider_pipeline`（provider_executor.py，drafts 生成后、return 前）加入：把 draft/humanize 返回的指标与 review 指标累加到对应 provider_calls。draft_section/humanize_section 返回 dict 需含 `prompt_tokens/completion_tokens/latency_ms`（Task 1 已透传）。review_sections 需返回时也带一个指标（可在其内累计 `_chat` 结果）。

在 return 前插入：

```python
    COST_PER_1K = 0.002

    def _apply_metrics(call: dict[str, Any], pt: int, ct: int, lat: int) -> None:
        call["prompt_tokens"] = pt
        call["completion_tokens"] = ct
        call["latency_ms"] = lat
        call["cost_estimate"] = round((pt + ct) / 1000 * COST_PER_1K, 4)
        call["cost_estimate_status"] = "measured"

    writer_metrics = {"pt": sum(d.get("prompt_tokens", 0) for d in drafts), "ct": sum(d.get("completion_tokens", 0) for d in drafts), "lat": max((d.get("latency_ms", 0) for d in drafts), default=0)}
    humanizer_metrics = {"pt": sum(h.get("prompt_tokens", 0) for h in humanized_results), "ct": sum(h.get("completion_tokens", 0) for h in humanized_results), "lat": max((h.get("latency_ms", 0) for h in humanized_results), default=0)}
    for call in provider_calls:
        if call.get("agent_role") == "writer" and call.get("status") == "succeeded":
            _apply_metrics(call, writer_metrics["pt"], writer_metrics["ct"], writer_metrics["lat"])
        elif call.get("agent_role") == "humanizer" and call.get("status") == "succeeded":
            _apply_metrics(call, humanizer_metrics["pt"], humanizer_metrics["ct"], humanizer_metrics["lat"])
        elif call.get("agent_role") == "critic" and call.get("status") == "succeeded" and critic_metrics:
            _apply_metrics(call, critic_metrics["pt"], critic_metrics["ct"], critic_metrics["lat"])
```

为此需在循环中收集 `humanized_results`（humanize_section 的完整返回 dict 列表）与 `critic_metrics`。把 humanize 调用改为 `humanized = humanizer_adapter.humanize_section(...)` 后 `humanized_results.append(humanized)`（在循环前 `humanized_results = []`）。critic_metrics 从 review_sections 返回获取——若 review_sections 不便改返回签名，则 critic 指标可省略真实化（保持 estimated），本 Task 至少保证 writer/humanizer 真实。

- [ ] **Step 4: 运行确认通过**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_provider_executor.py -q`
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add apps/ai-worker/worker/provider_executor.py apps/ai-worker/tests/test_provider_executor.py
git commit -m "feat: write measured token and latency metrics to provider calls"
```

---

### Task 3: 前端配置真落库

**Files:**
- Modify: `apps/web/src/lib/api-client.ts`
- Modify: `apps/web/src/state/phase-two-provider.tsx`（:53-62）
- Test: `apps/web/src/test/api-client.test.ts`（追加）

**Interfaces:**
- Produces: api-client `setModelProfileEnabled(modelProfileId, enabled)`、`updateAgentAssignment(assignmentId, modelProfileId)`、`updateQualityGateProfile(profileId, aiFlavorThreshold, originalitySafetyThreshold)`。

- [ ] **Step 1: 写失败测试**

追加到 `apps/web/src/test/api-client.test.ts`：

```typescript
it("posts configuration mutations", async () => {
  const fetcher = vi.fn().mockResolvedValue(jsonResponse({ configuration_snapshot: { modelProfiles: [] } }));
  const client = createNovelFactoryApiClient({ baseUrl: "http://api.local", fetcher });
  await client.setModelProfileEnabled("mp-1", false);
  expect(fetcher).toHaveBeenCalledWith("http://api.local/v1/configuration/model-profiles/mp-1", expect.objectContaining({
    method: "POST",
    body: JSON.stringify({ enabled: false }),
  }));
});
```

（端点路径以 configuration.py 实际路由为准，实现时核对 `apps/api-gateway`/`apps/core-service` 的 configuration 路由前缀。）

- [ ] **Step 2: 运行确认失败**

Run: `rtk pnpm --filter @novel-factory/web test --run src/test/api-client.test.ts`
Expected: FAIL — `setModelProfileEnabled` 不存在

- [ ] **Step 3: api-client 加方法**

先核对后端路由：`grep -rn "model-profiles\|agent-model-assignments\|quality-gate" apps/api-gateway/app/api apps/core-service/app/api`。按实际路径在 `apps/web/src/lib/api-client.ts` 的 NovelFactoryApiClient 加：

```typescript
  async setModelProfileEnabled(modelProfileId: string, enabled: boolean) {
    return this.post(`/v1/configuration/model-profiles/${modelProfileId}`, { enabled });
  }

  async updateAgentAssignment(assignmentId: string, modelProfileId: string) {
    return this.post(`/v1/configuration/agent-model-assignments/${assignmentId}`, { model_profile_id: modelProfileId });
  }

  async updateQualityGateProfile(profileId: string, aiFlavorThreshold: number, originalitySafetyThreshold: number) {
    return this.post(`/v1/configuration/quality-gate-profiles/${profileId}`, { ai_flavor_threshold: aiFlavorThreshold, originality_safety_threshold: originalitySafetyThreshold });
  }
```

（路径按实际后端路由调整。）

- [ ] **Step 4: 运行确认通过**

Run: `rtk pnpm --filter @novel-factory/web test --run src/test/api-client.test.ts`
Expected: PASS

- [ ] **Step 5: provider 接线（有 API 走后端）**

在 `apps/web/src/state/phase-two-provider.tsx`，用 `resolveApiBaseUrl()` 建 apiClient；toggleModelProfile/updateAgentAssignment/updateQualityGateProfile 改为：apiClient 存在时 await 后端方法并用返回 configuration_snapshot 刷新对应 state（若后端返回快照结构与本地 state 一致则 setState；否则保留本地 reducer 兜底），无 API 时保持现有 `...InState` reducer。保持函数签名不变（组件调用不改）。

- [ ] **Step 6: web 全量绿**

Run: `rtk pnpm --filter @novel-factory/web test --run`
Expected: PASS（现有 configuration 相关测试若断言本地 reducer 行为，在无 stubEnv API base 时仍走本地分支不变）

- [ ] **Step 7: 提交**

```bash
git add apps/web/src/lib/api-client.ts apps/web/src/state/phase-two-provider.tsx apps/web/src/test/api-client.test.ts
git commit -m "feat: persist configuration mutations to backend from web"
```

---

### Task 4: router 纳入 max_cost + 清 critic 硬编码

**Files:**
- Modify: `apps/core-service/app/core/phase_two_store.py`（`resolve_model_profile` :3960-4011）
- Modify: `apps/ai-worker/worker/provider_executor.py`（critic issue summary :220）
- Test: `apps/core-service/tests/test_phase_two_api.py`、`apps/ai-worker/tests/test_provider_executor.py`

**做法与验收见下。**

- [ ] **Step 1: 写失败测试（core router）**

追加到 `apps/core-service/tests/test_phase_two_api.py`：

```python
def test_resolve_model_profile_skips_over_max_cost():
    from app.core import phase_two_store as store
    store.reset_store()
    store.seed_phase_two_demo_data()
    # 给 default profile 标一个高 est_cost，assignment max_cost 很低 → 跳过走 fallback
    default_id = store.MODEL_PROFILE_DEFAULT_ID
    store.STORE.model_profiles[default_id]["est_cost"] = 9.99
    assignment = store._get_agent_assignment("writer")
    assignment["max_cost"] = 0.5
    result = store.resolve_model_profile("writer")
    # 应跳过超成本的 default，落到 fallback（structured）或返回 None 记 failed call
    assert result["selected_profile"] is None or result["selected_profile"]["model_profile_id"] != default_id
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_two_api.py::test_resolve_model_profile_skips_over_max_cost -q`
Expected: FAIL — 当前 resolve 不看 max_cost，仍返回 default

- [ ] **Step 3: resolve_model_profile 加 max_cost 过滤**

在 `resolve_model_profile`（phase_two_store.py:3977-3982 的候选遍历）里，除 enabled/structured 校验外，加：若 `assignment` 有 `max_cost` 且候选 profile 的 `est_cost`（缺省视为 0）超过 max_cost，则记一条 failed provider_call（error `cost_budget_exceeded`）、retry_count+1、跳过该候选。保持其余逻辑不变。

- [ ] **Step 4: 运行确认通过**

Run: `cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_two_api.py::test_resolve_model_profile_skips_over_max_cost -q`
Expected: PASS

- [ ] **Step 5: 清 critic 硬编码 + 测试**

将 `provider_executor.py:220` 的 `"summary": "主角境界描写与已批准设定冲突，需回收并重写冲突升级段。"` 改为用真实 issue 文本：`"summary": issue.get("summary", "一致性问题待复核。")`。

追加到 `apps/ai-worker/tests/test_provider_executor.py`：

```python
def test_critic_issue_summary_not_hardcoded(monkeypatch):
    import worker.provider_executor as pe
    from worker.provider_executor import AnthropicWritingAdapter
    monkeypatch.setattr(AnthropicWritingAdapter, "_chat", lambda self, **k: {"text": "境界前后矛盾需修正", "prompt_tokens": 1, "completion_tokens": 1, "latency_ms": 1})
    monkeypatch.setenv("NOVELIST_LLM_BASE_URL", "http://x")
    monkeypatch.setenv("NOVELIST_LLM_API_KEY", "k")
    # review_sections 有 key 时走真实判定，issue.summary 来自 review 文本，非写死斗破苍穹
    adapter = AnthropicWritingAdapter()
    issues = adapter.review_sections(
        section_runs=[{"draft_object_ref": "object://d1"}, {"draft_object_ref": "object://d2"}],
        drafts=[{"writer_output": "a"}, {"writer_output": "b"}],
        consistency_report_id="CR1", model_profile={"provider_model_name": "m"},
    )
    assert all("主角境界描写与已批准设定冲突" not in str(i) for i in issues)
```

- [ ] **Step 6: 运行确认通过**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_provider_executor.py -q`
Expected: PASS

- [ ] **Step 7: 提交**

```bash
git add apps/core-service/app/core/phase_two_store.py apps/ai-worker/worker/provider_executor.py apps/core-service/tests/test_phase_two_api.py apps/ai-worker/tests/test_provider_executor.py
git commit -m "feat: route by max cost budget and drop hardcoded critic summary"
```

---

## Verification（整批完成后）

```bash
git checkout -- apps/*/pyproject.toml 2>/dev/null; rm -f apps/*/uv.lock
cd apps/ai-worker && rtk python3 -m pytest tests -q
cd apps/core-service && .venv/bin/python -m pytest tests/test_phase_two_api.py tests/test_phase_three_api.py tests/test_persistence.py -q
rtk pnpm --filter @novel-factory/web test --run
rtk pnpm --filter @novel-factory/contracts test
```

浏览器手验：配置中心 toggle profile → 刷新后仍生效；配不同 role 的 base_url env → 生成时不同段走不同 provider；provider_calls 指标反映真实 token（配 key）。

## Done bar
- 不同 role 可配不同 provider（profile env 引用）。
- provider_calls token/latency/cost 真实（配 key），cost_estimate_status="measured"。
- 前端配置 POST 后端、刷新不丢。
- router 纳入 max_cost；critic issue 去硬编码。
- 全量测试绿；现有 demo 测试仍绿；未碰 deep_analysis/多书隔离。
