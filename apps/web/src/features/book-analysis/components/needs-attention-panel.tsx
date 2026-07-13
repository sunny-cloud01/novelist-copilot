import { AnalysisExceptionState, ReviewAction } from "../../../components/phase-two-state";
import { Badge } from "../../../components/ui/badge";
import { Button } from "../../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../../components/ui/card";

type NeedsAttentionPanelProps = {
  exceptions: AnalysisExceptionState[];
  onReview: (objectId: string, action: ReviewAction) => void;
};

function objectIdFromTargetRef(targetRef: string | undefined) {
  return (targetRef ?? "").replace("object://knowledge-objects/", "");
}

export function NeedsAttentionPanel({ exceptions, onReview }: NeedsAttentionPanelProps) {
  return (
    <Card className={exceptions.length > 0 ? "nf-attn-card" : undefined}>
      <CardHeader>
        <CardTitle>Needs attention</CardTitle>
        <CardDescription>只打断低置信、冲突或缺证据项目；不要求逐项审核全部候选。</CardDescription>
      </CardHeader>
      <CardContent>
        {exceptions.length === 0 ? <p>暂无必须处理的异常项。</p> : null}
        <ul className="nf-exception-list">
          {exceptions.map((item) => {
            const targetRef = item.targetRef ?? (item as { target_ref?: string }).target_ref;
            const evidenceRefs = item.evidenceRefs ?? (item as { evidence_refs?: string[] }).evidence_refs ?? [];
            const objectId = objectIdFromTargetRef(targetRef);
            return (
              <li className="nf-exception-item" key={item.exceptionId ?? (item as { exception_id?: string }).exception_id ?? targetRef}>
                <div className="nf-row-between">
                  <strong>{item.title}</strong>
                  <Badge variant={item.severity === "warning" ? "warning" : "danger"}>{item.severity}</Badge>
                </div>
                <p>{item.summary}</p>
                <small>{evidenceRefs.join("、")}</small>
                <div className="nf-exception-actions">
                  <Button type="button" size="sm" onClick={() => onReview(objectId, "approve")}>Approve</Button>
                  <Button type="button" size="sm" variant="secondary" onClick={() => onReview(objectId, "merge_alias")}>Merge alias</Button>
                  <Button type="button" size="sm" variant="warning" onClick={() => onReview(objectId, "request_reextract")}>Reextract</Button>
                </div>
              </li>
            );
          })}
        </ul>
      </CardContent>
    </Card>
  );
}
