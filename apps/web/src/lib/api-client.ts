export type ApiEnvelope<T> = {
  data: T;
  request_id: string;
  trace_id: string;
  workspace_id: string;
  actor_id: string;
  actor_role: string;
};

export type ApiClientOptions = {
  baseUrl?: string;
  fetcher?: typeof fetch;
};

export class ApiClientError extends Error {
  constructor(message: string, readonly status?: number) {
    super(message);
    this.name = "ApiClientError";
  }
}

export class NovelFactoryApiClient {
  private readonly baseUrl: string;
  private readonly fetcher: typeof fetch;

  constructor(options: ApiClientOptions = {}) {
    this.baseUrl = options.baseUrl ?? "";
    this.fetcher = options.fetcher ?? fetch;
  }

  async createBook(payload: {
    title: string;
    author_name: string;
    source_type: string;
    workspace_id?: string;
    platform?: string;
    genre?: string;
    usage_boundary?: string;
    source_text?: string;
  }) {
    return this.post("/v1/books", payload);
  }

  async getBook(bookId: string) {
    return this.get(`/v1/books/${bookId}`);
  }

  async listBookChapters(bookId: string) {
    return this.get(`/v1/books/${bookId}/chapters`);
  }

  async getBookContent(bookId: string) {
    return this.get(`/v1/books/${bookId}/content`);
  }

  async listBookEvidence(bookId: string) {
    return this.get(`/v1/books/${bookId}/evidence`);
  }

  async getBookAnalysis(bookId: string) {
    return this.get(`/v1/books/${bookId}/analysis`);
  }

  async getEvidence(evidenceIdOrRef: string) {
    const evidenceId = evidenceIdOrRef.replace(/^evidence:\/\//, "");
    return this.get(`/v1/evidence/${encodeURIComponent(evidenceId)}`);
  }

  async createExtractionRun(bookId: string) {
    return this.post("/v1/extraction-runs", { book_id: bookId });
  }

  async getExtractionRun(runId: string) {
    return this.get(`/v1/extraction-runs/${runId}`);
  }

  async getExtractionReport(runId: string) {
    return this.get(`/v1/extraction-runs/${runId}/report`);
  }

  async commitKnowledgePackage(runId: string) {
    return this.post(`/v1/extraction-runs/${runId}/commit`, {});
  }

  async listKnowledgeObjects(runId: string) {
    return this.get(`/v1/knowledge-objects?run_id=${encodeURIComponent(runId)}`);
  }

  async reviewKnowledgeObject(objectId: string, payload: { action: string; target_object_id?: string; note?: string }) {
    return this.post(`/v1/knowledge-objects/${objectId}/review-actions`, payload);
  }

  async listKnowledgeSources(params: { workspace_id?: string; status?: string } = {}) {
    const search = new URLSearchParams();
    if (params.workspace_id) search.set("workspace_id", params.workspace_id);
    if (params.status) search.set("status", params.status);
    const suffix = search.toString() ? `?${search.toString()}` : "";
    return this.get(`/v1/knowledge-sources${suffix}`);
  }

  async createNovelProject(payload: {
    title: string;
    genre_scope: string;
    workspace_id?: string;
    quality_gate_profile_id?: string;
    allowed_knowledge_source_refs?: string[];
    story_bible_payload?: Record<string, unknown>;
  }) {
    return this.post("/v1/novel-projects", payload);
  }

  async getNovelProject(projectId: string) {
    return this.get(`/v1/novel-projects/${projectId}`);
  }

  async getStoryBible(storyBibleId: string) {
    return this.get(`/v1/story-bibles/${storyBibleId}`);
  }

  async reviewStoryBible(
    storyBibleId: string,
    payload: { action: string; summary?: string; note?: string; story_bible_payload?: Record<string, unknown> },
  ) {
    return this.post(`/v1/story-bibles/${storyBibleId}/review-actions`, payload);
  }

  async getGraphSummary(bookId?: string) {
    const suffix = bookId ? `?book_id=${encodeURIComponent(bookId)}` : "";
    return this.get(`/v1/graph/summary${suffix}`);
  }

  async searchGraphNodes(params: { bookId?: string; query?: string; nodeType?: string } = {}) {
    const search = new URLSearchParams();
    if (params.bookId) search.set("book_id", params.bookId);
    if (params.query) search.set("query", params.query);
    if (params.nodeType) search.set("node_type", params.nodeType);
    const suffix = search.toString() ? `?${search.toString()}` : "";
    return this.get(`/v1/graph/search${suffix}`);
  }

  async getGraphNode(nodeId: string) {
    return this.get(`/v1/graph/nodes/${nodeId}`);
  }

  async getGraphNeighbors(nodeId: string) {
    return this.get(`/v1/graph/nodes/${nodeId}/neighbors`);
  }

  private async get<T = unknown>(path: string): Promise<T> {
    const response = await this.fetcher(`${this.baseUrl}${path}`);
    return this.parseResponse<T>(response);
  }

  private async post<T = unknown>(path: string, body: unknown): Promise<T> {
    const response = await this.fetcher(`${this.baseUrl}${path}`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
    });
    return this.parseResponse<T>(response);
  }

  private async parseResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      throw new ApiClientError(`API request failed with status ${response.status}`, response.status);
    }
    const envelope = (await response.json()) as ApiEnvelope<T>;
    return envelope.data;
  }
}

export function createNovelFactoryApiClient(options?: ApiClientOptions) {
  return new NovelFactoryApiClient(options);
}
