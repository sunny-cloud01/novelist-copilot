import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { PhaseTwoProvider, PlannerPage, ProjectHomePage, ProjectListPage, WorkspaceHomePage } from "../pages";

describe("project and planning pages", () => {
  it("renders workspace home with Chinese resource-backed sections", () => {
    render(
      <PhaseTwoProvider>
        <MemoryRouter initialEntries={["/workspaces/demo-workspace"]}>
          <Routes>
            <Route path="/workspaces/:workspaceId" element={<WorkspaceHomePage />} />
          </Routes>
        </MemoryRouter>
      </PhaseTwoProvider>,
    );

    expect(screen.getByRole("heading", { name: "工作台首页" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "工作区信息" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "最近任务" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "待审核项" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "快捷入口" })).toBeInTheDocument();
    expect(screen.getByText("默认中文工作区")).toBeInTheDocument();
    expect(screen.getByText("写作任务进入人工复核。", { exact: false })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "进入配置中心" })).toHaveAttribute("href", "/configuration");
  });

  it("renders project list with detail and planner links", () => {
    render(
      <PhaseTwoProvider>
        <MemoryRouter>
          <ProjectListPage />
        </MemoryRouter>
      </PhaseTwoProvider>,
    );

    expect(screen.getByRole("heading", { name: "小说项目" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "查看项目详情" })).toHaveAttribute(
      "href",
      "/projects/01JZPROJECT000000000000001",
    );
    expect(screen.getByRole("link", { name: "进入章节规划" })).toHaveAttribute(
      "href",
      "/projects/01JZPROJECT000000000000001/planner",
    );
  });

  it("renders project detail with story bible summary", () => {
    render(
      <PhaseTwoProvider>
        <MemoryRouter initialEntries={["/projects/01JZPROJECT000000000000001"]}>
          <Routes>
            <Route path="/projects/:projectId" element={<ProjectHomePage />} />
          </Routes>
        </MemoryRouter>
      </PhaseTwoProvider>,
    );

    expect(screen.getByRole("heading", { name: "项目主页" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "故事圣经摘要" })).toBeInTheDocument();
    expect(screen.getByText("少年背负退婚耻辱后，踏上逆袭与成长之路。")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "进入章节规划器" })).toHaveAttribute(
      "href",
      "/projects/01JZPROJECT000000000000001/planner",
    );
  });

  it("renders planner with section beats and writing entry", () => {
    render(
      <PhaseTwoProvider>
        <MemoryRouter initialEntries={["/projects/01JZPROJECT000000000000001/planner"]}>
          <Routes>
            <Route path="/projects/:projectId/planner" element={<PlannerPage />} />
          </Routes>
        </MemoryRouter>
      </PhaseTwoProvider>,
    );

    expect(screen.getByRole("heading", { name: "章节规划器" })).toBeInTheDocument();
    expect(screen.getByText("第 1 节 · 铺垫")).toBeInTheDocument();
    expect(screen.getByText("主角立下三年之约")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "关联任务" })).toBeInTheDocument();
    expect(screen.getByText("create_chapter_plan · 待复核 · 章节规划已生成，等待确认。", { exact: false })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "任务事件" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "规划审计轨迹" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "进入写作工作台（下一阶段）" })).toBeInTheDocument();
  });
});
