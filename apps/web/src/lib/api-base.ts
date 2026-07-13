export function resolveApiBaseUrl(): string | undefined {
  const explicit = import.meta.env.VITE_NOVEL_FACTORY_API_BASE_URL as string | undefined;
  if (explicit && explicit.trim()) {
    return explicit.trim();
  }
  if (import.meta.env.DEV && import.meta.env.MODE !== "test") {
    return "http://localhost:8080";
  }
  return undefined;
}
