import { ReactNode, createContext, useContext, useMemo, useState } from "react";

import {
  PhaseTwoState,
  ReviewAction,
  WritingReviewAction,
  applyReviewActionToState,
  applyWritingReviewActionToState,
  commitKnowledgePackage,
  createInitialPhaseTwoState,
  createUploadedBook,
  promoteStrategySuggestionInState,
  toggleModelProfileInState,
  updateAgentAssignmentInState,
  updatePromptVersionInState,
  updateQualityGateProfileInState,
} from "../components/phase-two-state";

export type PhaseTwoContextValue = {
  state: PhaseTwoState;
  uploadBook: (payload: { title: string; authorName: string; sourceType: string }) => void;
  applyReviewAction: (objectId: string, action: ReviewAction, targetObjectId?: string) => void;
  applyWritingReviewAction: (writingRunId: string, sectionRunId: string, action: WritingReviewAction) => void;
  toggleModelProfile: (modelProfileId: string, enabled: boolean) => void;
  updateQualityGateProfile: (qualityGateProfileId: string, aiFlavorThreshold: number, originalitySafetyThreshold: number) => void;
  updateAgentAssignment: (assignmentId: string, modelProfileId: string) => void;
  updatePromptVersion: (agentRole: string, templateRef: string) => void;
  promoteStrategySuggestion: (suggestionId: string) => void;
  commitRun: () => void;
};

const PhaseTwoContext = createContext<PhaseTwoContextValue | null>(null);

export function PhaseTwoProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<PhaseTwoState>(createInitialPhaseTwoState);

  const value = useMemo<PhaseTwoContextValue>(
    () => ({
      state,
      uploadBook: ({ title, authorName, sourceType }) => {
        setState((current) => ({
          ...current,
          book: createUploadedBook(title, authorName, sourceType),
          activityLog: [...current.activityLog, `已上传《${title}》，等待确定性抽取。`],
        }));
      },
      applyReviewAction: (objectId, action, targetObjectId) => {
        setState((current) => applyReviewActionToState(current, objectId, action, targetObjectId));
      },
      applyWritingReviewAction: (writingRunId, sectionRunId, action) => {
        setState((current) => applyWritingReviewActionToState(current, writingRunId, sectionRunId, action));
      },
      toggleModelProfile: (modelProfileId, enabled) => {
        setState((current) => toggleModelProfileInState(current, modelProfileId, enabled));
      },
      updateQualityGateProfile: (qualityGateProfileId, aiFlavorThreshold, originalitySafetyThreshold) => {
        setState((current) =>
          updateQualityGateProfileInState(current, qualityGateProfileId, aiFlavorThreshold, originalitySafetyThreshold),
        );
      },
      updateAgentAssignment: (assignmentId, modelProfileId) => {
        setState((current) => updateAgentAssignmentInState(current, assignmentId, modelProfileId));
      },
      updatePromptVersion: (agentRole, templateRef) => {
        setState((current) => updatePromptVersionInState(current, agentRole, templateRef));
      },
      promoteStrategySuggestion: (suggestionId) => {
        setState((current) => promoteStrategySuggestionInState(current, suggestionId));
      },
      commitRun: () => {
        setState((current) => commitKnowledgePackage(current));
      },
    }),
    [state],
  );

  return <PhaseTwoContext.Provider value={value}>{children}</PhaseTwoContext.Provider>;
}

export function usePhaseTwo() {
  const context = useContext(PhaseTwoContext);
  if (!context) {
    throw new Error("PhaseTwoContext missing");
  }
  return context;
}
