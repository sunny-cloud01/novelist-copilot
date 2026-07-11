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
  it("renders Chinese dashboard with quality, cost, feedback, and evidence", () => {
    renderFeedbackPageWithAcceptedChapter();
    fireEvent.click(screen.getByRole("button", { name: "接受本章" }));

    expect(screen.getByRole("heading", { name: "反馈看板" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "质量报告摘要" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "成本质量指标" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "反馈记录", level: 3 })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "证据链", level: 3 })).toBeInTheDocument();
    expect(screen.getByText("质量门禁通过后保留了节奏与可读性指标。")).toBeInTheDocument();
    expect(screen.getAllByText("prompt://writer/chapter-default").length).toBeGreaterThan(0);
    expect(screen.getByRole("heading", { name: "章节入稿后状态" })).toBeInTheDocument();
    expect(screen.getAllByText("第 1 章《乌坦城风起》已进入 manuscript，三年之约正式进入主线。").length).toBeGreaterThan(0);
  });
});
