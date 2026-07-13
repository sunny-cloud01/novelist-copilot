import { BookAnalysisSummaryState } from "../../../components/phase-two-state";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../../components/ui/card";

export function KnowledgePackageSummary({ summary }: { summary: BookAnalysisSummaryState }) {
  const metrics = [
    ["Chapters", summary.chapterCount],
    ["Scenes", summary.sceneCount],
    ["Knowledge", summary.knowledgeObjectCount],
    ["Evidence", summary.evidenceCount],
    ["Patterns", summary.patternCount],
    ["Rhythm", summary.rhythmProfileCount],
    ["Assets", summary.assetCount],
    ["Rules", summary.ruleCount],
  ] as const;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Knowledge Package</CardTitle>
        <CardDescription>提交后可用于 Story Bible、章节规划和一键生成。</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="nf-metric-grid">
          {metrics.map(([label, value]) => (
            <div className="nf-metric" key={label}>
              <span>{label}</span>
              <strong>{value}</strong>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
