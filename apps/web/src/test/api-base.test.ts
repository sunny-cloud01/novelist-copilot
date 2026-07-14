import { afterEach, describe, expect, it, vi } from "vitest";
import { resolveApiBaseUrl } from "../lib/api-base";

afterEach(() => vi.unstubAllEnvs());

describe("resolveApiBaseUrl", () => {
  it("uses explicit env when set", () => {
    vi.stubEnv("VITE_NOVEL_FACTORY_API_BASE_URL", "http://api.local");
    expect(resolveApiBaseUrl()).toBe("http://api.local");
  });

  it("falls back to localhost gateway in dev mode when env empty", () => {
    vi.stubEnv("VITE_NOVEL_FACTORY_API_BASE_URL", "");
    expect(resolveApiBaseUrl()).toBe("http://localhost:8002");
  });
});
