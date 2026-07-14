import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../../../components/ui/card";
import { Progress } from "../../../components/ui/progress";

const ALL_STAGES = [
  { key: "text_normalization", label: "文字标准化" },
  { key: "chapter_segmentation", label: "章节分拆" },
  { key: "entity_extraction", label: "实体抽取" },
  { key: "evidence_binding", label: "证据绑定" },
  { key: "object_normalization", label: "对象归一化" },
  { key: "quality_review", label: "质量审核" },
  { key: "knowledge_export", label: "知识包导出" },
] as const;

function stageProgress(
  stageKey: string,
  currentStage: string,
  status: string
): number {
  const idx = ALL_STAGES.findIndex((s) => s.key === stageKey);
  const currentIdx = ALL_STAGES.findIndex((s) => s.key === currentStage);
  if (status === "requires_review" || status === "succeeded") return 100;
  if (status === "failed") return idx < currentIdx ? 100 : 0;
  if (idx < currentIdx) return 100;
  if (idx === currentIdx) return 66;
  return 0;
}

export function AnalysisProgress({
  run,
}: {
  run?: Record<string, any> | null;
}) {
  const status: string = run?.status ?? "";
  const currentStage: string = run?.current_stage ?? "";
  const hasRun = Boolean(run);

  if (!hasRun) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>拆书进度</CardTitle>
          <CardDescription>尚未开始提取，请先导入书籍。</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>拆书进度</CardTitle>
        <CardDescription>
          {status === "requires_review"
            ? "提取完成，等待审核确认。"
            : status === "failed"
              ? "提取失败，请检查日志。"
              : "系统自动处理内部管线，界面展示关键进度。"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="nf-progress-list">
          {ALL_STAGES.map(({ key, label }) => {
            const value = stageProgress(key, currentStage, status);
            return (
              <li className="nf-progress-row" key={key}>
                <div className="nf-row-between">
                  <strong>{label}</strong>
                  <span>{value}%</span>
                </div>
                <Progress value={value} />
              </li>
            );
          })}
        </ul>
      </CardContent>
    </Card>
  );
}
