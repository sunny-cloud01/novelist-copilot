# P0 打通线1真实拆书 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让上传任意 txt 书后拆书产出属于那本书的真实实体、知识图谱节点/边、可导出 BookKnowledgePackage，不再恒返回写死的斗破苍穹。

**Architecture:** ai-worker 的 per-chapter LLM 调用已真实产出 scene/event/relationship；在同一调用加抽 entities，跨章聚合成 knowledge_objects，从深拆 relationships 建图谱三张表；无 LLM key 时从章节文本确定性派生实体（永不回退斗破苍穹）；core-service store 落 graph_node_details/neighbors 并组装真实 knowledge package；前端与 .env 默认化让开箱可跑。

**Tech Stack:** Python 3.11 (ai-worker worker/, core-service app/), pytest, React + Vite + vitest (apps/web), 内存 CoreStore + 业务表持久化。

## Global Constraints
- 不硬编码任何真实 API 密钥。
- 生产路径写失败必须失败，不静默 file fallback；测试需 fallback 时显式设 `NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK=1`。
- 保持 HTTP API shape 不变；现有 demo book（`GRAPH_BOOK_ID` seed）相关测试仍需绿。
- 实体/图谱 fallback 绝不含硬编码 "Xiao Yan"/"Yao Lao"/"Xiao Clan"。
- 每任务 ≤2 迭代 / ~15 分钟。
- 命令统一用 `rtk` 前缀运行。

---

### Task 1: 确定性实体 fallback + 跨章聚合

**Files:**
- Modify: `apps/ai-worker/worker/extraction.py`（在 `_build_fallback_chapter_analysis` 之后，约 :415 处新增函数）
- Test: `apps/ai-worker/tests/test_extraction_entities.py`（新建）

**Interfaces:**
- Produces:
  - `_extract_entity_candidates(chapter: dict) -> list[dict]`：从单章 raw_text/title 派生候选，元素 `{"name": str, "type": str, "aliases": list[str], "confidence": float, "summary": str}`。
  - `_aggregate_entities(entity_lists: list[list[dict]], run_id: str, workspace_id: str) -> list[dict]`：跨章合并去重，返回 knowledge_object dict（含 `object_id`, `object_type`, `canonical_name`, `lifecycle_status`, `review_status`, `confidence`, `evidence_refs`, `payload.aliases`）。

- [ ] **Step 1: 写失败测试**

新建 `apps/ai-worker/tests/test_extraction_entities.py`：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_extraction_entities.py -q`
Expected: FAIL — `ImportError: cannot import name '_extract_entity_candidates'`

- [ ] **Step 3: 实现两个函数**

在 `apps/ai-worker/worker/extraction.py` 的 `_build_fallback_chapter_analysis` 函数之后插入：

```python
import re

_ENTITY_TYPE_HINTS = {
    "宗": "faction", "门": "faction", "派": "faction", "族": "clan", "家": "clan",
    "城": "location", "山": "location", "谷": "location", "殿": "location",
}


def _guess_entity_type(name: str) -> str:
    for suffix, entity_type in _ENTITY_TYPE_HINTS.items():
        if name.endswith(suffix):
            return entity_type
    return "character"


def _extract_entity_candidates(chapter: dict[str, Any]) -> list[dict[str, Any]]:
    text = (chapter.get("raw_text") or chapter.get("text_excerpt") or "")
    title = str(chapter.get("title") or "").strip()
    # 中文专名候选：2-4 连续汉字，按频次排序
    tokens = re.findall(r"[一-龥]{2,4}", text)
    freq: dict[str, int] = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    if title and title not in seen:
        seen.add(title)
        candidates.append({
            "name": title, "type": _guess_entity_type(title), "aliases": [],
            "confidence": 0.55, "summary": f"章节《{title}》核心对象。",
        })
    for name, count in ranked:
        if count < 2 or name in seen:
            continue
        seen.add(name)
        candidates.append({
            "name": name, "type": _guess_entity_type(name), "aliases": [],
            "confidence": min(0.75, 0.5 + count * 0.05), "summary": f"章节高频对象 {name}。",
        })
        if len(candidates) >= 5:
            break
    return candidates


def _aggregate_entities(
    entity_lists: list[list[dict[str, Any]]], run_id: str, workspace_id: str
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for entity_list in entity_lists:
        for entity in entity_list:
            name = str(entity.get("name", "")).strip()
            if not name:
                continue
            key = name.lower()
            confidence = _confidence(entity.get("confidence"), 0.5)
            aliases = [a.strip() for a in entity.get("aliases", []) if isinstance(a, str) and a.strip()]
            if key not in merged:
                merged[key] = {
                    "canonical_name": name,
                    "object_type": str(entity.get("type") or "character"),
                    "aliases": set(aliases),
                    "confidence": confidence,
                    "summary": _text(entity.get("summary"), f"{name} 相关对象。"),
                }
            else:
                record = merged[key]
                record["aliases"].update(aliases)
                if confidence > record["confidence"]:
                    record["confidence"] = confidence
                    record["object_type"] = str(entity.get("type") or record["object_type"])
    objects: list[dict[str, Any]] = []
    for index, (_, record) in enumerate(merged.items(), start=1):
        confidence = record["confidence"]
        lifecycle = "approved" if confidence >= 0.95 else "candidate"
        objects.append({
            "schema_version": 1,
            "object_id": f"{run_id}OBJ{index:03d}",
            "workspace_id": workspace_id,
            "object_type": record["object_type"],
            "canonical_name": record["canonical_name"],
            "lifecycle_status": lifecycle,
            "review_status": "approved" if lifecycle == "approved" else "pending",
            "confidence": confidence,
            "evidence_refs": [],
            "payload": {"schema_version": 1, "aliases": sorted(record["aliases"]), "summary": record["summary"]},
        })
    return objects
```

- [ ] **Step 4: 运行确认通过**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_extraction_entities.py -q`
Expected: PASS (2 passed)

- [ ] **Step 5: 提交**

```bash
git add apps/ai-worker/worker/extraction.py apps/ai-worker/tests/test_extraction_entities.py
git commit -m "feat: add deterministic entity extraction and aggregation"
```

---

### Task 2: LLM entities 抽取 + 图谱构建 + run_extract_knowledge 接线

**Files:**
- Modify: `apps/ai-worker/worker/extraction.py`（`_build_chapter_prompt` :417 加 entities 字段；`build_extraction_fixture` :63 降级为空壳；`run_extract_knowledge` :790 接线；新增 `_build_graph_from_analysis`）
- Test: `apps/ai-worker/tests/test_extraction_entities.py`（追加）；`apps/ai-worker/tests/test_bootstrap.py`（如断言旧 fixture 三对象则更新）

**Interfaces:**
- Consumes: `_extract_entity_candidates`, `_aggregate_entities`（Task 1）。
- Produces:
  - `_build_graph_from_analysis(knowledge_objects: list[dict], relationship_edges: dict[str, dict], book_id: str, run_id: str) -> dict`：返回 `{"summary": {...}, "node_details": {node_id: {...}}, "neighbors": {node_id: [edge,...]}}`。node_details 元素含 `node_id, book_id, label, node_type, canonical_object_id, review_status, lifecycle_status, confidence, aliases, summary, evidence_refs`；neighbors 元素含 `edge_id, relation_type, direction, neighbor_node_id, neighbor_label, neighbor_type, confidence, evidence_refs`。
  - metrics 新增键 `graph_node_details`, `graph_neighbors_by_node`（供 Task 3 store 消费）。

- [ ] **Step 1: 写失败测试（graph 构建）**

追加到 `apps/ai-worker/tests/test_extraction_entities.py`：

```python
from worker.extraction import _build_graph_from_analysis


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
```

- [ ] **Step 2: 运行确认失败**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_extraction_entities.py::test_build_graph_from_analysis_links_relationships -q`
Expected: FAIL — `cannot import name '_build_graph_from_analysis'`

- [ ] **Step 3: 实现 `_build_graph_from_analysis`**

在 `apps/ai-worker/worker/extraction.py` 的 `_aggregate_entities` 之后插入：

```python
def _build_graph_from_analysis(
    knowledge_objects: list[dict[str, Any]],
    relationship_edges: dict[str, dict[str, Any]],
    book_id: str,
    run_id: str,
) -> dict[str, Any]:
    node_by_object: dict[str, str] = {}
    node_details: dict[str, dict[str, Any]] = {}
    summary_nodes: list[dict[str, Any]] = []
    for index, obj in enumerate(knowledge_objects, start=1):
        node_id = f"{run_id}NODE{index:03d}"
        node_by_object[obj["object_id"]] = node_id
        aliases = obj.get("payload", {}).get("aliases", [])
        node_details[node_id] = {
            "schema_version": 1,
            "node_id": node_id,
            "book_id": book_id,
            "label": obj["canonical_name"],
            "node_type": obj["object_type"],
            "canonical_object_id": obj["object_id"],
            "review_status": obj.get("review_status", "pending"),
            "lifecycle_status": obj.get("lifecycle_status", "candidate"),
            "confidence": obj.get("confidence", 0.5),
            "aliases": aliases,
            "summary": obj.get("payload", {}).get("summary", f"{obj['canonical_name']} 相关对象。"),
            "evidence_refs": obj.get("evidence_refs", []),
        }
        summary_nodes.append({
            "node_id": node_id,
            "label": obj["canonical_name"],
            "node_type": obj["object_type"],
            "evidence_refs": obj.get("evidence_refs", []),
        })

    def _resolve_node(ref: str) -> str | None:
        object_id = ref.rsplit("/", 1)[-1] if isinstance(ref, str) else ref
        return node_by_object.get(object_id)

    neighbors: dict[str, list[dict[str, Any]]] = {node_id: [] for node_id in node_details}
    edge_count = 0
    for edge in relationship_edges.values():
        source_node = _resolve_node(edge.get("source_id"))
        target_node = _resolve_node(edge.get("target_id"))
        if not source_node or not target_node or source_node == target_node:
            continue
        edge_count += 1
        relation = edge.get("relation_type", "related_to")
        confidence = edge.get("confidence", 0.7)
        evidence_refs = edge.get("evidence_refs", [])
        neighbors[source_node].append({
            "edge_id": edge["edge_id"], "relation_type": relation, "direction": "outgoing",
            "neighbor_node_id": target_node, "neighbor_label": node_details[target_node]["label"],
            "neighbor_type": node_details[target_node]["node_type"], "confidence": confidence,
            "evidence_refs": evidence_refs,
        })
        neighbors[target_node].append({
            "edge_id": edge["edge_id"], "relation_type": relation, "direction": "incoming",
            "neighbor_node_id": source_node, "neighbor_label": node_details[source_node]["label"],
            "neighbor_type": node_details[source_node]["node_type"], "confidence": confidence,
            "evidence_refs": evidence_refs,
        })

    return {
        "summary": {
            "schema_version": 1, "book_id": book_id,
            "node_count": len(summary_nodes), "edge_count": edge_count, "nodes": summary_nodes,
        },
        "node_details": node_details,
        "neighbors": neighbors,
    }
```

- [ ] **Step 4: 运行确认 graph 测试通过**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests/test_extraction_entities.py -q`
Expected: PASS (3 passed)

- [ ] **Step 5: prompt 加 entities 字段**

在 `_build_chapter_prompt`（:417）返回的 JSON 结构里，`"climax"` 行之后、`scenes` 数组同级加入顶层 `entities`。将函数末尾 return 的 JSON 模板字符串扩展，在 `"summary"` 键后追加：

```python
        '  "entities": [{"name": "人物或势力名", "type": "character|clan|mentor|faction|location", "aliases": ["别名"], "confidence": 0.0, "summary": "一句话说明"}],\n'
```

（插到 `'  "summary": "章节摘要",\n'` 之后一行。）

- [ ] **Step 6: `build_extraction_fixture` 降级为空壳**

将 `build_extraction_fixture`（:63）中 `low_confidence_items`、`approved_items` 改为空列表，并把 `knowledge_objects` 与 `graph_summary.nodes` 置空、计数归零：

```python
    low_confidence_items: list[dict[str, Any]] = []
    approved_items: list[dict[str, Any]] = []
```

并在 return 的 `run` 里 `"object_count": 0, "evidence_count": 0, "low_confidence_count": 0`，`graph_summary` 改为 `{"schema_version": 1, "book_id": book_id, "node_count": 0, "edge_count": 0, "nodes": []}`，`knowledge_objects` 使用空的 `low_confidence_items + approved_items`。

- [ ] **Step 7: `run_extract_knowledge` 接线真实实体+图谱**

在 `run_extract_knowledge`（:790）中，`deep_analysis` 循环之后、`scene_count` 之前，加入实体聚合与图谱构建，替换 fixture 数据：

```python
    # 收集每章 entities（provider 提供则用，否则确定性 fallback）
    entity_lists: list[list[dict[str, Any]]] = []
    if chapters:
        for index, chapter in enumerate(chapters[:3], start=1):
            # provider 分析已在上面循环产出；此处对同一 chapter 再取 entities
            pass
    # 用已获得的 chapter_analysis 累积 entities：改造上面的深拆循环，收集 chapter_analysis.get("entities")
```

实际接线方式：在 Step 前面的 `for index, chapter in enumerate(chapters[:3], ...)` 深拆循环体内，`normalized = _normalize_chapter_analysis(...)` 之后追加一行收集：

```python
            raw_entities = chapter_analysis.get("entities") if isinstance(chapter_analysis.get("entities"), list) else []
            if not raw_entities:
                raw_entities = _extract_entity_candidates(chapter)
            entity_lists.append(raw_entities)
```

并在循环外（`scene_count = ...` 之前）加：

```python
    knowledge_objects = _aggregate_entities(entity_lists, run_id=run_id, workspace_id=command["workspace_id"]) if entity_lists else []
    # 绑证据到真实对象
    for obj_index, obj in enumerate(knowledge_objects):
        if evidences:
            obj["evidence_refs"] = [evidences[min(obj_index, len(evidences) - 1)]["evidence_ref"]]
    graph = _build_graph_from_analysis(
        knowledge_objects, deep_analysis["relationship_edges"], book_id=book_id, run_id=run_id,
    )
```

然后把 `object_count`、`low_confidence_count`、`metrics` 中的 `graph_summary`/`knowledge_objects` 改用新变量，并新增两键：

```python
    object_count = len(knowledge_objects)
    low_confidence_count = len([
        item for item in knowledge_objects
        if item.get("review_status") == "pending" and item.get("confidence", 1) < 0.8
    ])
```

metrics 内：`"graph_summary": graph["summary"]`, `"knowledge_objects": knowledge_objects`, 并新增 `"graph_node_details": graph["node_details"]`, `"graph_neighbors_by_node": graph["neighbors"]`。

同时删除 :824-830 处对 `fixture["knowledge_objects"]` 的 evidence/graph 改写（已由新逻辑取代）；并将上面深拆循环里传给 `_chapter_provider_analysis` 和 `_normalize_chapter_analysis` 的 `knowledge_objects=fixture["knowledge_objects"]` 保持不变（首轮无对象时用空列表，normalize 内已有 fallback 到 "protagonist"）。

- [ ] **Step 8: 写端到端集成测试**

追加到 `apps/ai-worker/tests/test_extraction_entities.py`：

```python
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
```

- [ ] **Step 9: 运行 worker 全量**

Run: `cd apps/ai-worker && rtk python3 -m pytest tests -q`
Expected: PASS（若 `test_bootstrap.py` 有断言旧写死三对象/6场景计数，改为断言 `analysis_mode`/结构存在而非具体 Xiao Yan 值）

- [ ] **Step 10: 提交**

```bash
git add apps/ai-worker/worker/extraction.py apps/ai-worker/tests/
git commit -m "feat: build real entities and graph from extraction analysis"
```

---

### Task 3: store 落 graph_node_details / neighbors

**Files:**
- Modify: `apps/core-service/app/core/phase_two_store.py`（`apply_task_execution_result` extraction_run 分支 :5117-5118）
- Test: `apps/core-service/tests/test_persistence.py`

**Interfaces:**
- Consumes: metrics 键 `graph_node_details`, `graph_neighbors_by_node`（Task 2）。

- [ ] **Step 1: 写失败测试**

追加到 `apps/core-service/tests/test_persistence.py`：

```python
def test_apply_task_result_persists_graph_node_details():
    from app.core import phase_two_store as store
    store.reset_store()
    # 取一个真实 extraction task
    run_id = store.RUN_ID
    run = store.STORE.extraction_runs[run_id]
    task_id = run["task"]["task_id"]
    metrics = {
        "graph_summary": {"schema_version": 1, "book_id": run["book_id"], "node_count": 1, "edge_count": 0,
                          "nodes": [{"node_id": "NEWNODE1", "label": "萧宁", "node_type": "character", "evidence_refs": []}]},
        "graph_node_details": {"NEWNODE1": {"schema_version": 1, "node_id": "NEWNODE1", "book_id": run["book_id"],
                              "label": "萧宁", "node_type": "character", "canonical_object_id": "OBJ1",
                              "review_status": "pending", "lifecycle_status": "candidate", "confidence": 0.6,
                              "aliases": [], "summary": "少年", "evidence_refs": []}},
        "graph_neighbors_by_node": {"NEWNODE1": []},
    }
    store.apply_task_execution_result(task_id, "requires_review", run["task"]["output_refs"], metrics,
                                      trace_id="t", dispatch_token=run["task"].get("dispatch_token"))
    assert store.get_graph_node("NEWNODE1") is not None
    assert store.list_graph_neighbors("NEWNODE1") == {"node_id": "NEWNODE1", "items": []}
```

- [ ] **Step 2: 运行确认失败**

Run: `rtk python3 -m pytest apps/core-service/tests/test_persistence.py::test_apply_task_result_persists_graph_node_details -q`
Expected: FAIL — `get_graph_node("NEWNODE1")` 返回 None

- [ ] **Step 3: 实现落表**

在 `apply_task_execution_result` extraction_run 分支，`if graph_summary is not None:`（:5117）块之后追加：

```python
            node_details = metrics.get("graph_node_details")
            neighbors_map = metrics.get("graph_neighbors_by_node")
            if node_details is not None:
                # 清掉该 book 旧节点，再写新节点
                book_id = run["book_id"]
                stale_nodes = [
                    node_id for node_id, node in STORE.graph_node_details.items()
                    if node.get("book_id") == book_id
                ]
                for node_id in stale_nodes:
                    STORE.graph_node_details.pop(node_id, None)
                    STORE.graph_neighbors_by_node.pop(node_id, None)
                for node_id, node in node_details.items():
                    STORE.graph_node_details[node_id] = deepcopy(node)
                if neighbors_map is not None:
                    for node_id, items in neighbors_map.items():
                        STORE.graph_neighbors_by_node[node_id] = deepcopy(items)
```

- [ ] **Step 4: 运行确认通过**

Run: `rtk python3 -m pytest apps/core-service/tests/test_persistence.py::test_apply_task_result_persists_graph_node_details -q`
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add apps/core-service/app/core/phase_two_store.py apps/core-service/tests/test_persistence.py
git commit -m "feat: persist graph node details and neighbors from extraction"
```

---

### Task 4: commit_knowledge_package 真实组装

**Files:**
- Modify: `apps/core-service/app/core/phase_two_store.py`（CoreStore dataclass 加 `knowledge_packages` 字段 约 :120；`commit_knowledge_package` :3539）
- Test: `apps/core-service/tests/test_phase_two_api.py`

**Interfaces:**
- Produces: `commit_knowledge_package(run_id) -> {run_id, status, committed_object_count, package_ref}`；副作用写 `STORE.knowledge_packages[run_id]`。

- [ ] **Step 1: 写失败测试**

追加到 `apps/core-service/tests/test_phase_two_api.py`：

```python
def test_commit_knowledge_package_assembles_real_package():
    from app.core import phase_two_store as store
    store.reset_store()
    run_id = store.RUN_ID
    result = store.commit_knowledge_package(run_id)
    assert result["status"] == "succeeded"
    assert "package_ref" in result
    package = store.STORE.knowledge_packages[run_id]
    assert "metadata" in package
    assert "objects" in package
    assert "relationships" in package
    assert "scenes" in package
    assert package["metadata"]["run_id"] == run_id
```

- [ ] **Step 2: 运行确认失败**

Run: `rtk python3 -m pytest apps/core-service/tests/test_phase_two_api.py::test_commit_knowledge_package_assembles_real_package -q`
Expected: FAIL — `AttributeError: ... 'knowledge_packages'` 或 KeyError

- [ ] **Step 3: 加 CoreStore 字段**

在 CoreStore dataclass（约 :120，`knowledge_objects` 附近）加：

```python
    knowledge_packages: dict[str, dict[str, Any]] = field(default_factory=dict)
```

并在 `reset_store()`（约 :1114 清理块）加 `STORE.knowledge_packages.clear()`。

- [ ] **Step 4: 组装 package**

将 `commit_knowledge_package`（:3539）return 之前替换为：

```python
    object_ids = STORE.knowledge_by_run.get(run_id, [])
    objects = [
        deepcopy(STORE.knowledge_objects[oid]) for oid in object_ids
        if oid in STORE.knowledge_objects
        and STORE.knowledge_objects[oid].get("lifecycle_status") in {"approved", "merged"}
    ]
    book_id = run["book_id"]
    scenes = [
        scene for chapter in list_book_chapters(book_id)
        for scene in STORE.source_scenes_by_chapter.get(chapter["chapter_id"], [])
    ]
    relationships = [
        deepcopy(edge) for edge in STORE.relationship_edges.values()
        if edge.get("book_id") == book_id
    ]
    package_ref = f"object://knowledge-packages/{run_id}"
    STORE.knowledge_packages[run_id] = {
        "schema_version": 1,
        "package_ref": package_ref,
        "metadata": {
            "run_id": run_id, "book_id": book_id,
            "object_count": len(objects), "scene_count": len(scenes),
            "relationship_count": len(relationships), "committed_at": finished_at,
        },
        "source_book": deepcopy(get_book(book_id) or {}),
        "chapters": deepcopy(list_book_chapters(book_id)),
        "scenes": scenes,
        "objects": objects,
        "relationships": relationships,
    }
    run["knowledge_package_ref"] = package_ref
    return {
        "run_id": run_id,
        "status": run["status"],
        "committed_object_count": len(object_ids),
        "package_ref": package_ref,
    }
```

（注意 `STORE.relationship_edges` 值需含 `book_id`，Task 2 的深拆已写入。）

- [ ] **Step 5: 运行确认通过**

Run: `rtk python3 -m pytest apps/core-service/tests/test_phase_two_api.py::test_commit_knowledge_package_assembles_real_package -q`
Expected: PASS

- [ ] **Step 6: 运行相关回归**

Run: `rtk python3 -m pytest apps/core-service/tests/test_phase_two_api.py apps/core-service/tests/test_persistence.py -q`
Expected: PASS

- [ ] **Step 7: 提交**

```bash
git add apps/core-service/app/core/phase_two_store.py apps/core-service/tests/test_phase_two_api.py
git commit -m "feat: assemble real BookKnowledgePackage on commit"
```

---

### Task 5: 默认可跑 — .env.example + 前端 API base helper + 文档

**Files:**
- Modify: `.env.example`
- Create: `apps/web/src/lib/api-base.ts`
- Modify: `apps/web/src/pages.tsx`(:362, :661), `apps/web/src/features/projects/story-bible-wizard-page.tsx`(:17)
- Modify: `README.md`
- Test: `apps/web/src/test/api-base.test.ts`（新建）

**Interfaces:**
- Produces: `resolveApiBaseUrl(): string | undefined` — env 有值用 env；dev 且无 env 返回 `"http://localhost:8080"`；否则 undefined。

- [ ] **Step 1: 写失败测试**

新建 `apps/web/src/test/api-base.test.ts`：

```typescript
import { afterEach, describe, expect, it, vi } from "vitest";
import { resolveApiBaseUrl } from "../lib/api-base";

afterEach(() => vi.unstubAllEnvs());

describe("resolveApiBaseUrl", () => {
  it("uses explicit env when set", () => {
    vi.stubEnv("VITE_NOVEL_FACTORY_API_BASE_URL", "http://api.local");
    expect(resolveApiBaseUrl()).toBe("http://api.local");
  });

  it("falls back to localhost gateway when env empty", () => {
    vi.stubEnv("VITE_NOVEL_FACTORY_API_BASE_URL", "");
    expect(resolveApiBaseUrl()).toBe("http://localhost:8080");
  });
});
```

- [ ] **Step 2: 运行确认失败**

Run: `rtk pnpm --filter @novel-factory/web test --run src/test/api-base.test.ts`
Expected: FAIL — 找不到 `../lib/api-base`

- [ ] **Step 3: 实现 helper**

新建 `apps/web/src/lib/api-base.ts`：

```typescript
export function resolveApiBaseUrl(): string | undefined {
  const explicit = import.meta.env.VITE_NOVEL_FACTORY_API_BASE_URL as string | undefined;
  if (explicit && explicit.trim()) {
    return explicit.trim();
  }
  if (import.meta.env.DEV) {
    return "http://localhost:8080";
  }
  return undefined;
}
```

- [ ] **Step 4: 运行确认通过**

Run: `rtk pnpm --filter @novel-factory/web test --run src/test/api-base.test.ts`
Expected: PASS (2 passed)

- [ ] **Step 5: 接入消费点**

在 `apps/web/src/pages.tsx` 顶部 import 加 `import { resolveApiBaseUrl } from "./lib/api-base";`，将 :362 与 :661 的
`const apiBaseUrl = import.meta.env.VITE_NOVEL_FACTORY_API_BASE_URL as string | undefined;`
改为 `const apiBaseUrl = resolveApiBaseUrl();`。
在 `story-bible-wizard-page.tsx` import 加 `import { resolveApiBaseUrl } from "../../lib/api-base";`，:17 同样替换为 `const apiBaseUrl = resolveApiBaseUrl();`。

- [ ] **Step 6: 更新 .env.example**

在 `.env.example` 末尾追加：

```bash
# 拆书 / 生成 LLM（留空则走确定性 fallback，不报错；填 DeepSeek key 后走真实 LLM）
NOVELIST_LLM_BASE_URL=
NOVELIST_LLM_API_KEY=
NOVEL_FACTORY_EXTRACTION_PROVIDER=deepseek
# 前端调用的网关地址（dev 默认 http://localhost:8080）
VITE_NOVEL_FACTORY_API_BASE_URL=
```

- [ ] **Step 7: 更新 README 运行说明**

在 `README.md` 适当位置（本地运行段）追加一段：

```markdown
### LLM 拆书模式

- 配置 `NOVELIST_LLM_BASE_URL` + `NOVELIST_LLM_API_KEY`（DeepSeek 兼容）后，上传书走真实 LLM 实体/场景抽取。
- 不配置则走确定性 fallback：仍按上传书正文派生实体与图谱，不会返回内置 demo 数据。
- 前端 dev 默认连 `http://localhost:8080` 网关；用 `VITE_NOVEL_FACTORY_API_BASE_URL` 覆盖。
```

- [ ] **Step 8: 运行 web 全量**

Run: `rtk pnpm --filter @novel-factory/web test --run`
Expected: PASS（现有测试用 `vi.stubEnv` 显式设 base，不受 dev fallback 影响）

- [ ] **Step 9: 提交**

```bash
git add .env.example apps/web/src/lib/api-base.ts apps/web/src/pages.tsx apps/web/src/features/projects/story-bible-wizard-page.tsx apps/web/src/test/api-base.test.ts README.md
git commit -m "feat: default web to gateway and document LLM extraction env"
```

---

## Verification（整批完成后）

```bash
rtk python3 -m pytest apps/ai-worker/tests -q
rtk python3 -m pytest apps/core-service/tests/test_persistence.py apps/core-service/tests/test_phase_two_api.py apps/core-service/tests/test_phase_three_api.py -q
rtk pnpm --filter @novel-factory/web test --run
rtk pnpm --filter @novel-factory/contracts test
```

浏览器手验：上传自定义两章 txt（含「第一章 / 第二章」标题、自造人名地名）→ 拆书 → analysis 中心显示该书实体（非斗破苍穹）、图谱可点开节点与邻居、commit 出真实 package。

## Done bar
- 上传任意 txt：实体/图谱/包反映该书内容，无写死斗破苍穹。
- 无 LLM key 走确定性 fallback 不崩、不回退 demo 数据。
- 配 key 走真 LLM。
- `graph_node_details`/`graph_neighbors_by_node` 真实落表，新书节点可浏览。
- BookKnowledgePackage 真实组装含 objects/relationships/scenes。
- 前端开箱连网关。
- 全量测试绿；现有 demo book 测试仍绿。
