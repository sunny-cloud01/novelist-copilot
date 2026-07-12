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
  it("renders writing studio with phase one review surfaces", () => {
    renderWritingStudio();

    expect(screen.getByRole("heading", { name: "写作工作台" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "左侧：规划与分节" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "中间：草稿与润色" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "右侧：记忆包与质量" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "已选资源" })).toBeInTheDocument();
    expect(screen.getByText("退婚立誓 · conflict_escalation")).toBeInTheDocument();
    expect(screen.getByText("退婚压迫三段式 · suspense 0.74")).toBeInTheDocument();
    expect(screen.getByText("expression · 公开羞辱后主角反击")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "一致性复核" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "修订摘要" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "规则卡片" })).toBeInTheDocument();
    expect(screen.getByText(/境界不能倒退/)).toBeInTheDocument();
    expect(screen.getByText("若当前 draft 中能力状态低于已批准状态，则触发阻断。"))
      .toBeInTheDocument();
    expect(screen.getByText(/主角境界被写回斗之气三段/)).toBeInTheDocument();
    expect(screen.getByText("需先关闭 blocker 并完成修订确认。")).toBeInTheDocument();
  });

  it("applies accept section action from writing studio", () => {
    renderWritingStudio();

    fireEvent.click(screen.getByRole("button", { name: "接受当前 section" }));

    expect(screen.queryByText("阻断 · 主角情绪转折过快，缺少被压迫感铺垫。")).not.toBeInTheDocument();
    expect(screen.getByText("警告 · 金手指暗示可再收敛，避免过早泄露。")).toBeInTheDocument();
  });

  it("blocks chapter acceptance before review actions finish", () => {
    renderWritingStudio();

    fireEvent.click(screen.getByRole("button", { name: "接受本章" }));

    expect(screen.queryByText("已接受")).not.toBeInTheDocument();
    expect(screen.getByText("需先关闭 blocker 并完成修订确认。")).toBeInTheDocument();
    expect(screen.getByText("未解决 · object://drafts/01JZSECRUN00000000000002#p2")).toBeInTheDocument();
  });

  it("accepts chapter after resolve and approve flow", () => {
    renderWritingStudio();

    fireEvent.click(screen.getByRole("button", { name: "标记问题已解决" }));
    fireEvent.click(screen.getByRole("button", { name: "批准草稿" }));
    fireEvent.click(screen.getByRole("button", { name: "接受本章" }));

    expect(screen.getByText("当前可接受本章进入 manuscript。")).toBeInTheDocument();
    expect(screen.getAllByText("已接受").length).toBeGreaterThan(0);
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
