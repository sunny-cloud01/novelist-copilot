# 3. Input Requirements

## 3.1 Book Input

Book 输入必须包含 book_id、title、author、platform、genre、tags、completion_status、source 和 chapters。

## 3.2 Chapter Input

Chapter 输入必须包含 chapter_id、book_id、chapter_index、title、raw_text 和 text_length。

## 3.3 Optional Metadata

可选元数据包括 platform_category、reader_rating、publish_time、author_notes、volume_name 和 source_url。

## 3.4 Text Preprocessing Requirement

抽取前必须完成基础预处理：

- 清理广告、页眉、页脚和重复水印。
- 保留章节标题。
- 保留原始段落顺序。
- 标记疑似 OCR 错误。
- 生成稳定 text_range。
