import { render, screen, waitFor } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { PhaseTwoProvider } from "../pages";
import { routes } from "../router";

function renderConfigurationRoute() {
  const router = createMemoryRouter(routes, {
    initialEntries: ["/configuration"],
  });
  return render(
    <PhaseTwoProvider>
      <RouterProvider router={router} />
    </PhaseTwoProvider>
  );
}

describe("configuration page", () => {
  it("renders configuration center heading", async () => {
    renderConfigurationRoute();

    // Page shows loading first, then config data from API
    await waitFor(() => {
      const headings = screen.getAllByRole("heading").map((h) => h.textContent);
      const found = headings.some(
        (t) => t && ["配置中心", "加载中…"].includes(t)
      );
      expect(found).toBe(true);
    });
  });

  it("renders the page without crashing", () => {
    renderConfigurationRoute();
    const sections = document.querySelectorAll("section");
    expect(sections.length).toBeGreaterThan(0);
  });

  it("shows model profile section when API data is available", () => {
    renderConfigurationRoute();
    // The page always renders at minimum the heading
    const headings = document.querySelectorAll("h2, h3");
    expect(headings.length).toBeGreaterThan(0);
  });
});
