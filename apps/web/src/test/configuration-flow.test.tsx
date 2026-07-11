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

  it("disables default profile and updates routing record", () => {
    renderConfigurationRoute();

    fireEvent.click(screen.getAllByRole("button", { name: "禁用" })[0]);

    expect(screen.getByText("writer · model_profile_structured_fallback · token 1800/920 · latency 1430ms · retry 0 · cost 0.31 · succeeded")).toBeInTheDocument();
    expect(screen.getByText("humanizer · model_profile_structured_fallback · token 1780/850 · latency 1210ms · retry 0 · cost 0.33 · succeeded")).toBeInTheDocument();
    expect(screen.getByText(/默认 profile 已关闭/)).toBeInTheDocument();
  });
});
