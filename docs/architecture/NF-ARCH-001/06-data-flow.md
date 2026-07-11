# 6. Data Flow

## 6.1 Knowledge Extraction Flow

```text
Book Library
↓
Ingestion Layer
↓
Book Analysis Engine
↓
BookKnowledgePackage
↓
Structured Database
↓
Knowledge Base + Story Graph
```

## 6.2 Generation Flow

```text
Generation Request
↓
Knowledge Base Query
↓
Story Graph Query
↓
Prompt Engine
↓
Chapter Engine
↓
Consistency Engine
↓
AI Quality Review
↓
Human Review
↓
Feedback Loop
```

## 6.3 Feedback Flow

```text
Generated Chapter
↓
AI Quality Signals + Human Edits + Reader Feedback
↓
Feedback Loop
↓
Prompt Ranking + Pattern Ranking + Knowledge Ranking
↓
Rule Configuration Center + Knowledge Base
```
