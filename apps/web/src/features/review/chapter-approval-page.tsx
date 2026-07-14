import { FormEvent, useEffect, useMemo, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";

import { resolveApiBaseUrl } from "@/lib/api-base";
import { createNovelFactoryApiClient } from "@/lib/api-client";

const statusLabels: Record<string, string> = {
  active: "进行中",
  approved: "已批准",
  completed: "已完成",
  draft: "草稿",
};

function labelOf(labels: Record<string, string>, value: string) {
  return labels[value] ?? value;
}

export function ChapterApprovalPage() {
  const { projectId, writingRunId } = useParams();
  const navigate = useNavigate();
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
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    feedbackNote: "",
    suggestedRefinements: "",
    agreeToUseFeedback: false,
  });

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
        setError(caught instanceof Error ? caught.message : "数据加载失败");
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
  const warnings = (report?.issues ?? []).filter(
    (i: any) => i.type === "warning" || i.type === "suggestion"
  );
  const passedCount = report?.summary?.passed_count ?? 0;

  async function handleApprove(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!apiClient || !projectId || !writingRunId) return;

    setSubmitting(true);
    setError(null);
    try {
      const payload = {
        action: "approve",
        feedback_note: formData.feedbackNote,
        suggested_refinements: formData.suggestedRefinements
          .split("\n")
          .map((s) => s.trim())
          .filter(Boolean),
        agree_to_use_feedback: formData.agreeToUseFeedback,
      };

      await apiClient.approveChapter(projectId, writingRunId, payload);

      // 成功后导航到项目首页
      navigate(`/projects/${projectId}`, {
        replace: true,
        state: { message: "章节已批准并进入正式 Manuscript。" },
      });
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "批准失败");
    } finally {
      setSubmitting(false);
    }
  }

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>章节批准</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>章节批准</h2>
        <p>正在加载章节数据...</p>
      </section>
    );
  }

  if (!run || !report) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>章节批准</h2>
        <p>未找到章节数据。</p>
      </section>
    );
  }

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>章节最终批准</h2>
        <p>审查最终章节内容，确认可进入正式 Manuscript。</p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
      </div>

      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>章节信息</h3>
        <dl>
          <dt>生成运行 ID</dt>
          <dd>{writingRunId}</dd>
          <dt>章节</dt>
          <dd>第 {run?.chapter_index ?? "?"} 章</dd>
          <dt>状态</dt>
          <dd>{labelOf(statusLabels, run?.status)}</dd>
          <dt>字数</dt>
          <dd>
            {run?.word_count ?? "计算中"}
            {run?.target_word_count ? ` / 目标 ${run.target_word_count}` : ""}
          </dd>
          <dt>生成于</dt>
          <dd>{run?.created_at ?? "未记录"}</dd>
        </dl>
      </section>

      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>质量检查摘要</h3>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))",
            gap: 12,
          }}
        >
          <div
            style={{
              textAlign: "center",
              padding: 12,
              backgroundColor: "#f3f4f6",
              borderRadius: 4,
            }}
          >
            <div style={{ fontSize: 24, fontWeight: 600, color: "#10b981" }}>
              ✓
            </div>
            <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>
              {passedCount} 项通过
            </div>
          </div>
          <div
            style={{
              textAlign: "center",
              padding: 12,
              backgroundColor: "#f3f4f6",
              borderRadius: 4,
            }}
          >
            <div style={{ fontSize: 24, fontWeight: 600, color: "#f59e0b" }}>
              {warnings.length}
            </div>
            <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>
              警告或建议
            </div>
          </div>
        </div>

        {warnings.length > 0 ? (
          <div style={{ marginTop: 16 }}>
            <h4>可忽略的问题</h4>
            <ul
              style={{ display: "grid", gap: 8, padding: 0, listStyle: "none" }}
            >
              {warnings.map((issue: any) => (
                <li
                  key={issue.issue_id}
                  style={{
                    padding: 8,
                    backgroundColor: "#fef3c7",
                    borderLeft: "3px solid #f59e0b",
                    borderRadius: 2,
                  }}
                >
                  <div style={{ fontWeight: 500, fontSize: 12 }}>
                    {issue.title}
                  </div>
                  <div style={{ fontSize: 12, color: "#666", marginTop: 2 }}>
                    {issue.description}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </section>

      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>章节内容预览</h3>
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
          }}
        >
          {run?.draft_content ? (
            run.draft_content.substring(0, 500) +
            (run.draft_content.length > 500 ? "..." : "")
          ) : (
            <span style={{ color: "#999" }}>无预览内容</span>
          )}
        </div>
        {run?.draft_content ? (
          <small style={{ display: "block", marginTop: 4, color: "#666" }}>
            显示前 500 字，共 {run.word_count ?? "?"} 字
          </small>
        ) : null}
      </section>

      <form onSubmit={handleApprove}>
        <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
          <h3>批准与反馈</h3>

          <label style={{ display: "grid", gap: 6, marginBottom: 16 }}>
            <span style={{ fontWeight: 600 }}>批准备注</span>
            <textarea
              value={formData.feedbackNote}
              onChange={(e) =>
                setFormData((prev) => ({
                  ...prev,
                  feedbackNote: e.target.value,
                }))
              }
              placeholder="记录批准的关键考量或备注（可选）"
              style={{ minHeight: 80 }}
            />
            <small>这些备注会记录在审计日志中，帮助后续的策略优化。</small>
          </label>

          <label style={{ display: "grid", gap: 6, marginBottom: 16 }}>
            <span style={{ fontWeight: 600 }}>优化建议</span>
            <textarea
              value={formData.suggestedRefinements}
              onChange={(e) =>
                setFormData((prev) => ({
                  ...prev,
                  suggestedRefinements: e.target.value,
                }))
              }
              placeholder="一行一个，例如：需要加强人物心理、节奏过快等"
              style={{ minHeight: 80 }}
            />
            <small>这些建议将进入反馈循环，用于优化后续章节的生成策略。</small>
          </label>

          <label
            style={{
              display: "flex",
              gap: 8,
              alignItems: "center",
              marginBottom: 16,
            }}
          >
            <input
              type="checkbox"
              checked={formData.agreeToUseFeedback}
              onChange={(e) =>
                setFormData((prev) => ({
                  ...prev,
                  agreeToUseFeedback: e.target.checked,
                }))
              }
            />
            <span>同意本次批准和反馈用于优化后续生成策略</span>
          </label>
        </section>

        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <button
            type="submit"
            disabled={submitting}
            style={{
              padding: "10px 20px",
              backgroundColor: "#10b981",
              color: "white",
              border: "none",
              borderRadius: 4,
              cursor: submitting ? "not-allowed" : "pointer",
              opacity: submitting ? 0.5 : 1,
              fontWeight: 600,
            }}
          >
            {submitting ? "批准中..." : "✓ 批准章节并进入 Manuscript"}
          </button>
          <Link
            to={`/projects/${projectId}/writing-runs/${writingRunId}/quality-review`}
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
            返回质量审查
          </Link>
        </div>
      </form>

      <section
        style={{
          border: "1px solid #e5e7eb",
          padding: 12,
          backgroundColor: "#f9fafb",
          borderRadius: 4,
        }}
      >
        <h4>审批流程</h4>
        <ol style={{ fontSize: 12, color: "#666" }}>
          <li>质量检查 ✓</li>
          <li>处理阻塞问题 ✓</li>
          <li>最终批准 ← 当前步骤</li>
          <li>进入 Manuscript 库</li>
          <li>反馈进入优化循环</li>
        </ol>
      </section>
    </section>
  );
}
