# 6. Authoring Rules

## 6.1 Front Matter

所有规范级文档必须包含 YAML Front Matter：

```yaml
document_id:
title:
version:
status:
category:
owner:
created:
updated:
dependencies:
references:
```

## 6.2 Formal Content Only

正式 Markdown 文档不得包含聊天说明、模型自述、下载提示、临时计划、未确认假设或页面渲染残留。

正式 Markdown 文档可以包含 Front Matter、正文规范、表格、图示代码块、References、Change Log 和 Approval 信息。

## 6.3 Cross References

禁止复制其他文档中的权威定义。

正确引用方式：

```text
See NF-NKS-000 Character Definition.
```

错误方式：重新定义 Character。

## 6.4 AI Knowledge Base

进入 AI Knowledge Base 的文档必须使用 Markdown 格式、UTF-8 编码、稳定 ID、明确章节，并且可被机器按标题、Front Matter 和稳定 ID 切片。
