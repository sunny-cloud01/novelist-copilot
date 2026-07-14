import { useCallback, useEffect, useMemo, useState } from "react";

import { ReviewAction } from "../../components/phase-two-state";
import { createNovelFactoryApiClient } from "@/lib/api-client";
import { resolveApiBaseUrl } from "@/lib/api-base";

type BookAnalysisState = {
  loading: boolean;
  error: string | null;
  apiAnalysis: any | null;
};

export function useBookAnalysis(bookId?: string) {
  const apiClient = useMemo(
    () => createNovelFactoryApiClient({ baseUrl: resolveApiBaseUrl()! }),
    // resolveApiBaseUrl always returns the same value at runtime — stable ref
    []
  );
  const activeBookId = bookId ?? "";
  const [apiState, setApiState] = useState<BookAnalysisState>({
    loading: true,
    error: null,
    apiAnalysis: null,
  });

  const refresh = useCallback(async () => {
    if (!apiClient || !activeBookId) return;
    setApiState((current) => ({ ...current, loading: true, error: null }));
    try {
      const apiAnalysis = await apiClient.getBookAnalysis(activeBookId);
      setApiState({ loading: false, error: null, apiAnalysis });
    } catch (error) {
      setApiState({
        loading: false,
        error:
          error instanceof Error ? error.message : "Book analysis load failed",
        apiAnalysis: null,
      });
    }
  }, [activeBookId]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const analysis = apiState.apiAnalysis;
  return {
    mode: "api" as const,
    loading: apiState.loading,
    error: apiState.error,
    book: analysis?.book ?? null,
    chapters: analysis?.chapters ?? [],
    run: analysis?.run ?? null,
    summary: analysis?.summary ?? null,
    exceptions: analysis?.exceptions ?? [],
    evidenceSamples: analysis?.evidence_samples ?? [],
    knowledgeObjects: analysis?.knowledge_objects ?? [],
    scenes: analysis?.scenes ?? [],
    events: analysis?.events ?? [],
    conflicts: analysis?.conflicts ?? [],
    hooks: analysis?.hooks ?? [],
    rewards: analysis?.rewards ?? [],
    climaxes: analysis?.climaxes ?? [],
    relationships: analysis?.relationships ?? [],
    patterns: analysis?.patterns ?? [],
    rhythmProfiles: analysis?.rhythm_profiles ?? [],
    assets: analysis?.assets ?? [],
    rules: analysis?.rules ?? [],
    commitRun: async () => {
      if (analysis?.summary?.run_id && apiClient) {
        await apiClient.commitKnowledgePackage(analysis.summary.run_id);
        await refresh();
      }
    },
    applyReviewAction: async (
      objectId: string,
      action: ReviewAction,
      targetObjectId?: string
    ) => {
      if (!apiClient) return;
      await apiClient.reviewKnowledgeObject(objectId, {
        action,
        target_object_id: targetObjectId,
      });
      await refresh();
    },
    refresh,
    apiClient,
  };
}
