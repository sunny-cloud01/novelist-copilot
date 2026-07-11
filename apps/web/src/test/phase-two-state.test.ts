import { describe, expect, it } from "vitest";

import {
  applyReviewActionToState,
  applyWritingReviewActionToState,
  commitKnowledgePackage,
  createInitialPhaseTwoState,
  createUploadedBook,
  deriveLowConfidenceItems,
  toggleModelProfileInState,
} from "../components/phase-two-state";

describe("phase two state", () => {
  it("creates uploaded source book metadata", () => {
    const book = createUploadedBook("Coiling Dragon", "I Eat Tomatoes", "reference_novel");

    expect(book.title).toBe("Coiling Dragon");
    expect(book.authorName).toBe("I Eat Tomatoes");
    expect(book.importStatus).toBe("uploaded");
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

  it("commits knowledge package into graph stage", () => {
    const committed = commitKnowledgePackage(createInitialPhaseTwoState());

    expect(committed.run.status).toBe("succeeded");
    expect(committed.run.currentStage).toBe("knowledge_base_commit");
    expect(committed.activityLog.at(-1)).toBe("知识包已提交到故事图谱。");
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

  it("accepts whole chapter and passes quality gate", () => {
    const next = applyWritingReviewActionToState(
      createInitialPhaseTwoState(),
      "01JZWRITING00000000000001",
      "01JZSECRUN00000000000002",
      "accept_chapter",
    );

    expect(next.writingRuns[0].status).toBe("succeeded");
    expect(next.writingRuns[0].currentStage).toBe("quality_gate");
    expect(next.writingRuns[0].acceptedChapterRef).toContain("object://manuscripts/");
    expect(next.writingRuns[0].chapterSnapshot?.chapterTitle).toBe("乌坦城风起");
    expect(next.writingRuns[0].manuscriptState?.currentStoryState.qualityGateStatus).toBe("passed");
    expect(next.qualityReports[0].status).toBe("passed");
    expect(next.qualityReports[0].blockingIssues).toHaveLength(0);
    expect(next.feedbackRecords.some((item) => item.feedbackType === "acceptance")).toBe(true);
    expect(next.feedbackRecords.some((item) => item.feedbackType === "cost")).toBe(true);
    expect(next.sectionRunsByWriting["01JZWRITING00000000000001"].every((item) => item.status === "beat_approved")).toBe(true);
  });

  it("disables default profile and reroutes writing telemetry to fallback", () => {
    const next = toggleModelProfileInState(createInitialPhaseTwoState(), "model_profile_default", false);

    expect(next.configurationSnapshot.modelProfiles.find((item) => item.modelProfileId === "model_profile_default")?.enabled).toBe(false);
    expect(next.writingRuns[0].writerModelProfileId).toBe("model_profile_structured_fallback");
    expect(next.writingRuns[0].criticModelProfileId).toBe("model_profile_structured_fallback");
    expect(next.writingRuns[0].humanizerModelProfileId).toBe("model_profile_structured_fallback");
    expect(next.providerCallsByWriting["01JZWRITING00000000000001"][0].modelProfileId).toBe("model_profile_structured_fallback");
    expect(next.providerCallsByWriting["01JZWRITING00000000000001"][2].modelProfileId).toBe("model_profile_structured_fallback");
    expect(next.activityLog.at(-1)).toContain("已禁用模型 profile：model_profile_default");
  });
});
