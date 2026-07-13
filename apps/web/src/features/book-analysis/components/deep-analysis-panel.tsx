import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../../components/ui/card";

type DeepAnalysisPanelProps = {
  scenes: Array<Record<string, any>>;
  events: Array<Record<string, any>>;
  conflicts: Array<Record<string, any>>;
  hooks: Array<Record<string, any>>;
  rewards: Array<Record<string, any>>;
  climaxes: Array<Record<string, any>>;
  relationships: Array<Record<string, any>>;
};

export function DeepAnalysisPanel({ scenes, events, conflicts, hooks, rewards, climaxes, relationships }: DeepAnalysisPanelProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>深度拆书结构</CardTitle>
        <CardDescription>场景、事件、冲突、钩子、爽点、高潮与关系链。</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="nf-metric-grid">
          <div className="nf-metric"><span>Scenes</span><strong>{scenes.length}</strong></div>
          <div className="nf-metric"><span>Events</span><strong>{events.length}</strong></div>
          <div className="nf-metric"><span>Conflicts</span><strong>{conflicts.length}</strong></div>
          <div className="nf-metric"><span>Hooks</span><strong>{hooks.length}</strong></div>
          <div className="nf-metric"><span>Rewards</span><strong>{rewards.length}</strong></div>
          <div className="nf-metric"><span>Climaxes</span><strong>{climaxes.length}</strong></div>
          <div className="nf-metric"><span>Relationships</span><strong>{relationships.length}</strong></div>
        </div>
        <ul className="nf-source-list">
          {events.slice(0, 3).map((event, index) => (
            <li className="nf-source-item" key={String(event.event_id ?? event.eventId ?? index)}>
              <h3>{event.event_type ?? event.eventType ?? "event"}</h3>
              <p>{event.cause} → {event.action} → {event.result}</p>
            </li>
          ))}
          {conflicts.slice(0, 2).map((conflict, index) => (
            <li className="nf-source-item" key={String(conflict.conflict_id ?? conflict.conflictId ?? index)}>
              <h3>冲突：{conflict.objective}</h3>
              <p>{conflict.pressure}</p>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
