import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { resolveApiBaseUrl } from "@/lib/api-base";
import { createNovelFactoryApiClient } from "@/lib/api-client";

const statusLabels: Record<string, string> = {
  passed: "已通过",
  warning: "警告",
  blocking: "阻塞",
  suggestion: "建议",
};

const issueTypeColors: Record<string, string> = {
  blocking: "#ef4444",
  warning: "#f59e0b",
  suggestion: "#3b82f6",
  passed: "#10b981",
};

function labelOf(labels: Record<string, string>, value: string) {
  return labels[value] ?? value;
}

export function QualityReviewPage() {
  const { projectId, writingRunId } = useParams();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );

  const [apiWritingRun, setApiWritingRun] = useState<any | null>(null);
  const [apiQualityReport, setApiQualityReport] = useState<any | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);
  const [selectedIssue, setSelectedIssue] = useState<string | null>(null);
  const [fixingIssue, setFixingIssue] = useState<string | null>(null);

  useEffect(() => {
    if (!apiClient || !projectId || !writingRunId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);

    void Promise.all([
      apiClient.getWritingRun(projectId, writingRunId) as Promise<any>,
      apiClient.getQualityReport(projectId, writingRunId) as Promise<any>,
    ])
      .then(([run, report]) => {
        if (cancelled) return;
        setApiWritingRun(run);
        setApiQualityReport(report);
      })
      .catch((caught) => {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "质量报告加载失败");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [apiClient, projectId, writingRunId]);

  const run = apiWritingRun;
  const report = apiQualityReport;
  const issues = report?.issues ?? [];
  const blockingIssues = issues.filter((i: any) => i.type === "blocking");
  const warningIssues = issues.filter((i: any) => i.type === "warning");
  const suggestions = issues.filter((i: any) => i.type === "suggestion");

  async function handleFixIssue(issueId: string) {
    if (!apiClient || !projectId || !writingRunId) return;
    setFixingIssue(issueId);
    try {
      await apiClient.fixQualityIssue(projectId, writingRunId, {
        issue_id: issueId,
        action: "regenerate_section",
      });
      // 重新加载报告
      const report = await apiClient.getQualityReport(projectId, writingRunId);
      setApiQualityReport(report);
      setSelectedIssue(null);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "修复失败");
    } finally {
      setFixingIssue(null);
    }
  }

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>质量审查</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>质量审查</h2>
        <p>正在加载质量报告...</p>
      </section>
    );
  }

  if (!report) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>质量审查</h2>
        <p>未找到质量报告。</p>
      </section>
    );
  }

  const canApprove = blockingIssues.length === 0;

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>质量审查与问题处理</h2>
        <p>查看自动质量检查结果。处理阻塞问题后可进入批准流程。</p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
      </div>

      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>质量报告摘要</h3>
        <dl>
          <dt>生成运行 ID</dt>
          <dd>{run?.writing_run_id ?? writingRunId}</dd>
          <dt>总问题数</dt>
          <dd>{issues.length}</dd>
          <dt>阻塞问题</dt>
          <dd style={{ color: "#ef4444", fontWeight: 600 }}>
            {blockingIssues.length}
          </dd>
          <dt>警告</dt>
          <dd style={{ color: "#f59e0b" }}>{warningIssues.length}</dd>
          <dt>建议</dt>
          <dd style={{ color: "#3b82f6" }}>{suggestions.length}</dd>
          <dt>审核状态</dt>
          <dd>
            {blockingIssues.length === 0 ? (
              <span style={{ color: "#10b981" }}>✓ 可批准</span>
            ) : (
              <span style={{ color: "#ef4444" }}>✗ 待处理</span>
            )}
          </dd>
        </dl>
      </section>

      {blockingIssues.length > 0 ? (
        <section style={{ border: "2px solid #ef4444", padding: 16 }}>
          <h3 style={{ color: "#dc2626" }}>🚫 阻塞问题</h3>
          <p>必须处理这些问题后才能批准章节。</p>
          <ul
            style={{ display: "grid", gap: 12, padding: 0, listStyle: "none" }}
          >
            {blockingIssues.map((issue: any) => (
              <li
                key={issue.issue_id}
                style={{
                  border: `2px solid ${issueTypeColors.blocking}`,
                  padding: 12,
                  borderRadius: 4,
                  cursor: "pointer",
                  backgroundColor:
                    selectedIssue === issue.issue_id
                      ? "#fef2f2"
                      : "transparent",
                }}
                onClick={() =>
                  setSelectedIssue(
                    selectedIssue === issue.issue_id ? null : issue.issue_id
                  )
                }
              >
                <div style={{ fontWeight: 600 }}>{issue.title}</div>
                <p style={{ margin: "8px 0 0 0" }}>{issue.description}</p>

                {selectedIssue === issue.issue_id ? (
                  <div
                    style={{
                      marginTop: 12,
                      paddingTop: 12,
                      borderTop: "1px solid #fecaca",
                    }}
                  >
                    {issue.evidence ? (
                      <div style={{ marginBottom: 12 }}>
                        <strong>冲突证据：</strong>
                        <p
                          style={{
                            fontSize: 12,
                            fontStyle: "italic",
                            margin: "4px 0",
                            color: "#666",
                          }}
                        >
                          "{issue.evidence}"
                        </p>
                      </div>
                    ) : null}

                    {issue.suggested_fix ? (
                      <div style={{ marginBottom: 12 }}>
                        <strong>修复建议：</strong>
                        <p
                          style={{
                            fontSize: 12,
                            margin: "4px 0",
                            color: "#666",
                          }}
                        >
                          {issue.suggested_fix}
                        </p>
                      </div>
                    ) : null}

                    <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                      <button
                        type="button"
                        onClick={() => handleFixIssue(issue.issue_id)}
                        disabled={fixingIssue !== null}
                        style={{
                          padding: "6px 12px",
                          backgroundColor: "#ef4444",
                          color: "white",
                          border: "none",
                          borderRadius: 4,
                          cursor:
                            fixingIssue !== null ? "not-allowed" : "pointer",
                          opacity: fixingIssue !== null ? 0.5 : 1,
                        }}
                      >
                        {fixingIssue === issue.issue_id
                          ? "重新生成中..."
                          : "重新生成此部分"}
                      </button>
                      <button
                        type="button"
                        style={{
                          padding: "6px 12px",
                          backgroundColor: "#f5f5f5",
                          color: "#333",
                          border: "1px solid #ddd",
                          borderRadius: 4,
                          cursor: "pointer",
                        }}
                      >
                        查看详情
                      </button>
                    </div>
                  </div>
                ) : null}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      {warningIssues.length > 0 ? (
        <section style={{ border: "1px solid #fbbf24", padding: 16 }}>
          <h3 style={{ color: "#d97706" }}>⚠️ 警告（可忽略）</h3>
          <ul
            style={{ display: "grid", gap: 12, padding: 0, listStyle: "none" }}
          >
            {warningIssues.map((issue: any) => (
              <li
                key={issue.issue_id}
                style={{
                  border: "1px solid #fcd34d",
                  padding: 12,
                  borderRadius: 4,
                }}
              >
                <div style={{ fontWeight: 600 }}>{issue.title}</div>
                <p style={{ margin: "4px 0" }}>{issue.description}</p>
                {issue.suggested_fix ? (
                  <small style={{ color: "#666" }}>
                    建议：{issue.suggested_fix}
                  </small>
                ) : null}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      {suggestions.length > 0 ? (
        <section style={{ border: "1px solid #93c5fd", padding: 16 }}>
          <h3 style={{ color: "#2563eb" }}>💡 建议（可选）</h3>
          <ul
            style={{ display: "grid", gap: 12, padding: 0, listStyle: "none" }}
          >
            {suggestions.map((issue: any) => (
              <li
                key={issue.issue_id}
                style={{
                  border: "1px solid #bfdbfe",
                  padding: 12,
                  borderRadius: 4,
                }}
              >
                <div style={{ fontWeight: 600 }}>{issue.title}</div>
                <p style={{ margin: "4px 0" }}>{issue.description}</p>
                {issue.suggested_fix ? (
                  <small style={{ color: "#666" }}>{issue.suggested_fix}</small>
                ) : null}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <section style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        {canApprove ? (
          <Link
            to={`/projects/${projectId}/writing-runs/${writingRunId}/approval`}
            style={{
              padding: "8px 16px",
              backgroundColor: "#10b981",
              color: "white",
              border: "none",
              borderRadius: 4,
              textDecoration: "none",
              cursor: "pointer",
            }}
          >
            继续进入批准流程
          </Link>
        ) : (
          <button
            disabled
            style={{
              padding: "8px 16px",
              backgroundColor: "#d1d5db",
              color: "#6b7280",
              border: "none",
              borderRadius: 4,
              cursor: "not-allowed",
            }}
          >
            请先处理所有阻塞问题
          </button>
        )}
        <Link
          to={`/projects/${projectId}/writing-runs/${writingRunId}`}
          style={{
            padding: "8px 16px",
            backgroundColor: "#e5e7eb",
            color: "#1f2937",
            border: "none",
            borderRadius: 4,
            textDecoration: "none",
            cursor: "pointer",
          }}
        >
          返回写作运行
        </Link>
      </section>
    </section>
  );
}
