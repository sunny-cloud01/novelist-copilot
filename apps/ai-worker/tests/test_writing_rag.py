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
