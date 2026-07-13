from worker.extraction import _extract_entity_candidates, _aggregate_entities


def test_extract_entity_candidates_uses_chapter_title_not_hardcoded():
    chapter = {"chapter_index": 1, "title": "云岚宗试炼", "raw_text": "萧宁走入云岚宗，云岚宗长老出面。萧宁沉默。"}
    candidates = _extract_entity_candidates(chapter)
    names = {c["name"] for c in candidates}
    assert "Xiao Yan" not in names
    assert any("云岚宗" in n or "萧宁" in n for n in names)
    assert all(0.0 <= c["confidence"] <= 1.0 for c in candidates)


def test_aggregate_entities_merges_and_ids():
    lists = [
        [{"name": "萧宁", "type": "character", "aliases": ["宁"], "confidence": 0.6, "summary": "少年"}],
        [{"name": "萧宁", "type": "character", "aliases": ["小宁"], "confidence": 0.9, "summary": "少年"}],
    ]
    objects = _aggregate_entities(lists, run_id="RUN1", workspace_id="WS1")
    assert len(objects) == 1
    obj = objects[0]
    assert obj["object_id"].startswith("RUN1OBJ")
    assert obj["canonical_name"] == "萧宁"
    assert obj["confidence"] == 0.9
    assert set(obj["payload"]["aliases"]) == {"宁", "小宁"}
    assert obj["lifecycle_status"] in {"candidate", "approved"}
