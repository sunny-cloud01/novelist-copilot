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
    expect(screen.getByRole("link", { name: "工作台首页" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "反馈看板" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "配置中心" })).toBeInTheDocument();
  });
});
