# P0 打通线1真实拆书 Design

**Goal:** 让用户上传任意 txt 书后，拆书链路产出属于那本书的真实人物/势力实体、知识图谱节点与边、以及可导出的 BookKnowledgePackage —— 而非恒返回写死的斗破苍穹 Xiao Yan/Yao Lao/Xiao Clan。

**背景（当前真实状态）**
- 上传→切章→按章 LLM 深拆（scene/event/conflict/hook/reward/climax/**relationship**，含 participants 人名）已经是真的，落 deep_analysis。
- 缺口：`knowledge_objects` 与 `graph_summary` 恒来自 `build_extraction_fixture` 写死三对象；`apply_task_execution_result` 只写 `graph_summaries`，不写 `graph_node_details`/`graph_neighbors_by_node`；`commit_knowledge_package` 只翻状态不组装包；默认配置（provider=anthropic、无 .env、前端未设 API base）开箱不真跑。

**决策（已确认）**
1. 实体：复用现有 per-chapter LLM 调用，在同一次调用里加抽 `entities`（人物/势力/地点 + 别名 + 类型 + confidence），跨章聚合去重成 knowledge_objects；不新增 LLM 轮次。
2. 无 LLM key / provider 不支持时：确定性从章节标题+高频专名派生实体与单/少节点图谱，反映上传书，绝不回退斗破苍穹。
3. 默认可跑：补 `.env.example`（DeepSeek 占位+开关说明）、前端 API base 本地默认、文档；不改 docker-compose 默认 provider，不硬编码密钥。

---

## Task 1: extraction — LLM/确定性实体抽取 + 图谱构建

**Files**
- Modify `apps/ai-worker/worker/extraction.py`
- Test `apps/ai-worker/tests/test_bootstrap.py`(或 test_extraction 新增)

**做法**
- `_build_chapter_prompt`（:417）扩展：要求 JSON 额外含 `entities: [{name, type(character|clan|mentor|location|faction), aliases[], confidence, summary}]`。
- 新增 `_aggregate_entities(chapter_analyses) -> list[knowledge_object]`：跨章按归一名（小写去空格）合并别名、取最高 confidence、生成稳定 `object_id`（`{run_id}OBJ{n:03d}`）、lifecycle=candidate（confidence<0.8）/approved(≥0.95)。
- 新增 `_build_graph_from_analysis(knowledge_objects, relationships, evidences) -> {summary, node_details, neighbors}`：
  - node = 每个 knowledge_object，`node_id={run_id}NODE{n}`，`canonical_object_id` 指回对象，evidence_refs 取该对象证据。
  - edge = 从深拆 `relationship_edges` 映射，subject/object 匹配到 node_id；双向写 neighbors（outgoing+incoming）。
- 确定性 fallback：无 LLM 时 `_build_fallback_entities(chapters)` 用切章标题 + 章节文本高频 2-4 字专名候选（正则+频次阈值）产出 ≥1 实体，绝不含硬编码斗破苍穹名。
- `build_extraction_fixture` 降级为「无章节时的空壳」：run/task/events 元数据保留，但 `knowledge_objects=[]`、`graph_summary.nodes=[]`；真实数据一律由上面函数在 `run_extract_knowledge` 内填充。
- `run_extract_knowledge`（:790）改为：聚合 entities→objects；evidences 绑到真实 object；`_build_graph_from_analysis` 产 graph；metrics 增加 `graph_node_details`、`graph_neighbors_by_node`。

**验收**
- 上传含「第一章…第二章…」自定义文本 + 配 mock LLM 返回自定义 entities → knowledge_objects/graph 反映该文本，无 Xiao Yan。
- 无 LLM key → fallback 实体来自章节标题，非斗破苍穹。

## Task 2: store — 落 graph_node_details / neighbors

**Files**
- Modify `apps/core-service/app/core/phase_two_store.py`(`apply_task_execution_result` :5111-5118)
- Test `apps/core-service/tests/test_persistence.py`

**做法**
- 在 extraction_run 分支，读 `metrics.get("graph_node_details")`/`graph_neighbors_by_node`；非空则 `STORE.graph_node_details`/`graph_neighbors_by_node` 按 book 覆盖（先清该 book 旧节点再写）。
- 保持 `graph_summaries[book_id]` 写入不变。

**验收**
- worker 结果注入后 reload，`get_graph_node(new_node_id)` 非 None，`list_graph_neighbors` 返回真实边。

## Task 3: commit_knowledge_package — 真实组装 BookKnowledgePackage

**Files**
- Modify `apps/core-service/app/core/phase_two_store.py`(`commit_knowledge_package` :3539)
- Test `apps/core-service/tests/test_phase_two_api.py`

**做法**
- commit 时组装 package dict 存入 `STORE.knowledge_packages[run_id]`：`metadata`(run/book/counts)、`source_book`、`chapters`、`scenes`(from source_scenes_by_chapter)、`objects`(approved+merged knowledge_objects)、`relationships`(from graph neighbors/edges)。
- 保留状态翻转；返回增加 `package_ref` + `object_count`。
- object storage projection（若已有 register 机制）注册该 package artifact ref。

**验收**
- commit 后 `STORE.knowledge_packages[run_id]` 含 objects/relationships/scenes 且来自真实抽取，非空。

## Task 4: 默认可跑 — .env.example + 前端默认 + 文档

**Files**
- Modify `.env.example`
- Modify `apps/web`（API base 默认解析处，`import.meta.env.VITE_NOVEL_FACTORY_API_BASE_URL` 消费点集中到一个 helper 或给本地默认）
- Modify `README.md` 或 `docs` 运行说明

**做法**
- `.env.example` 增 `NOVELIST_LLM_BASE_URL=`、`NOVELIST_LLM_API_KEY=`、`NOVEL_FACTORY_EXTRACTION_PROVIDER=deepseek`（占位+注释：留空则走确定性 fallback，不报错）。
- 前端：新增 `resolveApiBaseUrl()`，dev 下默认 `http://localhost:8080`（gateway），env 覆盖；确保开箱连后端而非 demo state。
- 文档：一段「配 DeepSeek key 后真 LLM 拆书；不配走确定性 fallback」运行指引。

**验收**
- 空 env 启动不崩、拆书走 fallback 出真实（非斗破苍穹）实体。
- 配 key 后走真 LLM。
- 前端开箱指向 gateway。

---

## Global Constraints
- 不硬编码任何真实 API 密钥。
- 生产路径写失败必须失败，不静默 file fallback。
- 保持 HTTP API shape 不变；现有 demo book（GRAPH_BOOK_ID seed）测试仍需绿。
- 每任务 ≤2 迭代 / ~15 分钟。

## Verification
```
rtk python3 -m pytest apps/ai-worker/tests -q
rtk python3 -m pytest apps/core-service/tests/test_persistence.py apps/core-service/tests/test_phase_two_api.py -q
rtk pnpm --filter @novel-factory/web test --run
rtk pnpm --filter @novel-factory/contracts test
```
浏览器：上传自定义两章 txt → analysis 中心显示该书实体 + 图谱可点开节点/邻居 + commit 出包。
