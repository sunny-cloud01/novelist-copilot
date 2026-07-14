import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../../components/ui/card";
import { createNovelFactoryApiClient } from "@/lib/api-client";
import { resolveApiBaseUrl } from "@/lib/api-base";

export function ReviewQueuePage() {
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );

  const [apiObjects, setApiObjects] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);
  const [runId, setRunId] = useState<string>("");

  useEffect(() => {
    if (!apiClient) return;
    let cancelled = false;
    void apiClient
      .listKnowledgeSources()
      .then((payload: any) => {
        if (cancelled) return;
        const sources = payload?.items ?? payload ?? [];
        if (sources.length > 0 && sources[0]?.run_id) {
          setRunId(sources[0].run_id);
        }
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [apiClient]);

  useEffect(() => {
    if (!apiClient || !runId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    void (
      apiClient.listKnowledgeObjects(runId) as Promise<{
        items: any[];
      }>
    )
      .then((payload) => {
        if (!cancelled) setApiObjects(payload.items ?? []);
      })
      .catch((caught) => {
        if (!cancelled)
          setError(
            caught instanceof Error ? caught.message : "审核队列加载失败"
          );
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [apiClient, runId]);

  const analysisExceptions: any[] = [];
  const lowConfidenceItems = (apiObjects ?? []).filter(
    (o: any) =>
      (o.confidence ?? 1) < 0.7 ||
      (o.lifecycle_status ?? o.lifecycleStatus) === "pending_review"
  );
  const writingBlockers: any[] = [];
  const strategySuggestions: any[] = [];

  if (!apiClient) {
    return (
      <section className="nf-analysis-page">
        <h2>请配置 API</h2>
        <p>设置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }
  if (loading) {
    return (
      <section className="nf-analysis-page">
        <h2>正在加载审核队列...</h2>
      </section>
    );
  }

  return (
    <section className="nf-analysis-page">
      <div className="nf-analysis-hero">
        <div>
          <Badge variant="warning">Review</Badge>
          <h2>只处理必须打断的事项</h2>
          <p>
            低置信、证据缺失、质量 blocker 和策略建议进入
            Review；非阻塞信息留在报告页。
          </p>
          {error ? (
            <p role="alert" style={{ color: "red" }}>
              {error}
            </p>
          ) : null}
        </div>
      </div>

      <div className="nf-analysis-grid">
        <Card>
          <CardHeader>
            <CardTitle>Analysis exceptions</CardTitle>
            <CardDescription>来自拆书分析中心的异常项。</CardDescription>
          </CardHeader>
          <CardContent>
            {analysisExceptions.length === 0 ? (
              <p>暂无分析异常。</p>
            ) : (
              <ul className="nf-exception-list">
                {analysisExceptions.map((item) => (
                  <li className="nf-exception-item" key={item.exceptionId}>
                    <div className="nf-row-between">
                      <strong>{item.title}</strong>
                      <Badge variant="warning">{item.severity}</Badge>
                    </div>
                    <p>{item.summary}</p>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>
        <div className="nf-analysis-stack">
          <Card>
            <CardHeader>
              <CardTitle>Low confidence knowledge</CardTitle>
              <CardDescription>候选对象只显示需要确认项。</CardDescription>
            </CardHeader>
            <CardContent>
              {lowConfidenceItems.map((item: any) => (
                <p key={item.objectId ?? item.object_id}>
                  {item.canonicalName ?? item.canonical_name} · confidence{" "}
                  {item.confidence}
                </p>
              ))}
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Writing blockers</CardTitle>
              <CardDescription>章节批准前必须解决的问题。</CardDescription>
            </CardHeader>
            <CardContent>
              {writingBlockers.map((item) => (
                <p key={item.issueId}>
                  {item.severity} · {item.summary}
                </p>
              ))}
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Strategy suggestions</CardTitle>
              <CardDescription>反馈建议必须人工审批。</CardDescription>
            </CardHeader>
            <CardContent>
              {strategySuggestions.map((item) => (
                <p key={item.suggestionId}>{item.summary}</p>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
