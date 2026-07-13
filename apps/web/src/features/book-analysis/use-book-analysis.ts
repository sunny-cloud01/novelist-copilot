import { useCallback, useEffect, useMemo, useState } from "react";

import { ReviewAction } from "../../components/phase-two-state";
import { usePhaseTwo } from "../../state/phase-two-provider";
import { createNovelFactoryApiClient } from "../../lib/api-client";
import { resolveApiBaseUrl } from "../../lib/api-base";

type BookAnalysisState = {
  loading: boolean;
  error: string | null;
  apiAnalysis: any | null;
};

export function useBookAnalysis(bookId?: string) {
  const context = usePhaseTwo();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () => (apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null),
    [apiBaseUrl],
  );
  const activeBookId = bookId ?? context.state.book.bookId;
  const [apiState, setApiState] = useState<BookAnalysisState>({ loading: Boolean(apiClient), error: null, apiAnalysis: null });

  const refresh = useCallback(async () => {
    if (!apiClient) return;
    setApiState((current) => ({ ...current, loading: true, error: null }));
    try {
      const apiAnalysis = await apiClient.getBookAnalysis(activeBookId);
      setApiState({ loading: false, error: null, apiAnalysis });
    } catch (error) {
      setApiState({ loading: false, error: error instanceof Error ? error.message : "Book analysis load failed", apiAnalysis: null });
    }
  }, [activeBookId, apiClient]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  if (!apiClient) {
    return {
      mode: "demo-fallback" as const,
      loading: false,
      error: null,
      book: context.state.book,
      chapters: context.state.chapters,
      run: context.state.run,
      summary: context.state.bookAnalysisSummary,
      exceptions: context.state.analysisExceptions,
      evidenceSamples: context.state.evidences.slice(0, 3),
      knowledgeObjects: context.state.knowledgeObjects,
      scenes: [],
      events: [],
      conflicts: [],
      hooks: [],
      rewards: [],
      climaxes: [],
      relationships: [],
      patterns: context.state.patterns,
      rhythmProfiles: context.state.rhythmProfiles,
      assets: context.state.assets,
      rules: context.state.rules,
      commitRun: context.commitRun,
      applyReviewAction: context.applyReviewAction,
      refresh: () => undefined,
      apiClient: null,
    };
  }

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
      if (analysis?.summary?.run_id) {
        await apiClient.commitKnowledgePackage(analysis.summary.run_id);
        await refresh();
      }
    },
    applyReviewAction: async (objectId: string, action: ReviewAction, targetObjectId?: string) => {
      await apiClient.reviewKnowledgeObject(objectId, { action, target_object_id: targetObjectId });
      await refresh();
    },
    refresh,
    apiClient,
  };
}
