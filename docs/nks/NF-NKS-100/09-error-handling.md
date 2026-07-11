# 9. Error Handling

## 9.1 Error Categories

抽取错误分类：input_error、segmentation_error、extraction_error、normalization_error、relationship_error、validation_error、review_error。

## 9.2 Error Record

错误记录必须包含 error_id、error_category、source_id、severity、message、recovery_action、created_at。

## 9.3 Recovery Requirements

系统必须支持：

- 跳过单个失败 Scene 并继续处理后续 Scene。
- 标记失败章节并进入人工审核。
- 回滚单次抽取产生的候选对象。
- 在后续章节中补全缺失别名和关系。
