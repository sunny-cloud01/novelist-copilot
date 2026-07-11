# 3. Ingestion Stages

## 3.1 Source Submission

Source Submission 接收待拆解作品。

输入至少包含：

- title
- author
- platform
- genre
- tags
- source
- file_ref or text_ref
- submitted_by

输出：source_book candidate 和 ingestion_run。

## 3.2 Book Registration

Book Registration 创建 source_books 记录。

要求：

- 使用稳定 book_id。
- 记录 import_status。
- 记录 source metadata。
- 生成 idempotency_key，防止重复导入同一作品。

## 3.3 File Intake

File Intake 将原始文件写入 Object Storage，并在 PostgreSQL 保存 object_ref。

每个文件必须记录：

- object_ref
- checksum
- byte_size
- mime_type
- source_book_id
- uploaded_at

## 3.4 Text Normalization

Text Normalization 负责将原始文件转为 normalized_text。

处理内容：

- 编码归一化。
- 去除广告、水印、页眉和页脚。
- 保留章节标题。
- 保留段落顺序。
- 标记疑似 OCR 或排版错误。
- 生成 text_range。

不得改写正文语义。

## 3.5 Chapter Segmentation

Chapter Segmentation 识别章节边界并创建 source_chapters。

要求：

- chapter_index 必须连续。
- title 缺失时允许生成标题，但必须标记 generated_title。
- text_range 必须指向 normalized_text。
- 缺章、重复章、章节顺序异常必须进入 segmentation_report。
