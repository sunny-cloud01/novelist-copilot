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

export type WritingHumanReviewAction =
  | "approve_draft"
  | "request_revision"
  | "reject_draft"
  | "edit_draft"
  | "mark_issue_resolved"
  | "create_rule_update_request";

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
  | "feedback.ranking_suggestion_approved"
  | "writing.accept_chapter"
  | "writing.request_revision"
  | "writing.issue_resolved"
  | "writing.rule_update_requested";
