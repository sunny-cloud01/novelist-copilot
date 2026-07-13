import { ChapterAnalysisState } from "../../../components/phase-two-state";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../../components/ui/card";

type ChapterLike = Partial<ChapterAnalysisState> & {
  chapterId?: string;
  chapter_id?: string;
  chapterIndex?: number;
  chapter_index?: number;
  title?: string;
};

export function ChapterRhythmPanel({ chapters }: { chapters: ChapterLike[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>写作逻辑与节奏</CardTitle>
        <CardDescription>按章节学习冲突、悬念、爽点和证据覆盖。</CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="nf-rhythm-list">
          {chapters.map((chapter, fallbackIndex) => {
            const chapterId = chapter.chapterId ?? chapter.chapter_id ?? `chapter-${fallbackIndex}`;
            const chapterIndex = chapter.chapterIndex ?? chapter.chapter_index ?? fallbackIndex + 1;
            return (
              <li className="nf-rhythm-item" key={chapterId}>
                <div className="nf-row-between">
                  <strong>第 {chapterIndex} 章 · {chapter.title}</strong>
                  <span>证据覆盖 {Math.round((chapter.evidenceCoverage ?? 0) * 100)}%</span>
                </div>
                <p>
                  场景 {chapter.sceneCount ?? 0} · 事件 {chapter.eventCount ?? 0} · 冲突 {chapter.conflictIndex ?? 0} · 悬念 {chapter.suspenseIndex ?? 0} · 爽点 {chapter.rewardCount ?? 0}
                </p>
              </li>
            );
          })}
        </ul>
      </CardContent>
    </Card>
  );
}
