import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { createMemoryRouter, MemoryRouter, RouterProvider } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { SourceLibraryPage } from "../features/sources/source-library-page";
import { KnowledgeReviewPage, PhaseTwoProvider } from "../pages";
import { routes } from "../router";

function renderRoute(initialEntry: string) {
  const router = createMemoryRouter(routes, { initialEntries: [initialEntry] });
  return render(
    <PhaseTwoProvider>
      <RouterProvider router={router} />
    </PhaseTwoProvider>,
  );
}

afterEach(() => {
  cleanup();
});

beforeEach(() => {
  vi.spyOn(console, "error").mockImplementation(() => undefined);
});

afterEach(() => {
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
});

describe("phase 2 pages", () => {
  it("renders productized source upload entry", async () => {
    renderRoute("/sources");

    expect(screen.getByRole("heading", { name: "上传参考作品，自动拆书学习" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Upload and Analyze" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "继续分析中心" })).toHaveAttribute(
      "href",
      "/sources/01JZBOOK000000000000000001/analysis",
    );
    expect(screen.getByLabelText("选择 TXT 文件")).toHaveAttribute("accept", ".txt,text/plain");
    expect(screen.getByText("Usage boundary")).toBeInTheDocument();
  });

  it("uploads source text through API and navigates to real analysis route", async () => {
    vi.stubEnv("VITE_NOVEL_FACTORY_API_BASE_URL", "http://api.local");
    const fetcher = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: { book_id: "book-real" } })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: { run_id: "run-real" } })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: {
        book: { book_id: "book-real", title: "API Book", author_name: "Author", source_type: "reference_novel" },
        summary: { book_id: "book-real", status: "queued", current_stage: "source_submission", can_commit_knowledge: false },
        chapters: [],
        run: null,
        exceptions: [],
        evidence_samples: [],
        knowledge_objects: [],
      } })));
    render(
      <PhaseTwoProvider>
        <MemoryRouter>
          <SourceLibraryPage />
        </MemoryRouter>
      </PhaseTwoProvider>,
    );

    fireEvent.submit(screen.getByRole("form", { name: "上传来源书籍" }));

    await waitFor(() => expect(fetcher).toHaveBeenCalledTimes(2));
    expect(fetcher).toHaveBeenNthCalledWith(1, "http://api.local/v1/books", expect.objectContaining({
      method: "POST",
      body: expect.stringContaining("source_text"),
    }));
    expect(fetcher).toHaveBeenNthCalledWith(2, "http://api.local/v1/extraction-runs", expect.objectContaining({
      method: "POST",
      body: JSON.stringify({ book_id: "book-real" }),
    }));
  });

  it("reads txt file content into source_text before API upload", async () => {
    vi.stubEnv("VITE_NOVEL_FACTORY_API_BASE_URL", "http://api.local");
    const fetcher = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: { book_id: "book-file" } })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: { run_id: "run-file" } })));
    const file = new File(["第一章 文件上传\n主角打开旧卷。"], "novel.txt", { type: "text/plain" });
    Object.defineProperty(file, "text", { value: () => Promise.resolve("第一章 文件上传\n主角打开旧卷。") });

    render(
      <PhaseTwoProvider>
        <MemoryRouter>
          <SourceLibraryPage />
        </MemoryRouter>
      </PhaseTwoProvider>,
    );

    fireEvent.change(screen.getByLabelText("选择 TXT 文件"), { target: { files: [file] } });
    expect(await screen.findByText("已读取 novel.txt，可继续编辑文本。")).toBeInTheDocument();
    expect(screen.getByRole("textbox", { name: /TXT 文件内容/ })).toHaveValue("第一章 文件上传\n主角打开旧卷。");
    fireEvent.submit(screen.getByRole("form", { name: "上传来源书籍" }));

    await waitFor(() => expect(fetcher).toHaveBeenCalledTimes(2));
    expect(fetcher).toHaveBeenNthCalledWith(1, "http://api.local/v1/books", expect.objectContaining({
      body: expect.stringContaining("第一章 文件上传"),
    }));
  });

  it("rejects non-txt file uploads", async () => {
    const file = new File(["%PDF"], "novel.pdf", { type: "application/pdf" });

    render(
      <PhaseTwoProvider>
        <MemoryRouter>
          <SourceLibraryPage />
        </MemoryRouter>
      </PhaseTwoProvider>,
    );

    fireEvent.change(screen.getByLabelText("选择 TXT 文件"), { target: { files: [file] } });

    expect(await screen.findByRole("alert")).toHaveTextContent("仅支持 .txt 文本文件。");
  });

  it("renders extraction run detail and commits package in place", async () => {
    renderRoute("/extraction-runs/01JZRUN0000000000000000001");

    expect(screen.getByText("质量复核")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "提交知识包" }));

    expect(await screen.findByText("知识库提交")).toBeInTheDocument();
  });

  it("requeues extraction run from review page", async () => {
    renderRoute("/knowledge/review");

    fireEvent.click(screen.getAllByRole("button", { name: "请求重抽" })[0]);

    expect(await screen.findByText("已执行审核动作：请求重抽。" )).toBeInTheDocument();
    expect(screen.getByText("来源提交")).toBeInTheDocument();
  });

  it("shows graph node detail, neighbors, and evidence", async () => {
    renderRoute("/graph");

    expect(screen.getByText("节点详情")).toBeInTheDocument();
    expect(screen.getByText("候选")).toBeInTheDocument();
    expect(screen.getByText("待处理")).toBeInTheDocument();
    expect(screen.getByText("乌坦城萧家少年，正处于天赋跌落后的低谷期。", { selector: "p" })).toBeInTheDocument();
    expect(screen.getByText("指向Yao Lao · mentored_by · 置信度 0.91")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "evidence://01JZEVIDENCE0000000000001" })).toBeInTheDocument();
    expect(screen.getByText(/萧炎沉默地站在大厅中央/)).toBeInTheDocument();

    fireEvent.change(screen.getByRole("textbox", { name: "搜索图谱节点" }), { target: { value: "Yao" } });
    fireEvent.click(screen.getByRole("button", { name: "Yao Lao（导师）" }));

    expect(await screen.findByText("寄宿戒指中的神秘导师，对主角成长线至关重要。", { selector: "p" })).toBeInTheDocument();
    expect(screen.getByText("来自Xiao Yan · mentors · 置信度 0.91")).toBeInTheDocument();
    expect(screen.getByText(/戒指中传来苍老的低笑/)).toBeInTheDocument();
  });

  it("loads graph search and evidence jump from API", async () => {
    vi.stubEnv("VITE_NOVEL_FACTORY_API_BASE_URL", "http://api.local");
    const fetcher = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: { count: 1, items: [{ node_id: "node-mentor", label: "Yao Lao", node_type: "mentor", evidence_refs: ["evidence://evidence-mentor"] }] } })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: { node_id: "node-mentor", label: "Yao Lao", node_type: "mentor", canonical_object_id: "obj-mentor", review_status: "approved", lifecycle_status: "approved", confidence: 0.91, aliases: ["药老"], summary: "寄宿戒指中的神秘导师，对主角成长线至关重要。", evidence_refs: ["evidence://evidence-mentor"] } })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: { node_id: "node-mentor", items: [{ edge_id: "edge-1", direction: "incoming", neighbor_label: "Xiao Yan", relation_type: "mentors", confidence: 0.91 }] } })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: { evidence_id: "evidence-mentor", book_id: "book-real", chapter_id: "chapter-2", chapter_index: 2, text_range: "c2:p4-p8", excerpt: "戒指中传来苍老的低笑，药老第一次点破少年体内异变的根源。", source_object_refs: ["object://knowledge-objects/obj-mentor"], confidence: 0.91, trace_id: "trace-api" } })));

    renderRoute("/graph");

    expect(await screen.findByText("寄宿戒指中的神秘导师，对主角成长线至关重要。", { selector: "p" })).toBeInTheDocument();
    expect(screen.getByText(/戒指中传来苍老的低笑/)).toBeInTheDocument();
    expect(fetcher).toHaveBeenNthCalledWith(1, "http://api.local/v1/graph/search");
    fireEvent.change(screen.getByRole("textbox", { name: "搜索图谱节点" }), { target: { value: "Yao" } });
    expect(await screen.findByText("Yao Lao（导师）")).toBeInTheDocument();
    expect(fetcher).toHaveBeenCalledWith("http://api.local/v1/graph/search?query=Yao");
  });

});
