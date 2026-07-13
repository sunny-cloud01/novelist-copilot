import { Link, useParams } from "react-router-dom";

import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { usePhaseTwo } from "../../state/phase-two-provider";

export function SourceDetailPage() {
  const { bookId } = useParams();
  const { state } = usePhaseTwo();
  const activeBookId = bookId ?? state.book.bookId;

  return (
    <section className="nf-source-page">
      <div className="nf-analysis-hero">
        <div>
          <Badge variant="warning">{state.book.importStatus}</Badge>
          <h2>来源书详情</h2>
          <p>查看《{state.book.title}》的来源元数据、章节切分和自动分析入口。</p>
        </div>
        <div className="nf-analysis-actions">
          <Button asChild>
            <Link to={`/sources/${activeBookId}/analysis`}>进入拆书分析中心</Link>
          </Button>
          <Button asChild variant="secondary">
            <Link to={`/extraction-runs/${state.run.runId}`}>查看抽取任务</Link>
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>来源元数据</CardTitle>
          <CardDescription>{state.book.traceId}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="nf-metric-grid">
            <div className="nf-metric"><span>书籍 ID</span><strong>{activeBookId}</strong></div>
            <div className="nf-metric"><span>作者</span><strong>{state.book.authorName}</strong></div>
            <div className="nf-metric"><span>来源类型</span><strong>{state.book.sourceType}</strong></div>
            <div className="nf-metric"><span>章节数</span><strong>{state.chapters.length}</strong></div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>章节列表</CardTitle>
          <CardDescription>已完成基础切章，下一步进入自动拆书分析。</CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="nf-source-list">
            {state.chapters.map((chapter) => (
              <li className="nf-source-item" key={chapter.chapterId}>
                <h3>第 {chapter.chapterIndex} 章：{chapter.title}</h3>
                <p>{chapter.segmentationStatus}</p>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </section>
  );
}
