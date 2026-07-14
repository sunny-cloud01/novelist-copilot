import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { resolveApiBaseUrl } from "@/lib/api-base";
import { createNovelFactoryApiClient } from "@/lib/api-client";
import {
  DEFAULT_MODEL_PROFILE_ID,
  STRUCTURED_FALLBACK_MODEL_PROFILE_ID,
} from "@/components/phase-two-state";

export { PhaseTwoProvider, usePhaseTwo } from "@/state/phase-two-provider";
import { usePhaseTwo } from "@/state/phase-two-provider";

const statusLabels: Record<string, string> = {
  active: "进行中",
  approved: "已通过",
  pending: "待处理",
  pending_review: "待审核",
  draft: "草稿",
  planning: "规划中",
  ready: "已就绪",
  requires_review: "待复核",
  rewrite_required: "待重写",
  succeeded: "已完成",
  uploaded: "已上传",
  queued: "排队中",
  blocked: "已拦截",
  accepted: "已接受",
  revised: "已修订",
  rejected: "已驳回",
  requested: "已请求",
  open: "未解决",
  resolved: "已解决",
  candidate: "候选",
  merged: "已合并",
  reextract_requested: "已请求重抽",
  in_progress: "处理中",
};

const stageLabels: Record<string, string> = {
  knowledge_base_commit: "知识库提交",
  knowledge_package_export: "知识包导出",
  quality_review: "质量复核",
  source_submission: "来源提交",
};

const objectTypeLabels: Record<string, string> = {
  character: "角色",
  clan: "家族",
  mentor: "导师",
};

const segmentationStatusLabels: Record<string, string> = {
  segmented: "已切章",
};

const planningRoleLabels: Record<string, string> = {
  conflict: "冲突",
  payoff: "回收",
  setup: "铺垫",
  turn: "转折",
};

const beatStatusLabels: Record<string, string> = {
  planned: "待生成",
  writing: "写作中",
  critic_review: "批评复核",
  rewrite_required: "待重写",
  humanizer_pass: "润色通过",
  beat_approved: "本拍通过",
  blocked: "已阻断",
};

const qualityStatusLabels: Record<string, string> = {
  queued: "待质检",
  passed: "已通过",
  blocked: "已拦截",
  requires_review: "待复核",
};

const writingStageLabels: Record<string, string> = {
  queued: "排队中",
  memory_package: "记忆包整理",
  prompt_package: "提示包整理",
  writer_draft: "写手起草",
  critic_review: "批评复核",
  humanizer_pass: "润色通过",
  consistency_review: "一致性复核",
  revision_loop: "修订回合",
  human_review: "人工复核",
  quality_gate: "质量门禁",
};

const criticSeverityLabels: Record<string, string> = {
  blocking: "阻断",
  warning: "警告",
  high: "高",
  critical: "致命",
};

function labelOf(labels: Record<string, string>, value: string) {
  return labels[value] ?? value;
}

function Page({ title, body }: { title: string; body: string }) {
  return (
    <section>
      <h2>{title}</h2>
      <p>{body}</p>
    </section>
  );
}

export function WorkspaceHomePage() {
  const { workspaceId } = useParams();
  const apiBaseUrl = resolveApiBaseUrl();

  if (!apiBaseUrl) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>工作台首页</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>工作台首页</h2>
        <p>查看工作区入口、最近任务、待审核项与主流程快捷入口。</p>
        {workspaceId ? <p>当前工作区：{workspaceId}</p> : null}
      </div>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>工作区信息</h3>
        <p>暂无数据。</p>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>最近任务</h3>
        <p>暂无数据。</p>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>待审核项</h3>
        <p>暂无数据。</p>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>快捷入口</h3>
        <ul>
          <li>
            <Link to="/projects">项目列表</Link>
          </li>
          <li>
            <Link to="/configuration">进入配置中心</Link>
          </li>
          <li>
            <Link to="/sources">上传来源</Link>
          </li>
        </ul>
      </section>
    </section>
  );
}

export function ExtractionRunPage() {
  const { runId } = useParams();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );
  const activeRunId = runId ?? "";

  const [apiRun, setApiRun] = useState<Record<string, any> | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));

  useEffect(() => {
    if (!apiClient || !activeRunId) return;
    let cancelled = false;
    setLoading(true);
    void (
      apiClient.getExtractionRun(activeRunId) as Promise<Record<string, any>>
    )
      .then((run) => {
        if (!cancelled) setApiRun(run);
      })
      .catch((err) => {
        if (!cancelled)
          setError(err instanceof Error ? err.message : "加载失败");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [activeRunId, apiClient]);

  const [error, setError] = useState<string | null>(null);

  const run = apiRun;
  const lowConfidenceItems: any[] = [];

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>抽取任务详情</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>正在加载抽取任务...</h2>
      </section>
    );
  }

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>抽取任务详情</h2>
        <p>跟踪抽取状态、异常和任务报告。</p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
      </div>
      <dl>
        <dt>任务 ID</dt>
        <dd>{activeRunId}</dd>
        <dt>状态</dt>
        <dd>{labelOf(statusLabels, run?.status)}</dd>
        <dt>当前阶段</dt>
        <dd>{labelOf(stageLabels, run?.current_stage)}</dd>
        <dt>章节数</dt>
        <dd>{run?.chapter_count ?? "-"}</dd>
        <dt>场景数</dt>
        <dd>{run?.scene_count ?? "-"}</dd>
        <dt>对象数</dt>
        <dd>{run?.object_count ?? "-"}</dd>
        <dt>证据数</dt>
        <dd>{run?.evidence_count ?? "-"}</dd>
        <dt>低置信对象数</dt>
        <dd>{run?.low_confidence_count ?? "-"}</dd>
      </dl>
      <section>
        <h3>低置信对象队列</h3>
        {lowConfidenceItems.length === 0 ? <p>低置信对象已全部处理。</p> : null}
        <ul>
          {lowConfidenceItems.map((item: any) => (
            <li key={item.objectId}>
              {item.canonicalName}（置信度 {item.confidence}）
            </li>
          ))}
        </ul>
      </section>
      <div style={{ display: "flex", gap: 12 }}>
        {run?.status === "succeeded" ? (
          <Link
            to={`/knowledge-packages/${activeRunId}`}
            style={{
              padding: "8px 16px",
              backgroundColor: "#10b981",
              color: "white",
              borderRadius: 4,
              textDecoration: "none",
            }}
          >
            查看知识包详情
          </Link>
        ) : null}
        <Link to="/knowledge/review">进入知识审核</Link>
        <Link to={`/graph`}>查看故事图谱</Link>
      </div>
    </section>
  );
}

export function KnowledgeReviewPage() {
  const { runId } = useParams();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );
  const activeRunId = runId ?? "";

  const [apiRun, setApiRun] = useState<Record<string, any> | null>(null);
  const [apiObjects, setApiObjects] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!apiClient || !activeRunId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    void Promise.all([
      apiClient.getExtractionRun(activeRunId) as Promise<Record<string, any>>,
      apiClient.listKnowledgeObjects(activeRunId) as Promise<{ items: any[] }>,
    ])
      .then(([run, objectsPayload]) => {
        if (cancelled) return;
        setApiRun(run);
        setApiObjects(objectsPayload.items ?? []);
      })
      .catch((caught) => {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "审核数据加载失败");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [activeRunId, apiClient]);

  const run = apiRun;
  const knowledgeObjects = apiObjects ?? [];
  const lowConfidenceItems = (apiObjects ?? []).filter((o: any) => {
    const confidence = o.confidence ?? 1;
    return confidence < 0.7 || o.lifecycle_status === "pending_review";
  });

  const [reviewingObjects, setReviewingObjects] = useState<Set<string>>(
    new Set()
  );

  async function handleReviewAction(
    objectId: string,
    action: string,
    targetObjectId?: string
  ) {
    if (!apiClient) return;
    setReviewingObjects((prev) => new Set(prev).add(objectId));
    try {
      await apiClient.reviewKnowledgeObject(objectId, {
        action,
        target_object_id: targetObjectId,
      });
      setApiObjects((prev) =>
        (prev ?? []).map((o: any) =>
          (o.object_id ?? o.objectId) === objectId
            ? {
                ...o,
                lifecycle_status:
                  action === "approve"
                    ? "approved"
                    : action === "reject"
                      ? "rejected"
                      : "merged",
              }
            : o
        )
      );
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "审核操作失败");
    } finally {
      setReviewingObjects((prev) => {
        const next = new Set(prev);
        next.delete(objectId);
        return next;
      });
    }
  }

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>知识审核</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>正在加载审核数据...</h2>
      </section>
    );
  }

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>知识审核</h2>
        <p>对候选对象执行通过、驳回、合并别名或请求重抽。</p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
      </div>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>抽取运行状态</h3>
        <dl>
          <dt>状态</dt>
          <dd>
            {labelOf(statusLabels, run?.status ?? (apiRun as any)?.status)}
          </dd>
          <dt>当前阶段</dt>
          <dd>
            {labelOf(
              stageLabels,
              run?.current_stage ?? (apiRun as any)?.current_stage
            )}
          </dd>
          <dt>低置信对象数</dt>
          <dd>{lowConfidenceItems.length}</dd>
        </dl>
      </section>
      <ul style={{ display: "grid", gap: 16, padding: 0, listStyle: "none" }}>
        {lowConfidenceItems.map((item: any) => (
          <li
            key={item.objectId ?? item.object_id}
            style={{ border: "1px solid #d4d4d8", padding: 16 }}
          >
            <h3>{item.canonicalName ?? item.canonical_name}</h3>
            <p>
              {labelOf(objectTypeLabels, item.objectType ?? item.object_type)} ·
              置信度 {item.confidence}
            </p>
            <p>别名：{(item.aliases ?? []).join("、") || "无"}</p>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <button
                type="button"
                disabled={reviewingObjects.has(item.objectId ?? item.object_id)}
                onClick={() =>
                  handleReviewAction(item.objectId ?? item.object_id, "approve")
                }
              >
                通过
              </button>
              <button
                type="button"
                disabled={reviewingObjects.has(item.objectId ?? item.object_id)}
                onClick={() =>
                  handleReviewAction(item.objectId ?? item.object_id, "reject")
                }
              >
                驳回
              </button>
              <button
                type="button"
                disabled={reviewingObjects.has(item.objectId ?? item.object_id)}
                onClick={() =>
                  handleReviewAction(
                    item.objectId ?? item.object_id,
                    "merge_alias",
                    "01JZOBJ0000000000000000003"
                  )
                }
              >
                合并别名
              </button>
              <button
                type="button"
                disabled={reviewingObjects.has(item.objectId ?? item.object_id)}
                onClick={() =>
                  handleReviewAction(
                    item.objectId ?? item.object_id,
                    "request_reextract"
                  )
                }
              >
                请求重抽
              </button>
            </div>
          </li>
        ))}
      </ul>
      <section>
        <h3>故事图谱摘要</h3>
        <p>暂无图谱数据。</p>
      </section>
      <section>
        <h3>活动日志</h3>
        <p>暂无活动数据。</p>
      </section>
    </section>
  );
}

export function GraphPage() {
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );
  const [selectedNodeId, setSelectedNodeId] = useState<string>("");
  const [query, setQuery] = useState("");
  const [selectedNodeType, setSelectedNodeType] = useState<string>("");
  const [selectedEvidenceRef, setSelectedEvidenceRef] = useState<string>("");
  const [apiNodes, setApiNodes] = useState<any[] | null>(null);
  const [apiNode, setApiNode] = useState<any | null>(null);
  const [apiNeighbors, setApiNeighbors] = useState<any[] | null>(null);
  const [apiEvidence, setApiEvidence] = useState<any | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);
  const selectedNode = apiNode;
  const neighbors = apiNeighbors ?? [];
  const selectedEvidence = apiEvidence;
  const filteredNodes = apiNodes ?? [];

  useEffect(() => {
    if (!apiClient) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    void apiClient
      .searchGraphNodes({ query, nodeType: selectedNodeType || undefined })
      .then((result: any) => {
        if (cancelled) return;
        setApiNodes(result.items ?? []);
        if (result.items?.[0]?.node_id) {
          setSelectedNodeId((current) => current || result.items[0].node_id);
        }
      })
      .catch((caught) => {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "图谱检索失败");
        setApiNodes([]);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [apiClient, query, selectedNodeType]);

  useEffect(() => {
    if (!apiClient || !selectedNodeId) return;
    let cancelled = false;
    setError(null);
    void Promise.all([
      apiClient.getGraphNode(selectedNodeId),
      apiClient.getGraphNeighbors(selectedNodeId),
    ])
      .then(([node, neighborResult]: any[]) => {
        if (cancelled) return;
        setApiNode(node);
        setApiNeighbors(neighborResult.items ?? []);
        const nextEvidenceRef = node?.evidence_refs?.[0] ?? "";
        setSelectedEvidenceRef(nextEvidenceRef);
      })
      .catch((caught) => {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "图谱详情加载失败");
        setApiNode(null);
        setApiNeighbors([]);
      });
    return () => {
      cancelled = true;
    };
  }, [apiClient, selectedNodeId]);

  useEffect(() => {
    if (!apiClient || !selectedEvidenceRef) return;
    let cancelled = false;
    void apiClient
      .getEvidence(selectedEvidenceRef)
      .then((evidence: any) => {
        if (cancelled) return;
        setApiEvidence({
          evidenceId: evidence.evidence_id ?? selectedEvidenceRef,
          bookId: evidence.book_id,
          chapterId: evidence.chapter_id,
          chapterIndex: evidence.chapter_index,
          textRange: evidence.text_range,
          excerpt: evidence.excerpt,
          sourceObjectRefs: evidence.source_object_refs ?? [],
          confidence: evidence.confidence,
          traceId: evidence.trace_id,
        });
      })
      .catch(() => {
        if (cancelled) return;
        setApiEvidence(null);
      });
    return () => {
      cancelled = true;
    };
  }, [apiClient, selectedEvidenceRef]);

  if (!apiClient) {
    return (
      <section className="nf-analysis-page">
        <h2>故事图谱查看器</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  return (
    <section className="nf-analysis-page">
      <div>
        <h2>故事图谱查看器</h2>
        <p>
          搜索节点、查看关系来源，并跳转原文证据；图谱只做辅助查看，不做重编辑画布。
        </p>
      </div>
      <div className="nf-graph-grid">
        <section className="nf-card">
          <div className="nf-card-header">
            <h3 className="nf-card-title">图谱节点</h3>
            <p className="nf-card-description">
              按角色、势力、地点或事件搜索。
            </p>
          </div>
          <input
            aria-label="搜索图谱节点"
            className="nf-search-input"
            onChange={(event) => setQuery(event.target.value)}
            placeholder="搜索 Xiao Yan / mentor / clan"
            value={query}
          />
          <label className="nf-field" style={{ marginTop: 12 }}>
            节点类型
            <select
              aria-label="筛选节点类型"
              value={selectedNodeType}
              onChange={(event) => setSelectedNodeType(event.target.value)}
            >
              <option value="">全部</option>
              <option value="character">角色</option>
              <option value="mentor">导师</option>
              <option value="clan">家族</option>
            </select>
          </label>
          {loading ? <p>图谱检索中…</p> : null}
          {error ? <p role="alert">{error}</p> : null}
          <ul className="nf-source-list" style={{ marginTop: 12 }}>
            {filteredNodes.map((node: any) => {
              const nodeId = node.nodeId ?? node.node_id;
              const nodeType = node.nodeType ?? node.node_type;
              const evidenceRefs =
                node.evidenceRefs ?? node.evidence_refs ?? [];
              return (
                <li className="nf-source-item" key={nodeId}>
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedNodeId(nodeId);
                      setSelectedEvidenceRef(evidenceRefs[0] ?? "");
                    }}
                  >
                    {node.label}（{labelOf(objectTypeLabels, nodeType)}）
                  </button>
                  <p>证据 {evidenceRefs.length} 条</p>
                </li>
              );
            })}
          </ul>
        </section>
        {selectedNode ? (
          <div className="nf-analysis-stack">
            <section className="nf-card">
              <div className="nf-card-header">
                <h3 className="nf-card-title">节点详情</h3>
                <p className="nf-card-description">{selectedNode.summary}</p>
              </div>
              <dl>
                <dt>名称</dt>
                <dd>{selectedNode.label}</dd>
                <dt>类型</dt>
                <dd>
                  {labelOf(
                    objectTypeLabels,
                    selectedNode.nodeType ?? selectedNode.node_type
                  )}
                </dd>
                <dt>审核状态</dt>
                <dd>
                  {labelOf(
                    statusLabels,
                    selectedNode.reviewStatus ?? selectedNode.review_status
                  )}
                </dd>
                <dt>生命周期</dt>
                <dd>
                  {labelOf(
                    statusLabels,
                    selectedNode.lifecycleStatus ??
                      selectedNode.lifecycle_status
                  )}
                </dd>
                <dt>置信度</dt>
                <dd>{selectedNode.confidence}</dd>
                <dt>别名</dt>
                <dd>{(selectedNode.aliases ?? []).join("、") || "无"}</dd>
                <dt>对象引用</dt>
                <dd>
                  {selectedNode.canonicalObjectId ??
                    selectedNode.canonical_object_id}
                </dd>
              </dl>
            </section>
            <section className="nf-card">
              <div className="nf-card-header">
                <h3 className="nf-card-title">关系查看</h3>
                <p className="nf-card-description">关系必须来自已绑定证据。</p>
              </div>
              {neighbors.length === 0 ? <p>当前节点暂无关系。</p> : null}
              <ul>
                {neighbors.map((neighbor: any) => (
                  <li key={neighbor.edgeId ?? neighbor.edge_id}>
                    {neighbor.direction === "outgoing" ? "指向" : "来自"}
                    {neighbor.neighborLabel ?? neighbor.neighbor_label} ·{" "}
                    {neighbor.relationType ?? neighbor.relation_type} · 置信度{" "}
                    {neighbor.confidence}
                  </li>
                ))}
              </ul>
            </section>
            <section className="nf-card">
              <div className="nf-card-header">
                <h3 className="nf-card-title">Source evidence</h3>
                <p className="nf-card-description">
                  点击 evidence ref 查看原文片段。
                </p>
              </div>
              <ul>
                {(
                  selectedNode.evidenceRefs ??
                  selectedNode.evidence_refs ??
                  []
                ).map((ref: string) => (
                  <li key={ref}>
                    <button
                      className="nf-evidence-button"
                      type="button"
                      onClick={() => setSelectedEvidenceRef(ref)}
                    >
                      {ref}
                    </button>
                  </li>
                ))}
              </ul>
              {selectedEvidence ? (
                <article className="nf-evidence-item">
                  <strong>
                    第 {selectedEvidence.chapterIndex} 章 ·{" "}
                    {selectedEvidence.textRange}
                  </strong>
                  <p className="nf-evidence-excerpt">
                    “{selectedEvidence.excerpt}”
                  </p>
                  <small>trace {selectedEvidence.traceId}</small>
                </article>
              ) : null}
            </section>
          </div>
        ) : null}
      </div>
    </section>
  );
}

export function ProjectListPage() {
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );

  const [apiProjects, setApiProjects] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!apiClient) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    void (apiClient.listNovelProjects() as Promise<{ items: any[] }>)
      .then((payload) => {
        if (!cancelled) setApiProjects(payload.items ?? []);
      })
      .catch((caught) => {
        if (!cancelled)
          setError(
            caught instanceof Error ? caught.message : "项目列表加载失败"
          );
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [apiClient]);

  const projects = (apiProjects ?? []).map((p: any) => ({
    projectId: p.project_id ?? p.projectId ?? "",
    title: p.title ?? "",
    genreScope: p.genre_scope ?? p.genreScope ?? "",
    status: p.status ?? "",
    storyBibleStatus: p.story_bible_status ?? p.storyBibleStatus ?? null,
    allowedKnowledgeSourceRefs:
      p.allowed_knowledge_source_refs ?? p.allowedKnowledgeSourceRefs ?? [],
  }));

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>小说项目</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>正在加载项目列表...</h2>
      </section>
    );
  }

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>小说项目</h2>
        <p>查看项目、故事圣经与章节规划进度。</p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
      </div>
      <ul style={{ display: "grid", gap: 16, padding: 0, listStyle: "none" }}>
        {projects.map((project) => (
          <li
            key={project.projectId}
            style={{ border: "1px solid #d4d4d8", padding: 16 }}
          >
            <h3>{project.title}</h3>
            <p>
              {project.genreScope} · {labelOf(statusLabels, project.status)}
            </p>
            {project.storyBibleStatus ? (
              <p>
                Story Bible: {labelOf(statusLabels, project.storyBibleStatus)}
              </p>
            ) : null}
            <p>可用知识来源 {project.allowedKnowledgeSourceRefs.length} 项</p>
            <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
              <Link to={`/projects/${project.projectId}`}>查看项目详情</Link>
              <Link to={`/projects/${project.projectId}/planner`}>
                进入章节规划
              </Link>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}

function normalizeProjectView(project: any) {
  if (!project) return null;
  return {
    projectId: project.project_id ?? project.projectId ?? "",
    title: project.title ?? "",
    genreScope: project.genre_scope ?? project.genreScope ?? "",
    status: project.status ?? "",
    qualityGateProfileId:
      project.quality_gate_profile_id ?? project.qualityGateProfileId ?? "",
    storyBibleId: project.story_bible_id ?? project.storyBibleId ?? "",
  };
}

function normalizeStoryBibleView(storyBible: any) {
  if (!storyBible) return null;
  const payload = storyBible.payload ?? {
    premise: storyBible.premise,
    protagonist: storyBible.protagonist,
    core_conflict: storyBible.coreConflict,
    style_target: storyBible.styleTarget,
    forbidden_similarities: storyBible.forbiddenSimilarities,
    world_rules: storyBible.worldRules,
    narrative_promises: storyBible.narrativePromises,
  };
  const diffSource = storyBible.diff ?? null;
  const historySource = Array.isArray(storyBible.history)
    ? storyBible.history
    : [];
  return {
    storyBibleId: storyBible.story_bible_id ?? storyBible.storyBibleId ?? "",
    projectId: storyBible.project_id ?? storyBible.projectId ?? "",
    version: storyBible.version ?? 0,
    status: storyBible.status ?? "",
    premise: payload.premise ?? "",
    protagonist: payload.protagonist ?? "",
    coreConflict: payload.core_conflict ?? payload.coreConflict ?? "",
    styleTarget: payload.style_target ?? payload.styleTarget ?? "",
    forbiddenSimilarities:
      payload.forbidden_similarities ?? payload.forbiddenSimilarities ?? "",
    worldRules: Array.isArray(payload.world_rules ?? payload.worldRules)
      ? (payload.world_rules ?? payload.worldRules)
      : [],
    narrativePromises: Array.isArray(
      payload.narrative_promises ?? payload.narrativePromises
    )
      ? (payload.narrative_promises ?? payload.narrativePromises)
      : [],
    confirmedPayload:
      storyBible.confirmed_payload ?? storyBible.confirmedPayload ?? null,
    diff: diffSource
      ? {
          fromVersion:
            diffSource.from_version ?? diffSource.fromVersion ?? null,
          toVersion:
            diffSource.to_version ??
            diffSource.toVersion ??
            storyBible.version ??
            0,
          summary: diffSource.summary ?? "",
          changedFields:
            diffSource.changed_fields ?? diffSource.changedFields ?? [],
        }
      : null,
    history: historySource.map((item: any) => ({
      version: item.version ?? 0,
      status: item.status ?? "",
      changeType: item.change_type ?? item.changeType ?? "",
      summary: item.summary ?? "",
      note: item.note ?? null,
      createdAt: item.created_at ?? item.createdAt ?? "",
    })),
    approvedAt: storyBible.approved_at ?? storyBible.approvedAt ?? null,
    approvedBy: storyBible.approved_by ?? storyBible.approvedBy ?? null,
    traceId: storyBible.trace_id ?? storyBible.traceId ?? "",
  };
}

function parseMultilineList(value: string) {
  return value
    .split(/\n+/)
    .map((item: any) => item.trim())
    .filter(Boolean);
}

export function ProjectHomePage() {
  const { projectId } = useParams();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );
  const [apiProjectDetail, setApiProjectDetail] = useState<any | null>(null);
  const [apiStoryBible, setApiStoryBible] = useState<any | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const [submittingAction, setSubmittingAction] = useState<string | null>(null);
  const [draft, setDraft] = useState({
    premise: "",
    protagonist: "",
    coreConflict: "",
    styleTarget: "",
    forbiddenSimilarities: "",
    worldRules: "",
    narrativePromises: "",
    summary: "补强故事圣经候选版本。",
    note: "",
  });

  useEffect(() => {
    if (!apiClient || !projectId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    void (async () => {
      try {
        const detail: any = await apiClient.getNovelProject(projectId);
        if (cancelled) return;
        setApiProjectDetail(detail);
        const storyBibleId =
          detail?.story_bible?.story_bible_id ??
          detail?.project?.story_bible_id ??
          "";
        if (!storyBibleId) {
          setApiStoryBible(null);
          return;
        }
        const storyBible = await apiClient.getStoryBible(storyBibleId);
        if (cancelled) return;
        setApiStoryBible(storyBible);
      } catch (caught) {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "项目详情加载失败");
        setApiProjectDetail(null);
        setApiStoryBible(null);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [apiClient, projectId]);

  const project = normalizeProjectView(apiProjectDetail?.project) ?? null;
  const storyBible = normalizeStoryBibleView(
    apiStoryBible ?? apiProjectDetail?.story_bible ?? null
  );
  const chapterPlans = (apiProjectDetail?.chapter_plans ?? []).map(
    (plan: any) => ({
      chapterPlanId: plan.chapter_plan_id ?? plan.chapterPlanId,
      chapterIndex: plan.chapter_index ?? plan.chapterIndex,
      title: plan.title,
      status: plan.status,
      targetWordCount: plan.target_word_count ?? plan.targetWordCount,
    })
  );

  useEffect(() => {
    if (!storyBible) return;
    setDraft({
      premise: storyBible.premise,
      protagonist: storyBible.protagonist,
      coreConflict: storyBible.coreConflict,
      styleTarget: storyBible.styleTarget ?? "",
      forbiddenSimilarities: storyBible.forbiddenSimilarities ?? "",
      worldRules: (storyBible.worldRules ?? []).join("\n"),
      narrativePromises: (storyBible.narrativePromises ?? []).join("\n"),
      summary: storyBible.diff?.summary ?? "补强故事圣经候选版本。",
      note: "",
    });
  }, [storyBible?.storyBibleId, storyBible?.version, storyBible?.status]);

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>项目主页</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading && !project) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>项目主页</h2>
        <p>正在加载...</p>
      </section>
    );
  }

  if (!project) {
    return <Page title="项目不存在" body="未找到对应项目。" />;
  }

  async function handleStoryBibleAction(
    action: "regenerate" | "confirm" | "reject"
  ) {
    if (!apiClient || !storyBible?.storyBibleId) return;
    setSubmittingAction(action);
    setActionError(null);
    setActionMessage(null);
    try {
      const payload =
        action === "regenerate"
          ? {
              action,
              summary: draft.summary,
              note: draft.note,
              story_bible_payload: {
                premise: draft.premise,
                protagonist: draft.protagonist,
                core_conflict: draft.coreConflict,
                style_target: draft.styleTarget,
                forbidden_similarities: draft.forbiddenSimilarities,
                world_rules: parseMultilineList(draft.worldRules),
                narrative_promises: parseMultilineList(draft.narrativePromises),
              },
            }
          : {
              action,
              summary: draft.summary,
              note: draft.note,
            };
      const nextStoryBible = await apiClient.reviewStoryBible(
        storyBible.storyBibleId,
        payload
      );
      setApiStoryBible(nextStoryBible);
      setActionMessage(
        action === "confirm"
          ? "候选版本已确认。"
          : action === "reject"
            ? "候选版本已驳回。"
            : "已生成候选版本。"
      );
    } catch (caught) {
      setActionError(
        caught instanceof Error ? caught.message : "Story Bible 审核动作失败"
      );
    } finally {
      setSubmittingAction(null);
    }
  }

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>项目主页</h2>
        <p>查看项目状态、故事圣经摘要与章节入口。</p>
      </div>
      {loading ? <p>正在加载项目详情...</p> : null}
      {error ? <p role="alert">{error}</p> : null}
      <dl>
        <dt>项目名称</dt>
        <dd>{project.title}</dd>
        <dt>题材范围</dt>
        <dd>{project.genreScope}</dd>
        <dt>项目状态</dt>
        <dd>{labelOf(statusLabels, project.status)}</dd>
        <dt>质量门配置</dt>
        <dd>{project.qualityGateProfileId}</dd>
      </dl>
      {storyBible ? (
        <section style={{ display: "grid", gap: 16 }}>
          <div>
            <h3>故事圣经摘要</h3>
            <dl>
              <dt>版本</dt>
              <dd>{storyBible.version}</dd>
              <dt>状态</dt>
              <dd>{labelOf(statusLabels, storyBible.status)}</dd>
              <dt>故事前提</dt>
              <dd>{storyBible.premise}</dd>
              <dt>主角</dt>
              <dd>{storyBible.protagonist}</dd>
              <dt>核心冲突</dt>
              <dd>{storyBible.coreConflict}</dd>
              <dt>风格目标</dt>
              <dd>{storyBible.styleTarget || "未填写"}</dd>
              <dt>禁用相似点</dt>
              <dd>{storyBible.forbiddenSimilarities || "未填写"}</dd>
              <dt>批准时间</dt>
              <dd>{storyBible.approvedAt ?? "未确认"}</dd>
            </dl>
            {storyBible.worldRules.length ? (
              <div>
                <h4>世界规则</h4>
                <ul>
                  {storyBible.worldRules.map((item: string) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ) : null}
            {storyBible.narrativePromises.length ? (
              <div>
                <h4>叙事承诺</h4>
                <ul>
                  {storyBible.narrativePromises.map((item: string) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>
          {storyBible.diff ? (
            <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
              <h4>候选变更</h4>
              <p>{storyBible.diff.summary || "待补充变更摘要。"}</p>
              <p>
                版本 {storyBible.diff.fromVersion ?? storyBible.version - 1} 到{" "}
                {storyBible.diff.toVersion}
              </p>
              <p>
                变更字段：
                {storyBible.diff.changedFields.length
                  ? storyBible.diff.changedFields.join("、")
                  : "未标注"}
              </p>
            </section>
          ) : null}
          {storyBible.history.length ? (
            <section>
              <h4>审核历史</h4>
              <ul>
                {storyBible.history.map(
                  (item: {
                    changeType: string;
                    version: number;
                    createdAt?: string;
                    status: string;
                    summary?: string;
                  }) => (
                    <li
                      key={`${item.changeType}-${item.version}-${item.createdAt}`}
                    >
                      v{item.version} · {item.changeType} ·{" "}
                      {labelOf(statusLabels, item.status)} ·{" "}
                      {item.summary || "无摘要"}
                    </li>
                  )
                )}
              </ul>
            </section>
          ) : null}
          {apiClient ? (
            <section
              style={{
                border: "1px solid #d4d4d8",
                padding: 16,
                display: "grid",
                gap: 12,
              }}
            >
              <h4>Story Bible 审核</h4>
              <label>
                故事前提
                <textarea
                  value={draft.premise}
                  onChange={(event) =>
                    setDraft((current) => ({
                      ...current,
                      premise: event.target.value,
                    }))
                  }
                />
              </label>
              <label>
                主角
                <input
                  value={draft.protagonist}
                  onChange={(event) =>
                    setDraft((current) => ({
                      ...current,
                      protagonist: event.target.value,
                    }))
                  }
                />
              </label>
              <label>
                核心冲突
                <textarea
                  value={draft.coreConflict}
                  onChange={(event) =>
                    setDraft((current) => ({
                      ...current,
                      coreConflict: event.target.value,
                    }))
                  }
                />
              </label>
              <label>
                风格目标
                <input
                  value={draft.styleTarget}
                  onChange={(event) =>
                    setDraft((current) => ({
                      ...current,
                      styleTarget: event.target.value,
                    }))
                  }
                />
              </label>
              <label>
                禁用相似点
                <textarea
                  value={draft.forbiddenSimilarities}
                  onChange={(event) =>
                    setDraft((current) => ({
                      ...current,
                      forbiddenSimilarities: event.target.value,
                    }))
                  }
                />
              </label>
              <label>
                世界规则
                <textarea
                  value={draft.worldRules}
                  onChange={(event) =>
                    setDraft((current) => ({
                      ...current,
                      worldRules: event.target.value,
                    }))
                  }
                />
              </label>
              <label>
                叙事承诺
                <textarea
                  value={draft.narrativePromises}
                  onChange={(event) =>
                    setDraft((current) => ({
                      ...current,
                      narrativePromises: event.target.value,
                    }))
                  }
                />
              </label>
              <label>
                变更摘要
                <input
                  value={draft.summary}
                  onChange={(event) =>
                    setDraft((current) => ({
                      ...current,
                      summary: event.target.value,
                    }))
                  }
                />
              </label>
              <label>
                备注
                <textarea
                  value={draft.note}
                  onChange={(event) =>
                    setDraft((current) => ({
                      ...current,
                      note: event.target.value,
                    }))
                  }
                />
              </label>
              {actionMessage ? <p>{actionMessage}</p> : null}
              {actionError ? <p role="alert">{actionError}</p> : null}
              <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
                <button
                  type="button"
                  onClick={() => void handleStoryBibleAction("regenerate")}
                  disabled={submittingAction !== null}
                >
                  {submittingAction === "regenerate"
                    ? "生成中..."
                    : "生成候选版本"}
                </button>
                <button
                  type="button"
                  onClick={() => void handleStoryBibleAction("confirm")}
                  disabled={
                    submittingAction !== null ||
                    storyBible.status !== "pending_review"
                  }
                >
                  {submittingAction === "confirm"
                    ? "确认中..."
                    : "确认候选版本"}
                </button>
                <button
                  type="button"
                  onClick={() => void handleStoryBibleAction("reject")}
                  disabled={
                    submittingAction !== null ||
                    storyBible.status !== "pending_review"
                  }
                >
                  {submittingAction === "reject" ? "驳回中..." : "驳回候选版本"}
                </button>
              </div>
            </section>
          ) : (
            <p>
              配置 VITE_NOVEL_FACTORY_API_BASE_URL 后可生成候选、确认或驳回
              Story Bible。
            </p>
          )}
        </section>
      ) : null}
      <section>
        <h3>章节规划入口</h3>
        <ul>
          {chapterPlans.map((plan: any) => (
            <li key={plan.chapterPlanId}>
              第 {plan.chapterIndex} 章《{plan.title}》 ·{" "}
              {labelOf(statusLabels, plan.status)} · 目标 {plan.targetWordCount}{" "}
              字
            </li>
          ))}
        </ul>
      </section>
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        <Link to={`/projects/${project.projectId}/planner`}>
          进入章节规划器
        </Link>
        <Link to={`/projects/${project.projectId}/writing`}>查看写作入口</Link>
      </div>
    </section>
  );
}

export function PlannerPage() {
  const { projectId } = useParams();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );
  const activeProjectId = projectId ?? "";

  const [apiProjectDetail, setApiProjectDetail] = useState<any | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!apiClient || !activeProjectId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    void (apiClient.getNovelProject(activeProjectId) as Promise<any>)
      .then((detail) => {
        if (!cancelled) setApiProjectDetail(detail);
      })
      .catch((caught) => {
        if (!cancelled)
          setError(
            caught instanceof Error ? caught.message : "规划数据加载失败"
          );
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [activeProjectId, apiClient]);

  const project = normalizeProjectView(apiProjectDetail?.project) ?? null;

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>章节规划器</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>正在加载章节规划...</h2>
      </section>
    );
  }

  if (!project) {
    return <Page title="项目不存在" body="未找到对应项目。" />;
  }

  const chapterPlans = (apiProjectDetail?.chapter_plans ?? []).map(
    (plan: any) => ({
      chapterPlanId: plan.chapter_plan_id ?? plan.chapterPlanId ?? "",
      chapterIndex: plan.chapter_index ?? plan.chapterIndex ?? 0,
      title: plan.title ?? "",
      status: plan.status ?? "",
      summary: plan.summary ?? "",
      targetWordCount: plan.target_word_count ?? plan.targetWordCount ?? 0,
      selectedPatternId:
        plan.selected_pattern_id ?? plan.selectedPatternId ?? "",
      selectedRhythmProfileId:
        plan.selected_rhythm_profile_id ?? plan.selectedRhythmProfileId ?? "",
      selectedAssetIds: plan.selected_asset_ids ?? plan.selectedAssetIds ?? [],
      sceneCount: plan.scene_count ?? plan.sceneCount ?? 0,
      order: plan.order ?? 0,
    })
  );
  const patterns = apiProjectDetail?.patterns ?? [];
  const rhythmProfiles = apiProjectDetail?.rhythm_profiles ?? [];
  const assets = apiProjectDetail?.assets ?? [];
  const plannerTasks: any[] = [];
  const plannerAuditEvents: any[] = [];

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>章节规划器</h2>
        <p>查看章节目标、场景拆解、beat 明细、相关任务和审计记录。</p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
      </div>
      {chapterPlans.map((plan: any) => {
        const sections: any[] = [];
        const selectedPattern =
          patterns.find(
            (item: any) => item.patternId === plan.selectedPatternId
          ) ?? null;
        const selectedRhythmProfile =
          rhythmProfiles.find(
            (item: any) => item.rhythmProfileId === plan.selectedRhythmProfileId
          ) ?? null;
        const selectedAssets = assets.filter((item: any) =>
          plan.selectedAssetIds.includes(item.assetId)
        );
        return (
          <article
            key={plan.chapterPlanId}
            style={{
              border: "1px solid #d4d4d8",
              padding: 16,
              display: "grid",
              gap: 12,
            }}
          >
            <div>
              <h3>
                第 {plan.chapterIndex} 章《{plan.title}》
              </h3>
              <p>{plan.summary}</p>
              <p>
                {labelOf(statusLabels, plan.status)} · 目标{" "}
                {plan.targetWordCount} 字
              </p>
            </div>
            <section>
              <h4>已选资源</h4>
              <dl>
                <dt>Pattern</dt>
                <dd>
                  {selectedPattern
                    ? `${selectedPattern.canonicalName} · ${selectedPattern.patternType}`
                    : "未选择"}
                </dd>
                <dt>Rhythm</dt>
                <dd>
                  {selectedRhythmProfile
                    ? `${selectedRhythmProfile.label} · climax ${selectedRhythmProfile.climaxIndex}`
                    : "未选择"}
                </dd>
                <dt>Assets</dt>
                <dd>
                  {selectedAssets.length
                    ? selectedAssets
                        .map((item: any) => item.canonicalName)
                        .join("、")
                    : "未选择"}
                </dd>
              </dl>
              {selectedPattern ? (
                <p>{selectedPattern.expectedReaderEffect}</p>
              ) : null}
              {selectedAssets.length ? (
                <ul>
                  {selectedAssets.map((item: any) => (
                    <li key={item.assetId}>
                      {item.assetType} · {item.contentSummary}
                    </li>
                  ))}
                </ul>
              ) : null}
            </section>
            <section>
              <h4>分节规划</h4>
              <ul style={{ display: "grid", gap: 12 }}>
                {sections.map((section: any) => (
                  <li key={section.sectionPlanId}>
                    <strong>
                      第 {section.sectionIndex} 节 ·{" "}
                      {labelOf(planningRoleLabels, section.planningRole)}
                    </strong>
                    <p>{section.sceneGoal}</p>
                    <ol>
                      {section.beats.map((beat: any) => (
                        <li key={`${section.sectionPlanId}-${beat.index}`}>
                          {beat.summary}
                        </li>
                      ))}
                    </ol>
                  </li>
                ))}
              </ul>
            </section>
            <section>
              <h4>关联任务</h4>
              <ul>
                {plannerTasks.map((task: any) => (
                  <li key={task.taskId}>
                    {task.taskType} · {labelOf(statusLabels, task.status)} ·{" "}
                    {task.summary}
                  </li>
                ))}
              </ul>
            </section>
            <section>
              <h4>任务事件</h4>
              <ul>
                {plannerTasks
                  .flatMap((task) => task.events)
                  .map((event) => (
                    <li key={event.eventId}>
                      {event.eventType} · {labelOf(statusLabels, event.status)}{" "}
                      · {event.summary}
                    </li>
                  ))}
              </ul>
            </section>
            <section>
              <h4>规划审计轨迹</h4>
              <ul>
                {plannerAuditEvents.map((event) => (
                  <li key={event.auditEventId}>
                    {event.action} · {event.summary} · {event.traceId}
                  </li>
                ))}
              </ul>
            </section>
            <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
              <Link
                to={`/projects/${project.projectId}/chapters/${plan.chapterIndex}/setup`}
                style={{
                  padding: "8px 16px",
                  backgroundColor: "#2563eb",
                  color: "white",
                  borderRadius: 4,
                  textDecoration: "none",
                }}
              >
                设置章节参数（一键生成）
              </Link>
              <Link
                to={`/projects/${project.projectId}/writing`}
                style={{
                  padding: "8px 16px",
                  backgroundColor: "#e5e7eb",
                  color: "#1f2937",
                  borderRadius: 4,
                  textDecoration: "none",
                }}
              >
                进入写作工作台
              </Link>
            </div>
          </article>
        );
      })}
    </section>
  );
}

export function WritingStudioPage() {
  const { projectId, writingRunId } = useParams();
  const { applyWritingReviewAction } = usePhaseTwo();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );

  const [apiWritingRun, setApiWritingRun] = useState<Record<
    string,
    unknown
  > | null>(null);
  const [apiProjectDetail, setApiProjectDetail] = useState<Record<
    string,
    unknown
  > | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!apiClient || !writingRunId) return;
    let cancelled = false;
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const [wr, pd] = await Promise.all([
          apiClient!.getWritingRun(writingRunId!),
          projectId ? apiClient!.getNovelProject(projectId) : null,
        ]);
        if (!cancelled) {
          setApiWritingRun((wr as any) ?? null);
          setApiProjectDetail((pd as any) ?? null);
        }
      } catch (e) {
        if (!cancelled)
          setError(e instanceof Error ? e.message : "加载写作任务失败");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [writingRunId, projectId, apiClient]);

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>写作工作台</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading) return <Page title="加载中…" body="正在获取写作任务数据。" />;

  const apiWr = apiWritingRun as Record<string, unknown> | null;
  const apiPd = apiProjectDetail as Record<string, unknown> | null;
  const apiWritingRunData = (apiWr?.writing_run ?? apiWr) as Record<
    string,
    unknown
  > | null;

  const chapterPlans = (apiPd?.chapter_plans ??
    apiPd?.chapterPlans ??
    []) as any[];
  const sectionPlansByChapter: Record<string, any[]> = {};
  const rules: any[] = [];
  const project: any = normalizeProjectView(apiPd?.project) ?? null;

  const writingRun = (apiWritingRunData ?? null) as any;
  const sectionRuns = (apiWr?.section_runs ?? []) as any[];
  const memoryPackage = (apiWr?.memory_package ?? null) as any;
  const promptPackage = (apiWr?.prompt_package ?? null) as any;
  const qualityReport = (apiWr?.quality_report ?? null) as any;
  const consistencyReport = (writingRun?.consistency_report ??
    apiWr?.consistency_report ??
    null) as any;
  const revisionSummary = (writingRun?.revision_summary ??
    apiWr?.revision_summary ??
    null) as any;
  const chapterSnapshot = (writingRun?.chapter_snapshot ??
    apiWr?.chapter_snapshot ??
    null) as any;
  const manuscriptState = (writingRun?.manuscript_state ??
    apiWr?.manuscript_state ??
    null) as any;
  const apiFeedbackRecords = (apiWr?.feedback_records ?? []) as any[];
  const apiPatterns = (apiWr?.pattern_selection ?? []) as any[];
  const apiRhythmProfiles = (apiWr?.rhythm_profile_selection ?? []) as any[];
  const apiAssets = (apiWr?.asset_selection ?? []) as any[];

  const runFeedbackRecords = apiFeedbackRecords;

  if (!project || !writingRun) {
    return <Page title="写作任务不存在" body="未找到对应写作任务。" />;
  }

  const chapterPlan = (chapterPlans as any[]).find(
    (item: any) => item.chapterPlanId === (writingRun as any).chapterPlanId
  );
  const sectionPlans =
    (sectionPlansByChapter as any)[(writingRun as any).chapterPlanId] ?? [];
  const activeRules = (rules as any[]).filter((item: any) =>
    item.scopeRef.includes((project as any).projectId)
  );
  const focusSectionRun = ((sectionRuns as any[]).find(
    (item: any) => item.criticIssues?.length > 0
  ) ?? (sectionRuns as any[])[0]) as any;
  const focusSectionPlan = (sectionPlans as any[]).find(
    (item: any) => item.sectionPlanId === focusSectionRun?.sectionPlanId
  );
  const selectedPattern =
    (apiPatterns as any[]).find(
      (item: any) => item.patternId === (writingRun as any).selectedPatternId
    ) ?? null;
  const selectedRhythmProfile =
    (apiRhythmProfiles as any[]).find(
      (item: any) =>
        item.rhythmProfileId === (writingRun as any).selectedRhythmProfileId
    ) ?? null;
  const selectedAssets = (apiAssets as any[]).filter((item: any) =>
    ((writingRun as any).selectedAssetIds ?? []).includes(item.assetId)
  );
  const canAcceptChapter =
    !!consistencyReport &&
    (consistencyReport as any).blockingIssueCount === 0 &&
    !!qualityReport &&
    ((qualityReport as any).blockingIssues?.length ?? 0) === 0 &&
    (qualityReport as any).status !== "blocked" &&
    !(qualityReport as any).humanReviewRequired &&
    !!revisionSummary &&
    ["accepted", "revised"].includes((revisionSummary as any).status);

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>写作工作台</h2>
        <p>
          按 section / beat 推进写作，查看批评问题、润色结果、证据链与质量反馈。
        </p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
      </div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1.1fr 1.2fr 1fr",
          gap: 16,
          alignItems: "start",
        }}
      >
        <section
          style={{
            border: "1px solid #d4d4d8",
            padding: 16,
            display: "grid",
            gap: 12,
          }}
        >
          <div>
            <h3>左侧：规划与分节</h3>
            <p>{project.title}</p>
            {chapterPlan ? (
              <p>
                第 {chapterPlan.chapterIndex} 章《{chapterPlan.title}》 ·{" "}
                {chapterPlan.summary}
              </p>
            ) : null}
          </div>
          <ul
            style={{ display: "grid", gap: 12, padding: 0, listStyle: "none" }}
          >
            {sectionPlans.map((section: any) => {
              const sectionRun = sectionRuns.find(
                (item: any) => item.sectionPlanId === section.sectionPlanId
              );
              return (
                <li
                  key={section.sectionPlanId}
                  style={{ border: "1px solid #e4e4e7", padding: 12 }}
                >
                  <strong>
                    第 {section.sectionIndex} 节 ·{" "}
                    {labelOf(planningRoleLabels, section.planningRole)}
                  </strong>
                  <p>{section.sceneGoal}</p>
                  <p>
                    {sectionRun
                      ? labelOf(beatStatusLabels, sectionRun.status)
                      : "待生成"}
                  </p>
                  <ol>
                    {section.beats.map((beat: any) => {
                      const beatState = sectionRun?.beatStatus.find(
                        (item: any) => item.index === beat.index
                      );
                      return (
                        <li key={`${section.sectionPlanId}-${beat.index}`}>
                          {beat.summary} ·{" "}
                          {labelOf(
                            beatStatusLabels,
                            beatState?.status ?? "planned"
                          )}
                        </li>
                      );
                    })}
                  </ol>
                </li>
              );
            })}
          </ul>
          <article>
            <h4>已选资源</h4>
            <dl>
              <dt>Pattern</dt>
              <dd>
                {selectedPattern
                  ? `${selectedPattern.canonicalName} · ${selectedPattern.patternType}`
                  : "未选择"}
              </dd>
              <dt>Rhythm</dt>
              <dd>
                {selectedRhythmProfile
                  ? `${selectedRhythmProfile.label} · suspense ${selectedRhythmProfile.suspenseIndex}`
                  : "未选择"}
              </dd>
              <dt>Assets</dt>
              <dd>
                {selectedAssets.length
                  ? selectedAssets
                      .map((item: any) => item.canonicalName)
                      .join("、")
                  : "未选择"}
              </dd>
            </dl>
            {selectedPattern ? <p>{selectedPattern.intent}</p> : null}
            {selectedAssets.length ? (
              <ul>
                {selectedAssets.map((item: any) => (
                  <li key={item.assetId}>
                    {item.assetType} · {item.usageContext}
                  </li>
                ))}
              </ul>
            ) : null}
          </article>
          <article>
            <h4>规则卡片</h4>
            <ul>
              {activeRules.map((rule) => (
                <li key={rule.ruleId}>
                  {rule.title} · {labelOf(criticSeverityLabels, rule.severity)}{" "}
                  · {rule.autoBlock ? "自动阻断" : "人工关注"}
                  <div>{rule.conditionSummary}</div>
                </li>
              ))}
            </ul>
          </article>
        </section>

        <section
          style={{
            border: "1px solid #d4d4d8",
            padding: 16,
            display: "grid",
            gap: 12,
          }}
        >
          <div>
            <h3>中间：草稿与润色</h3>
            <p>
              当前 section：
              {focusSectionPlan
                ? `第 ${focusSectionPlan.sectionIndex} 节`
                : "未选择"}
            </p>
          </div>
          <article>
            <h4>写手草稿</h4>
            <p>{focusSectionRun?.writerOutput ?? "暂无草稿。"}</p>
          </article>
          <article>
            <h4>润色输出</h4>
            <p>{focusSectionRun?.humanizedText ?? "暂无润色稿。"}</p>
          </article>
          <article>
            <h4>组章结果</h4>
            <p>{writingRun.assembledChapter}</p>
          </article>
          <article>
            <h4>修订摘要</h4>
            {revisionSummary ? (
              <dl>
                <dt>状态</dt>
                <dd>{labelOf(statusLabels, revisionSummary.status)}</dd>
                <dt>修订轮次</dt>
                <dd>
                  第 {revisionSummary.revisionRound} /{" "}
                  {revisionSummary.maxRevisionRounds} 轮
                </dd>
                <dt>修订要求</dt>
                <dd>{revisionSummary.changeSummary}</dd>
                <dt>审阅说明</dt>
                <dd>{revisionSummary.reviewerNoteRef ?? "无"}</dd>
              </dl>
            ) : (
              <p>暂无修订摘要。</p>
            )}
          </article>
          <article>
            <h4>接受状态</h4>
            {writingRun.acceptedChapterRef ? (
              <dl>
                <dt>进入 manuscript</dt>
                <dd>已接受</dd>
                <dt>章节引用</dt>
                <dd>{writingRun.acceptedChapterRef}</dd>
                <dt>接受时间</dt>
                <dd>{writingRun.acceptedIntoManuscriptAt}</dd>
              </dl>
            ) : (
              <p>当前章节尚未接受进入 manuscript。</p>
            )}
          </article>
          <article>
            <h4>章节快照</h4>
            {chapterSnapshot ? (
              <dl>
                <dt>快照 ID</dt>
                <dd>{chapterSnapshot.chapterSnapshotId}</dd>
                <dt>章节标题</dt>
                <dd>{chapterSnapshot.chapterTitle}</dd>
                <dt>快照正文</dt>
                <dd>{chapterSnapshot.chapterText}</dd>
              </dl>
            ) : (
              <p>接受后生成章节快照。</p>
            )}
          </article>
        </section>

        <section
          style={{
            border: "1px solid #d4d4d8",
            padding: 16,
            display: "grid",
            gap: 12,
          }}
        >
          <div>
            <h3>右侧：记忆包与质量</h3>
          </div>
          <article>
            <h4>记忆包</h4>
            <p>{memoryPackage?.summary}</p>
            <ul>
              {(memoryPackage?.sourceRefs ?? []).map((item: any) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
          <article>
            <h4>提示包</h4>
            <p>{promptPackage?.summary}</p>
            <ul>
              {(promptPackage?.templateRefs ?? []).map((item: any) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
          <article>
            <h4>批评问题</h4>
            {focusSectionRun?.criticIssues.length ? (
              <ul>
                {focusSectionRun.criticIssues.map((issue: any) => (
                  <li key={issue.issueId}>
                    {labelOf(criticSeverityLabels, issue.severity)} ·{" "}
                    {issue.summary}
                  </li>
                ))}
              </ul>
            ) : (
              <p>当前 section 无阻断问题。</p>
            )}
          </article>
          <article>
            <h4>一致性复核</h4>
            {consistencyReport ? (
              <>
                <dl>
                  <dt>状态</dt>
                  <dd>{labelOf(statusLabels, consistencyReport.status)}</dd>
                  <dt>阻断问题数</dt>
                  <dd>{consistencyReport.blockingIssueCount}</dd>
                  <dt>检查域</dt>
                  <dd>{consistencyReport.checkedDomains.join("、")}</dd>
                </dl>
                <ul>
                  {consistencyReport.issues.map((issue: any) => (
                    <li key={issue.issueId}>
                      {labelOf(criticSeverityLabels, issue.severity)} ·{" "}
                      {issue.summary}
                      <div>
                        {labelOf(statusLabels, issue.resolutionStatus)} ·{" "}
                        {issue.affectedTextRef}
                      </div>
                    </li>
                  ))}
                </ul>
              </>
            ) : null}
          </article>
          <article>
            <h4>质量门禁</h4>
            {qualityReport ? (
              <>
                <dl>
                  <dt>状态</dt>
                  <dd>{labelOf(qualityStatusLabels, qualityReport.status)}</dd>
                  <dt>AI 味分数</dt>
                  <dd>{qualityReport.aiFlavorScore}</dd>
                  <dt>移动端可读性</dt>
                  <dd>{qualityReport.mobileReadabilityScore}</dd>
                  <dt>原创安全分数</dt>
                  <dd>{qualityReport.originalitySafetyScore}</dd>
                </dl>
                <ul>
                  {qualityReport.blockingIssues.map((issue: any) => (
                    <li key={issue.issueId}>
                      {labelOf(criticSeverityLabels, issue.severity)} ·{" "}
                      {issue.summary}
                    </li>
                  ))}
                </ul>
              </>
            ) : null}
          </article>
          <article>
            <h4>最新故事状态</h4>
            {manuscriptState ? (
              <dl>
                <dt>状态摘要</dt>
                <dd>{manuscriptState.currentStoryState.summary}</dd>
                <dt>质量门禁结果</dt>
                <dd>{manuscriptState.currentStoryState.qualityGateStatus}</dd>
                <dt>更新时间</dt>
                <dd>{manuscriptState.updatedAt}</dd>
              </dl>
            ) : (
              <p>接受后生成最新故事状态。</p>
            )}
          </article>
          <article>
            <h4>人物与关系更新</h4>
            {manuscriptState ? (
              <ul>
                {manuscriptState.characterDynamicState.map((item: any) => (
                  <li key={`character-${item.characterName}`}>
                    {item.characterName} · {item.stateSummary}
                  </li>
                ))}
                {manuscriptState.relationshipState.map((item: any) => (
                  <li key={`relationship-${item.subject}-${item.object}`}>
                    {item.subject} / {item.object} · {item.stateSummary}
                  </li>
                ))}
              </ul>
            ) : (
              <p>接受后同步人物动态与关系状态。</p>
            )}
          </article>
          <article>
            <h4>伏笔与前情摘要</h4>
            {manuscriptState ? (
              <>
                <ul>
                  {manuscriptState.hookState.map((item: any) => (
                    <li key={item.hookKey}>
                      {item.hookKey} · {item.status} · {item.summary}
                    </li>
                  ))}
                </ul>
                <ol>
                  {manuscriptState.priorSummaryPack.map((item: any) => (
                    <li key={item.summaryIndex}>{item.summary}</li>
                  ))}
                </ol>
              </>
            ) : (
              <p>接受后生成伏笔状态与前情摘要包。</p>
            )}
          </article>
          <article>
            <h4>证据链</h4>
            <ul>
              {(memoryPackage?.sourceRefs ?? []).map((item: any) => (
                <li key={`evidence-${item}`}>{item}</li>
              ))}
              {(promptPackage?.templateRefs ?? []).map((item: any) => (
                <li key={`template-${item}`}>{item}</li>
              ))}
              {focusSectionRun?.criticIssues.map((issue: any) => (
                <li key={issue.issueId}>{issue.affectedTextRef}</li>
              ))}
              {qualityReport?.blockingIssues.map((issue: any) => (
                <li key={issue.issueId}>{issue.affectedTextRef}</li>
              ))}
              {consistencyReport?.issues.map((issue: any) => (
                <li key={`consistency-${issue.issueId}`}>
                  {issue.affectedTextRef}
                </li>
              ))}
            </ul>
          </article>
        </section>
      </div>

      <section
        style={{
          border: "1px solid #d4d4d8",
          padding: 16,
          display: "grid",
          gap: 12,
        }}
      >
        <h3>底部：成本、重试与人工动作</h3>
        <dl
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(6, max-content)",
            gap: 8,
          }}
        >
          <dt>项目 ID</dt>
          <dd>{project.projectId}</dd>
          <dt>写作任务 ID</dt>
          <dd>{writingRun.writingRunId}</dd>
          <dt>当前阶段</dt>
          <dd>{labelOf(writingStageLabels, writingRun.currentStage)}</dd>
          <dt>总输入 Tokens</dt>
          <dd>{writingRun.modelCost.inputTokens}</dd>
          <dt>总输出 Tokens</dt>
          <dd>{writingRun.modelCost.outputTokens}</dd>
          <dt>预计成本</dt>
          <dd>{writingRun.modelCost.estimatedTotalCost}</dd>
          <dt>writer 输入</dt>
          <dd>{writingRun.modelCost.writerInputTokens}</dd>
          <dt>writer 输出</dt>
          <dd>{writingRun.modelCost.writerOutputTokens}</dd>
          <dt>critic 输入</dt>
          <dd>{writingRun.modelCost.criticInputTokens}</dd>
          <dt>critic 输出</dt>
          <dd>{writingRun.modelCost.criticOutputTokens}</dd>
          <dt>humanizer 输入</dt>
          <dd>{writingRun.modelCost.humanizerInputTokens}</dd>
          <dt>humanizer 输出</dt>
          <dd>{writingRun.modelCost.humanizerOutputTokens}</dd>
          <dt>retry_count</dt>
          <dd>{writingRun.modelCost.retryCount}</dd>
          <dt>trace_id</dt>
          <dd>{writingRun.traceId}</dd>
        </dl>
        <article>
          <h4>反馈记录</h4>
          <ul>
            {runFeedbackRecords.map((item: any) => (
              <li key={item.feedbackRecordId}>
                {item.feedbackType} · {item.score} ·{" "}
                {String(
                  item.payload.summary ??
                    item.payload.estimatedTotalCost ??
                    "无附注"
                )}
              </li>
            ))}
          </ul>
        </article>
        <article>
          <h4>人工动作</h4>
          <p>
            {canAcceptChapter
              ? "当前可接受本章进入 manuscript。"
              : "需先关闭 blocker 并完成修订确认。"}
          </p>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "accept_section"
                )
              }
            >
              接受当前 section
            </button>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "request_rewrite"
                )
              }
            >
              请求重写
            </button>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "edit_and_accept"
                )
              }
            >
              编辑后接受
            </button>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "block_generation"
                )
              }
            >
              阻止继续生成
            </button>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "edit_draft"
                )
              }
            >
              编辑草稿
            </button>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "mark_issue_resolved"
                )
              }
            >
              标记问题已解决
            </button>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "request_revision"
                )
              }
            >
              请求修订
            </button>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "approve_draft"
                )
              }
            >
              批准草稿
            </button>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "create_rule_update_request"
                )
              }
            >
              创建规则更新请求
            </button>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "reject_draft"
                )
              }
            >
              驳回草稿
            </button>
            <button
              type="button"
              onClick={() =>
                focusSectionRun &&
                applyWritingReviewAction(
                  writingRun.writingRunId,
                  focusSectionRun.sectionRunId,
                  "accept_chapter"
                )
              }
            >
              接受本章
            </button>
          </div>
        </article>
      </section>
    </section>
  );
}

export function FeedbackPage() {
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>反馈看板</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  const qualityReport: any = null;
  const writingRun: any = null;
  const feedbackRecords: any[] = [];
  const rankingSnapshot: any = null;
  const strategySuggestions: any[] = [];
  const memoryPackage: any = null;
  const promptPackage: any = null;
  const chapterSnapshot: any = null;
  const manuscriptState: any = null;
  const feedbackAuditEvents: any[] = [];

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>反馈看板</h2>
        <p>查看成本、质量、风格反馈、策略建议和证据链。</p>
      </div>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>质量报告摘要</h3>
        {qualityReport ? (
          <dl>
            <dt>状态</dt>
            <dd>{labelOf(qualityStatusLabels, qualityReport.status)}</dd>
            <dt>AI 味分数</dt>
            <dd>{qualityReport.aiFlavorScore}</dd>
            <dt>移动端可读性</dt>
            <dd>{qualityReport.mobileReadabilityScore}</dd>
            <dt>原创安全分数</dt>
            <dd>{qualityReport.originalitySafetyScore}</dd>
          </dl>
        ) : null}
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>成本质量指标</h3>
        {writingRun?.modelCost ? (
          <dl>
            <dt>总输入 Tokens</dt>
            <dd>{writingRun.modelCost.inputTokens}</dd>
            <dt>总输出 Tokens</dt>
            <dd>{writingRun.modelCost.outputTokens}</dd>
            <dt>预计成本</dt>
            <dd>{writingRun.modelCost.estimatedTotalCost}</dd>
            <dt>retry_count</dt>
            <dd>{writingRun.modelCost.retryCount}</dd>
          </dl>
        ) : null}
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>Prompt 排名</h3>
        {rankingSnapshot ? (
          <>
            <p>
              {rankingSnapshot.scopeRef} · v{rankingSnapshot.version}
            </p>
            <ul>
              {rankingSnapshot.items.map((item: any) => (
                <li key={`${item.rank}-${item.targetId}`}>
                  #{item.rank} · {item.label} · {item.score} · {item.status}
                  <div>{item.summary}</div>
                </li>
              ))}
            </ul>
          </>
        ) : (
          <p>暂无 prompt 排名快照。</p>
        )}
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>Ranking signals</h3>
        <ul>
          {(rankingSnapshot?.signals ?? []).map((item: any) => (
            <li key={item.signalId}>
              {item.signalType} · {item.targetId} · {item.score} · 权重{" "}
              {item.weight}
              <div>{item.summary}</div>
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>反馈记录</h3>
        <ul>
          {feedbackRecords.map((item: any) => (
            <li key={item.feedbackRecordId}>
              <strong>{item.feedbackType}</strong> · 来源 {item.source} · 分数{" "}
              {item.score}
              <div>
                {String(
                  item.payload.summary ??
                    item.payload.estimatedTotalCost ??
                    "无附注"
                )}
              </div>
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>Prompt 建议</h3>
        <ul>
          {(rankingSnapshot?.suggestions ?? []).map((item: any) => (
            <li key={item.suggestionId}>
              <strong>{item.targetScope}</strong> · {item.status} ·{" "}
              {item.summary}
              <div>{item.recommendedAction}</div>
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>策略建议</h3>
        <ul>
          {strategySuggestions.map((item: any) => (
            <li key={item.suggestionId}>
              <strong>{item.targetScope}</strong> · {item.status} ·{" "}
              {item.summary}
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>反馈审计轨迹</h3>
        <ul>
          {feedbackAuditEvents.map((item: any) => (
            <li key={item.auditEventId}>
              {item.action} · {item.summary} · {item.traceId}
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>章节入稿后状态</h3>
        {chapterSnapshot && manuscriptState ? (
          <>
            <p>
              {chapterSnapshot.chapterTitle} ·{" "}
              {chapterSnapshot.acceptedChapterRef}
            </p>
            <p>{manuscriptState.currentStoryState.summary}</p>
            <ul>
              {manuscriptState.priorSummaryPack.map((item: any) => (
                <li key={item.summaryIndex}>{item.summary}</li>
              ))}
            </ul>
          </>
        ) : (
          <p>当前章节尚未进入正文稿。</p>
        )}
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>证据链</h3>
        <ul>
          {(memoryPackage?.sourceRefs ?? []).map((item: any) => (
            <li key={`memory-${item}`}>{item}</li>
          ))}
          {(promptPackage?.templateRefs ?? []).map((item: any) => (
            <li key={`prompt-${item}`}>{item}</li>
          ))}
          {qualityReport?.blockingIssues.map((item: any) => (
            <li key={item.issueId}>{item.affectedTextRef}</li>
          ))}
        </ul>
      </section>
    </section>
  );
}

export function ConfigurationPage() {
  const {
    toggleModelProfile,
    updateQualityGateProfile,
    updateAgentAssignment,
    updatePromptVersion,
  } = usePhaseTwo();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );

  const [apiConfig, setApiConfig] = useState<Record<string, unknown> | null>(
    null
  );
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!apiClient) return;
    let cancelled = false;
    setLoading(true);
    void (apiClient.getConfiguration() as Promise<Record<string, unknown>>)
      .then((cfg) => {
        if (!cancelled) setApiConfig(cfg);
      })
      .catch((e) => {
        if (!cancelled)
          setError(e instanceof Error ? e.message : "加载配置失败");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [apiClient]);

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>配置中心</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  const snapshot = (apiConfig ?? {
    modelProfiles: [],
    agentModelAssignments: [],
    qualityGateProfiles: [],
    promptVersions: [],
    defaultModelProfileId: "",
  }) as any;
  const project: any = null;
  const writingRun: any = null;
  const providerCalls: any[] = [];
  const writerProfile = snapshot.modelProfiles.find(
    (item: any) => item.modelProfileId === DEFAULT_MODEL_PROFILE_ID
  );
  const fallbackProfile = snapshot.modelProfiles.find(
    (item: any) => item.modelProfileId === STRUCTURED_FALLBACK_MODEL_PROFILE_ID
  );
  const rankingSnapshot: any = null;

  if (loading) return <Page title="加载中…" body="正在获取配置数据。" />;

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>配置中心</h2>
        <p>
          查看模型路由、Agent 分配、质量阈值、提示版本、调用指标与配置审计。
        </p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
      </div>
      <section
        style={{
          border: "1px solid #d4d4d8",
          padding: 16,
          display: "grid",
          gap: 12,
        }}
      >
        <h3>模型 Profile</h3>
        <ul style={{ display: "grid", gap: 12, listStyle: "none", padding: 0 }}>
          {snapshot.modelProfiles.map((profile: any) => (
            <li
              key={profile.modelProfileId}
              style={{ border: "1px solid #e4e4e7", padding: 12 }}
            >
              <strong>{profile.label}</strong>
              <p>
                {profile.providerName} · {profile.providerModelName}
              </p>
              <p>
                {profile.enabled ? "已启用" : "已禁用"} ·{" "}
                {profile.supportsStructuredOutput
                  ? "支持结构化输出"
                  : "不支持结构化输出"}
              </p>
              <p>
                fallback_profile_ids：
                {profile.fallbackProfileIds.join("、") || "空"}
              </p>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <button
                  type="button"
                  onClick={() =>
                    toggleModelProfile(profile.modelProfileId, true)
                  }
                >
                  启用
                </button>
                <button
                  type="button"
                  onClick={() =>
                    toggleModelProfile(profile.modelProfileId, false)
                  }
                >
                  禁用
                </button>
              </div>
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>Agent 分配</h3>
        <ul>
          {snapshot.agentModelAssignments.map((assignment: any) => (
            <li key={assignment.assignmentId}>
              {assignment.agentRole} · {assignment.outputMode} ·{" "}
              {assignment.modelProfileId} · max_retry {assignment.maxRetry} ·
              max_cost {assignment.maxCost}
              {assignment.agentRole === "writer" ? (
                <button
                  type="button"
                  style={{ marginLeft: 8 }}
                  onClick={() =>
                    updateAgentAssignment(
                      assignment.assignmentId,
                      STRUCTURED_FALLBACK_MODEL_PROFILE_ID,
                      assignment.maxRetry,
                      assignment.maxCost,
                      assignment.enabled
                    )
                  }
                >
                  改用 fallback
                </button>
              ) : null}
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>质量阈值</h3>
        <ul>
          {snapshot.qualityGateProfiles.map((profile: any) => (
            <li key={profile.qualityGateProfileId}>
              {profile.label} · AI 味阈值 {profile.aiFlavorThreshold} ·
              原创安全阈值 {profile.originalitySafetyThreshold}
              <button
                type="button"
                style={{ marginLeft: 8 }}
                onClick={() =>
                  updateQualityGateProfile(
                    profile.qualityGateProfileId,
                    0.4,
                    0.9
                  )
                }
              >
                应用更严格阈值
              </button>
            </li>
          ))}
        </ul>
        <p>项目当前 quality_gate_profile_id：{project?.qualityGateProfileId}</p>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>Prompt 版本与规则</h3>
        <ul>
          {snapshot.promptVersions.map((item: any) => (
            <li key={`${item.agentRole}-${item.templateRef}`}>
              {item.agentRole} · {item.templateRef}
              {item.agentRole === "writer" ? (
                <button
                  type="button"
                  style={{ marginLeft: 8 }}
                  onClick={() =>
                    updatePromptVersion(
                      item.agentRole,
                      "prompt://writer/chapter-compact"
                    )
                  }
                >
                  切到紧凑版
                </button>
              ) : null}
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>Prompt 排名建议与受控变更</h3>
        <p>ranking suggestion 仅进入审核队列；正式生效仍需通过配置变更动作。</p>
        <ul>
          {(rankingSnapshot?.suggestions ?? []).map((item: any) => (
            <li key={`cfg-${item.suggestionId}`}>
              {item.summary} · {item.status} · {item.recommendedAction}
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>最近调用指标</h3>
        <ul>
          {providerCalls.map((call) => (
            <li key={call.providerCallId}>
              {call.agentRole} · {call.modelProfileId} · token{" "}
              {call.promptTokens}/{call.completionTokens} · latency{" "}
              {call.latencyMs}ms · retry {call.retryCount} · cost{" "}
              {call.costEstimate} · {call.status}
              {call.errorCode ? ` · ${call.errorCode}` : ""}
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>最近路由记录</h3>
        <dl>
          <dt>writer</dt>
          <dd>{writingRun?.writerModelProfileId}</dd>
          <dt>critic</dt>
          <dd>{writingRun?.criticModelProfileId}</dd>
          <dt>humanizer</dt>
          <dd>{writingRun?.humanizerModelProfileId}</dd>
          <dt>默认模型</dt>
          <dd>{snapshot.defaultModelProfileId}</dd>
        </dl>
        <p>
          默认 profile {writerProfile?.enabled ? "可用" : "已关闭"}，critic
          结构化输出走 {STRUCTURED_FALLBACK_MODEL_PROFILE_ID}。 默认 profile
          关闭时，writer / humanizer 改走{" "}
          {fallbackProfile?.enabled
            ? STRUCTURED_FALLBACK_MODEL_PROFILE_ID
            : "无可用 fallback"}
          。
        </p>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>配置变更记录</h3>
        <p>暂无变更记录。</p>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>配置审计轨迹</h3>
        <p>暂无审计事件。</p>
      </section>
    </section>
  );
}
