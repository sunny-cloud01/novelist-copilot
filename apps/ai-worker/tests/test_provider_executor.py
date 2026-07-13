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
