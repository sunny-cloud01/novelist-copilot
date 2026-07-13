import { fireEvent, render, screen } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import { PhaseTwoProvider } from "../state/phase-two-provider";
import { routes } from "../router";

function renderRoute(initialEntry: string) {
  const router = createMemoryRouter(routes, { initialEntries: [initialEntry] });
  return render(
    <PhaseTwoProvider>
      <RouterProvider router={router} />
    </PhaseTwoProvider>,
  );
}

function apiEnvelope(data: unknown) {
  return {
    data,
    request_id: "req-api",
    trace_id: "trace-api",
    workspace_id: "workspace-api",
    actor_id: "actor-api",
    actor_role: "owner",
  };
}

afterEach(() => {
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
});

describe("BookAnalysisCenterPage", () => {
  it("renders creator-facing book analysis center", () => {
    renderRoute("/sources/01JZBOOK000000000000000001/analysis");

    expect(screen.getByRole("heading", { name: "自动拆书完成，只处理异常" })).toBeInTheDocument();
    expect(screen.getByText("Auto analysis run")).toBeInTheDocument();
    expect(screen.getByText("写作逻辑与节奏")).toBeInTheDocument();
    expect(screen.getByText("Evidence sample")).toBeInTheDocument();
    expect(screen.getByText("Knowledge Package")).toBeInTheDocument();
    expect(screen.getByText("Needs attention")).toBeInTheDocument();
    expect(screen.getByText(/萧炎沉默地站在大厅中央/)).toBeInTheDocument();
  });

  it("commits knowledge from analysis center", async () => {
    renderRoute("/sources/01JZBOOK000000000000000001/analysis");

    fireEvent.click(screen.getByRole("button", { name: "Commit Knowledge" }));

    expect(await screen.findByText("succeeded")).toBeInTheDocument();
  });

  it("renders real API analysis when API base URL is configured", async () => {
    vi.stubEnv("VITE_NOVEL_FACTORY_API_BASE_URL", "http://api.local");
    const fetcher = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify(apiEnvelope({
        schema_version: 1,
        book: {
          book_id: "book-real",
          title: "真实上传书",
          author_name: "作者",
          source_type: "reference_novel",
          import_status: "ready",
        },
        run: { run_id: "run-real", status: "requires_review", current_stage: "quality_review" },
        chapters: [{ chapter_id: "chapter-real", chapter_index: 1, title: "真实章节" }],
        summary: {
          book_id: "book-real",
          run_id: "run-real",
          status: "requires_review",
          current_stage: "quality_review",
          chapter_count: 1,
          scene_count: 1,
          knowledge_object_count: 1,
          evidence_count: 1,
          pattern_count: 0,
          rhythm_profile_count: 0,
          asset_count: 0,
          rule_count: 0,
          needs_attention_count: 1,
          can_commit_knowledge: true,
        },
        exceptions: [{
          exception_id: "exception-real",
          type: "low_confidence_object",
          severity: "warning",
          title: "真实对象需要确认",
          summary: "真实对象证据需要确认。",
          target_ref: "object://knowledge-objects/object-real",
          evidence_refs: ["evidence://evidence-real"],
          recommended_action: "approve_or_reextract",
        }],
        evidence_samples: [{
          evidence_id: "evidence-real",
          evidence_ref: "evidence://evidence-real",
          chapter_index: 1,
          text_range: "c1:p1-p1",
          excerpt: "真实上传文本里的证据片段。",
          confidence: 0.91,
        }],
        knowledge_objects: [],
      }))),
    );

    renderRoute("/sources/book-real/analysis");

    expect(await screen.findByText(/真实上传书/)).toBeInTheDocument();
    expect(screen.queryByText("Battle Through the Heavens")).not.toBeInTheDocument();
    expect(screen.getByText(/真实上传文本里的证据片段/)).toBeInTheDocument();
    expect(fetcher).toHaveBeenCalledWith("http://api.local/v1/books/book-real/analysis");
  });
});
