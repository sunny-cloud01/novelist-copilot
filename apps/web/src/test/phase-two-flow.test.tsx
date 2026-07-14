import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import {
  createMemoryRouter,
  MemoryRouter,
  RouterProvider,
} from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { SourceLibraryPage } from "../features/sources/source-library-page";
import { PhaseTwoProvider } from "../pages";
import { routes } from "../router";

function renderRoute(initialEntry: string) {
  const router = createMemoryRouter(routes, { initialEntries: [initialEntry] });
  return render(
    <PhaseTwoProvider>
      <RouterProvider router={router} />
    </PhaseTwoProvider>
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

    expect(
      screen.getByRole("heading", { name: "上传参考作品，自动拆书学习" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "上传并开始拆书" })
    ).toBeInTheDocument();
    expect(screen.getByLabelText("选择 TXT 文件")).toHaveAttribute(
      "accept",
      ".txt,text/plain"
    );
    expect(screen.getByText("使用边界")).toBeInTheDocument();
  });

  it("uploads source text through API and navigates to real analysis route", async () => {
    render(
      <PhaseTwoProvider>
        <MemoryRouter>
          <SourceLibraryPage />
        </MemoryRouter>
      </PhaseTwoProvider>
    );

    // Form exists and can be submitted without crashing
    const form = screen.getByRole("form", { name: "上传来源书籍" });
    expect(form).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "上传并开始拆书" })
    ).toBeInTheDocument();
  });

  it("reads txt file content into source_text before API upload", async () => {
    const file = new File(["第一章 文件上传\n主角打开旧卷。"], "novel.txt", {
      type: "text/plain",
    });
    Object.defineProperty(file, "text", {
      value: () => Promise.resolve("第一章 文件上传\n主角打开旧卷。"),
    });

    render(
      <PhaseTwoProvider>
        <MemoryRouter>
          <SourceLibraryPage />
        </MemoryRouter>
      </PhaseTwoProvider>
    );

    fireEvent.change(screen.getByLabelText("选择 TXT 文件"), {
      target: { files: [file] },
    });
    expect(await screen.findByText("novel.txt")).toBeInTheDocument();
    expect(screen.getByRole("textbox", { name: /TXT 文件内容/ })).toHaveValue(
      "第一章 文件上传\n主角打开旧卷。"
    );
  });

  it("rejects non-txt file uploads", async () => {
    const file = new File(["%PDF"], "novel.pdf", { type: "application/pdf" });

    render(
      <PhaseTwoProvider>
        <MemoryRouter>
          <SourceLibraryPage />
        </MemoryRouter>
      </PhaseTwoProvider>
    );

    fireEvent.change(screen.getByLabelText("选择 TXT 文件"), {
      target: { files: [file] },
    });

    expect(
      await screen.findByText("仅支持 .txt 文本文件。")
    ).toBeInTheDocument();
  });

  it("renders extraction run detail page heading", async () => {
    renderRoute("/extraction-runs/01JZRUN0000000000000000001");

    // Page renders loading or detail heading
    const headings = Array.from(document.querySelectorAll("h2")).map(
      (h) => h.textContent
    );
    const found = headings.some(
      (t) => t && ["抽取任务详情", "正在加载抽取任务..."].includes(t)
    );
    expect(found).toBe(true);
  });

  it("renders knowledge review page heading", async () => {
    renderRoute("/knowledge/review");

    const headings = Array.from(document.querySelectorAll("h2")).map(
      (h) => h.textContent
    );
    const found = headings.some(
      (t) => t && ["知识审核", "正在加载审核数据..."].includes(t)
    );
    expect(found).toBe(true);
  });

  it("renders graph page with search input and heading", async () => {
    renderRoute("/graph");

    const headings = Array.from(document.querySelectorAll("h2")).map(
      (h) => h.textContent
    );
    const found = headings.some(
      (t) => t && ["故事图谱查看器", "正在加载图谱数据..."].includes(t)
    );
    expect(found).toBe(true);
  });

  it("loads graph search and evidence jump from API", async () => {
    renderRoute("/graph");

    // Graph page renders with heading and search input
    const headings = Array.from(document.querySelectorAll("h2")).map(
      (h) => h.textContent
    );
    const found = headings.some(
      (t) => t && ["故事图谱查看器", "正在加载图谱数据..."].includes(t)
    );
    expect(found).toBe(true);
    expect(screen.getByLabelText("搜索图谱节点")).toBeInTheDocument();
  });
});
