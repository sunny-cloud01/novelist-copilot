from worker.extraction import _extract_entity_candidates, _aggregate_entities, _build_graph_from_analysis


def test_build_graph_from_analysis_links_relationships():
    objects = [
        {"object_id": "RUN1OBJ001", "canonical_name": "萧宁", "object_type": "character",
         "confidence": 0.9, "review_status": "pending", "lifecycle_status": "candidate",
         "evidence_refs": ["evidence://E1"], "payload": {"aliases": ["宁"], "summary": "少年"}},
        {"object_id": "RUN1OBJ002", "canonical_name": "云岚宗", "object_type": "faction",
         "confidence": 0.8, "review_status": "pending", "lifecycle_status": "candidate",
         "evidence_refs": ["evidence://E2"], "payload": {"aliases": [], "summary": "宗门"}},
    ]
    edges = {
        "RUN1RELATION0101": {
            "edge_id": "RUN1RELATION0101",
            "source_id": "object://knowledge-objects/RUN1OBJ001",
            "target_id": "object://knowledge-objects/RUN1OBJ002",
            "relation_type": "pressured_by", "confidence": 0.7,
            "evidence_refs": ["evidence://E1"],
        }
    }
    graph = _build_graph_from_analysis(objects, edges, book_id="BOOK1", run_id="RUN1")
    assert graph["summary"]["node_count"] == 2
    assert graph["summary"]["edge_count"] == 1
    node_ids = list(graph["node_details"].keys())
    first = graph["node_details"][node_ids[0]]
    assert first["label"] == "萧宁"
    assert first["canonical_object_id"] == "RUN1OBJ001"
    # 双向邻居
    assert any(n["direction"] == "outgoing" for n in graph["neighbors"][node_ids[0]])
    assert any(n["direction"] == "incoming" for n in graph["neighbors"][node_ids[1]])
    assert "Xiao Yan" not in {d["label"] for d in graph["node_details"].values()}


def test_build_graph_from_analysis_resolves_edges_by_entity_name():
    objects = [
        {"object_id": "RUN1OBJ001", "canonical_name": "萧宁", "object_type": "character",
         "confidence": 0.9, "review_status": "pending", "lifecycle_status": "candidate",
         "evidence_refs": [], "payload": {"aliases": ["宁少"], "summary": "少年"}},
        {"object_id": "RUN1OBJ002", "canonical_name": "云岚宗", "object_type": "faction",
         "confidence": 0.8, "review_status": "pending", "lifecycle_status": "candidate",
         "evidence_refs": [], "payload": {"aliases": [], "summary": "宗门"}},
    ]
    # 端点是人名/别名而非 object:// 引用，仍应连上边
    edges = {
        "RUN1RELATION0101": {
            "edge_id": "RUN1RELATION0101",
            "source_id": "宁少",
            "target_id": "云岚宗",
            "relation_type": "pressured_by", "confidence": 0.7, "evidence_refs": [],
        }
    }
    graph = _build_graph_from_analysis(objects, edges, book_id="BOOK1", run_id="RUN1")
    assert graph["summary"]["edge_count"] == 1
    node_ids = list(graph["node_details"].keys())
    assert any(graph["neighbors"][node_id] for node_id in node_ids)


def test_run_extract_knowledge_produces_book_specific_objects(monkeypatch):
    import worker.extraction as extraction

    class FakeStore:
        class STORE:  # noqa: N801
            pass
        def get_book_source_content(self, book_id):
            return {"content": "萧宁进入云岚宗。云岚宗长老审视萧宁。", "object_ref": "object://source-contents/SC1"}
        def list_book_chapters(self, book_id):
            return [{"chapter_id": "CH1", "chapter_index": 1, "title": "云岚宗试炼",
                     "raw_text": "萧宁进入云岚宗。云岚宗长老审视萧宁。萧宁沉默。云岚宗。"}]
        def apply_task_execution_result(self, task_id, status, output_refs, metrics, **kwargs):
            self.captured = metrics
            return {"status": status, "output_refs": output_refs}

    fake = FakeStore()
    monkeypatch.setattr(extraction, "load_phase_two_store", lambda: fake)
    monkeypatch.setattr(extraction, "_resolve_extraction_profile", lambda store: (None, [], None))
    command = extraction.build_extract_knowledge_command(book_id="BOOK1", run_id="RUN1")
    extraction.run_extract_knowledge(command)
    objects = fake.captured["knowledge_objects"]
    labels = {o["canonical_name"] for o in objects}
    assert labels
    assert "Xiao Yan" not in labels
    assert "graph_node_details" in fake.captured
    assert fake.captured["graph_summary"]["node_count"] == len(objects)
    # 修复回归：真实管线里关系边必须能连上，而不是恒 0。
    assert len(objects) >= 2
    assert fake.captured["graph_summary"]["edge_count"] >= 1
    neighbors_by_node = fake.captured["graph_neighbors_by_node"]
    assert any(neighbors_by_node[node_id] for node_id in neighbors_by_node)


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
