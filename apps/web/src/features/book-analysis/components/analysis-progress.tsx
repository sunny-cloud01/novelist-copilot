import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../../components/ui/card";
import { Progress } from "../../../components/ui/progress";

const stages = [
  ["Text normalization", 100],
  ["Chapter segmentation", 100],
  ["Entity extraction", 100],
  ["Evidence binding", 92],
  ["Object normalization", 88],
  ["Quality review", 82],
  ["Knowledge package export", 72],
] as const;

export function AnalysisProgress() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Auto analysis run</CardTitle>
        <CardDescription>系统自动处理内部 pipeline，界面只展示关键进度。</CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="nf-progress-list">
          {stages.map(([label, value]) => (
            <li className="nf-progress-row" key={label}>
              <div className="nf-row-between">
                <strong>{label}</strong>
                <span>{value}%</span>
              </div>
              <Progress value={value} />
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
