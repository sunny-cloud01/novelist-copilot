import { useParams } from "react-router-dom";

import { useBookAnalysis } from "./use-book-analysis";
import { AnalysisHero } from "./components/analysis-hero";
import { AnalysisProgress } from "./components/analysis-progress";
import { ChapterRhythmPanel } from "./components/chapter-rhythm-panel";
import { DeepAnalysisPanel } from "./components/deep-analysis-panel";
import { EvidenceSamplePanel } from "./components/evidence-sample-panel";
import { KnowledgePackageSummary } from "./components/knowledge-package-summary";
import { NeedsAttentionPanel } from "./components/needs-attention-panel";

export function BookAnalysisCenterPage() {
  const { bookId } = useParams();
  const analysis = useBookAnalysis(bookId);

  if (analysis.loading) {
    return (
      <section className="nf-analysis-page">
        <h2>正在加载拆书分析...</h2>
      </section>
    );
  }
  if (analysis.error) {
    return (
      <section className="nf-analysis-page">
        <h2>拆书分析加载失败</h2>
        <p>{analysis.error}</p>
      </section>
    );
  }
  if (!analysis.book || !analysis.summary) {
    return (
      <section className="nf-analysis-page">
        <h2>拆书分析不存在</h2>
      </section>
    );
  }

  return (
    <section className="nf-analysis-page">
      <AnalysisHero
        book={analysis.book}
        summary={analysis.summary}
        onCommit={analysis.commitRun}
      />
      <KnowledgePackageSummary
        summary={analysis.summary}
        tabData={{
          chapters: analysis.chapters ?? [],
          scenes: analysis.scenes ?? [],
          events: analysis.events ?? [],
          conflicts: analysis.conflicts ?? [],
          hooks: analysis.hooks ?? [],
          rewards: analysis.rewards ?? [],
          climaxes: analysis.climaxes ?? [],
          knowledgeObjects: analysis.knowledgeObjects ?? [],
          relationships: analysis.relationships ?? [],
        }}
      />
      <div className="nf-analysis-grid">
        <div className="nf-analysis-stack">
          <AnalysisProgress run={analysis.run} />
          <DeepAnalysisPanel
            scenes={analysis.scenes ?? []}
            events={analysis.events ?? []}
            conflicts={analysis.conflicts ?? []}
            hooks={analysis.hooks ?? []}
            rewards={analysis.rewards ?? []}
            climaxes={analysis.climaxes ?? []}
            relationships={analysis.relationships ?? []}
          />
          <ChapterRhythmPanel chapters={analysis.chapters} />
          <EvidenceSamplePanel evidences={analysis.evidenceSamples} />
        </div>
        <NeedsAttentionPanel
          exceptions={analysis.exceptions}
          onReview={analysis.applyReviewAction}
        />
      </div>
    </section>
  );
}
