import { Link } from "react-router-dom";

import { deriveAnalysisExceptions, deriveLowConfidenceItems } from "../../components/phase-two-state";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { usePhaseTwo } from "../../state/phase-two-provider";

export function ReviewQueuePage() {
  const { state } = usePhaseTwo();
  const analysisExceptions = deriveAnalysisExceptions(state);
  const lowConfidenceItems = deriveLowConfidenceItems(state.knowledgeObjects);
  const writingBlockers = state.qualityReports.flatMap((report) => report.blockingIssues);
  const strategySuggestions = state.strategySuggestions.filter((item) => item.status === "review");

  return (
    <section className="nf-analysis-page">
      <div className="nf-analysis-hero">
        <div>
          <Badge variant="warning">Review</Badge>
          <h2>只处理必须打断的事项</h2>
          <p>低置信、证据缺失、质量 blocker 和策略建议进入 Review；非阻塞信息留在报告页。</p>
        </div>
      </div>

      <div className="nf-analysis-grid">
        <Card>
          <CardHeader>
            <CardTitle>Analysis exceptions</CardTitle>
            <CardDescription>来自拆书分析中心的异常项。</CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="nf-exception-list">
              {analysisExceptions.map((item) => (
                <li className="nf-exception-item" key={item.exceptionId}>
                  <div className="nf-row-between"><strong>{item.title}</strong><Badge variant="warning">{item.severity}</Badge></div>
                  <p>{item.summary}</p>
                  <Button asChild size="sm" variant="secondary"><Link to={`/sources/${state.book.bookId}/analysis`}>Resolve Exception</Link></Button>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
        <div className="nf-analysis-stack">
          <Card>
            <CardHeader><CardTitle>Low confidence knowledge</CardTitle><CardDescription>候选对象只显示需要确认项。</CardDescription></CardHeader>
            <CardContent>{lowConfidenceItems.map((item) => <p key={item.objectId}>{item.canonicalName} · confidence {item.confidence}</p>)}</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Writing blockers</CardTitle><CardDescription>章节批准前必须解决的问题。</CardDescription></CardHeader>
            <CardContent>{writingBlockers.map((item) => <p key={item.issueId}>{item.severity} · {item.summary}</p>)}</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Strategy suggestions</CardTitle><CardDescription>反馈建议必须人工审批。</CardDescription></CardHeader>
            <CardContent>{strategySuggestions.map((item) => <p key={item.suggestionId}>{item.summary}</p>)}</CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
