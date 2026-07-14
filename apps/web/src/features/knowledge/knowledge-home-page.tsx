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

const emptyArray: any[] = [];

export function KnowledgeHomePage() {
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
    setLoading(true);
    setError(null);
    void apiClient
      .listKnowledgeSources()
      .then((payload: any) => {
        if (cancelled) {
          const sources = payload?.items ?? payload ?? [];
          if (sources.length > 0 && sources[0]?.run_id) {
            setRunId(sources[0].run_id);
          }
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
            caught instanceof Error ? caught.message : "知识资产加载失败"
          );
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [apiClient, runId]);

  const knowledgeObjects = apiObjects ?? [];
  const approvedObjects = knowledgeObjects.filter((item: any) =>
    ["approved", "merged"].includes(
      item.lifecycleStatus ?? item.lifecycle_status
    )
  );

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
        <h2>正在加载知识资产...</h2>
      </section>
    );
  }

  return (
    <section className="nf-analysis-page">
      <div className="nf-analysis-hero">
        <div>
          <Badge variant="success">Knowledge</Badge>
          <h2>可复用知识资产</h2>
          <p>
            知识库展示已提交、可用于新书设定与章节生成的对象、规则、套路、节奏和素材。
          </p>
          {error ? (
            <p role="alert" style={{ color: "red" }}>
              {error}
            </p>
          ) : null}
        </div>
        <div className="nf-analysis-actions">
          <Button asChild variant="secondary">
            <Link to="/projects/new/story-bible">Use in Project</Link>
          </Button>
          <Button asChild variant="secondary">
            <Link to="/review">处理异常</Link>
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Knowledge Package</CardTitle>
          <CardDescription>
            来源：知识包 · evidence coverage {knowledgeObjects.length} 条
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="nf-metric-grid">
            <div className="nf-metric">
              <span>Approved objects</span>
              <strong>{approvedObjects.length}</strong>
            </div>
            <div className="nf-metric">
              <span>Patterns</span>
              <strong>0</strong>
            </div>
            <div className="nf-metric">
              <span>Rhythm</span>
              <strong>0</strong>
            </div>
            <div className="nf-metric">
              <span>Assets</span>
              <strong>0</strong>
            </div>
            <div className="nf-metric">
              <span>Rules</span>
              <strong>0</strong>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="nf-analysis-grid">
        <Card>
          <CardHeader>
            <CardTitle>Characters / entities</CardTitle>
            <CardDescription>按知识对象分类浏览。</CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="nf-source-list">
              {knowledgeObjects.map((item: any) => (
                <li
                  className="nf-source-item"
                  key={item.objectId ?? item.object_id}
                >
                  <div className="nf-row-between">
                    <h3>{item.canonicalName ?? item.canonical_name}</h3>
                    <Badge
                      variant={
                        (item.lifecycleStatus ?? item.lifecycle_status) ===
                        "approved"
                          ? "success"
                          : "warning"
                      }
                    >
                      {item.lifecycleStatus ?? item.lifecycle_status}
                    </Badge>
                  </div>
                  <p>
                    {item.objectType ?? item.object_type} · confidence{" "}
                    {item.confidence} · aliases{" "}
                    {(item.aliases ?? []).join("、") || "无"}
                  </p>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
        <div className="nf-analysis-stack">
          <Card>
            <CardHeader>
              <CardTitle>Patterns</CardTitle>
              <CardDescription>可参数化叙事套路。</CardDescription>
            </CardHeader>
            <CardContent>
              <p>暂无套路数据。</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Rhythm / Assets / Rules</CardTitle>
              <CardDescription>节奏、素材和一致性约束。</CardDescription>
            </CardHeader>
            <CardContent>
              <p>暂无节奏、素材和规则数据。</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
