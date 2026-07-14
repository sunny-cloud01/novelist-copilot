import { render, screen, waitFor } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { PhaseTwoProvider } from "../pages";
import { routes } from "../router";

describe("AppShell", () => {
  it("renders workspace home route from left navigation", async () => {
    const router = createMemoryRouter(routes, {
      initialEntries: ["/workspaces/demo-workspace"],
    });

    render(
      <PhaseTwoProvider>
        <RouterProvider router={router} />
      </PhaseTwoProvider>
    );

    expect(
      screen.getByRole("heading", { name: "工作台首页" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "工作区信息" })
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "上传来源" })).toHaveAttribute(
      "href",
      "/sources"
    );
  });

  it("renders writing studio with API-driven loading state", async () => {
    const router = createMemoryRouter(routes, {
      initialEntries: ["/projects/demo-project/writing/demo-run"],
    });

    render(
      <PhaseTwoProvider>
        <RouterProvider router={router} />
      </PhaseTwoProvider>
    );

    // After API fails in test, page shows error state; while loading shows 加载中…
    await waitFor(() => {
      const headings = screen.getAllByRole("heading").map((h) => h.textContent);
      const found = headings.some(
        (t) => t && ["加载中…", "写作任务不存在", "写作工作台"].includes(t)
      );
      expect(found).toBe(true);
    });
  });

  it("renders sidebar with icon-based lane navigation", async () => {
    const router = createMemoryRouter(routes, {
      initialEntries: ["/workspaces/demo-workspace"],
    });

    render(
      <PhaseTwoProvider>
        <RouterProvider router={router} />
      </PhaseTwoProvider>
    );

    // Sidebar has icon-only links with title tooltips
    expect(
      screen.getByRole("link", { name: "上传参考作品，自动拆解为知识" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "基于知识包生成原创章节" })
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "设置" })).toBeInTheDocument();
    // Header shows the active lane ("拆书" because we're on workspaces)
    expect(
      screen.getByRole("heading", { name: "拆书工作台" })
    ).toBeInTheDocument();
  });

  it("renders knowledge and review routes", async () => {
    for (const [route] of [["/knowledge"], ["/review"], ["/reports"]]) {
      const router = createMemoryRouter(routes, { initialEntries: [route] });

      render(
        <PhaseTwoProvider>
          <RouterProvider router={router} />
        </PhaseTwoProvider>
      );

      // Each page renders an <h2> via the Page component or its own markup
      const headings = screen.getAllByRole("heading");
      expect(headings.length).toBeGreaterThan(0);
    }
  });
});
