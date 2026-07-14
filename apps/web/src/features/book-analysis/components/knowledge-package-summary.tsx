import { useState } from "react";
import { Link } from "react-router-dom";
import { BookAnalysisSummaryState } from "../../../components/phase-two-state";
import { Button } from "../../../components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../../../components/ui/card";

type TabDataProps = {
  chapters: Array<Record<string, any>>;
  scenes: Array<Record<string, any>>;
  events: Array<Record<string, any>>;
  conflicts: Array<Record<string, any>>;
  hooks: Array<Record<string, any>>;
  rewards: Array<Record<string, any>>;
  climaxes: Array<Record<string, any>>;
  knowledgeObjects: Array<Record<string, any>>;
  relationships: Array<Record<string, any>>;
};

export function KnowledgePackageSummary({
  summary,
  tabData,
}: {
  summary: BookAnalysisSummaryState;
  tabData: TabDataProps;
}) {
  const [activeTab, setActiveTab] = useState<string | null>(null);

  const metrics = [
    ["章节", summary.chapterCount],
    ["场景", summary.sceneCount],
    ["知识对象", summary.knowledgeObjectCount],
    ["证据", summary.evidenceCount],
    ["模式", summary.patternCount],
    ["节奏", summary.rhythmProfileCount],
    ["资产", summary.assetCount],
    ["规则", summary.ruleCount],
  ] as const;

  const handleMetricClick = (label: string) => {
    setActiveTab((prev) => (prev === label ? null : label));
  };

  const tabPanelStyle: React.CSSProperties = {
    marginTop: 12,
    maxHeight: 260,
    overflowY: "auto",
    borderTop: "1px solid var(--border, #e5e7eb)",
    paddingTop: 10,
  };

  const itemStyle: React.CSSProperties = {
    padding: "4px 0",
    borderBottom: "1px solid var(--border-subtle, #f3f4f6)",
    fontSize: 13,
    lineHeight: 1.6,
  };

  const labelStyle: React.CSSProperties = {
    fontWeight: 600,
    color: "var(--primary, #2563eb)",
    marginRight: 4,
  };

  const badgeStyle: React.CSSProperties = {
    display: "inline-block",
    padding: "0 6px",
    borderRadius: 4,
    fontSize: 11,
    background: "var(--muted, #f3f4f6)",
    color: "var(--muted-foreground, #6b7280)",
    marginLeft: 4,
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Knowledge Package</CardTitle>
        <CardDescription>
          提交后可用于 Story Bible、章节规划和一键生成。点击指标可展开详情。
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="nf-metric-grid">
          {metrics.map(([label, value]) => (
            <div
              className={`nf-metric ${activeTab === label ? "nf-metric-active" : ""}`}
              key={label}
              onClick={() => handleMetricClick(label)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ")
                  handleMetricClick(label);
              }}
              role="button"
              tabIndex={0}
              style={{ cursor: "pointer" }}
            >
              <span>{label}</span>
              <strong>{value}</strong>
            </div>
          ))}
        </div>

        {activeTab && (
          <div style={tabPanelStyle}>
            {activeTab === "章节" &&
              tabData.chapters.slice(0, 10).map((ch) => (
                <div key={ch.chapter_id} style={itemStyle}>
                  <span style={labelStyle}>{ch.title}</span>
                  <span style={badgeStyle}>#{ch.chapter_index}</span>
                  {ch.text_excerpt && (
                    <span
                      style={{
                        display: "block",
                        color: "var(--muted-foreground, #6b7280)",
                        marginTop: 2,
                      }}
                    >
                      {String(ch.text_excerpt).slice(0, 80)}...
                    </span>
                  )}
                </div>
              ))}
            {activeTab === "场景" &&
              tabData.scenes.slice(0, 10).map((s) => (
                <div key={s.scene_id} style={itemStyle}>
                  <span style={labelStyle}>{s.title}</span>
                  <span style={badgeStyle}>{s.text_range}</span>
                </div>
              ))}
            {activeTab === "知识对象" &&
              tabData.knowledgeObjects.slice(0, 10).map((o) => (
                <div key={o.object_id} style={itemStyle}>
                  <span style={labelStyle}>{o.canonical_name}</span>
                  <span style={badgeStyle}>{o.object_type}</span>
                  <span
                    style={{
                      fontSize: 11,
                      color: "var(--muted-foreground, #6b7280)",
                      marginLeft: 6,
                    }}
                  >
                    confidence: {String(o.confidence ?? "?")}
                  </span>
                </div>
              ))}
            {activeTab === "证据" && tabData.knowledgeObjects.length === 0 && (
              <div style={itemStyle}>
                <span style={{ color: "var(--muted-foreground, #6b7280)" }}>
                  证据源于原文片段，现已绑定到对应知识对象。
                </span>
              </div>
            )}
            {activeTab === "模式" && tabData.knowledgeObjects.length === 0 && (
              <div style={itemStyle}>
                <span style={{ color: "var(--muted-foreground, #6b7280)" }}>
                  模式将在多书对比后自动生成。
                </span>
              </div>
            )}
            {activeTab === "节奏" && (
              <div style={itemStyle}>
                <span style={{ color: "var(--muted-foreground, #6b7280)" }}>
                  节奏画像将在更多章节分析后生成。
                </span>
              </div>
            )}
            {activeTab === "资产" && (
              <div style={itemStyle}>
                <span style={{ color: "var(--muted-foreground, #6b7280)" }}>
                  资产将在知识包确认后自动生成。
                </span>
              </div>
            )}
            {activeTab === "规则" && (
              <div style={itemStyle}>
                <span style={{ color: "var(--muted-foreground, #6b7280)" }}>
                  规则将在多书对比后自动提取。
                </span>
              </div>
            )}
          </div>
        )}

        {summary.runId ? (
          <div style={{ marginTop: 16 }}>
            <Link to={`/knowledge-packages/${summary.runId}`}>
              <Button type="button" variant="outline" style={{ width: "100%" }}>
                查看知识包详情
              </Button>
            </Link>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
