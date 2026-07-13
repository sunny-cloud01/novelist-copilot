import { Badge } from "../../../components/ui/badge";
import { Button } from "../../../components/ui/button";
import { BookAnalysisSummaryState, SourceBookState } from "../../../components/phase-two-state";

type AnalysisHeroProps = {
  book: SourceBookState;
  summary: BookAnalysisSummaryState;
  onCommit: () => void;
};

export function AnalysisHero({ book, summary, onCommit }: AnalysisHeroProps) {
  return (
    <section className="nf-analysis-hero">
      <div>
        <Badge variant={summary.status === "succeeded" ? "success" : "warning"}>{summary.status}</Badge>
        <h2>自动拆书完成，只处理异常</h2>
        <p>
          《{book.title}》已完成章节切分、对象抽取、证据绑定和写作节奏分析。创作者只需要处理低置信项，
          再把知识包提交给后续 Story Bible 与章节生成使用。
        </p>
      </div>
      <div className="nf-analysis-actions">
        <Button type="button" onClick={onCommit} disabled={!summary.canCommitKnowledge}>
          Commit Knowledge
        </Button>
        <Button type="button" variant="secondary">Resolve Exceptions</Button>
        <Button type="button" variant="ghost">Inspect Graph</Button>
      </div>
    </section>
  );
}
