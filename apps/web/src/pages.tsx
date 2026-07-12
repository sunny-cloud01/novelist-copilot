import { FormEvent, createContext, useContext, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import {
  DEMO_BOOK_ID,
  DEMO_RUN_ID,
  DEMO_WRITING_RUN_ID,
  PhaseTwoState,
  ReviewAction,
  WritingReviewAction,
  applyReviewActionToState,
  applyWritingReviewActionToState,
  commitKnowledgePackage,
  createInitialPhaseTwoState,
  createUploadedBook,
  deriveLowConfidenceItems,
  DEFAULT_MODEL_PROFILE_ID,
  STRUCTURED_FALLBACK_MODEL_PROFILE_ID,
  promoteStrategySuggestionInState,
  toggleModelProfileInState,
  updateAgentAssignmentInState,
  updatePromptVersionInState,
  updateQualityGateProfileInState,
} from "./components/phase-two-state";

const statusLabels: Record<string, string> = {
  active: "进行中",
  approved: "已通过",
  pending: "待处理",
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

type PhaseTwoContextValue = {
  state: PhaseTwoState;
  uploadBook: (payload: { title: string; authorName: string; sourceType: string }) => void;
  applyReviewAction: (objectId: string, action: ReviewAction, targetObjectId?: string) => void;
  applyWritingReviewAction: (writingRunId: string, sectionRunId: string, action: WritingReviewAction) => void;
  toggleModelProfile: (modelProfileId: string, enabled: boolean) => void;
  updateQualityGateProfile: (qualityGateProfileId: string, aiFlavorThreshold: number, originalitySafetyThreshold: number) => void;
  updateAgentAssignment: (assignmentId: string, modelProfileId: string) => void;
  updatePromptVersion: (agentRole: string, templateRef: string) => void;
  promoteStrategySuggestion: (suggestionId: string) => void;
  commitRun: () => void;
};

const PhaseTwoContext = createContext<PhaseTwoContextValue | null>(null);

export function PhaseTwoProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<PhaseTwoState>(createInitialPhaseTwoState);

  const value = useMemo<PhaseTwoContextValue>(
    () => ({
      state,
      uploadBook: ({ title, authorName, sourceType }) => {
        setState((current) => ({
          ...current,
          book: createUploadedBook(title, authorName, sourceType),
          activityLog: [...current.activityLog, `已上传《${title}》，等待确定性抽取。`],
        }));
      },
      applyReviewAction: (objectId, action, targetObjectId) => {
        setState((current) => applyReviewActionToState(current, objectId, action, targetObjectId));
      },
      applyWritingReviewAction: (writingRunId, sectionRunId, action) => {
        setState((current) => applyWritingReviewActionToState(current, writingRunId, sectionRunId, action));
      },
      toggleModelProfile: (modelProfileId, enabled) => {
        setState((current) => toggleModelProfileInState(current, modelProfileId, enabled));
      },
      updateQualityGateProfile: (qualityGateProfileId, aiFlavorThreshold, originalitySafetyThreshold) => {
        setState((current) =>
          updateQualityGateProfileInState(current, qualityGateProfileId, aiFlavorThreshold, originalitySafetyThreshold),
        );
      },
      updateAgentAssignment: (assignmentId, modelProfileId) => {
        setState((current) => updateAgentAssignmentInState(current, assignmentId, modelProfileId));
      },
      updatePromptVersion: (agentRole, templateRef) => {
        setState((current) => updatePromptVersionInState(current, agentRole, templateRef));
      },
      promoteStrategySuggestion: (suggestionId) => {
        setState((current) => promoteStrategySuggestionInState(current, suggestionId));
      },
      commitRun: () => {
        setState((current) => commitKnowledgePackage(current));
      },
    }),
    [state],
  );

  return <PhaseTwoContext.Provider value={value}>{children}</PhaseTwoContext.Provider>;
}

export function usePhaseTwo() {
  const context = useContext(PhaseTwoContext);
  if (!context) {
    throw new Error("PhaseTwoContext missing");
  }
  return context;
}

export function WorkspaceHomePage() {
  const { workspaceId } = useParams();
  const { state } = usePhaseTwo();
  const workspace = state.workspace;
  const home = state.workspaceHome;
  const isCurrentWorkspace = workspaceId === workspace.workspaceId;

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>工作台首页</h2>
        <p>查看工作区入口、最近任务、待审核项与主流程快捷入口。</p>
        {!isCurrentWorkspace ? <p>当前仅展示默认演示工作区。</p> : null}
      </div>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>工作区信息</h3>
        <dl>
          <dt>工作区 ID</dt>
          <dd>{workspace.workspaceId}</dd>
          <dt>名称</dt>
          <dd>{workspace.name}</dd>
          <dt>默认语言</dt>
          <dd>{workspace.defaultLanguage}</dd>
          <dt>状态</dt>
          <dd>{labelOf(statusLabels, workspace.status)}</dd>
        </dl>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>最近任务</h3>
        <ul>
          {home.recentTasks.map((item) => (
            <li key={item.taskId}>{item.taskType} · {labelOf(statusLabels, item.status)} · {item.summary}</li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>待审核项</h3>
        <ul>
          {home.pendingReviews.map((item) => (
            <li key={item.reviewId}>{item.reviewType} · {labelOf(statusLabels, item.status)} · {item.title}</li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>快捷入口</h3>
        <ul>
          {home.quickLinks.map((item) => (
            <li key={item.route}>
              <Link to={item.route}>{item.label}</Link>
            </li>
          ))}
        </ul>
      </section>
    </section>
  );
}

export function SourceLibraryPage() {
  const navigate = useNavigate();
  const { uploadBook } = usePhaseTwo();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    uploadBook({
      title: String(form.get("title") ?? ""),
      authorName: String(form.get("authorName") ?? ""),
      sourceType: String(form.get("sourceType") ?? "reference_novel"),
    });
    navigate(`/sources/${DEMO_BOOK_ID}`);
  }

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>来源书库</h2>
        <p>上传参考书籍，查看章节导入与切分状态。</p>
      </div>
      <form aria-label="上传来源书籍" onSubmit={handleSubmit} style={{ display: "grid", gap: 12, maxWidth: 480 }}>
        <label>
          书名
          <input name="title" defaultValue="Battle Through the Heavens" />
        </label>
        <label>
          作者
          <input name="authorName" defaultValue="Tian Can Tu Dou" />
        </label>
        <label>
          来源类型
          <select name="sourceType" defaultValue="reference_novel">
            <option value="reference_novel">参考小说</option>
            <option value="outline">大纲</option>
          </select>
        </label>
        <label>
          使用边界
          <input name="usageBoundary" defaultValue="仅供参考，不直接复写原文。" readOnly />
        </label>
        <button type="submit">上传来源书籍</button>
      </form>
    </section>
  );
}

export function SourceBookPage() {
  const { bookId } = useParams();
  const { state } = usePhaseTwo();

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>来源书详情</h2>
        <p>查看章节切分结果与来源元数据。</p>
      </div>
      <dl>
        <dt>书籍 ID</dt>
        <dd>{bookId ?? state.book.bookId}</dd>
        <dt>书名</dt>
        <dd>{state.book.title}</dd>
        <dt>作者</dt>
        <dd>{state.book.authorName}</dd>
        <dt>导入状态</dt>
        <dd>{labelOf(statusLabels, state.book.importStatus)}</dd>
        <dt>追踪 ID</dt>
        <dd>{state.book.traceId}</dd>
      </dl>
      <section>
        <h3>章节列表</h3>
        <ul>
          {state.chapters.map((chapter) => (
            <li key={chapter.chapterId}>
              第 {chapter.chapterIndex} 章：{chapter.title}（{labelOf(segmentationStatusLabels, chapter.segmentationStatus)}）
            </li>
          ))}
        </ul>
      </section>
      <Link to={`/extraction-runs/${state.run.runId}`}>查看抽取任务</Link>
    </section>
  );
}

export function ExtractionRunPage() {
  const { runId } = useParams();
  const { state, commitRun } = usePhaseTwo();
  const lowConfidenceItems = deriveLowConfidenceItems(state.knowledgeObjects);

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>抽取任务详情</h2>
        <p>跟踪抽取状态、异常和任务报告。</p>
      </div>
      <dl>
        <dt>任务 ID</dt>
        <dd>{runId ?? state.run.runId}</dd>
        <dt>状态</dt>
        <dd>{labelOf(statusLabels, state.run.status)}</dd>
        <dt>当前阶段</dt>
        <dd>{labelOf(stageLabels, state.run.currentStage)}</dd>
        <dt>章节数</dt>
        <dd>{state.run.chapterCount}</dd>
        <dt>场景数</dt>
        <dd>{state.run.sceneCount}</dd>
        <dt>对象数</dt>
        <dd>{state.run.objectCount}</dd>
        <dt>证据数</dt>
        <dd>{state.run.evidenceCount}</dd>
        <dt>低置信对象数</dt>
        <dd>{state.run.lowConfidenceCount}</dd>
      </dl>
      <section>
        <h3>低置信对象队列</h3>
        {lowConfidenceItems.length === 0 ? <p>低置信对象已全部处理。</p> : null}
        <ul>
          {lowConfidenceItems.map((item) => (
            <li key={item.objectId}>{item.canonicalName}（置信度 {item.confidence}）</li>
          ))}
        </ul>
      </section>
      <div style={{ display: "flex", gap: 12 }}>
        <Link to="/knowledge/review">进入知识审核</Link>
        <button type="button" onClick={commitRun}>提交知识包</button>
      </div>
    </section>
  );
}

export function KnowledgeReviewPage() {
  const { state, applyReviewAction } = usePhaseTwo();
  const lowConfidenceItems = deriveLowConfidenceItems(state.knowledgeObjects);

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>知识审核</h2>
        <p>对候选对象执行通过、驳回、合并别名或请求重抽。</p>
      </div>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>抽取运行状态</h3>
        <dl>
          <dt>状态</dt>
          <dd>{labelOf(statusLabels, state.run.status)}</dd>
          <dt>当前阶段</dt>
          <dd>{labelOf(stageLabels, state.run.currentStage)}</dd>
          <dt>低置信对象数</dt>
          <dd>{state.run.lowConfidenceCount}</dd>
        </dl>
      </section>
      <ul style={{ display: "grid", gap: 16, padding: 0, listStyle: "none" }}>
        {lowConfidenceItems.map((item) => (
          <li key={item.objectId} style={{ border: "1px solid #d4d4d8", padding: 16 }}>
            <h3>{item.canonicalName}</h3>
            <p>{labelOf(objectTypeLabels, item.objectType)} · 置信度 {item.confidence}</p>
            <p>别名：{item.aliases.join("、") || "无"}</p>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <button type="button" onClick={() => applyReviewAction(item.objectId, "approve")}>通过</button>
              <button type="button" onClick={() => applyReviewAction(item.objectId, "reject")}>驳回</button>
              <button type="button" onClick={() => applyReviewAction(item.objectId, "merge_alias", "01JZOBJ0000000000000000003")}>合并别名</button>
              <button type="button" onClick={() => applyReviewAction(item.objectId, "request_reextract")}>请求重抽</button>
            </div>
          </li>
        ))}
      </ul>
      <section>
        <h3>故事图谱摘要</h3>
        <ul>
          {state.graphNodes.map((node) => (
            <li key={node.nodeId}>{node.label}（{labelOf(objectTypeLabels, node.nodeType)}）</li>
          ))}
        </ul>
      </section>
      <section>
        <h3>活动日志</h3>
        <ul>
          {state.activityLog.map((item, index) => (
            <li key={`${index}-${item}`}>{item}</li>
          ))}
        </ul>
      </section>
    </section>
  );
}

export function GraphPage() {
  const { state } = usePhaseTwo();
  const [selectedNodeId, setSelectedNodeId] = useState<string>(state.graphNodes[0]?.nodeId ?? "");
  const selectedNode = selectedNodeId ? state.graphNodeDetails[selectedNodeId] : undefined;
  const neighbors = selectedNodeId ? state.graphNeighborsByNode[selectedNodeId] ?? [] : [];

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>故事图谱查看器</h2>
        <p>查看节点、关系与快照细节。</p>
      </div>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>图谱节点</h3>
        <ul style={{ display: "grid", gap: 12, padding: 0, listStyle: "none" }}>
          {state.graphNodes.map((node) => (
            <li key={node.nodeId} style={{ border: "1px solid #e4e4e7", padding: 12 }}>
              <button type="button" onClick={() => setSelectedNodeId(node.nodeId)}>
                {node.label}（{labelOf(objectTypeLabels, node.nodeType)}）
              </button>
              <p>证据 {node.evidenceRefs.length} 条</p>
            </li>
          ))}
        </ul>
      </section>
      {selectedNode ? (
        <>
          <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
            <h3>节点详情</h3>
            <dl>
              <dt>名称</dt>
              <dd>{selectedNode.label}</dd>
              <dt>类型</dt>
              <dd>{labelOf(objectTypeLabels, selectedNode.nodeType)}</dd>
              <dt>审核状态</dt>
              <dd>{labelOf(statusLabels, selectedNode.reviewStatus)}</dd>
              <dt>生命周期</dt>
              <dd>{labelOf(statusLabels, selectedNode.lifecycleStatus)}</dd>
              <dt>置信度</dt>
              <dd>{selectedNode.confidence}</dd>
              <dt>别名</dt>
              <dd>{selectedNode.aliases.join("、") || "无"}</dd>
              <dt>对象引用</dt>
              <dd>{selectedNode.canonicalObjectId}</dd>
            </dl>
            <p>{selectedNode.summary}</p>
          </section>
          <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
            <h3>关系查看</h3>
            {neighbors.length === 0 ? <p>当前节点暂无关系。</p> : null}
            <ul>
              {neighbors.map((neighbor) => (
                <li key={neighbor.edgeId}>
                  {neighbor.direction === "outgoing" ? "指向" : "来自"}
                  {neighbor.neighborLabel} · {neighbor.relationType} · 置信度 {neighbor.confidence}
                </li>
              ))}
            </ul>
          </section>
          <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
            <h3>Source evidence</h3>
            <ul>
              {selectedNode.evidenceRefs.map((ref) => (
                <li key={ref}>{ref}</li>
              ))}
            </ul>
          </section>
        </>
      ) : null}
    </section>
  );
}

export function ProjectListPage() {
  const { state } = usePhaseTwo();

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>小说项目</h2>
        <p>查看项目、故事圣经与章节规划进度。</p>
      </div>
      <ul style={{ display: "grid", gap: 16, padding: 0, listStyle: "none" }}>
        {state.projects.map((project) => (
          <li key={project.projectId} style={{ border: "1px solid #d4d4d8", padding: 16 }}>
            <h3>{project.title}</h3>
            <p>{project.genreScope} · {labelOf(statusLabels, project.status)}</p>
            <p>可用知识来源 {project.allowedKnowledgeSourceRefs.length} 项</p>
            <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
              <Link to={`/projects/${project.projectId}`}>查看项目详情</Link>
              <Link to={`/projects/${project.projectId}/planner`}>进入章节规划</Link>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}

export function ProjectHomePage() {
  const { projectId } = useParams();
  const { state } = usePhaseTwo();
  const project = state.projects.find((item) => item.projectId === projectId) ?? state.projects[0];

  if (!project) {
    return <Page title="项目不存在" body="未找到对应项目。" />;
  }

  const storyBible = state.storyBibles.find((item) => item.storyBibleId === project.storyBibleId);
  const chapterPlans = state.chapterPlans.filter((item) => item.projectId === project.projectId);

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>项目主页</h2>
        <p>查看项目状态、故事圣经摘要与章节入口。</p>
      </div>
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
        <section>
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
          </dl>
        </section>
      ) : null}
      <section>
        <h3>章节规划入口</h3>
        <ul>
          {chapterPlans.map((plan) => (
            <li key={plan.chapterPlanId}>
              第 {plan.chapterIndex} 章《{plan.title}》 · {labelOf(statusLabels, plan.status)} · 目标 {plan.targetWordCount} 字
            </li>
          ))}
        </ul>
      </section>
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        <Link to={`/projects/${project.projectId}/planner`}>进入章节规划器</Link>
        <Link to={`/projects/${project.projectId}/writing/${DEMO_WRITING_RUN_ID}`}>查看写作入口</Link>
      </div>
    </section>
  );
}

export function PlannerPage() {
  const { projectId } = useParams();
  const { state } = usePhaseTwo();
  const project = state.projects.find((item) => item.projectId === projectId) ?? state.projects[0];

  if (!project) {
    return <Page title="规划不存在" body="未找到对应项目规划。" />;
  }

  const chapterPlans = state.chapterPlans.filter((item) => item.projectId === project.projectId);
  const projectTaskIds = new Set(chapterPlans.map((item) => `object://chapter-plans/${item.chapterPlanId}`));
  const plannerTasks = state.agentTasks.filter(
    (item) => item.taskType === "create_chapter_plan" || projectTaskIds.has(item.targetRef),
  );
  const plannerAuditEvents = state.auditEvents.filter(
    (item) => item.targetType === "chapter_plan" || item.targetType === "quality_gate_profile",
  );
  const patterns = state.patterns ?? [];
  const rhythmProfiles = state.rhythmProfiles ?? [];
  const assets = state.assets ?? [];

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>章节规划器</h2>
        <p>查看章节目标、场景拆解、beat 明细、相关任务和审计记录。</p>
      </div>
      {chapterPlans.map((plan) => {
        const sections = state.sectionPlansByChapter[plan.chapterPlanId] ?? [];
        const selectedPattern = patterns.find((item) => item.patternId === plan.selectedPatternId) ?? null;
        const selectedRhythmProfile = rhythmProfiles.find((item) => item.rhythmProfileId === plan.selectedRhythmProfileId) ?? null;
        const selectedAssets = assets.filter((item) => plan.selectedAssetIds.includes(item.assetId));
        return (
          <article key={plan.chapterPlanId} style={{ border: "1px solid #d4d4d8", padding: 16, display: "grid", gap: 12 }}>
            <div>
              <h3>第 {plan.chapterIndex} 章《{plan.title}》</h3>
              <p>{plan.summary}</p>
              <p>{labelOf(statusLabels, plan.status)} · 目标 {plan.targetWordCount} 字</p>
            </div>
            <section>
              <h4>已选资源</h4>
              <dl>
                <dt>Pattern</dt>
                <dd>{selectedPattern ? `${selectedPattern.canonicalName} · ${selectedPattern.patternType}` : "未选择"}</dd>
                <dt>Rhythm</dt>
                <dd>
                  {selectedRhythmProfile
                    ? `${selectedRhythmProfile.label} · climax ${selectedRhythmProfile.climaxIndex}`
                    : "未选择"}
                </dd>
                <dt>Assets</dt>
                <dd>{selectedAssets.length ? selectedAssets.map((item) => item.canonicalName).join("、") : "未选择"}</dd>
              </dl>
              {selectedPattern ? <p>{selectedPattern.expectedReaderEffect}</p> : null}
              {selectedAssets.length ? (
                <ul>
                  {selectedAssets.map((item) => (
                    <li key={item.assetId}>{item.assetType} · {item.contentSummary}</li>
                  ))}
                </ul>
              ) : null}
            </section>
            <section>
              <h4>分节规划</h4>
              <ul style={{ display: "grid", gap: 12 }}>
                {sections.map((section) => (
                  <li key={section.sectionPlanId}>
                    <strong>第 {section.sectionIndex} 节 · {labelOf(planningRoleLabels, section.planningRole)}</strong>
                    <p>{section.sceneGoal}</p>
                    <ol>
                      {section.beats.map((beat) => (
                        <li key={`${section.sectionPlanId}-${beat.index}`}>{beat.summary}</li>
                      ))}
                    </ol>
                  </li>
                ))}
              </ul>
            </section>
            <section>
              <h4>关联任务</h4>
              <ul>
                {plannerTasks.map((task) => (
                  <li key={task.taskId}>
                    {task.taskType} · {labelOf(statusLabels, task.status)} · {task.summary}
                  </li>
                ))}
              </ul>
            </section>
            <section>
              <h4>任务事件</h4>
              <ul>
                {plannerTasks.flatMap((task) => task.events).map((event) => (
                  <li key={event.eventId}>
                    {event.eventType} · {labelOf(statusLabels, event.status)} · {event.summary}
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
            <Link to={`/projects/${project.projectId}/writing/${DEMO_WRITING_RUN_ID}`}>进入写作工作台（下一阶段）</Link>
          </article>
        );
      })}
    </section>
  );
}

export function WritingStudioPage() {
  const { projectId, writingRunId } = useParams();
  const { state, applyWritingReviewAction } = usePhaseTwo();
  const projects = state.projects ?? [];
  const writingRuns = state.writingRuns ?? [];
  const sectionRunsByWriting = state.sectionRunsByWriting ?? {};
  const chapterPlans = state.chapterPlans ?? [];
  const sectionPlansByChapter = state.sectionPlansByChapter ?? {};
  const memoryPackages = state.memoryPackages ?? [];
  const promptPackages = state.promptPackages ?? [];
  const qualityReports = state.qualityReports ?? [];
  const consistencyReports = state.consistencyReports ?? [];
  const revisionSummaries = state.revisionSummaries ?? [];
  const rules = state.rules ?? [];
  const feedbackRecords = state.feedbackRecords ?? [];
  const project = projects.find((item) => item.projectId === projectId) ?? projects[0];
  const writingRun = writingRuns.find((item) => item.writingRunId === writingRunId) ?? writingRuns[0];

  if (!project || !writingRun) {
    return <Page title="写作任务不存在" body="未找到对应写作任务。" />;
  }

  const chapterPlan = chapterPlans.find((item) => item.chapterPlanId === writingRun.chapterPlanId);
  const sectionPlans = sectionPlansByChapter[writingRun.chapterPlanId] ?? [];
  const sectionRuns = sectionRunsByWriting[writingRun.writingRunId] ?? [];
  const memoryPackage = memoryPackages.find((item) => item.memoryPackageId === writingRun.memoryPackageId);
  const promptPackage = promptPackages.find((item) => item.promptPackageId === writingRun.promptPackageId);
  const qualityReport = qualityReports.find((item) => item.qualityReportId === writingRun.qualityReportId);
  const consistencyReport =
    writingRun.consistencyReport ??
    consistencyReports.find((item) => item.consistencyReportId === writingRun.consistencyReportId) ??
    null;
  const revisionSummary =
    writingRun.revisionSummary ??
    revisionSummaries.find((item) => item.revisionSummaryId === writingRun.revisionSummaryId) ??
    null;
  const activeRules = rules.filter((item) => item.scopeRef.includes(project.projectId));
  const focusSectionRun = sectionRuns.find((item) => item.criticIssues.length > 0) ?? sectionRuns[0];
  const focusSectionPlan = sectionPlans.find((item) => item.sectionPlanId === focusSectionRun?.sectionPlanId);
  const selectedPattern = state.patterns.find((item) => item.patternId === writingRun.selectedPatternId) ?? null;
  const selectedRhythmProfile = state.rhythmProfiles.find((item) => item.rhythmProfileId === writingRun.selectedRhythmProfileId) ?? null;
  const selectedAssets = state.assets.filter((item) => writingRun.selectedAssetIds.includes(item.assetId));
  const runFeedbackRecords = feedbackRecords.filter(
    (item) => item.targetId === writingRun.writingRunId || item.targetId === writingRun.qualityReportId,
  );
  const chapterSnapshot = writingRun.chapterSnapshot;
  const manuscriptState = writingRun.manuscriptState;
  const canAcceptChapter =
    !!consistencyReport &&
    consistencyReport.blockingIssueCount === 0 &&
    !!qualityReport &&
    qualityReport.blockingIssues.length === 0 &&
    qualityReport.status !== "blocked" &&
    !qualityReport.humanReviewRequired &&
    !!revisionSummary &&
    ["accepted", "revised"].includes(revisionSummary.status);

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>写作工作台</h2>
        <p>按 section / beat 推进写作，查看批评问题、润色结果、证据链与质量反馈。</p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1.1fr 1.2fr 1fr", gap: 16, alignItems: "start" }}>
        <section style={{ border: "1px solid #d4d4d8", padding: 16, display: "grid", gap: 12 }}>
          <div>
            <h3>左侧：规划与分节</h3>
            <p>{project.title}</p>
            {chapterPlan ? <p>第 {chapterPlan.chapterIndex} 章《{chapterPlan.title}》 · {chapterPlan.summary}</p> : null}
          </div>
          <ul style={{ display: "grid", gap: 12, padding: 0, listStyle: "none" }}>
            {sectionPlans.map((section) => {
              const sectionRun = sectionRuns.find((item) => item.sectionPlanId === section.sectionPlanId);
              return (
                <li key={section.sectionPlanId} style={{ border: "1px solid #e4e4e7", padding: 12 }}>
                  <strong>第 {section.sectionIndex} 节 · {labelOf(planningRoleLabels, section.planningRole)}</strong>
                  <p>{section.sceneGoal}</p>
                  <p>{sectionRun ? labelOf(beatStatusLabels, sectionRun.status) : "待生成"}</p>
                  <ol>
                    {section.beats.map((beat) => {
                      const beatState = sectionRun?.beatStatus.find((item) => item.index === beat.index);
                      return (
                        <li key={`${section.sectionPlanId}-${beat.index}`}>
                          {beat.summary} · {labelOf(beatStatusLabels, beatState?.status ?? "planned")}
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
              <dd>{selectedPattern ? `${selectedPattern.canonicalName} · ${selectedPattern.patternType}` : "未选择"}</dd>
              <dt>Rhythm</dt>
              <dd>
                {selectedRhythmProfile
                  ? `${selectedRhythmProfile.label} · suspense ${selectedRhythmProfile.suspenseIndex}`
                  : "未选择"}
              </dd>
              <dt>Assets</dt>
              <dd>{selectedAssets.length ? selectedAssets.map((item) => item.canonicalName).join("、") : "未选择"}</dd>
            </dl>
            {selectedPattern ? <p>{selectedPattern.intent}</p> : null}
            {selectedAssets.length ? (
              <ul>
                {selectedAssets.map((item) => (
                  <li key={item.assetId}>{item.assetType} · {item.usageContext}</li>
                ))}
              </ul>
            ) : null}
          </article>
          <article>
            <h4>规则卡片</h4>
            <ul>
              {activeRules.map((rule) => (
                <li key={rule.ruleId}>
                  {rule.title} · {labelOf(criticSeverityLabels, rule.severity)} · {rule.autoBlock ? "自动阻断" : "人工关注"}
                  <div>{rule.conditionSummary}</div>
                </li>
              ))}
            </ul>
          </article>
        </section>

        <section style={{ border: "1px solid #d4d4d8", padding: 16, display: "grid", gap: 12 }}>
          <div>
            <h3>中间：草稿与润色</h3>
            <p>当前 section：{focusSectionPlan ? `第 ${focusSectionPlan.sectionIndex} 节` : "未选择"}</p>
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
                  第 {revisionSummary.revisionRound} / {revisionSummary.maxRevisionRounds} 轮
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

        <section style={{ border: "1px solid #d4d4d8", padding: 16, display: "grid", gap: 12 }}>
          <div>
            <h3>右侧：记忆包与质量</h3>
          </div>
          <article>
            <h4>记忆包</h4>
            <p>{memoryPackage?.summary}</p>
            <ul>
              {(memoryPackage?.sourceRefs ?? []).map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
          <article>
            <h4>提示包</h4>
            <p>{promptPackage?.summary}</p>
            <ul>
              {(promptPackage?.templateRefs ?? []).map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
          <article>
            <h4>批评问题</h4>
            {focusSectionRun?.criticIssues.length ? (
              <ul>
                {focusSectionRun.criticIssues.map((issue) => (
                  <li key={issue.issueId}>{labelOf(criticSeverityLabels, issue.severity)} · {issue.summary}</li>
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
                  {consistencyReport.issues.map((issue) => (
                    <li key={issue.issueId}>
                      {labelOf(criticSeverityLabels, issue.severity)} · {issue.summary}
                      <div>{labelOf(statusLabels, issue.resolutionStatus)} · {issue.affectedTextRef}</div>
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
                  {qualityReport.blockingIssues.map((issue) => (
                    <li key={issue.issueId}>{labelOf(criticSeverityLabels, issue.severity)} · {issue.summary}</li>
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
                {manuscriptState.characterDynamicState.map((item) => (
                  <li key={`character-${item.characterName}`}>{item.characterName} · {item.stateSummary}</li>
                ))}
                {manuscriptState.relationshipState.map((item) => (
                  <li key={`relationship-${item.subject}-${item.object}`}>{item.subject} / {item.object} · {item.stateSummary}</li>
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
                  {manuscriptState.hookState.map((item) => (
                    <li key={item.hookKey}>{item.hookKey} · {item.status} · {item.summary}</li>
                  ))}
                </ul>
                <ol>
                  {manuscriptState.priorSummaryPack.map((item) => (
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
              {(memoryPackage?.sourceRefs ?? []).map((item) => (
                <li key={`evidence-${item}`}>{item}</li>
              ))}
              {(promptPackage?.templateRefs ?? []).map((item) => (
                <li key={`template-${item}`}>{item}</li>
              ))}
              {focusSectionRun?.criticIssues.map((issue) => (
                <li key={issue.issueId}>{issue.affectedTextRef}</li>
              ))}
              {qualityReport?.blockingIssues.map((issue) => (
                <li key={issue.issueId}>{issue.affectedTextRef}</li>
              ))}
              {consistencyReport?.issues.map((issue) => (
                <li key={`consistency-${issue.issueId}`}>{issue.affectedTextRef}</li>
              ))}
            </ul>
          </article>
        </section>
      </div>

      <section style={{ border: "1px solid #d4d4d8", padding: 16, display: "grid", gap: 12 }}>
        <h3>底部：成本、重试与人工动作</h3>
        <dl style={{ display: "grid", gridTemplateColumns: "repeat(6, max-content)", gap: 8 }}>
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
            {runFeedbackRecords.map((item) => (
              <li key={item.feedbackRecordId}>
                {item.feedbackType} · {item.score} · {String(item.payload.summary ?? item.payload.estimatedTotalCost ?? "无附注")}
              </li>
            ))}
          </ul>
        </article>
        <article>
          <h4>人工动作</h4>
          <p>{canAcceptChapter ? "当前可接受本章进入 manuscript。" : "需先关闭 blocker 并完成修订确认。"}</p>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "accept_section")}>接受当前 section</button>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "request_rewrite")}>请求重写</button>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "edit_and_accept")}>编辑后接受</button>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "block_generation")}>阻止继续生成</button>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "edit_draft")}>编辑草稿</button>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "mark_issue_resolved")}>标记问题已解决</button>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "request_revision")}>请求修订</button>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "approve_draft")}>批准草稿</button>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "create_rule_update_request")}>创建规则更新请求</button>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "reject_draft")}>驳回草稿</button>
            <button type="button" onClick={() => focusSectionRun && applyWritingReviewAction(writingRun.writingRunId, focusSectionRun.sectionRunId, "accept_chapter")}>接受本章</button>
          </div>
        </article>
      </section>
    </section>
  );
}

export function FeedbackPage() {
  const { state, promoteStrategySuggestion } = usePhaseTwo();
  const writingRun = state.writingRuns[0];
  const qualityReport = state.qualityReports.find((item) => item.qualityReportId === writingRun?.qualityReportId);
  const feedbackRecords = (state.feedbackRecords ?? []).filter(
    (item) => item.targetId === writingRun?.writingRunId || item.targetId === writingRun?.qualityReportId,
  );
  const rankingSnapshot = (state.rankingSnapshots ?? []).find((item) => item.rankingType === "prompt");
  const strategySuggestions = (state.strategySuggestions ?? []).filter((item) =>
    feedbackRecords.some((record) => record.feedbackRecordId === item.basedOnFeedbackRecordId),
  );
  const memoryPackage = (state.memoryPackages ?? []).find((item) => item.writingRunId === writingRun?.writingRunId);
  const promptPackage = (state.promptPackages ?? []).find((item) => item.writingRunId === writingRun?.writingRunId);
  const chapterSnapshot = writingRun?.chapterSnapshot;
  const manuscriptState = writingRun?.manuscriptState;
  const feedbackAuditEvents = state.auditEvents.filter(
    (item) => item.action.startsWith("feedback.") || item.targetType === "strategy_suggestion",
  );

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
            <p>{rankingSnapshot.scopeRef} · v{rankingSnapshot.version}</p>
            <ul>
              {rankingSnapshot.items.map((item) => (
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
          {(rankingSnapshot?.signals ?? []).map((item) => (
            <li key={item.signalId}>
              {item.signalType} · {item.targetId} · {item.score} · 权重 {item.weight}
              <div>{item.summary}</div>
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>反馈记录</h3>
        <ul>
          {feedbackRecords.map((item) => (
            <li key={item.feedbackRecordId}>
              <strong>{item.feedbackType}</strong> · 来源 {item.source} · 分数 {item.score}
              <div>{String(item.payload.summary ?? item.payload.estimatedTotalCost ?? "无附注")}</div>
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>Prompt 建议</h3>
        <ul>
          {(rankingSnapshot?.suggestions ?? []).map((item) => (
            <li key={item.suggestionId}>
              <strong>{item.targetScope}</strong> · {item.status} · {item.summary}
              <div>{item.recommendedAction}</div>
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>策略建议</h3>
        <ul>
          {strategySuggestions.map((item) => (
            <li key={item.suggestionId}>
              <strong>{item.targetScope}</strong> · {item.status} · {item.summary}
              <div style={{ marginTop: 8 }}>
                <button type="button" onClick={() => promoteStrategySuggestion(item.suggestionId)}>
                  提升为已批准策略
                </button>
              </div>
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>反馈审计轨迹</h3>
        <ul>
          {feedbackAuditEvents.map((item) => (
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
            <p>{chapterSnapshot.chapterTitle} · {chapterSnapshot.acceptedChapterRef}</p>
            <p>{manuscriptState.currentStoryState.summary}</p>
            <ul>
              {manuscriptState.priorSummaryPack.map((item) => (
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
          {(memoryPackage?.sourceRefs ?? []).map((item) => (
            <li key={`memory-${item}`}>{item}</li>
          ))}
          {(promptPackage?.templateRefs ?? []).map((item) => (
            <li key={`prompt-${item}`}>{item}</li>
          ))}
          {qualityReport?.blockingIssues.map((item) => (
            <li key={item.issueId}>{item.affectedTextRef}</li>
          ))}
        </ul>
      </section>
    </section>
  );
}

export function ConfigurationPage() {
  const {
    state,
    toggleModelProfile,
    updateQualityGateProfile,
    updateAgentAssignment,
    updatePromptVersion,
  } = usePhaseTwo();
  const snapshot = state.configurationSnapshot;
  const project = state.projects[0];
  const writingRun = state.writingRuns[0];
  const providerCalls = state.providerCallsByWriting?.[writingRun?.writingRunId ?? ""] ?? [];
  const writerProfile = snapshot.modelProfiles.find((item) => item.modelProfileId === DEFAULT_MODEL_PROFILE_ID);
  const fallbackProfile = snapshot.modelProfiles.find((item) => item.modelProfileId === STRUCTURED_FALLBACK_MODEL_PROFILE_ID);
  const rankingSnapshot = (state.rankingSnapshots ?? []).find((item) => item.rankingType === "prompt");

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>配置中心</h2>
        <p>查看模型路由、Agent 分配、质量阈值、提示版本、调用指标与配置审计。</p>
      </div>
      <section style={{ border: "1px solid #d4d4d8", padding: 16, display: "grid", gap: 12 }}>
        <h3>模型 Profile</h3>
        <ul style={{ display: "grid", gap: 12, listStyle: "none", padding: 0 }}>
          {snapshot.modelProfiles.map((profile) => (
            <li key={profile.modelProfileId} style={{ border: "1px solid #e4e4e7", padding: 12 }}>
              <strong>{profile.label}</strong>
              <p>{profile.providerName} · {profile.providerModelName}</p>
              <p>{profile.enabled ? "已启用" : "已禁用"} · {profile.supportsStructuredOutput ? "支持结构化输出" : "不支持结构化输出"}</p>
              <p>fallback_profile_ids：{profile.fallbackProfileIds.join("、") || "空"}</p>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <button type="button" onClick={() => toggleModelProfile(profile.modelProfileId, true)}>启用</button>
                <button type="button" onClick={() => toggleModelProfile(profile.modelProfileId, false)}>禁用</button>
              </div>
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>Agent 分配</h3>
        <ul>
          {snapshot.agentModelAssignments.map((assignment) => (
            <li key={assignment.assignmentId}>
              {assignment.agentRole} · {assignment.outputMode} · {assignment.modelProfileId} · max_retry {assignment.maxRetry} · max_cost {assignment.maxCost}
              {assignment.agentRole === "writer" ? (
                <button type="button" style={{ marginLeft: 8 }} onClick={() => updateAgentAssignment(assignment.assignmentId, STRUCTURED_FALLBACK_MODEL_PROFILE_ID)}>
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
          {snapshot.qualityGateProfiles.map((profile) => (
            <li key={profile.qualityGateProfileId}>
              {profile.label} · AI 味阈值 {profile.aiFlavorThreshold} · 原创安全阈值 {profile.originalitySafetyThreshold}
              <button type="button" style={{ marginLeft: 8 }} onClick={() => updateQualityGateProfile(profile.qualityGateProfileId, 0.4, 0.9)}>
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
          {snapshot.promptVersions.map((item) => (
            <li key={`${item.agentRole}-${item.templateRef}`}>
              {item.agentRole} · {item.templateRef}
              {item.agentRole === "writer" ? (
                <button type="button" style={{ marginLeft: 8 }} onClick={() => updatePromptVersion(item.agentRole, "prompt://writer/chapter-compact") }>
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
          {(rankingSnapshot?.suggestions ?? []).map((item) => (
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
              {call.agentRole} · {call.modelProfileId} · token {call.promptTokens}/{call.completionTokens} · latency {call.latencyMs}ms · retry {call.retryCount} · cost {call.costEstimate} · {call.status}{call.errorCode ? ` · ${call.errorCode}` : ""}
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
          默认 profile {writerProfile?.enabled ? "可用" : "已关闭"}，critic 结构化输出走 {STRUCTURED_FALLBACK_MODEL_PROFILE_ID}。
          默认 profile 关闭时，writer / humanizer 改走 {fallbackProfile?.enabled ? STRUCTURED_FALLBACK_MODEL_PROFILE_ID : "无可用 fallback"}。
        </p>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>配置变更记录</h3>
        <ul>
          {state.configurationMutations.map((item) => (
            <li key={item.mutationId}>
              {item.mutationType} · {item.summary} · {item.traceId}
            </li>
          ))}
        </ul>
      </section>
      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>配置审计轨迹</h3>
        <ul>
          {state.auditEvents
            .filter((item) => item.action.startsWith("configuration."))
            .map((item) => (
              <li key={item.auditEventId}>
                {item.action} · {item.summary} · {item.requestId}
              </li>
            ))}
        </ul>
      </section>
    </section>
  );
}
