import { describe, expect, it, vi } from "vitest";

import { ApiClientError, createNovelFactoryApiClient } from "../lib/api-client";

function jsonResponse(data: unknown, init: ResponseInit = {}) {
  return new Response(JSON.stringify({
    data,
    request_id: "req-test",
    trace_id: "trace-test",
    workspace_id: "workspace-test",
    actor_id: "actor-test",
    actor_role: "owner",
  }), {
    status: 200,
    headers: { "content-type": "application/json" },
    ...init,
  });
}

describe("NovelFactoryApiClient", () => {
  it("unwraps gateway envelopes for book analysis endpoints", async () => {
    const fetcher = vi.fn().mockResolvedValue(jsonResponse({ book_id: "book-1", title: "Demo" }));
    const client = createNovelFactoryApiClient({ baseUrl: "http://api.local", fetcher });

    const book = await client.getBook("book-1");

    expect(book).toEqual({ book_id: "book-1", title: "Demo" });
    expect(fetcher).toHaveBeenCalledWith("http://api.local/v1/books/book-1");
  });

  it("posts extraction and knowledge commands as JSON", async () => {
    const fetcher = vi.fn()
      .mockResolvedValueOnce(jsonResponse({ run_id: "run-1" }))
      .mockResolvedValueOnce(jsonResponse({ status: "succeeded" }));
    const client = createNovelFactoryApiClient({ fetcher });

    await client.createExtractionRun("book-1");
    await client.commitKnowledgePackage("run-1");

    expect(fetcher).toHaveBeenNthCalledWith(1, "/v1/extraction-runs", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ book_id: "book-1" }),
    });
    expect(fetcher).toHaveBeenNthCalledWith(2, "/v1/extraction-runs/run-1/commit", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({}),
    });
  });

  it("builds project and story bible requests", async () => {
    const fetcher = vi.fn()
      .mockResolvedValueOnce(jsonResponse({ project_id: "project-1", story_bible_id: "story-1" }))
      .mockResolvedValueOnce(jsonResponse({ story_bible_id: "story-1", status: "pending_review" }))
      .mockResolvedValueOnce(jsonResponse({ story_bible_id: "story-1", status: "approved" }));
    const client = createNovelFactoryApiClient({ baseUrl: "http://api.local", fetcher });

    await client.getNovelProject("project-1");
    await client.getStoryBible("story-1");
    await client.reviewStoryBible("story-1", { action: "confirm", summary: "确认候选版本。" });

    expect(fetcher).toHaveBeenNthCalledWith(1, "http://api.local/v1/novel-projects/project-1");
    expect(fetcher).toHaveBeenNthCalledWith(2, "http://api.local/v1/story-bibles/story-1");
    expect(fetcher).toHaveBeenNthCalledWith(3, "http://api.local/v1/story-bibles/story-1/review-actions", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ action: "confirm", summary: "确认候选版本。" }),
    });
  });
  it("builds graph search and evidence requests", async () => {
    const fetcher = vi.fn()
      .mockResolvedValueOnce(jsonResponse({ count: 1, items: [{ node_id: "node-1" }] }))
      .mockResolvedValueOnce(jsonResponse({ evidence_id: "e1", excerpt: "snippet" }));
    const client = createNovelFactoryApiClient({ baseUrl: "http://api.local", fetcher });

    await client.searchGraphNodes({ query: "Yao", nodeType: "mentor", bookId: "book-1" });
    await client.getEvidence("evidence://e1");

    expect(fetcher).toHaveBeenNthCalledWith(1, "http://api.local/v1/graph/search?book_id=book-1&query=Yao&node_type=mentor");
    expect(fetcher).toHaveBeenNthCalledWith(2, "http://api.local/v1/evidence/e1");
  });
});
