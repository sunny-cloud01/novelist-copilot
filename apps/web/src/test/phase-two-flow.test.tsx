import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

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
  vi.restoreAllMocks();
});

describe("phase 2 pages", () => {
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
    expect(screen.getByText("乌坦城萧家少年，正处于天赋跌落后的低谷期。")).toBeInTheDocument();
    expect(screen.getByText("指向Yao Lao · mentored_by · 置信度 0.91")).toBeInTheDocument();
    expect(screen.getByText("evidence://01JZEVIDENCE0000000000001")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Yao Lao（导师）" }));

    expect(await screen.findByText("寄宿戒指中的神秘导师，对主角成长线至关重要。")).toBeInTheDocument();
    expect(screen.getByText("来自Xiao Yan · mentors · 置信度 0.91")).toBeInTheDocument();
  });

  it("keeps unique list keys when activity log repeats entries", async () => {
    render(
      <PhaseTwoProvider>
        <KnowledgeReviewPage />
      </PhaseTwoProvider>,
    );

    fireEvent.click(screen.getAllByRole("button", { name: "通过" })[0]);
    fireEvent.click(await screen.findByRole("button", { name: "通过" }));

    const duplicateKeyWarning = vi.mocked(console.error).mock.calls.some((args) =>
      args.some((value) => String(value).includes("Encountered two children with the same key")),
    );

    expect(duplicateKeyWarning).toBe(false);
  });
});
