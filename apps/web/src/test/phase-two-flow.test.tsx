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

  it("renders review queue and applies approve action", async () => {
    renderRoute("/knowledge/review");

    fireEvent.click(screen.getAllByRole("button", { name: "通过" })[0]);

    expect(await screen.findByText("已执行审核动作：通过。" )).toBeInTheDocument();
    expect(screen.getByText("Xiao Clan（家族）")).toBeInTheDocument();
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
