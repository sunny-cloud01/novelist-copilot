import { fireEvent, render, screen } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { PhaseTwoProvider } from "../pages";
import { routes } from "../router";

function renderConfigurationRoute() {
  const router = createMemoryRouter(routes, { initialEntries: ["/configuration"] });
  return render(
    <PhaseTwoProvider>
      <RouterProvider router={router} />
    </PhaseTwoProvider>,
  );
}

describe("configuration page", () => {
  it("renders Chinese configuration center sections and telemetry", () => {
    renderConfigurationRoute();

    expect(screen.getByRole("heading", { name: "配置中心" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "模型 Profile" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Agent 分配" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "质量阈值" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Prompt 版本与规则" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "最近调用指标" })).toBeInTheDocument();
    expect(screen.getByText("writer · model_profile_default · token 1800/920 · latency 1430ms · retry 0 · cost 0.31 · succeeded")).toBeInTheDocument();
    expect(screen.getByText(/critic · model_profile_default .* structured_output_validation_failed/)).toBeInTheDocument();
  });

  it("shows ranking suggestions separate from governed configuration mutations", () => {
    renderConfigurationRoute();

    expect(screen.getByRole("heading", { name: "Prompt 排名建议与受控变更" })).toBeInTheDocument();
    expect(screen.getByText(/ranking suggestion 仅进入审核队列；正式生效仍需通过配置变更动作。/)).toBeInTheDocument();
    expect(screen.getByText(/切换到 prompt:\/\/writer\/chapter-compact 进行下一轮写作。/)).toBeInTheDocument();
    expect(screen.getByText(/writer · prompt:\/\/writer\/chapter-default/)).toBeInTheDocument();
  });

  it("updates governance records for config mutations", () => {
    renderConfigurationRoute();

    fireEvent.click(screen.getByRole("button", { name: "应用更严格阈值" }));
    fireEvent.click(screen.getByRole("button", { name: "改用 fallback" }));
    fireEvent.click(screen.getByRole("button", { name: "切到紧凑版" }));

    expect(screen.getByText(/AI 味阈值 0.4 · 原创安全阈值 0.9/)).toBeInTheDocument();
    expect(screen.getByText(/writer · text · model_profile_structured_fallback/)).toBeInTheDocument();
    expect(screen.getByText(/writer · prompt:\/\/writer\/chapter-compact/)).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "配置变更记录" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "配置审计轨迹" })).toBeInTheDocument();
    expect(screen.getAllByText(/configuration\.quality_gate_profile_updated/).length).toBeGreaterThan(1);
    expect(screen.getAllByText(/configuration\.prompt_version_updated/).length).toBeGreaterThan(0);
  });
});
