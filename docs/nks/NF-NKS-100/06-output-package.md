# 6. Output Package

## 6.1 Package Structure

Book Knowledge Extraction 的标准输出包包含：

```text
BookKnowledgePackage
├── metadata
├── source_book
├── chapters
├── scenes
├── objects
├── relationships
├── rhythm_profiles
├── patterns
├── rules
├── evidence
├── review_report
└── export_manifest
```

## 6.2 Metadata

metadata 必须包含 package_id、document_id、book_id、extraction_version、extraction_time、extractor 和 status。

## 6.3 Objects

objects 必须按 NF-NKS-000 对象类型组织。

允许对象类型包括 Book、Chapter、Scene、Character、Faction、Location、Worldview、Power System、Artifact、Resource、Event、Conflict、Emotion、Reward、Hook、Climax、Foreshadowing、Pattern、Rhythm Profile、Asset、Rule、Prompt Template。

## 6.4 Relationships

relationships 必须引用 NF-NKS-000 的 Relationship Model。

每条关系必须包含 source_id、relation_type、target_id、confidence、evidence_id。

## 6.5 Export Manifest

export_manifest 必须记录 exported_files、object_count、relationship_count、evidence_count、validation_status 和 review_status。
