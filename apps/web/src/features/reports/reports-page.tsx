import { Badge } from "../../components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { usePhaseTwo } from "../../state/phase-two-provider";

export function ReportsPage() {
  const { state } = usePhaseTwo();
  const writingRun = state.writingRuns[0];
  const qualityReport = state.qualityReports.find((item) => item.qualityReportId === writingRun?.qualityReportId);
  const rankingSnapshot = state.rankingSnapshots.find((item) => item.rankingType === "prompt");

  return (
    <section className="nf-analysis-page">
      <div className="nf-analysis-hero">
        <div>
          <Badge variant="success">Reports</Badge>
          <h2>成本、质量与反馈报告</h2>
          <p>报告页承接成本、AI 味、质量门、反馈记录和策略建议，非阻塞信息不打断创作者。</p>
        </div>
      </div>
      <div className="nf-analysis-grid">
        <Card>
          <CardHeader><CardTitle>Quality report</CardTitle><CardDescription>{qualityReport?.qualityReportId}</CardDescription></CardHeader>
          <CardContent>
            <div className="nf-metric-grid">
              <div className="nf-metric"><span>AI flavor</span><strong>{qualityReport?.aiFlavorScore}</strong></div>
              <div className="nf-metric"><span>Readability</span><strong>{qualityReport?.mobileReadabilityScore}</strong></div>
              <div className="nf-metric"><span>Originality</span><strong>{qualityReport?.originalitySafetyScore}</strong></div>
              <div className="nf-metric"><span>Cost</span><strong>{writingRun?.modelCost.estimatedTotalCost}</strong></div>
            </div>
          </CardContent>
        </Card>
        <div className="nf-analysis-stack">
          <Card>
            <CardHeader><CardTitle>Feedback records</CardTitle><CardDescription>人工反馈和系统质量信号。</CardDescription></CardHeader>
            <CardContent>{state.feedbackRecords.map((item) => <p key={item.feedbackRecordId}>{item.feedbackType} · score {item.score} · {String(item.payload.summary ?? "")}</p>)}</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Prompt rankings</CardTitle><CardDescription>反馈学习不自动生效，先形成建议。</CardDescription></CardHeader>
            <CardContent>{rankingSnapshot?.items.map((item) => <p key={item.targetId}>#{item.rank} · {item.label} · {item.score} · {item.summary}</p>)}</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Strategy suggestions</CardTitle><CardDescription>待人工审批后影响后续生成。</CardDescription></CardHeader>
            <CardContent>{state.strategySuggestions.map((item) => <p key={item.suggestionId}>{item.status} · {item.summary}</p>)}</CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
