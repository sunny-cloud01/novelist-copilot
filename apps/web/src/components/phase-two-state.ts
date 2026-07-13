export type ReviewAction = "approve" | "reject" | "merge_alias" | "request_reextract";
export type WritingReviewAction =
  | "accept_section"
  | "accept_chapter"
  | "request_rewrite"
  | "edit_and_accept"
  | "block_generation"
  | "approve_draft"
  | "request_revision"
  | "reject_draft"
  | "edit_draft"
  | "mark_issue_resolved"
  | "create_rule_update_request";

export type KnowledgeObject = {
  objectId: string;
  objectType: string;
  canonicalName: string;
  confidence: number;
  reviewStatus: string;
  lifecycleStatus: string;
  aliases: string[];
  mergedInto?: string;
};

export type ExtractionRunState = {
  runId: string;
  taskId: string;
  status: string;
  currentStage: string;
  chapterCount: number;
  sceneCount: number;
  objectCount: number;
  evidenceCount: number;
  lowConfidenceCount: number;
  errors: string[];
};

export type SourceBookState = {
  bookId: string;
  workspaceId: string;
  title: string;
  authorName: string;
  sourceType: string;
  importStatus: string;
  traceId: string;
};

export type SourceChapterState = {
  chapterId: string;
  chapterIndex: number;
  title: string;
  segmentationStatus: string;
};

export type GraphNodeState = {
  nodeId: string;
  label: string;
  nodeType: string;
  evidenceRefs: string[];
};

export type GraphNodeDetailState = {
  nodeId: string;
  bookId: string;
  label: string;
  nodeType: string;
  canonicalObjectId: string;
  reviewStatus: string;
  lifecycleStatus: string;
  confidence: number;
  aliases: string[];
  summary: string;
  evidenceRefs: string[];
};

export type GraphNeighborState = {
  edgeId: string;
  relationType: string;
  direction: "incoming" | "outgoing";
  neighborNodeId: string;
  neighborLabel: string;
  neighborType: string;
  confidence: number;
  evidenceRefs: string[];
};

export type NovelProjectState = {
  projectId: string;
  workspaceId: string;
  title: string;
  genreScope: string;
  status: string;
  storyBibleId: string;
  qualityGateProfileId: string;
  allowedKnowledgeSourceRefs: string[];
};

export type StoryBibleState = {
  storyBibleId: string;
  projectId: string;
  version: number;
  status: string;
  premise: string;
  protagonist: string;
  coreConflict: string;
  styleTarget: string;
  forbiddenSimilarities: string;
  worldRules: string[];
  narrativePromises: string[];
  confirmedPayload?: {
    premise?: string;
    protagonist?: string;
    core_conflict?: string;
    style_target?: string;
    forbidden_similarities?: string;
    world_rules?: string[];
    narrative_promises?: string[];
  } | null;
  diff: {
    fromVersion?: number | null;
    toVersion?: number;
    summary?: string;
    changedFields?: string[];
  } | null;
  history: Array<{
    version: number;
    status: string;
    changeType: string;
    summary?: string;
    note?: string | null;
    createdAt?: string;
  }>;
  approvedAt?: string | null;
  approvedBy?: string | null;
  traceId: string;
};

export type ChapterPlanState = {
  chapterPlanId: string;
  projectId: string;
  chapterIndex: number;
  status: string;
  targetWordCount: number;
  title: string;
  summary: string;
  selectedPatternId: string | null;
  selectedRhythmProfileId: string | null;
  selectedAssetIds: string[];
};

export type SectionBeatState = {
  index: number;
  summary: string;
};

export type SectionPlanState = {
  sectionPlanId: string;
  chapterPlanId: string;
  sectionIndex: number;
  planningRole: string;
  sceneGoal: string;
  beats: SectionBeatState[];
};

export type SectionRunBeatState = {
  index: number;
  status: string;
};

export type CriticIssueState = {
  issueId: string;
  severity: string;
  category: string;
  summary: string;
  affectedTextRef: string;
};

export type SectionRunState = {
  sectionRunId: string;
  writingRunId: string;
  sectionPlanId: string;
  status: string;
  draftObjectRef: string;
  criticReportRef: string;
  humanizedObjectRef: string;
  modelProfileId: string;
  beatStatus: SectionRunBeatState[];
  writerOutput: string;
  criticIssues: CriticIssueState[];
  humanizedText: string;
};

export type MemoryPackageState = {
  memoryPackageId: string;
  writingRunId: string;
  summary: string;
  sourceRefs: string[];
};

export type PromptPackageState = {
  promptPackageId: string;
  writingRunId: string;
  summary: string;
  templateRefs: string[];
};

export type ConsistencyIssueState = {
  issueId: string;
  category: string;
  severity: string;
  summary: string;
  affectedTextRef: string;
  ruleId: string;
  resolutionStatus: string;
  inputRefs: string[];
  outputRefs: string[];
  note: string | null;
};

export type QualityIssueState = ConsistencyIssueState;

export type QualityReportState = {
  qualityReportId: string;
  writingRunId: string;
  status: string;
  aiFlavorScore: number;
  mobileReadabilityScore: number;
  originalitySafetyScore: number;
  humanReviewRequired: boolean;
  blockingIssues: QualityIssueState[];
};

export type ConsistencyReportState = {
  consistencyReportId: string;
  writingRunId: string;
  status: string;
  issueCount: number;
  blockingIssueCount: number;
  checkedDomains: string[];
  issues: ConsistencyIssueState[];
};

export type RevisionSummaryState = {
  revisionSummaryId: string;
  writingRunId: string;
  status: string;
  revisionRound: number;
  maxRevisionRounds: number;
  sourceIssueIds: string[];
  changeSummary: string;
  reviewerNoteRef: string | null;
};

export type RuleProfileState = {
  ruleId: string;
  ruleType: string;
  title: string;
  severity: string;
  status: string;
  scopeType: string;
  scopeRef: string;
  description: string;
  conditionSummary: string;
  autoBlock: boolean;
};

export type PatternState = {
  patternId: string;
  canonicalName: string;
  patternType: string;
  status: string;
  intent: string;
  preconditions: string[];
  steps: SectionBeatState[];
  slots: string[];
  expectedReaderEffect: string;
  compatibleRhythmProfileId: string | null;
};

export type RhythmProfileState = {
  rhythmProfileId: string;
  targetId: string;
  status: string;
  label: string;
  climaxIndex: number;
  conflictIndex: number;
  dialogueRatio: number;
  descriptionRatio: number;
  battleRatio: number;
  informationDensity: number;
  suspenseIndex: number;
  rewardCount: number;
  emotionCurve: Array<{ beat: number; intensity: number; summary: string }>;
};

export type AssetState = {
  assetId: string;
  assetType: string;
  canonicalName: string;
  status: string;
  contentSummary: string;
  styleTags: string[];
  genreScope: string;
  usageContext: string;
  constraints: string[];
  expressionTypeRefs: string[];
  qualityScore: number;
};

export type FeedbackRecordState = {
  feedbackRecordId: string;
  workspaceId: string;
  targetType: string;
  targetId: string;
  feedbackType: string;
  score: number;
  source: string;
  commentRef: string | null;
  payload: Record<string, string | number | boolean | null>;
};

export type RankingSignalState = {
  signalId: string;
  rankingType: string;
  targetType: string;
  targetId: string;
  signalType: string;
  score: number;
  weight: number;
  source: string;
  sourceFeedbackRecordId: string | null;
  summary: string;
  evidenceRefs: string[];
};

export type RankingSuggestionState = {
  suggestionId: string;
  rankingType: string;
  targetScope: string;
  status: string;
  summary: string;
  recommendedAction: string;
  sourceSignalIds: string[];
  promotedFromFeedbackRecordId: string | null;
  promotedAt: string | null;
};

export type RankingSnapshotItemState = {
  rank: number;
  targetType: string;
  targetId: string;
  label: string;
  score: number;
  status: string;
  signalIds: string[];
  summary: string | null;
};

export type RankingSnapshotState = {
  rankingSnapshotId: string;
  rankingType: string;
  scopeRef: string;
  version: number;
  updatedAt: string;
  items: RankingSnapshotItemState[];
  signals: RankingSignalState[];
  suggestions: RankingSuggestionState[];
};

export type ModelCostState = {
  inputTokens: number;
  outputTokens: number;
  estimatedTotalCost: number;
  retryCount: number;
  writerInputTokens: number;
  writerOutputTokens: number;
  criticInputTokens: number;
  criticOutputTokens: number;
  humanizerInputTokens: number;
  humanizerOutputTokens: number;
};

export type ChapterSnapshotState = {
  chapterSnapshotId: string;
  writingRunId: string;
  projectId: string;
  chapterPlanId: string;
  acceptedChapterRef: string;
  chapterTitle: string;
  chapterText: string;
  sourceSectionRefs: string[];
  createdAt: string;
};

export type CharacterDynamicStateItem = {
  characterName: string;
  stateSummary: string;
};

export type RelationshipStateItem = {
  subject: string;
  object: string;
  stateSummary: string;
};

export type HookStateItem = {
  hookKey: string;
  status: string;
  summary: string;
};

export type PriorSummaryStateItem = {
  summaryIndex: number;
  summary: string;
};

export type ManuscriptStateState = {
  manuscriptStateId: string;
  projectId: string;
  writingRunId: string;
  currentStoryState: {
    summary: string;
    acceptedChapterRef: string;
    qualityGateStatus: string;
  };
  characterDynamicState: CharacterDynamicStateItem[];
  relationshipState: RelationshipStateItem[];
  hookState: HookStateItem[];
  priorSummaryPack: PriorSummaryStateItem[];
  updatedAt: string;
};

export type ModelProfileState = {
  modelProfileId: string;
  providerName: string;
  providerModelName: string;
  label: string;
  description: string | null;
  enabled: boolean;
  supportsStructuredOutput: boolean;
  fallbackProfileIds: string[];
};

export type AgentModelAssignmentState = {
  assignmentId: string;
  agentRole: string;
  taskType: string;
  outputMode: string;
  modelProfileId: string;
  fallbackProfileIds: string[];
  maxRetry: number;
  maxCost: number;
  enabled: boolean;
};

export type ProviderCallState = {
  providerCallId: string;
  agentRole: string;
  modelProfileId: string;
  providerName: string;
  promptTokens: number;
  completionTokens: number;
  latencyMs: number;
  retryCount: number;
  costEstimate: number;
  status: string;
  errorCode: string | null;
};

export type QualityGateProfileSummaryState = {
  qualityGateProfileId: string;
  label: string;
  aiFlavorThreshold: number;
  originalitySafetyThreshold: number;
};

export type PromptVersionState = {
  agentRole: string;
  templateRef: string;
};

export type AuditEventState = {
  auditEventId: string;
  workspaceId: string;
  action: string;
  actorId: string;
  actorRole: string;
  targetType: string;
  targetId: string;
  traceId: string;
  requestId: string;
  createdAt: string;
  summary: string;
  inputRefs: string[];
  outputRefs: string[];
};

export type AgentTaskEventState = {
  eventId: string;
  taskId: string;
  eventType: string;
  status: string;
  summary: string;
  createdAt: string;
};

export type AgentTaskState = {
  taskId: string;
  workspaceId: string;
  taskType: string;
  status: string;
  actorId: string;
  actorRole: string;
  targetRef: string;
  traceId: string;
  requestId: string;
  createdAt: string;
  updatedAt: string;
  summary: string;
  events: AgentTaskEventState[];
};

export type StrategySuggestionState = {
  suggestionId: string;
  basedOnFeedbackRecordId: string;
  status: string;
  targetScope: string;
  summary: string;
  promotedAt: string | null;
};

export type ConfigurationMutationState = {
  mutationId: string;
  mutationType: string;
  targetId: string;
  actorId: string;
  actorRole: string;
  status: string;
  requestId: string;
  traceId: string;
  createdAt: string;
  summary: string;
};

export type ConfigurationSnapshotState = {
  defaultModelProfileId: string;
  modelProfiles: ModelProfileState[];
  agentModelAssignments: AgentModelAssignmentState[];
  qualityGateProfiles: QualityGateProfileSummaryState[];
  promptVersions: PromptVersionState[];
};

export type WorkspaceState = {
  workspaceId: string;
  ownerUserId: string;
  name: string;
  slug: string;
  defaultLanguage: string;
  status: string;
};

export type WorkspaceMemberState = {
  workspaceMemberId: string;
  workspaceId: string;
  userId: string;
  role: string;
  status: string;
};

export type WorkspaceHomeTaskState = {
  taskId: string;
  taskType: string;
  status: string;
  summary: string;
  updatedAt: string;
  targetRef: string | null;
};

export type WorkspaceHomeReviewState = {
  reviewId: string;
  reviewType: string;
  status: string;
  title: string;
  targetRef: string;
};

export type WorkspaceHomeQuickLinkState = {
  label: string;
  route: string;
  resourceRef: string;
};

export type WorkspaceHomeState = {
  workspaceId: string;
  recentTasks: WorkspaceHomeTaskState[];
  pendingReviews: WorkspaceHomeReviewState[];
  quickLinks: WorkspaceHomeQuickLinkState[];
};

export type WritingRunState = {
  writingRunId: string;
  projectId: string;
  chapterPlanId: string;
  status: string;
  currentStage: string;
  taskId: string;
  memoryPackageId: string;
  promptPackageId: string;
  chapterDraftId: string;
  qualityReportId: string;
  consistencyReportId: string;
  revisionSummaryId: string;
  traceId: string;
  writerModelProfileId: string;
  criticModelProfileId: string;
  humanizerModelProfileId: string;
  assembledChapter: string;
  modelCost: ModelCostState;
  revisionRound: number;
  maxRevisionRounds: number;
  acceptedIntoManuscriptAt: string | null;
  acceptedChapterRef: string | null;
  chapterSnapshotId: string | null;
  manuscriptStateId: string | null;
  chapterSnapshot: ChapterSnapshotState | null;
  manuscriptState: ManuscriptStateState | null;
  consistencyReport: ConsistencyReportState | null;
  revisionSummary: RevisionSummaryState | null;
  selectedPatternId: string | null;
  selectedRhythmProfileId: string | null;
  selectedAssetIds: string[];
};

export type EvidenceState = {
  evidenceId: string;
  bookId: string;
  chapterId: string;
  chapterIndex: number;
  textRange: string;
  excerpt: string;
  sourceObjectRefs: string[];
  confidence: number;
  traceId: string;
};

export type ChapterAnalysisState = {
  chapterId: string;
  chapterIndex: number;
  title: string;
  sceneCount: number;
  eventCount: number;
  conflictIndex: number;
  suspenseIndex: number;
  rewardCount: number;
  evidenceCoverage: number;
  needsAttentionCount: number;
};

export type BookAnalysisSummaryState = {
  bookId: string;
  runId: string;
  status: string;
  currentStage: string;
  chapterCount: number;
  sceneCount: number;
  knowledgeObjectCount: number;
  evidenceCount: number;
  patternCount: number;
  rhythmProfileCount: number;
  assetCount: number;
  ruleCount: number;
  needsAttentionCount: number;
  canCommitKnowledge: boolean;
};

export type AnalysisExceptionState = {
  exceptionId: string;
  type: string;
  severity: string;
  title: string;
  summary: string;
  targetRef: string;
  evidenceRefs: string[];
  recommendedAction: string;
};

export type PhaseTwoState = {
  workspace: WorkspaceState;
  workspaceMembers: WorkspaceMemberState[];
  workspaceHome: WorkspaceHomeState;
  book: SourceBookState;
  chapters: SourceChapterState[];
  run: ExtractionRunState;
  evidences: EvidenceState[];
  chapterAnalysis: ChapterAnalysisState[];
  bookAnalysisSummary: BookAnalysisSummaryState;
  analysisExceptions: AnalysisExceptionState[];
  knowledgeObjects: KnowledgeObject[];
  graphNodes: GraphNodeState[];
  graphNodeDetails: Record<string, GraphNodeDetailState>;
  graphNeighborsByNode: Record<string, GraphNeighborState[]>;
  projects: NovelProjectState[];
  storyBibles: StoryBibleState[];
  chapterPlans: ChapterPlanState[];
  sectionPlansByChapter: Record<string, SectionPlanState[]>;
  writingRuns: WritingRunState[];
  sectionRunsByWriting: Record<string, SectionRunState[]>;
  memoryPackages: MemoryPackageState[];
  promptPackages: PromptPackageState[];
  qualityReports: QualityReportState[];
  consistencyReports: ConsistencyReportState[];
  revisionSummaries: RevisionSummaryState[];
  rules: RuleProfileState[];
  patterns: PatternState[];
  rhythmProfiles: RhythmProfileState[];
  assets: AssetState[];
  feedbackRecords: FeedbackRecordState[];
  rankingSnapshots: RankingSnapshotState[];
  strategySuggestions: StrategySuggestionState[];
  configurationSnapshot: ConfigurationSnapshotState;
  configurationMutations: ConfigurationMutationState[];
  agentTasks: AgentTaskState[];
  auditEvents: AuditEventState[];
  providerCallsByWriting: Record<string, ProviderCallState[]>;
  activityLog: string[];
};

export const DEMO_BOOK_ID = "01JZBOOK000000000000000001";
export const DEMO_RUN_ID = "01JZRUN0000000000000000001";
export const DEMO_WORKSPACE_ID = "demo-workspace";
export const DEMO_PROJECT_ID = "01JZPROJECT000000000000001";
export const DEMO_CHAPTER_PLAN_ID = "01JZCHPLAN000000000000001";
export const DEMO_WRITING_RUN_ID = "01JZWRITING00000000000001";
export const DEFAULT_MODEL_PROFILE_ID = "model_profile_default";
export const STRUCTURED_FALLBACK_MODEL_PROFILE_ID = "model_profile_structured_fallback";

const reviewActionLabels: Record<ReviewAction, string> = {
  approve: "通过",
  reject: "驳回",
  merge_alias: "合并别名",
  request_reextract: "请求重抽",
};

const writingReviewActionLabels: Record<WritingReviewAction, string> = {
  accept_section: "接受本节",
  accept_chapter: "接受本章",
  request_rewrite: "请求重写",
  edit_and_accept: "编辑后接受",
  block_generation: "阻止继续生成",
  approve_draft: "批准草稿",
  request_revision: "请求修订",
  reject_draft: "驳回草稿",
  edit_draft: "编辑草稿",
  mark_issue_resolved: "标记问题已解决",
  create_rule_update_request: "创建规则更新请求",
};

export function createInitialPhaseTwoState(): PhaseTwoState {
  return {
    workspace: {
      workspaceId: DEMO_WORKSPACE_ID,
      ownerUserId: "demo-user",
      name: "默认中文工作区",
      slug: DEMO_WORKSPACE_ID,
      defaultLanguage: "zh-CN",
      status: "active",
    },
    workspaceMembers: [
      {
        workspaceMemberId: "demo-workspace-member",
        workspaceId: DEMO_WORKSPACE_ID,
        userId: "demo-user",
        role: "owner",
        status: "active",
      },
    ],
    workspaceHome: {
      workspaceId: DEMO_WORKSPACE_ID,
      recentTasks: [
        {
          taskId: "01JZWRITETASK0000000000001",
          taskType: "create_writing_run",
          status: "requires_review",
          summary: "写作任务进入人工复核。",
          updatedAt: "2026-07-11T03:05:00Z",
          targetRef: "object://writing-runs/01JZWRITING00000000000001",
        },
        {
          taskId: "01JZPLANTASK0000000000001",
          taskType: "create_chapter_plan",
          status: "requires_review",
          summary: "章节规划已生成，等待确认。",
          updatedAt: "2026-07-11T02:12:00Z",
          targetRef: "object://chapter-plans/01JZCHPLAN000000000000001",
        },
        {
          taskId: "01JZTASK000000000000000001",
          taskType: "extract_knowledge",
          status: "requires_review",
          summary: "确定性抽取结果仍有低置信对象待处理。",
          updatedAt: "2026-07-11T00:01:00Z",
          targetRef: "object://extraction-runs/01JZRUN0000000000000000001",
        },
      ],
      pendingReviews: [
        {
          reviewId: "01JZOBJ0000000000000000002",
          reviewType: "knowledge_object",
          status: "pending",
          title: "Yao Lao 待知识审核",
          targetRef: "object://knowledge-objects/01JZOBJ0000000000000000002",
        },
        {
          reviewId: "01JZSECRUN00000000000002",
          reviewType: "section_run",
          status: "rewrite_required",
          title: "第二节仍需补足压迫递进",
          targetRef: "object://section-runs/01JZSECRUN00000000000002",
        },
      ],
      quickLinks: [
        { label: "进入来源书库", route: "/sources", resourceRef: "object://source-books/01JZBOOK000000000000000001" },
        { label: "进入写作工作台", route: "/projects/demo-project/writing/demo-run", resourceRef: "object://writing-runs/01JZWRITING00000000000001" },
        { label: "进入配置中心", route: "/configuration", resourceRef: "object://configuration/default" },
      ],
    },
    book: {
      bookId: DEMO_BOOK_ID,
      workspaceId: DEMO_WORKSPACE_ID,
      title: "Battle Through the Heavens",
      authorName: "Tian Can Tu Dou",
      sourceType: "reference_novel",
      importStatus: "ready",
      traceId: "01JZTRC000000000000000001",
    },
    chapters: [
      {
        chapterId: "01JZCHAPTER00000000000001",
        chapterIndex: 1,
        title: "Three-Year Agreement",
        segmentationStatus: "segmented",
      },
      {
        chapterId: "01JZCHAPTER00000000000002",
        chapterIndex: 2,
        title: "Yao Lao Appears",
        segmentationStatus: "segmented",
      },
    ],
    run: {
      runId: DEMO_RUN_ID,
      taskId: "01JZTASK000000000000000001",
      status: "requires_review",
      currentStage: "quality_review",
      chapterCount: 2,
      sceneCount: 6,
      objectCount: 3,
      evidenceCount: 3,
      lowConfidenceCount: 2,
      errors: [],
    },
    evidences: [
      {
        evidenceId: "evidence://01JZEVIDENCE0000000000001",
        bookId: DEMO_BOOK_ID,
        chapterId: "01JZCHAPTER0000000000001",
        chapterIndex: 1,
        textRange: "c1:p12-p14",
        excerpt: "萧炎沉默地站在大厅中央，所有目光都落在他身上，少年把羞辱压进喉间。",
        sourceObjectRefs: ["object://knowledge-objects/01JZOBJ0000000000000000001"],
        confidence: 0.82,
        traceId: "01JZTRC000000000000000001",
      },
      {
        evidenceId: "evidence://01JZEVIDENCE0000000000002",
        bookId: DEMO_BOOK_ID,
        chapterId: "01JZCHAPTER0000000000002",
        chapterIndex: 2,
        textRange: "c2:p4-p8",
        excerpt: "戒指中传来苍老的低笑，药老第一次点破少年体内异变的根源。",
        sourceObjectRefs: ["object://knowledge-objects/01JZOBJ0000000000000000002"],
        confidence: 0.76,
        traceId: "01JZTRC000000000000000001",
      },
      {
        evidenceId: "evidence://01JZEVIDENCE0000000000003",
        bookId: DEMO_BOOK_ID,
        chapterId: "01JZCHAPTER0000000000001",
        chapterIndex: 1,
        textRange: "c1:p1-p3",
        excerpt: "乌坦城萧家大厅气氛压抑，族人窃语让家族压力成为本章底色。",
        sourceObjectRefs: ["object://knowledge-objects/01JZOBJ0000000000000000003"],
        confidence: 0.91,
        traceId: "01JZTRC000000000000000001",
      },
    ],
    chapterAnalysis: [
      {
        chapterId: "01JZCHAPTER0000000000001",
        chapterIndex: 1,
        title: "The Fallen Genius",
        sceneCount: 3,
        eventCount: 5,
        conflictIndex: 0.78,
        suspenseIndex: 0.62,
        rewardCount: 1,
        evidenceCoverage: 0.86,
        needsAttentionCount: 1,
      },
      {
        chapterId: "01JZCHAPTER0000000000002",
        chapterIndex: 2,
        title: "Yao Lao Appears",
        sceneCount: 3,
        eventCount: 4,
        conflictIndex: 0.66,
        suspenseIndex: 0.82,
        rewardCount: 2,
        evidenceCoverage: 0.74,
        needsAttentionCount: 1,
      },
    ],
    bookAnalysisSummary: {
      bookId: DEMO_BOOK_ID,
      runId: DEMO_RUN_ID,
      status: "requires_review",
      currentStage: "quality_review",
      chapterCount: 2,
      sceneCount: 6,
      knowledgeObjectCount: 3,
      evidenceCount: 3,
      patternCount: 1,
      rhythmProfileCount: 1,
      assetCount: 1,
      ruleCount: 1,
      needsAttentionCount: 2,
      canCommitKnowledge: true,
    },
    analysisExceptions: [
      {
        exceptionId: "analysis-exception-low-confidence-xiao-yan",
        type: "low_confidence_object",
        severity: "warning",
        title: "角色身份置信度偏低",
        summary: "Xiao Yan 的别名与章节证据需要确认后再进入知识包。",
        targetRef: "object://knowledge-objects/01JZOBJ0000000000000000001",
        evidenceRefs: ["evidence://01JZEVIDENCE0000000000001"],
        recommendedAction: "approve_or_merge_alias",
      },
      {
        exceptionId: "analysis-exception-low-confidence-yao-lao",
        type: "low_confidence_object",
        severity: "warning",
        title: "导师对象需要确认",
        summary: "Yao Lao 首次出现证据充分，但命名归一化仍需人工确认。",
        targetRef: "object://knowledge-objects/01JZOBJ0000000000000000002",
        evidenceRefs: ["evidence://01JZEVIDENCE0000000000002"],
        recommendedAction: "approve_or_reextract",
      },
    ],
    knowledgeObjects: [
      {
        objectId: "01JZOBJ0000000000000000001",
        objectType: "character",
        canonicalName: "Xiao Yan",
        confidence: 0.58,
        reviewStatus: "pending",
        lifecycleStatus: "candidate",
        aliases: ["Yan"],
      },
      {
        objectId: "01JZOBJ0000000000000000002",
        objectType: "mentor",
        canonicalName: "Yao Lao",
        confidence: 0.44,
        reviewStatus: "pending",
        lifecycleStatus: "candidate",
        aliases: ["Old Yao"],
      },
      {
        objectId: "01JZOBJ0000000000000000003",
        objectType: "clan",
        canonicalName: "Xiao Clan",
        confidence: 0.97,
        reviewStatus: "approved",
        lifecycleStatus: "approved",
        aliases: [],
      },
    ],
    graphNodes: [
      {
        nodeId: "01JZNODE000000000000000001",
        label: "Xiao Yan",
        nodeType: "character",
        evidenceRefs: ["evidence://01JZEVIDENCE0000000000001"],
      },
      {
        nodeId: "01JZNODE000000000000000002",
        label: "Yao Lao",
        nodeType: "mentor",
        evidenceRefs: ["evidence://01JZEVIDENCE0000000000002"],
      },
      {
        nodeId: "01JZNODE000000000000000003",
        label: "Xiao Clan",
        nodeType: "clan",
        evidenceRefs: ["evidence://01JZEVIDENCE0000000000003"],
      },
    ],
    graphNodeDetails: {
      "01JZNODE000000000000000001": {
        nodeId: "01JZNODE000000000000000001",
        bookId: DEMO_BOOK_ID,
        label: "Xiao Yan",
        nodeType: "character",
        canonicalObjectId: "01JZOBJ0000000000000000001",
        reviewStatus: "pending",
        lifecycleStatus: "candidate",
        confidence: 0.58,
        aliases: ["Yan"],
        summary: "乌坦城萧家少年，正处于天赋跌落后的低谷期。",
        evidenceRefs: ["evidence://01JZEVIDENCE0000000000001"],
      },
      "01JZNODE000000000000000002": {
        nodeId: "01JZNODE000000000000000002",
        bookId: DEMO_BOOK_ID,
        label: "Yao Lao",
        nodeType: "mentor",
        canonicalObjectId: "01JZOBJ0000000000000000002",
        reviewStatus: "pending",
        lifecycleStatus: "candidate",
        confidence: 0.44,
        aliases: ["Old Yao"],
        summary: "寄宿戒指中的神秘导师，对主角成长线至关重要。",
        evidenceRefs: ["evidence://01JZEVIDENCE0000000000002"],
      },
      "01JZNODE000000000000000003": {
        nodeId: "01JZNODE000000000000000003",
        bookId: DEMO_BOOK_ID,
        label: "Xiao Clan",
        nodeType: "clan",
        canonicalObjectId: "01JZOBJ0000000000000000003",
        reviewStatus: "approved",
        lifecycleStatus: "approved",
        confidence: 0.97,
        aliases: [],
        summary: "乌坦城本地家族势力，也是主角当前承受压力的核心环境。",
        evidenceRefs: ["evidence://01JZEVIDENCE0000000000003"],
      },
    },
    graphNeighborsByNode: {
      "01JZNODE000000000000000001": [
        {
          edgeId: "01JZEDGE000000000000000001",
          relationType: "mentored_by",
          direction: "outgoing",
          neighborNodeId: "01JZNODE000000000000000002",
          neighborLabel: "Yao Lao",
          neighborType: "mentor",
          confidence: 0.91,
          evidenceRefs: ["evidence://01JZEVIDENCE0000000000002"],
        },
        {
          edgeId: "01JZEDGE000000000000000002",
          relationType: "member_of",
          direction: "outgoing",
          neighborNodeId: "01JZNODE000000000000000003",
          neighborLabel: "Xiao Clan",
          neighborType: "clan",
          confidence: 0.96,
          evidenceRefs: ["evidence://01JZEVIDENCE0000000000003"],
        },
      ],
      "01JZNODE000000000000000002": [
        {
          edgeId: "01JZEDGE000000000000000001",
          relationType: "mentors",
          direction: "incoming",
          neighborNodeId: "01JZNODE000000000000000001",
          neighborLabel: "Xiao Yan",
          neighborType: "character",
          confidence: 0.91,
          evidenceRefs: ["evidence://01JZEVIDENCE0000000000002"],
        },
      ],
      "01JZNODE000000000000000003": [
        {
          edgeId: "01JZEDGE000000000000000002",
          relationType: "has_member",
          direction: "incoming",
          neighborNodeId: "01JZNODE000000000000000001",
          neighborLabel: "Xiao Yan",
          neighborType: "character",
          confidence: 0.96,
          evidenceRefs: ["evidence://01JZEVIDENCE0000000000003"],
        },
      ],
    },
    projects: [
      {
        projectId: DEMO_PROJECT_ID,
        workspaceId: DEMO_WORKSPACE_ID,
        title: "斗破苍穹衍生原创",
        genreScope: "玄幻升级流",
        status: "planning",
        storyBibleId: "01JZBIBLE0000000000000001",
        qualityGateProfileId: "01JZQUALITY00000000000001",
        allowedKnowledgeSourceRefs: [
          "object://source-books/01JZBOOK000000000000000001",
          "object://graph-summaries/01JZBOOK000000000000000001",
        ],
      },
    ],
    storyBibles: [
      {
        storyBibleId: "01JZBIBLE0000000000000001",
        projectId: DEMO_PROJECT_ID,
        version: 1,
        status: "approved",
        premise: "少年背负退婚耻辱后，踏上逆袭与成长之路。",
        protagonist: "萧炎",
        coreConflict: "天赋跌落后的家族压力与三年之约。",
        styleTarget: "压强递进、成长兑现、情绪克制。",
        forbiddenSimilarities: "不复刻原作金手指机制与关键名场面。",
        worldRules: ["每次突破都需真实代价。"],
        narrativePromises: ["前三章完成受压、立誓、破局线索。"],
        confirmedPayload: {
          premise: "少年背负退婚耻辱后，踏上逆袭与成长之路。",
          protagonist: "萧炎",
          core_conflict: "天赋跌落后的家族压力与三年之约。",
          style_target: "压强递进、成长兑现、情绪克制。",
          forbidden_similarities: "不复刻原作金手指机制与关键名场面。",
          world_rules: ["每次突破都需真实代价。"],
          narrative_promises: ["前三章完成受压、立誓、破局线索。"],
        },
        diff: null,
        history: [
          {
            version: 1,
            status: "approved",
            changeType: "create",
            summary: "创建初始故事圣经。",
            createdAt: "2026-07-10T10:00:00Z",
          },
          {
            version: 1,
            status: "approved",
            changeType: "confirm",
            summary: "确认项目故事圣经。",
            createdAt: "2026-07-10T10:05:00Z",
          },
        ],
        approvedAt: "2026-07-10T10:05:00Z",
        approvedBy: "demo-user",
        traceId: "01JZTRC000000000000000002",
      },
    ],
    chapterPlans: [
      {
        chapterPlanId: DEMO_CHAPTER_PLAN_ID,
        projectId: DEMO_PROJECT_ID,
        chapterIndex: 1,
        status: "requires_review",
        targetWordCount: 3200,
        title: "乌坦城风起",
        summary: "主角在第一章完成进入主线前的势能铺垫。",
        selectedPatternId: "01JZPATTERN00000000000001",
        selectedRhythmProfileId: "01JZRHYTHM00000000000001",
        selectedAssetIds: ["01JZASSET000000000000001"],
      },
    ],
    sectionPlansByChapter: {
      [DEMO_CHAPTER_PLAN_ID]: [
        {
          sectionPlanId: "01JZSECT0000000000000001",
          chapterPlanId: DEMO_CHAPTER_PLAN_ID,
          sectionIndex: 1,
          planningRole: "setup",
          sceneGoal: "建立乌坦城压抑氛围",
          beats: [
            { index: 1, summary: "主角出场" },
            { index: 2, summary: "家族压力显现" },
          ],
        },
        {
          sectionPlanId: "01JZSECT0000000000000002",
          chapterPlanId: DEMO_CHAPTER_PLAN_ID,
          sectionIndex: 2,
          planningRole: "conflict",
          sceneGoal: "压强进一步落到主角身上",
          beats: [
            { index: 1, summary: "长辈对主角失望" },
            { index: 2, summary: "纳兰家消息传来" },
          ],
        },
        {
          sectionPlanId: "01JZSECT0000000000000003",
          chapterPlanId: DEMO_CHAPTER_PLAN_ID,
          sectionIndex: 3,
          planningRole: "turn",
          sceneGoal: "把侮辱转化为主线承诺",
          beats: [
            { index: 1, summary: "退婚现场升级" },
            { index: 2, summary: "主角立下三年之约" },
          ],
        },
      ],
    },
    writingRuns: [
      {
        writingRunId: DEMO_WRITING_RUN_ID,
        projectId: DEMO_PROJECT_ID,
        chapterPlanId: DEMO_CHAPTER_PLAN_ID,
        status: "requires_review",
        currentStage: "consistency_review",
        taskId: "01JZWRITETASK0000000000001",
        memoryPackageId: "01JZMEMPKG000000000000001",
        promptPackageId: "01JZPROMPTPKG000000000001",
        chapterDraftId: "01JZDRAFT0000000000000001",
        qualityReportId: "01JZQLTREP000000000000001",
        consistencyReportId: "01JZCONSIST00000000000001",
        revisionSummaryId: "01JZREVISION0000000000001",
        traceId: "01JZTRC000000000000000003",
        writerModelProfileId: DEFAULT_MODEL_PROFILE_ID,
        criticModelProfileId: STRUCTURED_FALLBACK_MODEL_PROFILE_ID,
        humanizerModelProfileId: DEFAULT_MODEL_PROFILE_ID,
        assembledChapter:
          "萧炎在家族议事厅外停步，先听见堂内压抑的议论，再踏入众人目光中心。纳兰家的退婚信像利刃一样落下，他在众目睽睽之下接住羞辱，也在心底立下三年之约。",
        modelCost: {
          inputTokens: 4980,
          outputTokens: 2310,
          estimatedTotalCost: 0.86,
          retryCount: 1,
          writerInputTokens: 1800,
          writerOutputTokens: 920,
          criticInputTokens: 1400,
          criticOutputTokens: 540,
          humanizerInputTokens: 1780,
          humanizerOutputTokens: 850,
        },
        revisionRound: 1,
        maxRevisionRounds: 3,
        acceptedIntoManuscriptAt: null,
        acceptedChapterRef: null,
        chapterSnapshotId: null,
        manuscriptStateId: null,
        chapterSnapshot: null,
        manuscriptState: null,
        consistencyReport: null,
        revisionSummary: null,
        selectedPatternId: "01JZPATTERN00000000000001",
        selectedRhythmProfileId: "01JZRHYTHM00000000000001",
        selectedAssetIds: ["01JZASSET000000000000001"],
      },
    ],
    sectionRunsByWriting: {
      [DEMO_WRITING_RUN_ID]: [
        {
          sectionRunId: "01JZSECRUN00000000000001",
          writingRunId: DEMO_WRITING_RUN_ID,
          sectionPlanId: "01JZSECT0000000000000001",
          status: "beat_approved",
          draftObjectRef: "object://drafts/01JZSECRUN00000000000001",
          criticReportRef: "object://critic-reports/01JZSECRUN00000000000001",
          humanizedObjectRef: "object://humanized/01JZSECRUN00000000000001",
          modelProfileId: DEFAULT_MODEL_PROFILE_ID,
          beatStatus: [
            { index: 1, status: "beat_approved" },
            { index: 2, status: "beat_approved" },
          ],
          writerOutput: "乌坦城天色未亮，萧炎已经听见议事堂传来的细碎争论。",
          criticIssues: [],
          humanizedText: "天还没亮透，议事堂里的争论已经顺着长廊飘到萧炎耳边。",
        },
        {
          sectionRunId: "01JZSECRUN00000000000002",
          writingRunId: DEMO_WRITING_RUN_ID,
          sectionPlanId: "01JZSECT0000000000000002",
          status: "rewrite_required",
          draftObjectRef: "object://drafts/01JZSECRUN00000000000002",
          criticReportRef: "object://critic-reports/01JZSECRUN00000000000002",
          humanizedObjectRef: "object://humanized/01JZSECRUN00000000000002",
          modelProfileId: DEFAULT_MODEL_PROFILE_ID,
          beatStatus: [
            { index: 1, status: "critic_review" },
            { index: 2, status: "rewrite_required" },
          ],
          writerOutput: "纳兰家的消息在厅内炸开，所有目光都压向萧炎。",
          criticIssues: [
            {
              issueId: "01JZCRTIC000000000000001",
              severity: "blocking",
              category: "character_consistency",
              summary: "主角情绪转折过快，缺少被压迫感铺垫。",
              affectedTextRef: "object://drafts/01JZSECRUN00000000000002#p1",
            },
          ],
          humanizedText: "纳兰家的来信一到，厅里的空气像骤然压低了一层，所有审视都落到萧炎身上。",
        },
        {
          sectionRunId: "01JZSECRUN00000000000003",
          writingRunId: DEMO_WRITING_RUN_ID,
          sectionPlanId: "01JZSECT0000000000000003",
          status: "humanizer_pass",
          draftObjectRef: "object://drafts/01JZSECRUN00000000000003",
          criticReportRef: "object://critic-reports/01JZSECRUN00000000000003",
          humanizedObjectRef: "object://humanized/01JZSECRUN00000000000003",
          modelProfileId: DEFAULT_MODEL_PROFILE_ID,
          beatStatus: [
            { index: 1, status: "humanizer_pass" },
            { index: 2, status: "humanizer_pass" },
          ],
          writerOutput: "萧炎当众抬头，把退婚羞辱化成三年之约。",
          criticIssues: [
            {
              issueId: "01JZCRTIC000000000000002",
              severity: "warning",
              category: "style",
              summary: "金手指暗示可再收敛，避免过早泄露。",
              affectedTextRef: "object://drafts/01JZSECRUN00000000000003#p1",
            },
          ],
          humanizedText: "他在众人的嘲讽里抬起头，把那封退婚信压回桌上，只留下一句三年后再见。",
        },
      ],
    },
    memoryPackages: [
      {
        memoryPackageId: "01JZMEMPKG000000000000001",
        writingRunId: DEMO_WRITING_RUN_ID,
        summary: "已汇总故事圣经、章节目标、人物状态与来源证据。",
        sourceRefs: [
          "object://story-bibles/01JZBIBLE0000000000000001",
          "object://chapter-plans/01JZCHPLAN000000000000001",
          "object://section-plans/01JZSECT0000000000000001",
          "object://graph-summaries/01JZBOOK000000000000000001",
        ],
      },
    ],
    promptPackages: [
      {
        promptPackageId: "01JZPROMPTPKG000000000001",
        writingRunId: DEMO_WRITING_RUN_ID,
        summary: "写手、批评者与润色器共用同一章级提示包。",
        templateRefs: [
          "prompt://writer/chapter-default",
          "prompt://critic/chapter-default",
          "prompt://humanizer/chapter-default",
        ],
      },
    ],
    qualityReports: [
      {
        qualityReportId: "01JZQLTREP000000000000001",
        writingRunId: DEMO_WRITING_RUN_ID,
        status: "blocked",
        aiFlavorScore: 0.34,
        mobileReadabilityScore: 0.82,
        originalitySafetyScore: 0.91,
        humanReviewRequired: true,
        blockingIssues: [
          {
            issueId: "01JZQLTISSUE000000000001",
            category: "power_system_constraint",
            severity: "high",
            summary: "第二节仍需补足压迫递进。",
            affectedTextRef: "object://drafts/01JZSECRUN00000000000002#p2",
            ruleId: "rule-01JZPOWER000000000000001",
            resolutionStatus: "open",
            inputRefs: ["object://rules/rule-01JZPOWER000000000000001"],
            outputRefs: ["object://quality-reports/01JZQLTREP000000000000001/issues/1"],
            note: null,
          },
        ],
      },
    ],
    consistencyReports: [
      {
        consistencyReportId: "01JZCONSIST00000000000001",
        writingRunId: DEMO_WRITING_RUN_ID,
        status: "blocked",
        issueCount: 1,
        blockingIssueCount: 1,
        checkedDomains: ["character_continuity", "power_system_constraint"],
        issues: [
          {
            issueId: "01JZCONSISTISSUE000000001",
            category: "power_system_constraint",
            severity: "critical",
            summary: "主角境界被写回斗之气三段，与已批准状态冲突。",
            affectedTextRef: "object://drafts/01JZSECRUN00000000000002#p2",
            ruleId: "rule-01JZPOWER000000000000001",
            resolutionStatus: "open",
            inputRefs: ["object://rules/rule-01JZPOWER000000000000001"],
            outputRefs: ["object://consistency-reports/01JZCONSIST00000000000001/issues/1"],
            note: null,
          },
        ],
      },
    ],
    revisionSummaries: [
      {
        revisionSummaryId: "01JZREVISION0000000000001",
        writingRunId: DEMO_WRITING_RUN_ID,
        status: "requested",
        revisionRound: 1,
        maxRevisionRounds: 3,
        sourceIssueIds: ["01JZCONSISTISSUE000000001"],
        changeSummary: "要求重写第二节，恢复主角当前境界并补足冲突升级。",
        reviewerNoteRef: "object://review-notes/01JZREVISION0000000000001",
      },
    ],
    rules: [
      {
        ruleId: "rule-01JZPOWER000000000000001",
        ruleType: "power_system_constraint",
        title: "境界不能倒退",
        severity: "critical",
        status: "approved",
        scopeType: "project",
        scopeRef: "project://01JZPROJECT000000000000001",
        description: "主角已批准境界状态不能在后续章节无原因倒退。",
        conditionSummary: "若当前 draft 中能力状态低于已批准状态，则触发阻断。",
        autoBlock: true,
      },
    ],
    patterns: [
      {
        patternId: "01JZPATTERN00000000000001",
        canonicalName: "退婚立誓",
        patternType: "conflict_escalation",
        status: "approved",
        intent: "用公开羞辱触发主角长期目标与情绪反弹。",
        preconditions: ["主角处于低谷", "公开场合发生身份压迫"],
        steps: [
          { index: 1, summary: "先压低主角处境" },
          { index: 2, summary: "让压迫升级到无法退让" },
          { index: 3, summary: "主角公开立誓，把羞辱转为主线目标" },
        ],
        slots: ["压迫者", "见证者", "誓约代价"],
        expectedReaderEffect: "先压后燃，形成升级流期待。",
        compatibleRhythmProfileId: "01JZRHYTHM00000000000001",
      },
    ],
    rhythmProfiles: [
      {
        rhythmProfileId: "01JZRHYTHM00000000000001",
        targetId: DEMO_CHAPTER_PLAN_ID,
        status: "approved",
        label: "退婚压迫三段式",
        climaxIndex: 0.86,
        conflictIndex: 0.78,
        dialogueRatio: 0.42,
        descriptionRatio: 0.28,
        battleRatio: 0,
        informationDensity: 0.65,
        suspenseIndex: 0.74,
        rewardCount: 2,
        emotionCurve: [
          { beat: 1, intensity: 0.35, summary: "压抑铺垫" },
          { beat: 2, intensity: 0.68, summary: "冲突加压" },
          { beat: 3, intensity: 0.92, summary: "立誓爆点" },
        ],
      },
    ],
    assets: [
      {
        assetId: "01JZASSET000000000000001",
        assetType: "expression",
        canonicalName: "三年之约宣言模板",
        status: "approved",
        contentSummary: "用于公开立誓场景的短句式资产。",
        styleTags: ["克制", "燃点前压"],
        genreScope: "玄幻升级流",
        usageContext: "公开羞辱后主角反击",
        constraints: ["避免过早泄露金手指", "句式不超过两行"],
        expressionTypeRefs: ["expression://oath-line"],
        qualityScore: 0.88,
      },
    ],
    feedbackRecords: [
      {
        feedbackRecordId: "01JZFDBK0000000000000001",
        workspaceId: DEMO_WORKSPACE_ID,
        targetType: "writing_run",
        targetId: DEMO_WRITING_RUN_ID,
        feedbackType: "quality",
        score: 0.82,
        source: "quality_gate",
        commentRef: "object://quality-comments/01JZFDBK0000000000000001",
        payload: {
          qualityReportId: "01JZQLTREP000000000000001",
          summary: "质量门禁通过后保留了节奏与可读性指标。",
        },
      },
      {
        feedbackRecordId: "01JZFDBK0000000000000002",
        workspaceId: DEMO_WORKSPACE_ID,
        targetType: "quality_report",
        targetId: "01JZQLTREP000000000000001",
        feedbackType: "style",
        score: 0.64,
        source: "critic",
        commentRef: "object://critic-comments/01JZFDBK0000000000000002",
        payload: {
          affectedTextRef: "object://drafts/01JZSECRUN00000000000003#p1",
          summary: "金手指暗示仍偏早，可继续收敛。",
        },
      },
    ],
    rankingSnapshots: [
      {
        rankingSnapshotId: "01JZRANKSNAP0000000000001",
        rankingType: "prompt",
        scopeRef: `object://writing-runs/${DEMO_WRITING_RUN_ID}`,
        version: 1,
        updatedAt: "2026-07-12T01:34:00Z",
        items: [
          {
            rank: 1,
            targetType: "prompt_version",
            targetId: "prompt://writer/chapter-default",
            label: "writer 默认提示",
            score: 0.83,
            status: "leading",
            signalIds: ["01JZRANKSIG00000000000001"],
            summary: "质量稳定，但风格线索仍偏显性。",
          },
          {
            rank: 2,
            targetType: "prompt_version",
            targetId: "prompt://writer/chapter-compact",
            label: "writer 紧凑提示",
            score: 0.76,
            status: "watch",
            signalIds: ["01JZRANKSIG00000000000002"],
            summary: "可作为下一轮收紧表达候选。",
          },
        ],
        signals: [
          {
            signalId: "01JZRANKSIG00000000000001",
            rankingType: "prompt",
            targetType: "prompt_version",
            targetId: "prompt://writer/chapter-default",
            signalType: "prompt_effectiveness",
            score: 0.87,
            weight: 0.7,
            source: "quality_gate",
            sourceFeedbackRecordId: "01JZFDBK0000000000000001",
            summary: "默认 writer prompt 在质量门禁后保留了节奏与可读性。",
            evidenceRefs: ["object://quality-reports/01JZQLTREP000000000000001"],
          },
          {
            signalId: "01JZRANKSIG00000000000002",
            rankingType: "prompt",
            targetType: "prompt_version",
            targetId: "prompt://writer/chapter-compact",
            signalType: "reader_interest",
            score: 0.72,
            weight: 0.5,
            source: "critic",
            sourceFeedbackRecordId: "01JZFDBK0000000000000002",
            summary: "批评者认为默认 prompt 对金手指提示过早，紧凑版更适合后续回合。",
            evidenceRefs: ["object://critic-comments/01JZFDBK0000000000000002"],
          },
        ],
        suggestions: [
          {
            suggestionId: "01JZSTRAT000000000000001",
            rankingType: "prompt",
            targetScope: "prompt",
            status: "review_required",
            summary: "收紧 writer 默认提示中对金手指线索的显性表达。",
            recommendedAction: "切换到 prompt://writer/chapter-compact 进行下一轮写作。",
            sourceSignalIds: ["01JZRANKSIG00000000000002"],
            promotedFromFeedbackRecordId: "01JZFDBK0000000000000002",
            promotedAt: null,
          },
        ],
      },
    ],
    strategySuggestions: [
      {
        suggestionId: "01JZSTRAT000000000000001",
        basedOnFeedbackRecordId: "01JZFDBK0000000000000002",
        status: "review_required",
        targetScope: "prompt",
        summary: "收紧 writer 默认提示中对金手指线索的显性表达。",
        promotedAt: null,
      },
    ],
    configurationSnapshot: {
      defaultModelProfileId: DEFAULT_MODEL_PROFILE_ID,
      modelProfiles: [
        {
          modelProfileId: DEFAULT_MODEL_PROFILE_ID,
          providerName: "anthropic",
          providerModelName: "claude-sonnet-5",
          label: "默认中文长文本模型",
          description: "大多数 Agent role 默认使用。",
          enabled: true,
          supportsStructuredOutput: false,
          fallbackProfileIds: [STRUCTURED_FALLBACK_MODEL_PROFILE_ID],
        },
        {
          modelProfileId: STRUCTURED_FALLBACK_MODEL_PROFILE_ID,
          providerName: "anthropic",
          providerModelName: "claude-haiku-4-5-20251001",
          label: "结构化兜底模型",
          description: "结构化输出失败后重试使用。",
          enabled: true,
          supportsStructuredOutput: true,
          fallbackProfileIds: [],
        },
      ],
      agentModelAssignments: [
        { assignmentId: "01JZASSIGN000000000000001", agentRole: "extraction", taskType: "extraction_task", outputMode: "text", modelProfileId: DEFAULT_MODEL_PROFILE_ID, fallbackProfileIds: [], maxRetry: 1, maxCost: 0.8, enabled: true },
        { assignmentId: "01JZASSIGN000000000000002", agentRole: "normalization", taskType: "normalization_task", outputMode: "text", modelProfileId: DEFAULT_MODEL_PROFILE_ID, fallbackProfileIds: [], maxRetry: 1, maxCost: 0.8, enabled: true },
        { assignmentId: "01JZASSIGN000000000000003", agentRole: "planning", taskType: "planning_task", outputMode: "text", modelProfileId: DEFAULT_MODEL_PROFILE_ID, fallbackProfileIds: [], maxRetry: 1, maxCost: 0.8, enabled: true },
        { assignmentId: "01JZASSIGN000000000000004", agentRole: "memory", taskType: "memory_task", outputMode: "text", modelProfileId: DEFAULT_MODEL_PROFILE_ID, fallbackProfileIds: [], maxRetry: 1, maxCost: 0.8, enabled: true },
        { assignmentId: "01JZASSIGN000000000000005", agentRole: "style_analyzer", taskType: "style_analyzer_task", outputMode: "text", modelProfileId: DEFAULT_MODEL_PROFILE_ID, fallbackProfileIds: [], maxRetry: 1, maxCost: 0.8, enabled: true },
        { assignmentId: "01JZASSIGN000000000000006", agentRole: "writer", taskType: "writer_task", outputMode: "text", modelProfileId: DEFAULT_MODEL_PROFILE_ID, fallbackProfileIds: [STRUCTURED_FALLBACK_MODEL_PROFILE_ID], maxRetry: 1, maxCost: 1.5, enabled: true },
        { assignmentId: "01JZASSIGN000000000000007", agentRole: "critic", taskType: "critic_task", outputMode: "structured", modelProfileId: DEFAULT_MODEL_PROFILE_ID, fallbackProfileIds: [STRUCTURED_FALLBACK_MODEL_PROFILE_ID], maxRetry: 2, maxCost: 0.8, enabled: true },
        { assignmentId: "01JZASSIGN000000000000008", agentRole: "humanizer", taskType: "humanizer_task", outputMode: "text", modelProfileId: DEFAULT_MODEL_PROFILE_ID, fallbackProfileIds: [STRUCTURED_FALLBACK_MODEL_PROFILE_ID], maxRetry: 1, maxCost: 0.8, enabled: true },
        { assignmentId: "01JZASSIGN000000000000009", agentRole: "review", taskType: "review_task", outputMode: "structured", modelProfileId: DEFAULT_MODEL_PROFILE_ID, fallbackProfileIds: [STRUCTURED_FALLBACK_MODEL_PROFILE_ID], maxRetry: 2, maxCost: 0.8, enabled: true },
        { assignmentId: "01JZASSIGN000000000000010", agentRole: "feedback", taskType: "feedback_task", outputMode: "structured", modelProfileId: DEFAULT_MODEL_PROFILE_ID, fallbackProfileIds: [STRUCTURED_FALLBACK_MODEL_PROFILE_ID], maxRetry: 2, maxCost: 0.8, enabled: true },
      ],
      qualityGateProfiles: [
        {
          qualityGateProfileId: "01JZQUALITY00000000000001",
          label: "默认质量阈值",
          aiFlavorThreshold: 0.45,
          originalitySafetyThreshold: 0.85,
        },
      ],
      promptVersions: [
        { agentRole: "writer", templateRef: "prompt://writer/chapter-default" },
        { agentRole: "critic", templateRef: "prompt://critic/chapter-default" },
        { agentRole: "humanizer", templateRef: "prompt://humanizer/chapter-default" },
        { agentRole: "feedback", templateRef: "prompt://feedback/chapter-default" },
      ],
    },
    configurationMutations: [
      {
        mutationId: "01JZCFG0000000000000001",
        mutationType: "quality_gate_profile_updated",
        targetId: "01JZQUALITY00000000000001",
        actorId: "demo-user",
        actorRole: "owner",
        status: "succeeded",
        requestId: "req-config-quality-1",
        traceId: "trace-config-quality-1",
        createdAt: "2026-07-11T02:30:00Z",
        summary: "将 AI 味阈值调到 0.45，原创安全阈值调到 0.85。",
      },
      {
        mutationId: "01JZCFG0000000000000002",
        mutationType: "prompt_version_updated",
        targetId: "writer",
        actorId: "demo-user",
        actorRole: "owner",
        status: "succeeded",
        requestId: "req-config-prompt-1",
        traceId: "trace-config-prompt-1",
        createdAt: "2026-07-11T02:34:00Z",
        summary: "writer 已切到 prompt://writer/chapter-default。",
      },
    ],
    agentTasks: [
      {
        taskId: "01JZTASK000000000000000001",
        workspaceId: DEMO_WORKSPACE_ID,
        taskType: "extract_knowledge",
        status: "requires_review",
        actorId: "demo-user",
        actorRole: "editor",
        targetRef: `object://extraction-runs/${DEMO_RUN_ID}`,
        traceId: "01JZTRC000000000000000010",
        requestId: "req-extraction-1",
        createdAt: "2026-07-11T00:00:00Z",
        updatedAt: "2026-07-11T00:01:00Z",
        summary: "确定性抽取结果仍有低置信对象待处理。",
        events: [
          {
            eventId: "01JZTEVT0000000000000001",
            taskId: "01JZTASK000000000000000001",
            eventType: "created",
            status: "queued",
            summary: "抽取任务已入队。",
            createdAt: "2026-07-11T00:00:00Z",
          },
          {
            eventId: "01JZTEVT0000000000000002",
            taskId: "01JZTASK000000000000000001",
            eventType: "review_required",
            status: "requires_review",
            summary: "发现低置信对象，转入人工审核。",
            createdAt: "2026-07-11T00:01:00Z",
          },
        ],
      },
      {
        taskId: "01JZPLANTASK0000000000001",
        workspaceId: DEMO_WORKSPACE_ID,
        taskType: "create_chapter_plan",
        status: "requires_review",
        actorId: "demo-user",
        actorRole: "editor",
        targetRef: `object://chapter-plans/${DEMO_CHAPTER_PLAN_ID}`,
        traceId: "01JZTRC000000000000000011",
        requestId: "req-plan-1",
        createdAt: "2026-07-11T02:05:00Z",
        updatedAt: "2026-07-11T02:12:00Z",
        summary: "章节规划已生成，等待确认。",
        events: [
          {
            eventId: "01JZTEVT0000000000000003",
            taskId: "01JZPLANTASK0000000000001",
            eventType: "created",
            status: "running",
            summary: "章节规划生成中。",
            createdAt: "2026-07-11T02:05:00Z",
          },
          {
            eventId: "01JZTEVT0000000000000004",
            taskId: "01JZPLANTASK0000000000001",
            eventType: "review_required",
            status: "requires_review",
            summary: "章节规划已生成，等待人工确认。",
            createdAt: "2026-07-11T02:12:00Z",
          },
        ],
      },
      {
        taskId: "01JZWRITETASK0000000000001",
        workspaceId: DEMO_WORKSPACE_ID,
        taskType: "create_writing_run",
        status: "requires_review",
        actorId: "demo-user",
        actorRole: "editor",
        targetRef: `object://writing-runs/${DEMO_WRITING_RUN_ID}`,
        traceId: "01JZTRC000000000000000012",
        requestId: "req-writing-1",
        createdAt: "2026-07-11T02:40:00Z",
        updatedAt: "2026-07-11T03:05:00Z",
        summary: "写作任务进入人工复核。",
        events: [
          {
            eventId: "01JZTEVT0000000000000005",
            taskId: "01JZWRITETASK0000000000001",
            eventType: "retry_scheduled",
            status: "retrying",
            summary: "critic 结构化输出失败，已切到 fallback。",
            createdAt: "2026-07-11T02:52:00Z",
          },
          {
            eventId: "01JZTEVT0000000000000006",
            taskId: "01JZWRITETASK0000000000001",
            eventType: "review_required",
            status: "requires_review",
            summary: "润色通过，等待人工接受章节。",
            createdAt: "2026-07-11T03:05:00Z",
          },
        ],
      },
    ],
    auditEvents: [
      {
        auditEventId: "01JZAUDIT000000000000001",
        workspaceId: DEMO_WORKSPACE_ID,
        action: "knowledge.approve",
        actorId: "demo-user",
        actorRole: "editor",
        targetType: "knowledge_object",
        targetId: "01JZOBJ0000000000000000003",
        traceId: "01JZTRC000000000000000020",
        requestId: "req-knowledge-1",
        createdAt: "2026-07-11T00:10:00Z",
        summary: "已确认 Xiao Clan 为有效知识对象。",
        inputRefs: ["object://knowledge-objects/01JZOBJ0000000000000000003"],
        outputRefs: ["object://graph-nodes/01JZNODE000000000000000003"],
      },
      {
        auditEventId: "01JZAUDIT000000000000002",
        workspaceId: DEMO_WORKSPACE_ID,
        action: "configuration.quality_gate_profile_updated",
        actorId: "demo-user",
        actorRole: "owner",
        targetType: "quality_gate_profile",
        targetId: "01JZQUALITY00000000000001",
        traceId: "trace-config-quality-1",
        requestId: "req-config-quality-1",
        createdAt: "2026-07-11T02:30:00Z",
        summary: "更新默认质量阈值。",
        inputRefs: ["object://quality-gate-profiles/01JZQUALITY00000000000001"],
        outputRefs: ["object://configuration/default"],
      },
      {
        auditEventId: "01JZAUDIT000000000000003",
        workspaceId: DEMO_WORKSPACE_ID,
        action: "feedback.record_promoted",
        actorId: "demo-user",
        actorRole: "owner",
        targetType: "strategy_suggestion",
        targetId: "01JZSTRAT000000000000001",
        traceId: "trace-feedback-promotion-1",
        requestId: "req-feedback-promotion-1",
        createdAt: "2026-07-11T03:08:00Z",
        summary: "风格反馈已转为 prompt 调整建议，待批准。",
        inputRefs: ["object://feedback-records/01JZFDBK0000000000000002"],
        outputRefs: ["object://strategy-suggestions/01JZSTRAT000000000000001"],
      },
    ],
    providerCallsByWriting: {
      [DEMO_WRITING_RUN_ID]: [
        { providerCallId: "01JZPCALL0000000000000001", agentRole: "writer", modelProfileId: DEFAULT_MODEL_PROFILE_ID, providerName: "anthropic", promptTokens: 1800, completionTokens: 920, latencyMs: 1430, retryCount: 0, costEstimate: 0.31, status: "succeeded", errorCode: null },
        { providerCallId: "01JZPCALL0000000000000002", agentRole: "critic", modelProfileId: DEFAULT_MODEL_PROFILE_ID, providerName: "anthropic", promptTokens: 1400, completionTokens: 0, latencyMs: 490, retryCount: 1, costEstimate: 0.11, status: "failed", errorCode: "structured_output_validation_failed" },
        { providerCallId: "01JZPCALL0000000000000003", agentRole: "critic", modelProfileId: STRUCTURED_FALLBACK_MODEL_PROFILE_ID, providerName: "anthropic", promptTokens: 1400, completionTokens: 540, latencyMs: 980, retryCount: 1, costEstimate: 0.22, status: "succeeded", errorCode: null },
        { providerCallId: "01JZPCALL0000000000000004", agentRole: "humanizer", modelProfileId: DEFAULT_MODEL_PROFILE_ID, providerName: "anthropic", promptTokens: 1780, completionTokens: 850, latencyMs: 1210, retryCount: 0, costEstimate: 0.33, status: "succeeded", errorCode: null },
      ],
    },
    activityLog: [
      "来源书籍已就绪，等待抽取。",
      "确定性抽取任务已进入质量复核。",
      "写作任务已进入润色通过后的人工复核。",
    ],
  };
}

export function createUploadedBook(title: string, authorName: string, sourceType: string): SourceBookState {
  return {
    bookId: DEMO_BOOK_ID,
    workspaceId: DEMO_WORKSPACE_ID,
    title,
    authorName,
    sourceType,
    importStatus: "uploaded",
    traceId: "trace-web-upload",
  };
}

export function deriveLowConfidenceItems(items: KnowledgeObject[]): KnowledgeObject[] {
  return items.filter((item) => item.confidence < 0.8 && item.reviewStatus === "pending");
}

export function findEvidenceByRef(state: PhaseTwoState, evidenceRef: string): EvidenceState | undefined {
  const normalizedId = evidenceRef.replace(/^evidence:\/\//, "");
  return state.evidences.find((item) => item.evidenceId.replace(/^evidence:\/\//, "") === normalizedId);
}

export function getBookAnalysisSummary(state: PhaseTwoState, bookId: string): BookAnalysisSummaryState | undefined {
  return state.bookAnalysisSummary.bookId === bookId ? state.bookAnalysisSummary : undefined;
}

export function deriveAnalysisExceptions(state: PhaseTwoState): AnalysisExceptionState[] {
  return deriveLowConfidenceItems(state.knowledgeObjects).map((item) => ({
    exceptionId: `analysis-exception-${item.objectId}`,
    type: "low_confidence_object",
    severity: "warning",
    title: `${item.canonicalName} 需要确认`,
    summary: `${item.canonicalName} 的置信度为 ${item.confidence}，需要确认后再进入知识包。`,
    targetRef: `object://knowledge-objects/${item.objectId}`,
    evidenceRefs: state.graphNodes.find((node) => node.label === item.canonicalName)?.evidenceRefs ?? [],
    recommendedAction: "approve_or_reextract",
  }));
}

export function applyReviewActionToState(
  state: PhaseTwoState,
  objectId: string,
  action: ReviewAction,
  targetObjectId?: string,
): PhaseTwoState {
  const knowledgeObjects = state.knowledgeObjects.map((item) => {
    if (item.objectId !== objectId) {
      return item;
    }

    if (action === "approve") {
      return { ...item, reviewStatus: "approved", lifecycleStatus: "approved" };
    }
    if (action === "reject") {
      return { ...item, reviewStatus: "rejected", lifecycleStatus: "rejected" };
    }
    if (action === "merge_alias") {
      return {
        ...item,
        reviewStatus: "merged",
        lifecycleStatus: "approved",
        mergedInto: targetObjectId,
      };
    }
    return { ...item, reviewStatus: "reextract_requested" };
  });

  const pending = deriveLowConfidenceItems(knowledgeObjects);
  const runStatus = action === "request_reextract" ? "queued" : pending.length === 0 ? "succeeded" : state.run.status;
  const runStage = action === "request_reextract"
    ? "source_submission"
    : pending.length === 0
      ? "knowledge_package_export"
      : state.run.currentStage;
  const nextState = {
    ...state,
    knowledgeObjects,
    run: {
      ...state.run,
      lowConfidenceCount: pending.length,
      status: runStatus,
      currentStage: runStage,
    },
    bookAnalysisSummary: {
      ...state.bookAnalysisSummary,
      status: runStatus,
      currentStage: runStage,
      needsAttentionCount: pending.length,
      canCommitKnowledge: action !== "request_reextract",
    },
    activityLog: [...state.activityLog, `已执行审核动作：${reviewActionLabels[action]}。`],
  };

  return {
    ...nextState,
    analysisExceptions: deriveAnalysisExceptions(nextState),
  };
}

export function commitKnowledgePackage(state: PhaseTwoState): PhaseTwoState {
  return {
    ...state,
    run: {
      ...state.run,
      status: "succeeded",
      currentStage: "knowledge_base_commit",
    },
    bookAnalysisSummary: {
      ...state.bookAnalysisSummary,
      status: "succeeded",
      currentStage: "knowledge_base_commit",
      canCommitKnowledge: false,
    },
    activityLog: [...state.activityLog, "知识包已提交到故事图谱。"],
  };
}

export function applyWritingReviewActionToState(
  state: PhaseTwoState,
  writingRunId: string,
  sectionRunId: string,
  action: WritingReviewAction,
): PhaseTwoState {
  const sectionRuns = state.sectionRunsByWriting[writingRunId] ?? [];
  const providerCalls = state.providerCallsByWriting[writingRunId] ?? [];
  const targetRun = state.writingRuns.find((item) => item.writingRunId === writingRunId);
  const qualityReport = state.qualityReports.find((item) => item.writingRunId === writingRunId);
  const consistencyReport = state.consistencyReports.find((item) => item.writingRunId === writingRunId);
  const revisionSummary = state.revisionSummaries.find((item) => item.writingRunId === writingRunId);

  if (!targetRun || !qualityReport || !consistencyReport || !revisionSummary) {
    return state;
  }

  const acceptedAt = "2026-07-12T01:22:00Z";
  const acceptedChapterRef = `object://manuscripts/${writingRunId}/chapters/1`;
  const nextWritingRun = { ...targetRun };
  const nextQualityReport = {
    ...qualityReport,
    blockingIssues: qualityReport.blockingIssues.map((item) => ({
      ...item,
      inputRefs: [...item.inputRefs],
      outputRefs: [...item.outputRefs],
    })),
  };
  const nextConsistencyReport = {
    ...consistencyReport,
    issues: consistencyReport.issues.map((item) => ({
      ...item,
      inputRefs: [...item.inputRefs],
      outputRefs: [...item.outputRefs],
    })),
  };
  const nextRevisionSummary = { ...revisionSummary };

  const nextSectionRuns = sectionRuns.map((item) => {
    if (item.sectionRunId !== sectionRunId) {
      return item;
    }

    if (action === "accept_section") {
      return {
        ...item,
        status: "beat_approved",
        beatStatus: item.beatStatus.map((beat) => ({ ...beat, status: "beat_approved" })),
        criticIssues: [],
      };
    }
    if (action === "request_rewrite") {
      return {
        ...item,
        status: "rewrite_required",
        beatStatus: item.beatStatus.map((beat, index) => ({
          ...beat,
          status: index === item.beatStatus.length - 1 ? "rewrite_required" : beat.status,
        })),
      };
    }
    if (action === "edit_and_accept") {
      return {
        ...item,
        status: "beat_approved",
        beatStatus: item.beatStatus.map((beat) => ({ ...beat, status: "beat_approved" })),
        humanizedText: `${item.humanizedText}（已人工微调）`,
        criticIssues: [],
      };
    }
    if (action === "edit_draft") {
      return {
        ...item,
        humanizedText: `${item.humanizedText}（已人工补写一致性细节）`,
      };
    }
    if (action === "block_generation") {
      return {
        ...item,
        status: "blocked",
        beatStatus: item.beatStatus.map((beat) => ({ ...beat, status: "blocked" })),
      };
    }
    return item;
  });

  const matchingQualityIssue = (issue: ConsistencyIssueState, candidate: QualityIssueState) =>
    candidate.issueId === issue.issueId ||
    (candidate.ruleId === issue.ruleId && candidate.affectedTextRef === issue.affectedTextRef);

  if (action === "mark_issue_resolved") {
    const issue = nextConsistencyReport.issues.find((item) => item.resolutionStatus === "open");
    if (!issue) {
      return state;
    }
    issue.resolutionStatus = "resolved";
    issue.note = "已在工作台标记为已解决。";
    nextConsistencyReport.blockingIssueCount = nextConsistencyReport.issues.filter((item) => item.resolutionStatus === "open").length;
    nextConsistencyReport.status = nextConsistencyReport.blockingIssueCount === 0 ? "passed" : "blocked";
    nextQualityReport.blockingIssues = nextQualityReport.blockingIssues.filter((item) => !matchingQualityIssue(issue, item));
    if (nextConsistencyReport.blockingIssueCount === 0) {
      nextQualityReport.blockingIssues = [];
      nextQualityReport.status = "requires_review";
      nextRevisionSummary.status = "revised";
    }
  }

  if (action === "approve_draft") {
    nextWritingRun.status = "requires_review";
    nextWritingRun.currentStage = "quality_gate";
    nextQualityReport.status = "requires_review";
    nextQualityReport.humanReviewRequired = false;
    nextQualityReport.blockingIssues = [];
    nextConsistencyReport.status = "passed";
    nextConsistencyReport.blockingIssueCount = 0;
    nextConsistencyReport.issues = nextConsistencyReport.issues.map((item) => ({
      ...item,
      resolutionStatus: "resolved",
      note: item.note ?? "已批准通过一致性复核。",
      inputRefs: [...item.inputRefs],
      outputRefs: [...item.outputRefs],
    }));
    nextRevisionSummary.status = "accepted";
  }

  if (action === "request_revision") {
    nextWritingRun.status = "blocked";
    nextWritingRun.currentStage = "revision_loop";
    nextWritingRun.revisionRound = Math.min(nextWritingRun.revisionRound + 1, nextWritingRun.maxRevisionRounds);
    nextQualityReport.status = "blocked";
    nextQualityReport.humanReviewRequired = true;
    nextConsistencyReport.status = "blocked";
    nextConsistencyReport.blockingIssueCount = nextConsistencyReport.issues.filter((item) => item.resolutionStatus === "open").length;
    nextRevisionSummary.status = nextWritingRun.revisionRound < nextWritingRun.maxRevisionRounds ? "requested" : "blocked";
    nextRevisionSummary.revisionRound = nextWritingRun.revisionRound;
    nextRevisionSummary.changeSummary = "要求重写第二节，恢复主角当前境界并补足冲突升级。";
  }

  if (action === "reject_draft") {
    nextWritingRun.status = "blocked";
    nextWritingRun.currentStage = "human_review";
    nextQualityReport.status = "blocked";
    nextQualityReport.humanReviewRequired = true;
    nextConsistencyReport.status = "blocked";
    nextRevisionSummary.status = "blocked";
  }

  if (action === "edit_draft") {
    nextWritingRun.status = "requires_review";
    nextWritingRun.currentStage = "human_review";
    nextQualityReport.status = "requires_review";
    nextQualityReport.humanReviewRequired = true;
    nextRevisionSummary.status = "requires_review";
  }

  if (action === "create_rule_update_request") {
    nextRevisionSummary.status = "requires_review";
    nextRevisionSummary.reviewerNoteRef = "object://rule-update-requests/rule-01JZPOWER000000000000001";
  }

  if (action === "request_rewrite") {
    nextWritingRun.status = "blocked";
    nextWritingRun.currentStage = "revision_loop";
    nextQualityReport.status = "blocked";
    nextQualityReport.humanReviewRequired = true;
    nextRevisionSummary.status = "requested";
  }

  if (action === "block_generation") {
    nextWritingRun.status = "blocked";
    nextWritingRun.currentStage = "human_review";
    nextQualityReport.status = "blocked";
    nextQualityReport.humanReviewRequired = true;
    nextRevisionSummary.status = "blocked";
  }

  let feedbackRecords = state.feedbackRecords;

  if (action === "accept_chapter") {
    const consistencyClear = nextConsistencyReport.blockingIssueCount === 0;
    const qualityClear = nextQualityReport.blockingIssues.length === 0 && nextQualityReport.status !== "blocked";
    const reviewClear = !nextQualityReport.humanReviewRequired;
    const revisionClear = ["accepted", "revised"].includes(nextRevisionSummary.status);

    if (!consistencyClear || !qualityClear || !reviewClear || !revisionClear) {
      return {
        ...state,
        activityLog: [...state.activityLog, "一致性或修订仍未完成，暂不能接受本章。"],
      };
    }

    const reviewedSectionRuns = nextSectionRuns.map((item) => ({
      ...item,
      status: "beat_approved",
      beatStatus: item.beatStatus.map((beat) => ({ ...beat, status: "beat_approved" })),
      criticIssues: [],
    }));

    const chapterSnapshot = {
      chapterSnapshotId: `chapter-snapshot:${writingRunId}`,
      writingRunId,
      projectId: targetRun.projectId,
      chapterPlanId: targetRun.chapterPlanId,
      acceptedChapterRef,
      chapterTitle: state.chapterPlans.find((item) => item.chapterPlanId === targetRun.chapterPlanId)?.title ?? "当前章节",
      chapterText: targetRun.assembledChapter,
      sourceSectionRefs: reviewedSectionRuns.map((item) => `object://section-runs/${item.sectionRunId}`),
      createdAt: acceptedAt,
    };
    const manuscriptState = {
      manuscriptStateId: `manuscript-state:${targetRun.projectId}`,
      projectId: targetRun.projectId,
      writingRunId,
      currentStoryState: {
        summary: "第 1 章《乌坦城风起》已进入 manuscript，三年之约正式进入主线。",
        acceptedChapterRef,
        qualityGateStatus: "passed",
      },
      characterDynamicState: [
        {
          characterName: "萧炎",
          stateSummary: "从公开羞辱中立下三年之约，主线动机被明确激活。",
        },
      ],
      relationshipState: [
        {
          subject: "萧炎",
          object: "三年之约",
          stateSummary: "人物目标从承压转为正面回应，冲突升级为长期承诺。",
        },
      ],
      hookState: [
        {
          hookKey: "core_conflict",
          status: "active",
          summary: "天赋跌落后的家族压力与三年之约仍是当前核心挂钩。",
        },
      ],
      priorSummaryPack: [
        { summaryIndex: 1, summary: "议事堂压抑氛围与家族压力被建立。" },
        { summaryIndex: 2, summary: "纳兰家退婚消息引爆公开冲突。" },
        { summaryIndex: 3, summary: "主角在羞辱中立下三年之约。" },
      ],
      updatedAt: acceptedAt,
    };

    nextWritingRun.status = "succeeded";
    nextWritingRun.currentStage = "quality_gate";
    nextWritingRun.acceptedIntoManuscriptAt = acceptedAt;
    nextWritingRun.acceptedChapterRef = acceptedChapterRef;
    nextWritingRun.chapterSnapshotId = chapterSnapshot.chapterSnapshotId;
    nextWritingRun.manuscriptStateId = manuscriptState.manuscriptStateId;
    nextWritingRun.chapterSnapshot = chapterSnapshot;
    nextWritingRun.manuscriptState = manuscriptState;
    nextQualityReport.status = "passed";
    nextQualityReport.humanReviewRequired = false;
    nextQualityReport.blockingIssues = [];
    nextConsistencyReport.status = "passed";
    nextConsistencyReport.blockingIssueCount = 0;
    nextRevisionSummary.status = "accepted";

    feedbackRecords = [
      ...state.feedbackRecords,
      ...[
        {
          feedbackRecordId: "01JZFDBK0000000000000101",
          workspaceId: DEMO_WORKSPACE_ID,
          targetType: "writing_run",
          targetId: writingRunId,
          feedbackType: "acceptance",
          score: 1,
          source: "human_review",
          commentRef: "object://feedback-comments/01JZFDBK0000000000000101",
          payload: {
            acceptedChapterRef,
            summary: "人工复核已接受本章进入 manuscript。",
          } as Record<string, string | number | boolean | null>,
        },
        {
          feedbackRecordId: "01JZFDBK0000000000000102",
          workspaceId: DEMO_WORKSPACE_ID,
          targetType: "writing_run",
          targetId: writingRunId,
          feedbackType: "cost",
          score: 0.78,
          source: "system",
          commentRef: null,
          payload: {
            estimatedTotalCost: targetRun.modelCost.estimatedTotalCost,
            retryCount: targetRun.modelCost.retryCount,
          } as Record<string, string | number | boolean | null>,
        },
      ].filter(
        (nextItem) =>
          !state.feedbackRecords.some(
            (current) => current.targetId === nextItem.targetId && current.feedbackType === nextItem.feedbackType,
          ),
      ),
    ];

    nextWritingRun.consistencyReport = nextConsistencyReport;
    nextWritingRun.revisionSummary = nextRevisionSummary;
    nextWritingRun.revisionRound = nextRevisionSummary.revisionRound;
    nextWritingRun.maxRevisionRounds = nextRevisionSummary.maxRevisionRounds;

    return {
      ...state,
      writingRuns: state.writingRuns.map((item) => (item.writingRunId === writingRunId ? nextWritingRun : item)),
      qualityReports: state.qualityReports.map((item) => (item.writingRunId === writingRunId ? nextQualityReport : item)),
      consistencyReports: state.consistencyReports.map((item) =>
        item.writingRunId === writingRunId ? { ...nextConsistencyReport, issueCount: nextConsistencyReport.issues.length } : item,
      ),
      revisionSummaries: state.revisionSummaries.map((item) => (item.writingRunId === writingRunId ? nextRevisionSummary : item)),
      feedbackRecords,
      providerCallsByWriting: {
        ...state.providerCallsByWriting,
        [writingRunId]: providerCalls,
      },
      sectionRunsByWriting: {
        ...state.sectionRunsByWriting,
        [writingRunId]: reviewedSectionRuns,
      },
      activityLog: [...state.activityLog, `已执行写作审核动作：${writingReviewActionLabels[action]}。`],
    };
  }

  nextConsistencyReport.issueCount = nextConsistencyReport.issues.length;
  nextWritingRun.consistencyReport = nextConsistencyReport;
  nextWritingRun.revisionSummary = nextRevisionSummary;
  nextWritingRun.revisionRound = nextRevisionSummary.revisionRound;
  nextWritingRun.maxRevisionRounds = nextRevisionSummary.maxRevisionRounds;

  return {
    ...state,
    writingRuns: state.writingRuns.map((item) => (item.writingRunId === writingRunId ? nextWritingRun : item)),
    qualityReports: state.qualityReports.map((item) => (item.writingRunId === writingRunId ? nextQualityReport : item)),
    consistencyReports: state.consistencyReports.map((item) => (item.writingRunId === writingRunId ? nextConsistencyReport : item)),
    revisionSummaries: state.revisionSummaries.map((item) => (item.writingRunId === writingRunId ? nextRevisionSummary : item)),
    providerCallsByWriting: {
      ...state.providerCallsByWriting,
      [writingRunId]: providerCalls,
    },
    sectionRunsByWriting: {
      ...state.sectionRunsByWriting,
      [writingRunId]: nextSectionRuns,
    },
    activityLog: [...state.activityLog, `已执行写作审核动作：${writingReviewActionLabels[action]}。`],
  };
}

export function toggleModelProfileInState(
  state: PhaseTwoState,
  modelProfileId: string,
  enabled: boolean,
): PhaseTwoState {
  const occurrence = state.configurationMutations.filter((item) => item.mutationType === "model_profile_toggled").length + 1;
  const modelProfiles = state.configurationSnapshot.modelProfiles.map((item) =>
    item.modelProfileId === modelProfileId ? { ...item, enabled } : item,
  );
  const writerProfile = modelProfiles.find((item) => item.modelProfileId === DEFAULT_MODEL_PROFILE_ID);
  const fallbackProfile = modelProfiles.find((item) => item.modelProfileId === STRUCTURED_FALLBACK_MODEL_PROFILE_ID);
  const writerResolvedProfileId = writerProfile?.enabled ? DEFAULT_MODEL_PROFILE_ID : STRUCTURED_FALLBACK_MODEL_PROFILE_ID;
  const criticResolvedProfileId = writerProfile?.enabled ? STRUCTURED_FALLBACK_MODEL_PROFILE_ID : STRUCTURED_FALLBACK_MODEL_PROFILE_ID;
  const providerCallsByWriting = Object.fromEntries(
    Object.entries(state.providerCallsByWriting).map(([writingRunId, calls]) => [
      writingRunId,
      calls.map((call) => {
        if (call.agentRole === "writer") {
          return {
            ...call,
            modelProfileId: writerResolvedProfileId,
            status: writerProfile?.enabled ? "succeeded" : fallbackProfile?.enabled ? "succeeded" : "failed",
            errorCode: writerProfile?.enabled ? null : fallbackProfile?.enabled ? null : "model_profile_unavailable",
          };
        }
        if (call.agentRole === "critic" && call.status === "failed") {
          return {
            ...call,
            modelProfileId: DEFAULT_MODEL_PROFILE_ID,
            errorCode: "structured_output_validation_failed",
          };
        }
        if (call.agentRole === "critic" && call.status === "succeeded") {
          return {
            ...call,
            modelProfileId: criticResolvedProfileId,
          };
        }
        if (call.agentRole === "humanizer") {
          return {
            ...call,
            modelProfileId: writerResolvedProfileId,
            status: writerProfile?.enabled ? "succeeded" : fallbackProfile?.enabled ? "succeeded" : "failed",
            errorCode: writerProfile?.enabled ? null : fallbackProfile?.enabled ? null : "model_profile_unavailable",
          };
        }
        return call;
      }),
    ]),
  ) as Record<string, ProviderCallState[]>;

  const writingRuns = state.writingRuns.map((item) => ({
    ...item,
    writerModelProfileId: writerResolvedProfileId,
    criticModelProfileId: criticResolvedProfileId,
    humanizerModelProfileId: writerResolvedProfileId,
  }));

  const mutation = {
    mutationId: `cfg-model-${modelProfileId}-${enabled ? "enable" : "disable"}-${occurrence}`,
    mutationType: "model_profile_toggled",
    targetId: modelProfileId,
    actorId: "demo-user",
    actorRole: "owner",
    status: "succeeded",
    requestId: `req-model-${modelProfileId}-${enabled ? "enable" : "disable"}-${occurrence}`,
    traceId: `trace-model-${modelProfileId}-${enabled ? "enable" : "disable"}-${occurrence}`,
    createdAt: "2026-07-11T03:09:00Z",
    summary: enabled ? `已启用模型 profile：${modelProfileId}。` : `已禁用模型 profile：${modelProfileId}，路由已切换到 fallback。`,
  };
  const auditEvent = {
    auditEventId: `audit-model-${modelProfileId}-${enabled ? "enable" : "disable"}-${occurrence}`,
    workspaceId: DEMO_WORKSPACE_ID,
    action: "configuration.model_profile_toggled",
    actorId: "demo-user",
    actorRole: "owner",
    targetType: "model_profile",
    targetId: modelProfileId,
    traceId: mutation.traceId,
    requestId: mutation.requestId,
    createdAt: mutation.createdAt,
    summary: mutation.summary,
    inputRefs: [`object://model-profiles/${modelProfileId}`],
    outputRefs: [`object://configuration/default`],
  };

  return {
    ...state,
    configurationSnapshot: {
      ...state.configurationSnapshot,
      modelProfiles,
    },
    configurationMutations: [...state.configurationMutations, mutation],
    auditEvents: [...state.auditEvents, auditEvent],
    providerCallsByWriting,
    writingRuns,
    activityLog: [...state.activityLog, mutation.summary],
  };
}

export function updateQualityGateProfileInState(
  state: PhaseTwoState,
  qualityGateProfileId: string,
  aiFlavorThreshold: number,
  originalitySafetyThreshold: number,
): PhaseTwoState {
  const occurrence = state.configurationMutations.filter((item) => item.mutationType === "quality_gate_profile_updated").length + 1;
  const qualityGateProfiles = state.configurationSnapshot.qualityGateProfiles.map((item) =>
    item.qualityGateProfileId === qualityGateProfileId
      ? { ...item, aiFlavorThreshold, originalitySafetyThreshold }
      : item,
  );
  const summary = `已更新质量阈值：AI 味 ${aiFlavorThreshold}，原创安全 ${originalitySafetyThreshold}。`;
  const mutation = {
    mutationId: `cfg-quality-${qualityGateProfileId}-${occurrence}`,
    mutationType: "quality_gate_profile_updated",
    targetId: qualityGateProfileId,
    actorId: "demo-user",
    actorRole: "owner",
    status: "succeeded",
    requestId: `req-quality-${qualityGateProfileId}-${occurrence}`,
    traceId: `trace-quality-${qualityGateProfileId}-${occurrence}`,
    createdAt: "2026-07-11T03:10:00Z",
    summary,
  };
  const auditEvent = {
    auditEventId: `audit-quality-${qualityGateProfileId}-${occurrence}`,
    workspaceId: DEMO_WORKSPACE_ID,
    action: "configuration.quality_gate_profile_updated",
    actorId: "demo-user",
    actorRole: "owner",
    targetType: "quality_gate_profile",
    targetId: qualityGateProfileId,
    traceId: mutation.traceId,
    requestId: mutation.requestId,
    createdAt: mutation.createdAt,
    summary,
    inputRefs: [`object://quality-gate-profiles/${qualityGateProfileId}`],
    outputRefs: [`object://configuration/default`],
  };

  return {
    ...state,
    configurationSnapshot: {
      ...state.configurationSnapshot,
      qualityGateProfiles,
    },
    configurationMutations: [...state.configurationMutations, mutation],
    auditEvents: [...state.auditEvents, auditEvent],
    activityLog: [...state.activityLog, summary],
  };
}

export function updateAgentAssignmentInState(
  state: PhaseTwoState,
  assignmentId: string,
  modelProfileId: string,
): PhaseTwoState {
  const occurrence = state.configurationMutations.filter((item) => item.mutationType === "agent_model_assignment_updated").length + 1;
  const agentModelAssignments = state.configurationSnapshot.agentModelAssignments.map((item) =>
    item.assignmentId === assignmentId ? { ...item, modelProfileId } : item,
  );
  const assignment = agentModelAssignments.find((item) => item.assignmentId === assignmentId);
  const summary = `已更新 Agent 分配：${assignment?.agentRole ?? assignmentId} 改用 ${modelProfileId}。`;
  const mutation = {
    mutationId: `cfg-assignment-${assignmentId}-${occurrence}`,
    mutationType: "agent_model_assignment_updated",
    targetId: assignmentId,
    actorId: "demo-user",
    actorRole: "owner",
    status: "succeeded",
    requestId: `req-assignment-${assignmentId}-${occurrence}`,
    traceId: `trace-assignment-${assignmentId}-${occurrence}`,
    createdAt: "2026-07-11T03:11:00Z",
    summary,
  };
  const auditEvent = {
    auditEventId: `audit-assignment-${assignmentId}-${occurrence}`,
    workspaceId: DEMO_WORKSPACE_ID,
    action: "configuration.agent_model_assignment_updated",
    actorId: "demo-user",
    actorRole: "owner",
    targetType: "agent_model_assignment",
    targetId: assignmentId,
    traceId: mutation.traceId,
    requestId: mutation.requestId,
    createdAt: mutation.createdAt,
    summary,
    inputRefs: [`object://agent-model-assignments/${assignmentId}`],
    outputRefs: [`object://configuration/default`],
  };

  return {
    ...state,
    configurationSnapshot: {
      ...state.configurationSnapshot,
      agentModelAssignments,
    },
    configurationMutations: [...state.configurationMutations, mutation],
    auditEvents: [...state.auditEvents, auditEvent],
    activityLog: [...state.activityLog, summary],
  };
}

export function updatePromptVersionInState(state: PhaseTwoState, agentRole: string, templateRef: string): PhaseTwoState {
  const occurrence = state.configurationMutations.filter((item) => item.mutationType === "prompt_version_updated").length + 1;
  const promptVersions = state.configurationSnapshot.promptVersions.map((item) =>
    item.agentRole === agentRole ? { ...item, templateRef } : item,
  );
  const summary = `已更新 Prompt 版本：${agentRole} 改到 ${templateRef}。`;
  const mutation = {
    mutationId: `cfg-prompt-${agentRole}-${occurrence}`,
    mutationType: "prompt_version_updated",
    targetId: agentRole,
    actorId: "demo-user",
    actorRole: "owner",
    status: "succeeded",
    requestId: `req-prompt-${agentRole}-${occurrence}`,
    traceId: `trace-prompt-${agentRole}-${occurrence}`,
    createdAt: "2026-07-11T03:12:00Z",
    summary,
  };
  const auditEvent = {
    auditEventId: `audit-prompt-${agentRole}-${occurrence}`,
    workspaceId: DEMO_WORKSPACE_ID,
    action: "configuration.prompt_version_updated",
    actorId: "demo-user",
    actorRole: "owner",
    targetType: "prompt_version",
    targetId: agentRole,
    traceId: mutation.traceId,
    requestId: mutation.requestId,
    createdAt: mutation.createdAt,
    summary,
    inputRefs: [`object://prompt-versions/${agentRole}`],
    outputRefs: [templateRef],
  };

  return {
    ...state,
    configurationSnapshot: {
      ...state.configurationSnapshot,
      promptVersions,
    },
    configurationMutations: [...state.configurationMutations, mutation],
    auditEvents: [...state.auditEvents, auditEvent],
    activityLog: [...state.activityLog, summary],
  };
}

export function promoteStrategySuggestionInState(state: PhaseTwoState, suggestionId: string): PhaseTwoState {
  const occurrence = state.configurationMutations.filter((item) => item.mutationType === "feedback_record_promoted").length + 1;
  const strategySuggestions = state.strategySuggestions.map((item) =>
    item.suggestionId === suggestionId ? { ...item, status: "approved", promotedAt: "2026-07-11T03:13:00Z" } : item,
  );
  const target = strategySuggestions.find((item) => item.suggestionId === suggestionId);
  const summary = `已提升策略建议：${target?.summary ?? suggestionId}`;
  const mutation = {
    mutationId: `feedback-promotion-${suggestionId}-${occurrence}`,
    mutationType: "feedback_record_promoted",
    targetId: suggestionId,
    actorId: "demo-user",
    actorRole: "owner",
    status: "succeeded",
    requestId: `req-feedback-promotion-${suggestionId}-${occurrence}`,
    traceId: `trace-feedback-promotion-${suggestionId}-${occurrence}`,
    createdAt: "2026-07-11T03:13:00Z",
    summary,
  };
  const auditEvent = {
    auditEventId: `audit-feedback-promotion-${suggestionId}-${occurrence}`,
    workspaceId: DEMO_WORKSPACE_ID,
    action: "feedback.record_promoted",
    actorId: "demo-user",
    actorRole: "owner",
    targetType: "strategy_suggestion",
    targetId: suggestionId,
    traceId: mutation.traceId,
    requestId: mutation.requestId,
    createdAt: mutation.createdAt,
    summary,
    inputRefs: target ? [`object://feedback-records/${target.basedOnFeedbackRecordId}`] : [],
    outputRefs: [`object://strategy-suggestions/${suggestionId}`],
  };

  return {
    ...state,
    strategySuggestions,
    configurationMutations: [...state.configurationMutations, mutation],
    auditEvents: [...state.auditEvents, auditEvent],
    activityLog: [...state.activityLog, summary],
  };
}
