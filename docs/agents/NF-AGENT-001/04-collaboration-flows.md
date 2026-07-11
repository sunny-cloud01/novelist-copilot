# 4. Collaboration Flows

## 4.1 Knowledge Extraction Flow

```text
Ingestion Agent
↓
Extraction Agent
↓
Normalization Agent
↓
Graph Agent
↓
Review Agent
↓
Human Reviewer
↓
Knowledge Base
```

## 4.2 Generation Flow

```text
Planning Agent
↓
Prompt Engine
↓
Generation Agent
↓
Consistency Agent
↓
Review Agent
↓
Human Reviewer
↓
Feedback Agent
```

## 4.3 Novel Writing Flow

```text
Planning Agent
↓
Scene Planning Agent
↓
Memory Agent + Style Analyzer Agent
↓
Writer Agent
↓
Critic Agent
↓ failed: Writer Agent rewrite same Beat
↓ passed
Humanizer Agent
↓
Review Agent
↓
Human Reviewer
↓
Feedback Agent
```

## 4.4 Feedback Learning Flow

```text
Human Edits + Reader Feedback + Quality Metrics
↓
Feedback Agent
↓
Ranking Suggestions
↓
Human Approval
↓
Rule Configuration Center + Knowledge Base
```
