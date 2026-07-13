import { render, screen } from "@testing-library/react";
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
      </PhaseTwoProvider>,
    );

    expect(screen.getByRole("heading", { name: "工作台首页" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "工作区信息" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "进入来源书库" })).toHaveAttribute("href", "/sources");
  });

  it("renders route-complete writing studio shell with left navigation", async () => {
    const router = createMemoryRouter(routes, {
      initialEntries: ["/projects/demo-project/writing/demo-run"],
    });

    render(
      <PhaseTwoProvider>
        <RouterProvider router={router} />
      </PhaseTwoProvider>,
    );

    expect(screen.getByRole("heading", { name: "写作工作台" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Home/ })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Reports/ })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Settings/ })).toBeInTheDocument();
  });

  it("renders productized creator navigation", async () => {
    const router = createMemoryRouter(routes, {
      initialEntries: ["/workspaces/demo-workspace"],
    });

    render(
      <PhaseTwoProvider>
        <RouterProvider router={router} />
      </PhaseTwoProvider>,
    );

    for (const label of ["Home", "Sources", "Knowledge", "Projects", "Writing", "Review", "Reports", "Settings"]) {
      expect(screen.getByRole("link", { name: new RegExp(label) })).toBeInTheDocument();
    }
    expect(screen.getByRole("link", { name: /Reports/ })).toHaveAttribute("href", "/reports");
    expect(screen.getByRole("link", { name: /Settings/ })).toHaveAttribute("href", "/settings");
    expect(screen.getByText("少输入，自动运行，只在异常和关键确认处打断。")).toBeInTheDocument();
  });

  it("renders productized knowledge review and reports routes", async () => {
    for (const [route, heading] of [
      ["/knowledge", "可复用知识资产"],
      ["/review", "只处理必须打断的事项"],
      ["/reports", "成本、质量与反馈报告"],
    ]) {
      const router = createMemoryRouter(routes, { initialEntries: [route] });

      render(
        <PhaseTwoProvider>
          <RouterProvider router={router} />
        </PhaseTwoProvider>,
      );

      expect(await screen.findByRole("heading", { name: heading })).toBeInTheDocument();
    }
  });
});
