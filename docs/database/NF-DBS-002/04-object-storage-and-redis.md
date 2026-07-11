# 4. Object Storage and Redis

## 4.1 Object Storage Role

Object Storage 保存不适合直接进入 PostgreSQL 行字段的大文本和文件型资产。

推荐第一阶段使用 MinIO 本地兼容 S3 接口，后续可迁移到 S3-compatible 云存储。

## 4.2 Object Storage Data

Object Storage 保存：

- raw_text
- normalized_text
- source_file_uploads
- BookKnowledgePackage
- graph_package
- extraction_report
- quality_report
- generated_chapter_draft
- revision_diff
- long evidence excerpt

PostgreSQL 中只保存 object_ref、checksum、mime_type、byte_size、created_at 和 access policy。

## 4.3 Object Reference Rule

每个 object_ref 必须满足：

- 可追踪到创建任务或人工上传记录。
- 保存 checksum，支持完整性校验。
- 保存 logical owner，例如 book_id、chapter_id、extraction_run_id 或 generation_request_id。
- 不直接暴露永久公开 URL。

## 4.4 Redis Role

Redis 用于运行期协调，不作为权威数据源。

Redis 可保存：

- worker queue state
- task lock
- extraction progress cache
- generation progress cache
- rate limit counter
- short-lived retrieval cache
- agent orchestration heartbeat

Redis 中的数据必须可从 PostgreSQL 或 Object Storage 恢复，不能作为唯一事实来源。
