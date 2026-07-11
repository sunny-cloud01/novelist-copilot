export type RequestMeta = {
  request_id: string;
  trace_id: string;
  workspace_id: string;
  actor_id: string;
  actor_role: string;
};

export type ApiSuccessEnvelope<T> = {
  data: T;
  meta: RequestMeta;
};

export type ApiError = {
  code: string;
  message: string;
  details?: Record<string, unknown> | null;
};

export type ApiErrorEnvelope = {
  error: ApiError;
  meta: Partial<RequestMeta>;
};
