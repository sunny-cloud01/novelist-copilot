export type BadgeTone = "neutral" | "success" | "warning" | "danger";

export function taskStatusBadgeTone(status: string): BadgeTone {
  if (status === "succeeded") return "success";
  if (status === "blocked" || status === "failed") return "danger";
  if (status === "requires_review" || status === "retrying") return "warning";
  return "neutral";
}

export function formatTraceLinks(refs: string[]): string[] {
  return refs.filter(Boolean);
}
