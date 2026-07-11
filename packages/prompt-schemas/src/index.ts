export type MemoryPackageSummary = {
  memory_package_id: string;
  summary: string;
  source_refs: string[];
};

export type PromptPackageSummary = {
  prompt_package_id: string;
  summary: string;
  template_refs: string[];
};

export type CriticStructuredIssue = {
  issue_id: string;
  severity: "blocking" | "warning";
  category: string;
  summary: string;
  affected_text_ref: string;
};

export type StrategySuggestion = {
  suggestion_id: string;
  based_on_feedback_record_id: string;
  status: "review_required" | "approved" | "rejected";
  target_scope: "prompt" | "router" | "retrieval";
  summary: string;
};
