import type {
  AgentModelAssignmentState,
  ConfigurationSnapshotState,
  ModelProfileState,
  PromptVersionState,
  QualityGateProfileSummaryState,
} from "../components/phase-two-state";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type AnyRecord = Record<string, any>;

function normalizeModelProfile(raw: AnyRecord): ModelProfileState {
  return {
    modelProfileId: raw["model_profile_id"] ?? "",
    providerName: raw["provider_name"] ?? "",
    providerModelName: raw["provider_model_name"] ?? "",
    label: raw["label"] ?? "",
    description: raw["description"] ?? null,
    enabled: raw["enabled"] ?? false,
    supportsStructuredOutput: raw["supports_structured_output"] ?? false,
    fallbackProfileIds: raw["fallback_profile_ids"] ?? [],
  };
}

function normalizeAgentModelAssignment(raw: AnyRecord): AgentModelAssignmentState {
  return {
    assignmentId: raw["assignment_id"] ?? "",
    agentRole: raw["agent_role"] ?? "",
    taskType: raw["task_type"] ?? "",
    outputMode: raw["output_mode"] ?? "",
    modelProfileId: raw["model_profile_id"] ?? "",
    fallbackProfileIds: raw["fallback_profile_ids"] ?? [],
    maxRetry: raw["max_retry"] ?? 1,
    maxCost: raw["max_cost"] ?? 1.0,
    enabled: raw["enabled"] ?? true,
  };
}

function normalizeQualityGateProfile(raw: AnyRecord): QualityGateProfileSummaryState {
  return {
    qualityGateProfileId: raw["quality_gate_profile_id"] ?? "",
    label: raw["label"] ?? "",
    aiFlavorThreshold: raw["ai_flavor_threshold"] ?? 0,
    originalitySafetyThreshold: raw["originality_safety_threshold"] ?? 0,
  };
}

function normalizePromptVersion(raw: AnyRecord): PromptVersionState {
  return {
    agentRole: raw["agent_role"] ?? "",
    templateRef: raw["template_ref"] ?? "",
  };
}

/**
 * Normalize a backend snake_case configuration_snapshot into the frontend
 * camelCase ConfigurationSnapshotState. Returns null if the input is missing
 * or structurally invalid so callers can safely fall back to local reducers.
 */
export function normalizeConfigurationSnapshot(result: unknown): ConfigurationSnapshotState | null {
  if (!result || typeof result !== "object") return null;
  const r = result as AnyRecord;
  const raw = r["configuration_snapshot"];
  if (!raw || typeof raw !== "object") return null;
  const s = raw as AnyRecord;

  if (!Array.isArray(s["model_profiles"])) return null;

  return {
    defaultModelProfileId: s["default_model_profile_id"] ?? "",
    modelProfiles: (s["model_profiles"] as AnyRecord[]).map(normalizeModelProfile),
    agentModelAssignments: Array.isArray(s["agent_model_assignments"])
      ? (s["agent_model_assignments"] as AnyRecord[]).map(normalizeAgentModelAssignment)
      : [],
    qualityGateProfiles: Array.isArray(s["quality_gate_profiles"])
      ? (s["quality_gate_profiles"] as AnyRecord[]).map(normalizeQualityGateProfile)
      : [],
    promptVersions: Array.isArray(s["prompt_versions"])
      ? (s["prompt_versions"] as AnyRecord[]).map(normalizePromptVersion)
      : [],
  };
}
