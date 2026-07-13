import { EvidenceState } from "../../../components/phase-two-state";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../../components/ui/card";

export function EvidenceSamplePanel({ evidences }: { evidences: EvidenceState[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Evidence sample</CardTitle>
        <CardDescription>原文证据用于解释对象、关系和写作套路来源。</CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="nf-evidence-list">
          {evidences.map((evidence, index) => {
            const evidenceId = evidence.evidenceId ?? (evidence as { evidence_id?: string }).evidence_id ?? `evidence-${index}`;
            const chapterIndex = evidence.chapterIndex ?? (evidence as { chapter_index?: number }).chapter_index;
            const textRange = evidence.textRange ?? (evidence as { text_range?: string }).text_range;
            return (
            <li className="nf-evidence-item" key={evidenceId}>
              <div className="nf-row-between">
                <strong>第 {chapterIndex} 章 · {textRange}</strong>
                <span>confidence {evidence.confidence}</span>
              </div>
              <p className="nf-evidence-excerpt">“{evidence.excerpt}”</p>
              <small>{evidenceId}</small>
            </li>
          );
          })}
        </ul>
      </CardContent>
    </Card>
  );
}
