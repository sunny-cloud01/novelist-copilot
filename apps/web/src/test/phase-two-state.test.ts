import { describe, expect, it } from "vitest";

import {
  applyReviewActionToState,
  applyWritingReviewActionToState,
  commitKnowledgePackage,
  createInitialPhaseTwoState,
  createUploadedBook,
  deriveAnalysisExceptions,
  deriveLowConfidenceItems,
  findEvidenceByRef,
  getBookAnalysisSummary,
  promoteStrategySuggestionInState,
  toggleModelProfileInState,
  updateAgentAssignmentInState,
  updatePromptVersionInState,
  updateQualityGateProfileInState,
} from "../components/phase-two-state";

describe("phase two state", () => {
  it("creates book analysis summary with evidence and exception mappings", () => {
    const initial = createInitialPhaseTwoState();
    const summary = getBookAnalysisSummary(initial, initial.book.bookId);
    const evidence = findEvidenceByRef(initial, "evidence://01JZEVIDENCE0000000000002");
    const exceptions = deriveAnalysisExceptions(initial);

    expect(summary?.sceneCount).toBe(6);
    expect(summary?.patternCount).toBe(1);
    expect(summary?.canCommitKnowledge).toBe(true);
    expect(initial.chapterAnalysis[0].conflictIndex).toBeGreaterThan(0.7);
    expect(evidence?.excerpt).toContain("药老");
    expect(exceptions).toHaveLength(2);
    expect(exceptions[0].targetRef).toContain("object://knowledge-objects/");
  });

  it("syncs analysis summary when knowledge is reviewed and committed", () => {
    const initial = createInitialPhaseTwoState();
    const reviewed = applyReviewActionToState(initial, "01JZOBJ0000000000000000001", "approve");
    const committed = commitKnowledgePackage(reviewed);

    expect(reviewed.bookAnalysisSummary.needsAttentionCount).toBe(1);
    expect(reviewed.analysisExceptions).toHaveLength(1);
    expect(committed.bookAnalysisSummary.status).toBe("succeeded");
    expect(committed.bookAnalysisSummary.currentStage).toBe("knowledge_base_commit");
    expect(committed.bookAnalysisSummary.canCommitKnowledge).toBe(false);
  });

  it("finds evidence by ref or raw id", () => {
    const initial = createInitialPhaseTwoState();

    expect(findEvidenceByRef(initial, "evidence://01JZEVIDENCE0000000000002")?.excerpt).toContain("药老");
    expect(findEvidenceByRef(initial, "01JZEVIDENCE0000000000002")?.excerpt).toContain("药老");
  });


  it("resolves low-confidence queue after approvals", () => {
    const initial = createInitialPhaseTwoState();
    const afterFirst = applyReviewActionToState(initial, "01JZOBJ0000000000000000001", "approve");
    const afterSecond = applyReviewActionToState(afterFirst, "01JZOBJ0000000000000000002", "approve");

    expect(deriveLowConfidenceItems(afterFirst.knowledgeObjects)).toHaveLength(1);
    expect(deriveLowConfidenceItems(afterSecond.knowledgeObjects)).toHaveLength(0);
    expect(afterSecond.run.status).toBe("succeeded");
    expect(afterSecond.run.currentStage).toBe("knowledge_package_export");
  });

  it("requeues extraction run when reextract is requested", () => {
    const next = applyReviewActionToState(createInitialPhaseTwoState(), "01JZOBJ0000000000000000001", "request_reextract");

    expect(next.knowledgeObjects.find((item) => item.objectId === "01JZOBJ0000000000000000001")?.reviewStatus).toBe("reextract_requested");
    expect(next.run.status).toBe("queued");
    expect(next.run.currentStage).toBe("source_submission");
    expect(next.run.lowConfidenceCount).toBe(1);
  });

  it("accepts current writing section and clears critic issues", () => {
    const next = applyWritingReviewActionToState(
      createInitialPhaseTwoState(),
      "01JZWRITING00000000000001",
      "01JZSECRUN00000000000002",
      "accept_section",
    );

    const updated = next.sectionRunsByWriting["01JZWRITING00000000000001"][1];
    expect(updated.status).toBe("beat_approved");
    expect(updated.criticIssues).toHaveLength(0);
    expect(updated.beatStatus.every((beat) => beat.status === "beat_approved")).toBe(true);
  });

  it("blocks direct chapter acceptance until review dependencies clear", () => {
    const next = applyWritingReviewActionToState(
      createInitialPhaseTwoState(),
      "01JZWRITING00000000000001",
      "01JZSECRUN00000000000002",
      "accept_chapter",
    );

    expect(next.writingRuns[0].status).toBe("requires_review");
    expect(next.writingRuns[0].acceptedChapterRef).toBeNull();
    expect(next.activityLog.at(-1)).toBe("一致性或修订仍未完成，暂不能接受本章。");
  });

  it("resolves blocker then approves draft before chapter acceptance", () => {
    const resolved = applyWritingReviewActionToState(
      createInitialPhaseTwoState(),
      "01JZWRITING00000000000001",
      "01JZSECRUN00000000000002",
      "mark_issue_resolved",
    );
    const approved = applyWritingReviewActionToState(
      resolved,
      "01JZWRITING00000000000001",
      "01JZSECRUN00000000000002",
      "approve_draft",
    );
    const accepted = applyWritingReviewActionToState(
      approved,
      "01JZWRITING00000000000001",
      "01JZSECRUN00000000000002",
      "accept_chapter",
    );

    expect(resolved.consistencyReports[0].blockingIssueCount).toBe(0);
    expect(resolved.revisionSummaries[0].status).toBe("revised");
    expect(resolved.qualityReports[0].status).toBe("requires_review");
    expect(approved.qualityReports[0].humanReviewRequired).toBe(false);
    expect(approved.revisionSummaries[0].status).toBe("accepted");
    expect(accepted.writingRuns[0].status).toBe("succeeded");
    expect(accepted.writingRuns[0].currentStage).toBe("quality_gate");
    expect(accepted.writingRuns[0].acceptedChapterRef).toContain("object://manuscripts/");
    expect(accepted.writingRuns[0].chapterSnapshot?.chapterTitle).toBe("乌坦城风起");
    expect(accepted.writingRuns[0].manuscriptState?.currentStoryState.qualityGateStatus).toBe("passed");
    expect(accepted.qualityReports[0].status).toBe("passed");
    expect(accepted.qualityReports[0].blockingIssues).toHaveLength(0);
    expect(accepted.feedbackRecords.some((item) => item.feedbackType === "acceptance")).toBe(true);
    expect(accepted.feedbackRecords.some((item) => item.feedbackType === "cost")).toBe(true);
    expect(accepted.sectionRunsByWriting["01JZWRITING00000000000001"].every((item) => item.status === "beat_approved")).toBe(true);
  });

  it("records unique ids for repeated model toggles", () => {
    const initial = createInitialPhaseTwoState();
    const once = toggleModelProfileInState(initial, "model_profile_default", true);
    const twice = toggleModelProfileInState(once, "model_profile_default", true);

    expect(twice.configurationMutations.at(-2)?.mutationId).not.toBe(twice.configurationMutations.at(-1)?.mutationId);
    expect(twice.auditEvents.at(-2)?.auditEventId).not.toBe(twice.auditEvents.at(-1)?.auditEventId);
    expect(twice.auditEvents.at(-1)?.requestId).toContain("-2");
  });

  it("keeps prompt ranking snapshot while promotion only changes suggestion approval state", () => {
    const initial = createInitialPhaseTwoState();
    const next = promoteStrategySuggestionInState(initial, "01JZSTRAT000000000000001");

    expect(initial.rankingSnapshots[0].rankingType).toBe("prompt");
    expect(initial.rankingSnapshots[0].items[0].targetId).toBe("prompt://writer/chapter-default");
    expect(initial.rankingSnapshots[0].suggestions[0].summary).toBe("收紧 writer 默认提示中对金手指线索的显性表达。");
    expect(next.rankingSnapshots[0]).toEqual(initial.rankingSnapshots[0]);
    expect(next.strategySuggestions[0].status).toBe("approved");
    expect(next.strategySuggestions[0].promotedAt).toBe("2026-07-11T03:13:00Z");
    expect(next.auditEvents.at(-1)?.inputRefs).toEqual([
      `object://feedback-records/${next.strategySuggestions[0].basedOnFeedbackRecordId}`,
    ]);
  });
  it("records audit and mutation entries for governance actions", () => {
    const initial = createInitialPhaseTwoState();
    const afterQuality = updateQualityGateProfileInState(initial, "01JZQUALITY00000000000001", 0.4, 0.9);
    const afterAssignment = updateAgentAssignmentInState(
      afterQuality,
      "01JZASSIGN000000000000006",
      "model_profile_structured_fallback",
    );
    const afterPrompt = updatePromptVersionInState(afterAssignment, "writer", "prompt://writer/chapter-compact");
    const afterPromotion = promoteStrategySuggestionInState(afterPrompt, "01JZSTRAT000000000000001");

    expect(afterPromotion.configurationSnapshot.qualityGateProfiles[0].aiFlavorThreshold).toBe(0.4);
    expect(
      afterPromotion.configurationSnapshot.agentModelAssignments.find((item) => item.assignmentId === "01JZASSIGN000000000000006")
        ?.modelProfileId,
    ).toBe("model_profile_structured_fallback");
    expect(
      afterPromotion.configurationSnapshot.promptVersions.find((item) => item.agentRole === "writer")?.templateRef,
    ).toBe("prompt://writer/chapter-compact");
    expect(afterPromotion.strategySuggestions[0].status).toBe("approved");
    expect(afterPromotion.configurationMutations.at(-1)?.mutationType).toBe("feedback_record_promoted");
    expect(afterPromotion.auditEvents.at(-1)?.action).toBe("feedback.record_promoted");
  });
});
