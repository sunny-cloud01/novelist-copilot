export type RequestMeta = {
  request_id: string;
  trace_id: string;
  workspace_id: string;
  actor_id: string;
  actor_role: string;
};

export type ApiSuccessEnvelope<T> = {
  data: T;
  meta: RequestMeta;
};

export type ApiError = {
  code: string;
  message: string;
  details?: Record<string, unknown> | null;
};

export type ApiErrorEnvelope = {
  error: ApiError;
  meta: Partial<RequestMeta>;
};

export type RankingType = "prompt" | "pattern" | "knowledge" | "rhythm" | "asset";

export type RankingTargetType = "prompt_version" | "pattern" | "knowledge_object" | "rhythm_profile" | "asset";

export type RankingSignalType =
  | "prompt_effectiveness"
  | "pattern_fit"
  | "rhythm_fit"
  | "character_consistency"
  | "world_consistency"
  | "reader_interest"
  | "repetition"
  | "human_edit_distance";

export type RankingSignal = {
  signal_id: string;
  workspace_id: string;
  trace_id: string;
  ranking_type: RankingType;
  target_type: RankingTargetType;
  target_id: string;
  signal_type: RankingSignalType;
  score: number;
  weight: number;
  source: "quality_gate" | "critic" | "human_review" | "system";
  source_feedback_record_id?: string | null;
  summary: string;
  evidence_refs: string[];
  input_refs: string[];
  output_refs: string[];
  created_at: string;
  updated_at?: string | null;
};

export type RankingSuggestion = {
  suggestion_id: string;
  workspace_id: string;
  trace_id: string;
  ranking_type: RankingType;
  target_scope: string;
  status: "review_required" | "approved" | "rejected" | "superseded";
  summary: string;
  recommended_action: string;
  source_signal_ids: string[];
  promoted_from_feedback_record_id?: string | null;
  input_refs: string[];
  output_refs: string[];
  created_at: string;
  updated_at?: string | null;
  promoted_at?: string | null;
};

export type RankingSnapshotItem = {
  rank: number;
  target_type: RankingTargetType;
  target_id: string;
  label: string;
  score: number;
  status: "leading" | "watch" | "deprecated";
  signal_ids: string[];
  summary?: string | null;
};

export type RankingSnapshot = {
  ranking_snapshot_id: string;
  workspace_id: string;
  trace_id: string;
  ranking_type: RankingType;
  scope_ref: string;
  version: number;
  updated_at: string;
  items: RankingSnapshotItem[];
  signals: RankingSignal[];
  suggestions: RankingSuggestion[];
};

export type ConsistencyIssue = {
  issue_id: string;
  category:
    | "character_continuity"
    | "relationship_state"
    | "timeline_continuity"
    | "location_continuity"
    | "power_system_constraint"
    | "artifact_uniqueness"
    | "foreshadowing_constraint"
    | "world_rule";
  severity: "low" | "medium" | "high" | "critical";
  summary: string;
  affected_text_ref: string;
  rule_id: string;
  resolution_status: "open" | "resolved" | "waived";
  input_refs: string[];
  output_refs: string[];
  note?: string | null;
};

export type RuleProfile = {
  rule_id: string;
  workspace_id: string;
  trace_id: string;
  rule_type:
    | "character_continuity"
    | "timeline_continuity"
    | "location_continuity"
    | "power_system_constraint"
    | "artifact_uniqueness"
    | "foreshadowing_constraint"
    | "world_rule";
  title: string;
  severity: "low" | "medium" | "high" | "critical";
  status: "draft" | "approved" | "archived";
  scope_type: "workspace" | "project" | "chapter_plan" | "writing_run" | "knowledge_object";
  scope_ref: string;
  description: string;
  condition_summary: string;
  auto_block: boolean;
  source_refs: string[];
  evidence_refs: string[];
  input_refs: string[];
  output_refs: string[];
  created_at: string;
  updated_at?: string | null;
};

export type ConsistencyReport = {
  consistency_report_id: string;
  workspace_id: string;
  writing_run_id: string;
  trace_id: string;
  task_id: string;
  status: "queued" | "passed" | "blocked" | "requires_review";
  issue_count: number;
  blocking_issue_count: number;
  checked_domains: Array<ConsistencyIssue["category"]>;
  issues: ConsistencyIssue[];
  input_refs: string[];
  output_refs: string[];
  created_at: string;
  updated_at?: string | null;
};

export type RevisionSummary = {
  revision_summary_id: string;
  workspace_id: string;
  writing_run_id: string;
  trace_id: string;
  status: "queued" | "requested" | "revised" | "requires_review" | "blocked" | "accepted";
  revision_round: number;
  max_revision_rounds: number;
  source_issue_ids: string[];
  change_summary: string;
  revision_diff_ref?: string | null;
  reviewer_note_ref?: string | null;
  input_refs: string[];
  output_refs: string[];
  created_at: string;
  updated_at?: string | null;
};

export type PatternStep = {
  index: number;
  summary: string;
};

export type Pattern = {
  schema_version: number;
  pattern_id: string;
  workspace_id: string;
  trace_id: string;
  canonical_name: string;
  pattern_type: string;
  status: "draft" | "approved" | "archived";
  intent: string;
  preconditions: string[];
  steps: PatternStep[];
  slots: string[];
  expected_reader_effect: string;
  compatible_rhythm_profile_id?: string | null;
  evidence_refs: string[];
  created_at: string;
  updated_at?: string | null;
};

export type EmotionCurvePoint = {
  beat: number;
  intensity: number;
  summary: string;
};

export type RhythmProfile = {
  schema_version: number;
  rhythm_profile_id: string;
  workspace_id: string;
  trace_id: string;
  target_id: string;
  status: "draft" | "approved" | "archived";
  label: string;
  climax_index: number;
  conflict_index: number;
  dialogue_ratio: number;
  description_ratio: number;
  battle_ratio: number;
  information_density: number;
  suspense_index: number;
  reward_count: number;
  emotion_curve: EmotionCurvePoint[];
  created_at: string;
  updated_at?: string | null;
};

export type Asset = {
  schema_version: number;
  asset_id: string;
  workspace_id: string;
  trace_id: string;
  asset_type: string;
  canonical_name: string;
  status: "draft" | "approved" | "archived";
  content_summary: string;
  style_tags: string[];
  genre_scope: string;
  usage_context: string;
  constraints: string[];
  expression_type_refs: string[];
  source_refs: string[];
  evidence_refs: string[];
  quality_score: number;
  created_at: string;
  updated_at?: string | null;
};
