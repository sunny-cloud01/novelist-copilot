import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { FeedbackPage, PhaseTwoProvider } from "../pages";

function renderFeedbackPage() {
  return render(
    <PhaseTwoProvider>
      <MemoryRouter initialEntries={["/feedback"]}>
        <Routes>
          <Route path="/feedback" element={<FeedbackPage />} />
        </Routes>
      </MemoryRouter>
    </PhaseTwoProvider>
  );
}

describe("feedback page", () => {
  it("renders feedback dashboard header and sections", () => {
    renderFeedbackPage();

    expect(
      screen.getByRole("heading", { name: "反馈看板" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "质量报告摘要" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "成本质量指标" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Prompt 排名" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Ranking signals" })
    ).toBeInTheDocument();
  });

  it("shows empty state for prompt rankings when no data", () => {
    renderFeedbackPage();
    expect(screen.getByText("暂无 prompt 排名快照。")).toBeInTheDocument();
  });

  it("shows manuscript state section with no data message", () => {
    renderFeedbackPage();
    expect(screen.getByText("当前章节尚未进入正文稿。")).toBeInTheDocument();
  });
});
