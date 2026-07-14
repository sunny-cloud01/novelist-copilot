import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { resolveApiBaseUrl } from "@/lib/api-base";
import { createNovelFactoryApiClient } from "@/lib/api-client";

const statusLabels: Record<string, string> = {
  committed: "已落库",
  draft: "草稿",
  approved: "已通过",
  pending_review: "待审核",
};

const objectTypeLabels: Record<string, string> = {
  character: "角色",
  location: "地点",
  event: "事件",
  faction: "势力",
  artifact: "物品",
  rule: "规则",
};

function labelOf(labels: Record<string, string>, value: string) {
  return labels[value] ?? value;
}

export function KnowledgePackageDetailPage() {
  const { packageId } = useParams();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );

  const [apiPackage, setApiPackage] = useState<any | null>(null);
  const [apiObjects, setApiObjects] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);
  const [selectedObjectType, setSelectedObjectType] = useState<string>("");

  useEffect(() => {
    if (!apiClient || !packageId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);

    void Promise.all([
      apiClient.getExtractionRun(packageId) as Promise<any>,
      apiClient.listKnowledgeObjects(packageId) as Promise<{ items?: any[] }>,
    ])
      .then(([run, objectsPayload]) => {
        if (cancelled) return;
        setApiPackage(run);
        setApiObjects(
          Array.isArray(objectsPayload)
            ? objectsPayload
            : (objectsPayload?.items ?? [])
        );
      })
      .catch((caught) => {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "知识包加载失败");
        setApiPackage(null);
        setApiObjects(null);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [apiClient, packageId]);

  const pkg = apiPackage;
  const objects = apiObjects ?? [];
  const filteredObjects = selectedObjectType
    ? objects.filter(
        (obj: any) => (obj.object_type ?? obj.objectType) === selectedObjectType
      )
    : objects;

  if (!apiClient) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>知识包详情</h2>
        <p>请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }

  if (loading) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>知识包详情</h2>
        <p>正在加载知识包...</p>
      </section>
    );
  }

  if (!pkg) {
    return (
      <section style={{ display: "grid", gap: 16 }}>
        <h2>知识包详情</h2>
        <p>未找到该知识包。</p>
      </section>
    );
  }

  const objectCounts: Record<string, number> = {};
  objects.forEach((obj: any) => {
    const type = obj.object_type ?? obj.objectType ?? "other";
    objectCounts[type] = (objectCounts[type] ?? 0) + 1;
  });

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <div>
        <h2>知识包详情</h2>
        <p>查看已落库知识包内容、统计与关系。</p>
        {error ? (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        ) : null}
        <Link
          to={`/extraction-runs/${packageId}`}
          style={{ display: "inline-block", marginTop: 12 }}
        >
          返回拆书任务 →
        </Link>
      </div>

      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>包基本信息</h3>
        <dl>
          <dt>知识包 / 运行 ID</dt>
          <dd>{pkg.run_id ?? pkg.runId ?? packageId}</dd>
          <dt>状态</dt>
          <dd>{labelOf(statusLabels, pkg.status)}</dd>
          <dt>创建时间</dt>
          <dd>{pkg.created_at ?? "未记录"}</dd>
          <dt>来源</dt>
          <dd>{pkg.source_ref ?? pkg.sourceRef ?? "未关联"}</dd>
        </dl>
      </section>

      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>抽取统计</h3>
        <dl>
          <dt>章节数</dt>
          <dd>{pkg.chapter_count ?? 0}</dd>
          <dt>场景数</dt>
          <dd>{pkg.scene_count ?? 0}</dd>
          <dt>知识对象数</dt>
          <dd>{objects.length}</dd>
          <dt>证据引用数</dt>
          <dd>{pkg.evidence_count ?? 0}</dd>
        </dl>
      </section>

      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>对象类型分布</h3>
        <ul>
          {Object.entries(objectCounts).map(([type, count]) => (
            <li key={type}>
              {labelOf(objectTypeLabels, type)}: {count} 个
            </li>
          ))}
        </ul>
      </section>

      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>知识对象列表</h3>
        <div style={{ marginBottom: 12 }}>
          <label style={{ display: "block", marginBottom: 8 }}>
            筛选类型：
            <select
              value={selectedObjectType}
              onChange={(e) => setSelectedObjectType(e.target.value)}
            >
              <option value="">全部</option>
              {Object.keys(objectCounts).map((type) => (
                <option key={type} value={type}>
                  {labelOf(objectTypeLabels, type)}
                </option>
              ))}
            </select>
          </label>
        </div>

        {filteredObjects.length === 0 ? (
          <p>该筛选条件下无对象。</p>
        ) : (
          <ul
            style={{ display: "grid", gap: 12, padding: 0, listStyle: "none" }}
          >
            {filteredObjects.map((obj: any) => (
              <li
                key={obj.object_id ?? obj.objectId}
                style={{
                  border: "1px solid #e5e7eb",
                  borderRadius: 4,
                  padding: 12,
                }}
              >
                <div style={{ fontWeight: 600 }}>
                  {obj.canonical_name ?? obj.canonicalName}
                </div>
                <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>
                  {labelOf(objectTypeLabels, obj.object_type ?? obj.objectType)}{" "}
                  · 置信度 {obj.confidence ?? "N/A"} · 别名{" "}
                  {(obj.aliases ?? []).length}
                </div>
                {obj.summary ? (
                  <p style={{ fontSize: 14, margin: "8px 0 0 0" }}>
                    {obj.summary}
                  </p>
                ) : null}
                <div style={{ marginTop: 8 }}>
                  <small>
                    {obj.evidence_count ?? 0} 条证据 · 生命周期:{" "}
                    {obj.lifecycle_status ?? obj.lifecycleStatus}
                  </small>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section style={{ border: "1px solid #d4d4d8", padding: 16 }}>
        <h3>快速操作</h3>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <Link to={`/graph?source=${packageId}`}>查看图谱</Link>
          <Link to={`/projects/new?knowledgePackage=${packageId}`}>
            用该包创建项目
          </Link>
          <Link to="/knowledge">返回知识库</Link>
        </div>
      </section>
    </section>
  );
}
