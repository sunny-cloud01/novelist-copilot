import worker.provider_executor as pe
from worker.provider_executor import AnthropicWritingAdapter


def test_base_adapter_has_chat_with_fallback(monkeypatch):
    monkeypatch.delenv("NOVELIST_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("NOVELIST_LLM_API_KEY", raising=False)
    adapter = AnthropicWritingAdapter()
    # 无 key → 确定性 fallback，非 user[:320] 裸截断，含可读中文
    out = adapter._chat(model_profile={"provider_model_name": "m"}, system="s", user="写一段")
    assert isinstance(out, dict) and out.get("text")


def test_draft_injects_knowledge_context(monkeypatch):
    captured = {}

    def fake_chat(self, *, model_profile, system, user):
        captured["user"] = user
        captured["system"] = system
        return {"text": "草稿正文", "prompt_tokens": 1, "completion_tokens": 1, "latency_ms": 0}

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
