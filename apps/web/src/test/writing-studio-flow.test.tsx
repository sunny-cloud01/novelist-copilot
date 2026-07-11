import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { PhaseTwoProvider, WritingStudioPage } from "../pages";

function renderWritingStudio() {
  return render(
    <PhaseTwoProvider>
      <MemoryRouter initialEntries={["/projects/01JZPROJECT000000000000001/writing/01JZWRITING00000000000001"]}>
        <Routes>
          <Route path="/projects/:projectId/writing/:writingRunId" element={<WritingStudioPage />} />
        </Routes>
      </MemoryRouter>
    </PhaseTwoProvider>,
  );
}

describe("writing studio page", () => {
  it("renders writing studio with Chinese panels and quality data", () => {
    renderWritingStudio();

    expect(screen.getByRole("heading", { name: "写作工作台" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "左侧：规划与分节" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "中间：草稿与润色" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "右侧：记忆包与质量" })).toBeInTheDocument();
    expect(screen.getByText("已拦截")).toBeInTheDocument();
    expect(screen.getByText("阻断 · 主角情绪转折过快，缺少被压迫感铺垫。")).toBeInTheDocument();
  });

  it("applies accept section action from writing studio", () => {
    renderWritingStudio();

    fireEvent.click(screen.getByRole("button", { name: "接受当前 section" }));

    expect(screen.queryByText("阻断 · 主角情绪转折过快，缺少被压迫感铺垫。")).not.toBeInTheDocument();
    expect(screen.getByText("警告 · 金手指暗示可再收敛，避免过早泄露。")).toBeInTheDocument();
  });

  it("applies accept chapter action and unlocks quality gate", () => {
    renderWritingStudio();

    fireEvent.click(screen.getByRole("button", { name: "接受本章" }));

    expect(screen.getAllByText("已通过").length).toBeGreaterThan(0);
    expect(screen.getByText("记忆包")).toBeInTheDocument();
    expect(screen.getByText("当前阶段")).toBeInTheDocument();
    expect(screen.getAllByText("质量门禁").length).toBeGreaterThan(0);
    expect(screen.getByText("已接受")).toBeInTheDocument();
    expect(screen.getByText("章节快照")).toBeInTheDocument();
    expect(screen.getByText("最新故事状态")).toBeInTheDocument();
    expect(screen.getByText("人物与关系更新")).toBeInTheDocument();
    expect(screen.getByText("伏笔与前情摘要")).toBeInTheDocument();
    expect(screen.getByText("乌坦城风起")).toBeInTheDocument();
    expect(screen.getByText("第 1 章《乌坦城风起》已进入 manuscript，三年之约正式进入主线。")).toBeInTheDocument();
    expect(screen.getByText("object://manuscripts/01JZWRITING00000000000001/chapters/1")).toBeInTheDocument();
    expect(screen.getByText("acceptance · 1 · 人工复核已接受本章进入 manuscript。")).toBeInTheDocument();
  });
});
