import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { resolveApiBaseUrl } from "@/lib/api-base";
import { createNovelFactoryApiClient } from "@/lib/api-client";

const statusLabels: Record<string, string> = {
  running: "生成中",
  completed: "已完成",
  blocked: "已阻塞",
  failed: "失败",
  approved: "已批准",
};

const pipelineStages = [
  {
    id: "memory_assembly",
    label: "记忆包",
    description: "收集和组织世界观资料",
  },
  { id: "prompt_assembly", label: "提示词", description: "生成写作指导提示词" },
  { id: "writer_draft", label: "初稿生成", description: "AI 生成章节初稿" },
  { id: "critic_review", label: "评论", description: "自动评论检查质量" },
  { id: "humanizer", label: "润色", description: "调整文风和流畅性" },
  { id: "quality_gate", label: "质量门", description: "最终质量检查" },
];

function labelOf(labels: Record<string, string>, value: string) {
  return labels[value] ?? value;
}

function getPipelineStatusColor(status: string) {
  const colors: Record<string, string> = {
    pending: "#d1d5db",
    running: "#3b82f6",
    completed: "#10b981",
    failed: "#ef4444",
    skipped: "#9ca3af",
  };
  return colors[status] ?? "#d1d5db";
}

export function WritingRunDetailPage() {
  const { projectId, writingRunId } = useParams();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );

  const [apiWritingRun, setApiWritingRun] = useState<any | null>(null);
  const [apiProject, setApiProject] = useState<any | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    if (!apiClient || !projectId || !writingRunId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);

    void Promise.all([
      apiClient.getWritingRun(projectId, writingRunId) as Promise<any>,
      apiClient.getNovelProject(projectId) as Promise<any>,
    ])
      .then(([run, project]) => {
        if (cancelled) return;
        setApiWritingRun(run);
        setApiProject(project);
      })
      .catch((caught) => {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "生成运行加载失败");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [apiClient, projectId, writingRunId]);

  // 自动刷新运行中的任务
  useEffect(() => {
    if (
      !apiClient ||
      !projectId ||
      !writingRunId ||
      !autoRefresh ||
      apiWritingRun?.status !== "running"
    ) {
      return;
    }

    const interval = setInterval(() => {
      void (async () => {
        try {
          const run = await apiClient.getWritingRun(projectId, writingRunId);
          setApiWritingRun(run);
        } catch (error) {
          console.error("自动刷新失败:", error);
        }
      })();
    }, 3000); // 每 3 秒刷新一次

    return () => clearInterval(interval);
  }, [apiClient, projectId, writingRunId, autoRefresh, apiWritingRun?.status]);

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>写作生成运行</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>写作生成运行</h2>
        <p>正在加载生成数据...</p>
      </section>
    );
  }

  if (!apiWritingRun) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>写作生成运行</h2>
        <p>未找到该生成运行。</p>
        <Link to={`/projects/${projectId}`}>返回项目</Link>
      </section>
    );
  }

  const run = apiWritingRun;
  const pipeline = run.pipeline_stages ?? [];
  const hasBlockingIssues = run.has_blocking_issues ?? false;
  const progressPercent = run.progress_percent ?? 0;

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>章节生成进度</h2>
        <p>实时跟踪章节生成的各个阶段和进度。</p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>生成运行摘要</CardTitle>
          <CardDescription>
            {run.chapter_index && `第 ${run.chapter_index} 章`}
          </CardDescription>
        </CardHeader>
        <CardContent style={{ display: "grid", gap: 12 }}>
          <dl
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
              gap: 12,
            }}
          >
            <div>
              <dt style={{ fontWeight: 600 }}>生成运行 ID</dt>
              <dd style={{ fontSize: 12, color: "#666" }}>{writingRunId}</dd>
            </div>
            <div>
              <dt style={{ fontWeight: 600 }}>状态</dt>
              <dd
                style={{
                  fontSize: 12,
                  color:
                    run.status === "completed"
                      ? "#10b981"
                      : run.status === "failed"
                        ? "#ef4444"
                        : "#2563eb",
                }}
              >
                {labelOf(statusLabels, run.status)}
              </dd>
            </div>
            <div>
              <dt style={{ fontWeight: 600 }}>目标字数</dt>
              <dd style={{ fontSize: 12, color: "#666" }}>
                {run.target_word_count ?? "未指定"}
              </dd>
            </div>
            <div>
              <dt style={{ fontWeight: 600 }}>当前字数</dt>
              <dd style={{ fontSize: 12, color: "#666" }}>
                {run.word_count ?? "生成中"}
              </dd>
            </div>
            <div>
              <dt style={{ fontWeight: 600 }}>开始时间</dt>
              <dd style={{ fontSize: 12, color: "#666" }}>
                {run.created_at ?? "未记录"}
              </dd>
            </div>
            <div>
              <dt style={{ fontWeight: 600 }}>完成时间</dt>
              <dd style={{ fontSize: 12, color: "#666" }}>
                {run.completed_at ?? "进行中"}
              </dd>
            </div>
          </dl>

          {run.status === "running" ? (
            <div style={{ marginTop: 12 }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginBottom: 4,
                }}
              >
                <span style={{ fontSize: 12, fontWeight: 600 }}>整体进度</span>
                <span style={{ fontSize: 12, color: "#666" }}>
                  {progressPercent}%
                </span>
              </div>
              <div
                style={{
                  width: "100%",
                  height: 24,
                  backgroundColor: "#e5e7eb",
                  borderRadius: 4,
                  overflow: "hidden",
                }}
              >
                <div
                  style={{
                    width: `${progressPercent}%`,
                    height: "100%",
                    backgroundColor: "#3b82f6",
                    transition: "width 0.3s ease-in-out",
                  }}
                />
              </div>
              <label
                style={{
                  marginTop: 8,
                  display: "flex",
                  gap: 6,
                  alignItems: "center",
                  fontSize: 12,
                }}
              >
                <input
                  type="checkbox"
                  checked={autoRefresh}
                  onChange={(e) => setAutoRefresh(e.target.checked)}
                />
                自动刷新（每 3 秒）
              </label>
            </div>
          ) : null}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>生成管道阶段</CardTitle>
          <CardDescription>
            {run.status === "running"
              ? "生成中，每个阶段按顺序执行..."
              : "生成已完成或停止"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            style={{
              display: "grid",
              gap: 12,
            }}
          >
            {pipelineStages.map((stage, index) => {
              const pipelineStage = pipeline.find(
                (p: any) => p.stage_id === stage.id
              ) || {
                stage_id: stage.id,
                status: "pending",
                started_at: null,
                completed_at: null,
              };

              return (
                <div
                  key={stage.id}
                  style={{
                    display: "flex",
                    gap: 12,
                    alignItems: "center",
                    padding: 12,
                    backgroundColor: "#f9fafb",
                    borderRadius: 4,
                  }}
                >
                  <div
                    style={{
                      width: 32,
                      height: 32,
                      borderRadius: "50%",
                      backgroundColor: getPipelineStatusColor(
                        pipelineStage.status
                      ),
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      color: "white",
                      fontSize: 12,
                      fontWeight: 600,
                      flexShrink: 0,
                    }}
                  >
                    {pipelineStage.status === "completed"
                      ? "✓"
                      : pipelineStage.status === "running"
                        ? index + 1
                        : pipelineStage.status === "failed"
                          ? "✗"
                          : "−"}
                  </div>

                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, fontSize: 14 }}>
                      {stage.label}
                    </div>
                    <p
                      style={{
                        fontSize: 12,
                        color: "#666",
                        margin: "2px 0 0 0",
                      }}
                    >
                      {stage.description}
                    </p>
                    <p
                      style={{
                        fontSize: 11,
                        color: "#999",
                        margin: "4px 0 0 0",
                      }}
                    >
                      {pipelineStage.status === "running"
                        ? "生成中..."
                        : pipelineStage.status === "completed"
                          ? `已完成 · ${pipelineStage.completed_at}`
                          : pipelineStage.status === "failed"
                            ? `失败: ${pipelineStage.error_message}`
                            : "等待中"}
                    </p>
                  </div>

                  <div
                    style={{
                      fontSize: 12,
                      fontWeight: 600,
                      color:
                        pipelineStage.status === "completed"
                          ? "#10b981"
                          : pipelineStage.status === "running"
                            ? "#3b82f6"
                            : pipelineStage.status === "failed"
                              ? "#ef4444"
                              : "#999",
                      textTransform: "capitalize",
                    }}
                  >
                    {pipelineStage.status}
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {run.memory_package ? (
        <Card>
          <CardHeader>
            <CardTitle>记忆包（世界观资料）</CardTitle>
            <CardDescription>本次生成的知识库和角色资料快照</CardDescription>
          </CardHeader>
          <CardContent>
            <dl>
              <dt>资料来源</dt>
              <dd>{run.memory_package.source_package_id ?? "不详"}</dd>
              <dt>字符数</dt>
              <dd>{run.memory_package.character_count ?? 0}</dd>
              <dt>包装时间</dt>
              <dd>{run.memory_package.packaged_at ?? "未记录"}</dd>
            </dl>
          </CardContent>
        </Card>
      ) : null}

      {run.prompt_package ? (
        <Card>
          <CardHeader>
            <CardTitle>提示词包</CardTitle>
            <CardDescription>本次生成的写作指导信息</CardDescription>
          </CardHeader>
          <CardContent>
            <dl>
              <dt>关键指令数</dt>
              <dd>{run.prompt_package.directive_count ?? 0}</dd>
              <dt>字符数</dt>
              <dd>{run.prompt_package.character_count ?? 0}</dd>
              <dt>包装时间</dt>
              <dd>{run.prompt_package.packaged_at ?? "未记录"}</dd>
            </dl>
          </CardContent>
        </Card>
      ) : null}

      {run.draft_content ? (
        <Card>
          <CardHeader>
            <CardTitle>初稿内容</CardTitle>
            <CardDescription>生成的章节初稿（前 500 字预览）</CardDescription>
          </CardHeader>
          <CardContent>
            <div
              style={{
                maxHeight: 300,
                overflow: "auto",
                padding: 12,
                backgroundColor: "#f9fafb",
                borderRadius: 4,
                fontFamily: "monospace",
                fontSize: 12,
                lineHeight: 1.6,
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
              }}
            >
              {run.draft_content.substring(0, 500)}
              {run.draft_content.length > 500 ? "..." : ""}
            </div>
            <small style={{ display: "block", marginTop: 8, color: "#666" }}>
              显示前 500 字，共 {run.word_count ?? "?"} 字
            </small>
          </CardContent>
        </Card>
      ) : null}

      {run.status === "completed" || hasBlockingIssues ? (
        <section style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          {hasBlockingIssues ? (
            <Link
              to={`/projects/${projectId}/writing-runs/${writingRunId}/quality-review`}
              style={{
                padding: "10px 20px",
                backgroundColor: "#f59e0b",
                color: "white",
                border: "none",
                borderRadius: 4,
                textDecoration: "none",
                cursor: "pointer",
                fontWeight: 600,
              }}
            >
              处理质量问题
            </Link>
          ) : (
            <Link
              to={`/projects/${projectId}/writing-runs/${writingRunId}/quality-review`}
              style={{
                padding: "10px 20px",
                backgroundColor: "#3b82f6",
                color: "white",
                border: "none",
                borderRadius: 4,
                textDecoration: "none",
                cursor: "pointer",
                fontWeight: 600,
              }}
            >
              进入质量审查
            </Link>
          )}
          <Link
            to={`/projects/${projectId}`}
            style={{
              padding: "10px 20px",
              backgroundColor: "#e5e7eb",
              color: "#1f2937",
              border: "none",
              borderRadius: 4,
              textDecoration: "none",
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            返回项目
          </Link>
        </section>
      ) : null}
    </section>
  );
}
