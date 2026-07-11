import { render, screen } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { routes } from "../router";

describe("AppShell", () => {
  it("renders route-complete writing studio shell with left navigation", async () => {
    const router = createMemoryRouter(routes, {
      initialEntries: ["/projects/demo-project/writing/demo-run"],
    });

    render(<RouterProvider router={router} />);

    expect(screen.getByRole("heading", { name: "Writing Studio" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Workspace Home" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Feedback Dashboard" })).toBeInTheDocument();
  });
});
