# 4. Extraction Pipeline

标准抽取流水线：

```text
Step 1: Input Normalization
↓
Step 2: Chapter Segmentation
↓
Step 3: Scene Segmentation
↓
Step 4: Entity Extraction
↓
Step 5: Event Extraction
↓
Step 6: Relationship Extraction
↓
Step 7: Pattern Extraction
↓
Step 8: Rhythm Extraction
↓
Step 9: Rule and Consistency Extraction
↓
Step 10: Evidence Binding
↓
Step 11: Object Normalization
↓
Step 12: Quality Review
↓
Step 13: Knowledge Package Export
```

流水线必须支持 Book 级、Chapter 级和 Scene 级增量执行。
