import { Link } from "react-router-dom";

import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { usePhaseTwo } from "../../state/phase-two-provider";

export function KnowledgeHomePage() {
  const { state } = usePhaseTwo();
  const approvedObjects = state.knowledgeObjects.filter((item) => ["approved", "merged"].includes(item.lifecycleStatus));

  return (
    <section className="nf-analysis-page">
      <div className="nf-analysis-hero">
        <div>
          <Badge variant="success">Knowledge</Badge>
          <h2>可复用知识资产</h2>
          <p>知识库展示已提交、可用于新书设定与章节生成的对象、规则、套路、节奏和素材。</p>
        </div>
        <div className="nf-analysis-actions">
          <Button asChild>
            <Link to={`/sources/${state.book.bookId}/analysis`}>回到拆书分析中心</Link>
          </Button>
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
          <CardDescription>来源：{state.book.title} · evidence coverage {state.bookAnalysisSummary.evidenceCount} 条</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="nf-metric-grid">
            <div className="nf-metric"><span>Approved objects</span><strong>{approvedObjects.length}</strong></div>
            <div className="nf-metric"><span>Patterns</span><strong>{state.patterns.length}</strong></div>
            <div className="nf-metric"><span>Rhythm</span><strong>{state.rhythmProfiles.length}</strong></div>
            <div className="nf-metric"><span>Assets</span><strong>{state.assets.length}</strong></div>
            <div className="nf-metric"><span>Rules</span><strong>{state.rules.length}</strong></div>
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
              {state.knowledgeObjects.map((item) => (
                <li className="nf-source-item" key={item.objectId}>
                  <div className="nf-row-between">
                    <h3>{item.canonicalName}</h3>
                    <Badge variant={item.lifecycleStatus === "approved" ? "success" : "warning"}>{item.lifecycleStatus}</Badge>
                  </div>
                  <p>{item.objectType} · confidence {item.confidence} · aliases {item.aliases.join("、") || "无"}</p>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
        <div className="nf-analysis-stack">
          <Card>
            <CardHeader><CardTitle>Patterns</CardTitle><CardDescription>可参数化叙事套路。</CardDescription></CardHeader>
            <CardContent>{state.patterns.map((item) => <p key={item.patternId}>{item.canonicalName} · {item.expectedReaderEffect}</p>)}</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Rhythm / Assets / Rules</CardTitle><CardDescription>节奏、素材和一致性约束。</CardDescription></CardHeader>
            <CardContent>
              {state.rhythmProfiles.map((item) => <p key={item.rhythmProfileId}>{item.label} · climax {item.climaxIndex} · suspense {item.suspenseIndex}</p>)}
              {state.assets.map((item) => <p key={item.assetId}>{item.canonicalName} · {item.usageContext}</p>)}
              {state.rules.map((item) => <p key={item.ruleId}>{item.title} · {item.conditionSummary}</p>)}
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
