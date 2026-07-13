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
