import { FormEvent, useEffect, useMemo, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { createNovelFactoryApiClient } from "@/lib/api-client";
import { resolveApiBaseUrl } from "@/lib/api-base";

const statusLabels: Record<string, string> = {
  active: "进行中",
  approved: "已批准",
  draft: "草稿",
  pending: "待处理",
};

function labelOf(labels: Record<string, string>, value: string) {
  return labels[value] ?? value;
}

export function ChapterDirectionSetupPage() {
  const { projectId, chapterIndex } = useParams();
  const navigate = useNavigate();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );

  const [apiProject, setApiProject] = useState<any | null>(null);
  const [apiChapterPlan, setApiChapterPlan] = useState<any | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    chapterGoal: "",
    targetWordCount: "3000",
    mainConflict: "",
    rewardOrHook: "",
    emotionalDirection: "",
    mustInclude: "",
    mustNotChange: "",
  });

  useEffect(() => {
    if (!apiClient || !projectId || !chapterIndex) return;
    let cancelled = false;
    setLoading(true);
    setError(null);

    void (async () => {
      try {
        const project = await apiClient.getNovelProject(projectId);
        if (cancelled) return;
        setApiProject(project);

        const chapterPlans = project.chapter_plans ?? [];
        const chap = chapterPlans.find(
          (p: any) =>
            (p.chapter_index ?? p.chapterIndex) ===
            parseInt(chapterIndex as string)
        );
        if (chap) {
          setApiChapterPlan(chap);
          // 预填表单
          setFormData({
            chapterGoal: chap.summary ?? "",
            targetWordCount: String(chap.target_word_count ?? 3000),
            mainConflict: chap.main_conflict ?? "",
            rewardOrHook: chap.reward_or_hook ?? "",
            emotionalDirection: chap.emotional_direction ?? "",
            mustInclude: Array.isArray(chap.must_include)
              ? chap.must_include.join("\n")
              : (chap.must_include ?? ""),
            mustNotChange: Array.isArray(chap.must_not_change)
              ? chap.must_not_change.join("\n")
              : (chap.must_not_change ?? ""),
          });
        }
      } catch (caught) {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "章节加载失败");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [apiClient, projectId, chapterIndex]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!apiClient || !projectId || !chapterIndex || !apiChapterPlan) return;

    setSubmitting(true);
    setError(null);
    try {
      const payload = {
        chapter_plan_id:
          apiChapterPlan.chapter_plan_id ?? apiChapterPlan.chapterPlanId,
        summary: formData.chapterGoal,
        target_word_count: parseInt(formData.targetWordCount) || 3000,
        main_conflict: formData.mainConflict,
        reward_or_hook: formData.rewardOrHook,
        emotional_direction: formData.emotionalDirection,
        must_include: formData.mustInclude
          .split("\n")
          .map((s) => s.trim())
          .filter(Boolean),
        must_not_change: formData.mustNotChange
          .split("\n")
          .map((s) => s.trim())
          .filter(Boolean),
      };

      await apiClient.updateChapterDirection(
        projectId,
        parseInt(chapterIndex),
        payload
      );

      // 跳转到 Writing Studio
      navigate(`/projects/${projectId}/writing`);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "章节设置失败");
    } finally {
      setSubmitting(false);
    }
  }

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>章节方向设置</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>章节方向设置</h2>
        <p>正在加载章节数据...</p>
      </section>
    );
  }

  if (!apiChapterPlan) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>章节方向设置</h2>
        <p>未找到该章节。</p>
        <Link to={`/projects/${projectId}/planner`}>返回规划器</Link>
      </section>
    );
  }

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>第 {chapterIndex} 章方向设置</h2>
        <p>
          为本章确定生成参数：目标、冲突、字数和禁用约束。这些参数将指导一键生成。
        </p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>当前章节信息</CardTitle>
          <CardDescription>
            第 {apiChapterPlan.chapter_index ?? chapterIndex} 章 ·{" "}
            {labelOf(statusLabels, apiChapterPlan.status)}
          </CardDescription>
        </CardHeader>
        <CardContent style={{ display: "grid", gap: 12 }}>
          <dl>
            <dt>章节标题</dt>
            <dd>{apiChapterPlan.title ?? "未填写"}</dd>
            <dt>当前摘要</dt>
            <dd>{apiChapterPlan.summary ?? "未填写"}</dd>
            <dt>目标字数</dt>
            <dd>{apiChapterPlan.target_word_count ?? 0}</dd>
          </dl>
        </CardContent>
      </Card>

      <form onSubmit={handleSubmit}>
        <Card>
          <CardHeader>
            <CardTitle>生成参数</CardTitle>
            <CardDescription>
              填写本章的生成参数，系统将根据这些参数生成约 3000 字的章节草稿。
            </CardDescription>
          </CardHeader>
          <CardContent style={{ display: "grid", gap: 16 }}>
            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ fontWeight: 600 }}>章节目标 *</span>
              <textarea
                required
                value={formData.chapterGoal}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    chapterGoal: e.target.value,
                  }))
                }
                placeholder="描述本章的主要叙事目标，比如：主角逃脱困境、发现重要信息等"
                style={{ minHeight: 80 }}
              />
              <small>说明本章要推动故事发展的具体方向和预期情感效果。</small>
            </label>

            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ fontWeight: 600 }}>目标字数 *</span>
              <input
                type="number"
                required
                min="500"
                max="10000"
                step="100"
                value={formData.targetWordCount}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    targetWordCount: e.target.value,
                  }))
                }
              />
              <small>通常为 3000 字，可根据需要调整。</small>
            </label>

            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ fontWeight: 600 }}>主要冲突</span>
              <textarea
                value={formData.mainConflict}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    mainConflict: e.target.value,
                  }))
                }
                placeholder="本章的主要冲突或对立是什么？"
                style={{ minHeight: 60 }}
              />
            </label>

            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ fontWeight: 600 }}>爽点或钩子</span>
              <textarea
                value={formData.rewardOrHook}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    rewardOrHook: e.target.value,
                  }))
                }
                placeholder="本章的爽点（读者期待的奖励）或钩子（吸引继续阅读的悬念）"
                style={{ minHeight: 60 }}
              />
            </label>

            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ fontWeight: 600 }}>情感走向</span>
              <input
                type="text"
                value={formData.emotionalDirection}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    emotionalDirection: e.target.value,
                  }))
                }
                placeholder="例如：紧张 → 恍然大悟 → 释然，或其他情感弧线"
              />
            </label>

            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ fontWeight: 600 }}>必须包含</span>
              <textarea
                value={formData.mustInclude}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    mustInclude: e.target.value,
                  }))
                }
                placeholder="一行一个，列举本章必须包含的内容、人物、事件等"
                style={{ minHeight: 60 }}
              />
              <small>多项请用换行分隔。例如：徐龙出场、揭露真相等。</small>
            </label>

            <label style={{ display: "grid", gap: 6 }}>
              <span style={{ fontWeight: 600 }}>禁用改变</span>
              <textarea
                value={formData.mustNotChange}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    mustNotChange: e.target.value,
                  }))
                }
                placeholder="一行一个，列举本章禁止改变或违背的约束"
                style={{ minHeight: 60 }}
              />
              <small>例如：不能透露秘密、人物属性不变、时间线连续等。</small>
            </label>
          </CardContent>
        </Card>

        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <button
            type="submit"
            disabled={submitting}
            style={{
              padding: "8px 16px",
              backgroundColor: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: 4,
              cursor: submitting ? "not-allowed" : "pointer",
              opacity: submitting ? 0.5 : 1,
            }}
          >
            {submitting ? "保存中..." : "保存并进入写作"}
          </button>
          <Link
            to={`/projects/${projectId}/planner`}
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
            取消
          </Link>
        </div>
      </form>
    </section>
  );
}
