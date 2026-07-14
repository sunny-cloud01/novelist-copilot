import axios, { type AxiosInstance } from "axios";

export type ApiEnvelope<T> = {
  data: T;
  request_id: string;
  trace_id: string;
  workspace_id: string;
  actor_id: string;
  actor_role: string;
};

export class ApiClientError extends Error {
  constructor(
    message: string,
    readonly status?: number
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

export type ApiClientOptions = {
  baseUrl?: string;
};

export class NovelFactoryApiClient {
  private readonly http: AxiosInstance;

  constructor(options: ApiClientOptions = {}) {
    this.http = axios.create({
      baseURL: options.baseUrl ?? "",
      headers: { "content-type": "application/json" },
      timeout: 30000,
    });

    this.http.interceptors.response.use(
      (response) => {
        const envelope = response.data as ApiEnvelope<unknown>;
        return { ...response, data: envelope.data };
      },
      (error) => {
        if (axios.isAxiosError(error) && error.response) {
          throw new ApiClientError(
            `API request failed with status ${error.response.status}`,
            error.response.status
          );
        }
        throw error;
      }
    );
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
    return this.get(
      `/v1/knowledge-objects?run_id=${encodeURIComponent(runId)}`
    );
  }

  async reviewKnowledgeObject(
    objectId: string,
    payload: { action: string; target_object_id?: string; note?: string }
  ) {
    return this.post(
      `/v1/knowledge-objects/${objectId}/review-actions`,
      payload
    );
  }

  async listKnowledgeSources(
    params: { workspace_id?: string; status?: string } = {}
  ) {
    const search = new URLSearchParams();
    if (params.workspace_id) search.set("workspace_id", params.workspace_id);
    if (params.status) search.set("status", params.status);
    const suffix = search.toString() ? `?${search.toString()}` : "";
    return this.get(`/v1/knowledge-sources${suffix}`);
  }

  async listNovelProjects() {
    return this.get("/v1/novel-projects");
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

  async getWritingRun(writingRunId: string) {
    return this.get(`/v1/writing-runs/${writingRunId}`);
  }

  async postWritingReviewAction(
    writingRunId: string,
    payload: {
      schema_version?: number;
      action: string;
      requested_by: string;
      trace_id: string;
      issue_id?: string;
      note?: string;
      output_ref?: string;
    }
  ) {
    return this.post(
      `/v1/writing-runs/${writingRunId}/review-actions`,
      payload
    );
  }

  async acceptChapter(writingRunId: string) {
    return this.post(`/v1/writing-runs/${writingRunId}/accept-chapter`, {});
  }

  async getStoryBible(storyBibleId: string) {
    return this.get(`/v1/story-bibles/${storyBibleId}`);
  }

  async reviewStoryBible(
    storyBibleId: string,
    payload: {
      action: string;
      summary?: string;
      note?: string;
      story_bible_payload?: Record<string, unknown>;
    }
  ) {
    return this.post(
      `/v1/story-bibles/${storyBibleId}/review-actions`,
      payload
    );
  }

  async getGraphSummary(bookId?: string) {
    const suffix = bookId ? `?book_id=${encodeURIComponent(bookId)}` : "";
    return this.get(`/v1/graph/summary${suffix}`);
  }

  async searchGraphNodes(
    params: { bookId?: string; query?: string; nodeType?: string } = {}
  ) {
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

  async getConfiguration() {
    return this.get("/v1/configuration");
  }

  async setModelProfileEnabled(modelProfileId: string, enabled: boolean) {
    const action = enabled ? "enable" : "disable";
    return this.post(`/v1/model-profiles/${modelProfileId}/${action}`, {});
  }

  async updateAgentAssignment(
    assignmentId: string,
    {
      modelProfileId,
      maxRetry,
      maxCost,
      enabled,
    }: {
      modelProfileId: string;
      maxRetry: number;
      maxCost: number;
      enabled: boolean;
    }
  ) {
    return this.post(`/v1/agent-model-assignments/${assignmentId}`, {
      model_profile_id: modelProfileId,
      max_retry: maxRetry,
      max_cost: maxCost,
      enabled,
    });
  }

  async updateQualityGateProfile(
    profileId: string,
    aiFlavorThreshold: number,
    originalitySafetyThreshold: number
  ) {
    return this.post(`/v1/quality-gate-profiles/${profileId}`, {
      ai_flavor_threshold: aiFlavorThreshold,
      originality_safety_threshold: originalitySafetyThreshold,
    });
  }

  private async get<T = unknown>(path: string): Promise<T> {
    const { data } = await this.http.get<T>(path);
    return data;
  }

  private async post<T = unknown>(path: string, body: unknown): Promise<T> {
    const { data } = await this.http.post<T>(path, body);
    return data;
  }
}

export function createNovelFactoryApiClient(options?: ApiClientOptions) {
  return new NovelFactoryApiClient(options);
}
