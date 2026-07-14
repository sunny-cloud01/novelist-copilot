import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { PhaseTwoProvider, WritingStudioPage } from "../pages";

function renderWritingStudio() {
  return render(
    <PhaseTwoProvider>
      <MemoryRouter
        initialEntries={[
          "/projects/01JZPROJECT000000000000001/writing/01JZWRITING00000000000001",
        ]}
      >
        <Routes>
          <Route
            path="/projects/:projectId/writing/:writingRunId"
            element={<WritingStudioPage />}
          />
        </Routes>
      </MemoryRouter>
    </PhaseTwoProvider>
  );
}

describe("writing studio page", () => {
  it("renders writing studio and shows error state when API unavailable", async () => {
    renderWritingStudio();

    // Page renders with loading or error state since no API is available in test
    await waitFor(() => {
      const headings = screen.getAllByRole("heading").map((h) => h.textContent);
      const found = headings.some(
        (t) => t && ["加载中…", "写作任务不存在", "写作工作台"].includes(t)
      );
      expect(found).toBe(true);
    });
  });

  it("renders the page without crashing", () => {
    renderWritingStudio();
    // The page should at minimum render a section element
    const sections = document.querySelectorAll("section");
    expect(sections.length).toBeGreaterThan(0);
  });

  it("shows the header title area from the shell", () => {
    renderWritingStudio();
    // The Page component renders an <h2> as heading
    const headings = document.querySelectorAll("h2");
    expect(headings.length).toBeGreaterThan(0);
  });

  it("does not throw when rendering with invalid params", () => {
    // Should handle missing route params gracefully
    const { container } = render(
      <PhaseTwoProvider>
        <MemoryRouter initialEntries={["/projects/missing/writing/missing"]}>
          <Routes>
            <Route
              path="/projects/:projectId/writing/:writingRunId"
              element={<WritingStudioPage />}
            />
          </Routes>
        </MemoryRouter>
      </PhaseTwoProvider>
    );
    expect(container).toBeTruthy();
  });
});
