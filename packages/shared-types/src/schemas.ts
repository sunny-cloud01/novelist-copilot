export type TaskStatus =
  | "queued"
  | "running"
  | "retrying"
  | "succeeded"
  | "failed"
  | "cancelled"
  | "requires_review"
  | "blocked";

export type ReviewAction = "approve" | "reject" | "merge_alias" | "request_reextract";

export type WritingReviewAction =
  | "accept_section"
  | "accept_chapter"
  | "request_rewrite"
  | "edit_and_accept"
  | "block_generation";

export type AuditAction =
  | "knowledge.approve"
  | "knowledge.reject"
  | "knowledge.merge_alias"
  | "knowledge.request_reextract"
  | "configuration.model_profile_toggled"
  | "configuration.quality_gate_profile_updated"
  | "configuration.agent_model_assignment_updated"
  | "configuration.prompt_version_updated"
  | "feedback.record_promoted"
  | "writing.accept_chapter";
