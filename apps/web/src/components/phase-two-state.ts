export type ReviewAction = "approve" | "reject" | "merge_alias" | "request_reextract";
export type WritingReviewAction = "accept_section" | "accept_chapter" | "request_rewrite" | "edit_and_accept" | "block_generation";

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

export type QualityIssueState = {
  issueId: string;
  category: string;
  summary: string;
  affectedTextRef: string;
};

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
  traceId: string;
  writerModelProfileId: string;
  criticModelProfileId: string;
  humanizerModelProfileId: string;
  assembledChapter: string;
  modelCost: ModelCostState;
  acceptedIntoManuscriptAt: string | null;
  acceptedChapterRef: string | null;
  chapterSnapshotId: string | null;
  manuscriptStateId: string | null;
  chapterSnapshot: ChapterSnapshotState | null;
  manuscriptState: ManuscriptStateState | null;
};

export type PhaseTwoState = {
  workspace: WorkspaceState;
  workspaceMembers: WorkspaceMemberState[];
  workspaceHome: WorkspaceHomeState;
  book: SourceBookState;
  chapters: SourceChapterState[];
  run: ExtractionRunState;
  knowledgeObjects: KnowledgeObject[];
  graphNodes: GraphNodeState[];
  projects: NovelProjectState[];
  storyBibles: StoryBibleState[];
  chapterPlans: ChapterPlanState[];
  sectionPlansByChapter: Record<string, SectionPlanState[]>;
  writingRuns: WritingRunState[];
  sectionRunsByWriting: Record<string, SectionRunState[]>;
  memoryPackages: MemoryPackageState[];
  promptPackages: PromptPackageState[];
  qualityReports: QualityReportState[];
  feedbackRecords: FeedbackRecordState[];
  configurationSnapshot: ConfigurationSnapshotState;
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
      status: "requires_review",
      currentStage: "quality_review",
      chapterCount: 2,
      sceneCount: 6,
      objectCount: 3,
      evidenceCount: 3,
      lowConfidenceCount: 2,
      errors: [],
    },
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
      { nodeId: "01JZNODE000000000000000001", label: "Xiao Yan", nodeType: "character" },
      { nodeId: "01JZNODE000000000000000002", label: "Yao Lao", nodeType: "mentor" },
      { nodeId: "01JZNODE000000000000000003", label: "Xiao Clan", nodeType: "clan" },
    ],
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
        currentStage: "humanizer_pass",
        taskId: "01JZWRITETASK0000000000001",
        memoryPackageId: "01JZMEMPKG000000000000001",
        promptPackageId: "01JZPROMPTPKG000000000001",
        chapterDraftId: "01JZDRAFT0000000000000001",
        qualityReportId: "01JZQLTREP000000000000001",
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
        acceptedIntoManuscriptAt: null,
        acceptedChapterRef: null,
        chapterSnapshotId: null,
        manuscriptStateId: null,
        chapterSnapshot: null,
        manuscriptState: null,
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
            category: "character_consistency",
            summary: "第二节仍需补足压迫递进。",
            affectedTextRef: "object://drafts/01JZSECRUN00000000000002#p1",
          },
        ],
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
  return {
    ...state,
    knowledgeObjects,
    run: {
      ...state.run,
      lowConfidenceCount: pending.length,
      status: pending.length === 0 ? "succeeded" : state.run.status,
      currentStage: pending.length === 0 ? "knowledge_package_export" : state.run.currentStage,
    },
    activityLog: [...state.activityLog, `已执行审核动作：${reviewActionLabels[action]}。`],
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
  const acceptedAt = "2026-07-11T03:12:00Z";
  const acceptedChapterRef = `object://manuscripts/${writingRunId}/chapters/1`;

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
    if (action === "block_generation") {
      return {
        ...item,
        status: "blocked",
        beatStatus: item.beatStatus.map((beat) => ({ ...beat, status: "blocked" })),
      };
    }
    return item;
  });

  const reviewedSectionRuns =
    action === "accept_chapter"
      ? nextSectionRuns.map((item) => ({
          ...item,
          status: "beat_approved",
          beatStatus: item.beatStatus.map((beat) => ({ ...beat, status: "beat_approved" })),
          criticIssues: [],
        }))
      : nextSectionRuns;

  const allApproved = reviewedSectionRuns.length > 0 && reviewedSectionRuns.every((item) => item.status === "beat_approved");
  const hasBlocked = reviewedSectionRuns.some((item) => item.status === "blocked");
  const chapterSnapshot = {
    chapterSnapshotId: `chapter-snapshot:${writingRunId}`,
    writingRunId,
    projectId: targetRun?.projectId ?? DEMO_PROJECT_ID,
    chapterPlanId: targetRun?.chapterPlanId ?? DEMO_CHAPTER_PLAN_ID,
    acceptedChapterRef,
    chapterTitle: state.chapterPlans.find((item) => item.chapterPlanId === targetRun?.chapterPlanId)?.title ?? "当前章节",
    chapterText: targetRun?.assembledChapter ?? "",
    sourceSectionRefs: reviewedSectionRuns.map((item) => `object://section-runs/${item.sectionRunId}`),
    createdAt: acceptedAt,
  };
  const manuscriptState = {
    manuscriptStateId: `manuscript-state:${targetRun?.projectId ?? DEMO_PROJECT_ID}`,
    projectId: targetRun?.projectId ?? DEMO_PROJECT_ID,
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
  const writingRuns = state.writingRuns.map((item) => {
    if (item.writingRunId !== writingRunId) {
      return item;
    }
    if (action === "accept_chapter") {
      return {
        ...item,
        status: "succeeded",
        currentStage: "quality_gate",
        acceptedIntoManuscriptAt: acceptedAt,
        acceptedChapterRef,
        chapterSnapshotId: chapterSnapshot.chapterSnapshotId,
        manuscriptStateId: manuscriptState.manuscriptStateId,
        chapterSnapshot,
        manuscriptState,
      };
    }
    if (hasBlocked) {
      return {
        ...item,
        status: "blocked",
        currentStage: "critic_review",
      };
    }
    if (allApproved) {
      return {
        ...item,
        status: "succeeded",
        currentStage: "quality_gate",
      };
    }
    return item;
  });

  const qualityReports = state.qualityReports.map((item) => {
    if (item.writingRunId !== writingRunId) {
      return item;
    }
    if (action === "accept_chapter" || allApproved) {
      return {
        ...item,
        status: "passed",
        humanReviewRequired: false,
        blockingIssues: [],
      };
    }
    if (hasBlocked) {
      return {
        ...item,
        status: "blocked",
        humanReviewRequired: true,
      };
    }
    return item;
  });

  const feedbackRecords =
    action === "accept_chapter" && targetRun && qualityReport
      ? [
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
        ]
      : state.feedbackRecords;

  return {
    ...state,
    writingRuns,
    qualityReports,
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

export function toggleModelProfileInState(
  state: PhaseTwoState,
  modelProfileId: string,
  enabled: boolean,
): PhaseTwoState {
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

  return {
    ...state,
    configurationSnapshot: {
      ...state.configurationSnapshot,
      modelProfiles,
    },
    providerCallsByWriting,
    writingRuns,
    activityLog: [
      ...state.activityLog,
      enabled
        ? `已启用模型 profile：${modelProfileId}。`
        : `已禁用模型 profile：${modelProfileId}，路由已切换到 fallback。`,
    ],
  };
}
