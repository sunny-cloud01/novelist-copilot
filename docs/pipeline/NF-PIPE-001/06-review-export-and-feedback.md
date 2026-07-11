# 6. Review, Export and Feedback

## 6.1 Quality Review

Quality Review 在 BookKnowledgePackage 导出前执行。

检查内容：

- chapter coverage
- scene coverage
- object evidence coverage
- relationship validity
- unresolved object ratio
- contradiction candidates
- rhythm profile completeness
- extraction error severity

## 6.2 Human Review Gate

以下情况必须进入人工审核：

- 章节顺序存在严重冲突。
- 大量角色或地点无法归并。
- Story Graph 出现关键关系冲突。
- Rule 或 Consistency constraint 存在高严重级别矛盾。
- Quality Review 阻塞项未解决。

## 6.3 Package Export

Package Export 生成 BookKnowledgePackage 并写入 Object Storage。

PostgreSQL 必须保存：

- package_id
- book_id
- extraction_run_id
- package_ref
- checksum
- object_count
- relationship_count
- evidence_count
- validation_status
- review_status

## 6.4 Knowledge Base Commit

只有通过审核的对象和关系可以进入 Approved Knowledge Base。

Candidate 或 Reviewed 对象可以保留用于实验，但生成系统必须显式标记其来源和状态。

## 6.5 Feedback Capture

Pipeline 必须记录：

- 人工修正。
- 审核驳回原因。
- 抽取错误类别。
- 对后续 Prompt、Pattern、Rule 或 extraction rule 的改进建议。

这些信号进入 Feedback Service，用于后续优化抽取与生成质量。
