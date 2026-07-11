import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { FeedbackPage, PhaseTwoProvider, WritingStudioPage } from "../pages";

function renderFeedbackPageWithAcceptedChapter() {
  return render(
    <PhaseTwoProvider>
      <MemoryRouter initialEntries={["/projects/01JZPROJECT000000000000001/writing/01JZWRITING00000000000001"]}>
        <Routes>
          <Route path="/projects/:projectId/writing/:writingRunId" element={<WritingStudioPage />} />
        </Routes>
      </MemoryRouter>
      <MemoryRouter initialEntries={["/feedback"]}>
        <Routes>
          <Route path="/feedback" element={<FeedbackPage />} />
        </Routes>
      </MemoryRouter>
    </PhaseTwoProvider>,
  );
}

describe("feedback page", () => {
  it("promotes strategy suggestion from feedback dashboard", () => {
    renderFeedbackPageWithAcceptedChapter();
    fireEvent.click(screen.getByRole("button", { name: "接受本章" }));
    fireEvent.click(screen.getByRole("button", { name: "提升为已批准策略" }));

    expect(screen.getAllByText(/收紧 writer 默认提示中对金手指线索的显性表达。/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/feedback\.record_promoted/).length).toBeGreaterThan(1);
  });
});
