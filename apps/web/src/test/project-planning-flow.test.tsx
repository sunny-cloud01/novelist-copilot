import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import { StoryBibleWizardPage } from "../features/projects/story-bible-wizard-page";
import { PhaseTwoProvider, PlannerPage, ProjectHomePage, ProjectListPage, WorkspaceHomePage } from "../pages";

afterEach(() => {
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
});

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

  it("loads story bible detail from API and confirms candidate", async () => {
    vi.stubEnv("VITE_NOVEL_FACTORY_API_BASE_URL", "http://api.local");
    const fetcher = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: {
        project: {
          project_id: "project-real",
          title: "API 项目",
          genre_scope: "东方玄幻",
          status: "planning",
          quality_gate_profile_id: "quality-real",
          story_bible_id: "story-real",
        },
        story_bible: {
          story_bible_id: "story-real",
          project_id: "project-real",
          version: 2,
          status: "pending_review",
          payload: {
            premise: "新前提",
            protagonist: "林澈",
            core_conflict: "新冲突",
            style_target: "稳步升级",
            forbidden_similarities: "不复刻原作名场面",
            world_rules: ["突破需要代价"],
            narrative_promises: ["前三章完成立誓"],
          },
          diff: {
            from_version: 1,
            to_version: 2,
            summary: "补强世界规则。",
            changed_fields: ["world_rules", "narrative_promises"],
          },
          history: [
            { version: 1, status: "draft", change_type: "create", summary: "创建初始故事圣经。", created_at: "2026-07-10T10:00:00Z" },
            { version: 2, status: "pending_review", change_type: "regenerate", summary: "补强世界规则。", created_at: "2026-07-10T10:05:00Z" },
          ],
          approved_at: null,
          approved_by: null,
          trace_id: "trace-story-real",
        },
        chapter_plans: [],
      } })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: {
        story_bible_id: "story-real",
        project_id: "project-real",
        version: 2,
        status: "pending_review",
        payload: {
          premise: "新前提",
          protagonist: "林澈",
          core_conflict: "新冲突",
          style_target: "稳步升级",
          forbidden_similarities: "不复刻原作名场面",
          world_rules: ["突破需要代价"],
          narrative_promises: ["前三章完成立誓"],
        },
        diff: {
          from_version: 1,
          to_version: 2,
          summary: "补强世界规则。",
          changed_fields: ["world_rules", "narrative_promises"],
        },
        history: [
          { version: 1, status: "draft", change_type: "create", summary: "创建初始故事圣经。", created_at: "2026-07-10T10:00:00Z" },
          { version: 2, status: "pending_review", change_type: "regenerate", summary: "补强世界规则。", created_at: "2026-07-10T10:05:00Z" },
        ],
        approved_at: null,
        approved_by: null,
        trace_id: "trace-story-real",
      } })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: {
        story_bible_id: "story-real",
        project_id: "project-real",
        version: 2,
        status: "approved",
        payload: {
          premise: "新前提",
          protagonist: "林澈",
          core_conflict: "新冲突",
          style_target: "稳步升级",
          forbidden_similarities: "不复刻原作名场面",
          world_rules: ["突破需要代价"],
          narrative_promises: ["前三章完成立誓"],
        },
        confirmed_payload: {
          premise: "新前提",
          protagonist: "林澈",
          core_conflict: "新冲突",
        },
        diff: null,
        history: [
          { version: 1, status: "draft", change_type: "create", summary: "创建初始故事圣经。", created_at: "2026-07-10T10:00:00Z" },
          { version: 2, status: "pending_review", change_type: "regenerate", summary: "补强世界规则。", created_at: "2026-07-10T10:05:00Z" },
          { version: 2, status: "approved", change_type: "confirm", summary: "确认候选版本。", created_at: "2026-07-10T10:06:00Z" },
        ],
        approved_at: "2026-07-10T10:06:00Z",
        approved_by: "demo-user",
        trace_id: "trace-story-real",
      } }))) ;

    render(
      <PhaseTwoProvider>
        <MemoryRouter initialEntries={["/projects/project-real"]}>
          <Routes>
            <Route path="/projects/:projectId" element={<ProjectHomePage />} />
          </Routes>
        </MemoryRouter>
      </PhaseTwoProvider>,
    );

    expect(await screen.findByText("候选变更")).toBeInTheDocument();
    expect(screen.getByText("补强世界规则。" )).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "确认候选版本" }));

    await waitFor(() => expect(fetcher).toHaveBeenCalledTimes(3));
    expect(fetcher).toHaveBeenNthCalledWith(1, "http://api.local/v1/novel-projects/project-real");
    expect(fetcher).toHaveBeenNthCalledWith(2, "http://api.local/v1/story-bibles/story-real");
    expect(fetcher).toHaveBeenNthCalledWith(3, "http://api.local/v1/story-bibles/story-real/review-actions", expect.objectContaining({
      method: "POST",
      body: JSON.stringify({ action: "confirm", summary: "补强世界规则。", note: "" }),
    }));
    expect(await screen.findByText("候选版本已确认。" )).toBeInTheDocument();
    expect(screen.getByText("已通过")).toBeInTheDocument();
  });

});
