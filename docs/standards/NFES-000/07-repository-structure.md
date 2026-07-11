# 7. Repository Structure

推荐目录：

```text
NovelFactory-Docs/
├── docs/
│   ├── zh-CN/
│   ├── en-US/
│   ├── i18n/
│   ├── standards/
│   ├── prd/
│   ├── nks/
│   ├── adr/
│   ├── architecture/
│   ├── database/
│   ├── pipeline/
│   ├── agents/
│   ├── prompts/
│   ├── rag/
│   ├── quality/
│   ├── implementation/
│   └── operations/
├── schemas/
├── templates/
├── examples/
├── assets/
├── scripts/
└── build/
```

规范文件命名：

```text
NF-{CATEGORY}-{NUMBER}-{NAME}.md
```

在文档工程中，推荐同时维护：

```text
docs/{category}/{document-id}.md
docs/{category}/{document-id}/README.md
docs/{category}/{document-id}/{chapter}.md
```

双语文档入口推荐维护：

```text
docs/zh-CN/README.md
docs/en-US/README.md
docs/i18n/README.md
docs/i18n/document-map.md
```

`docs/{category}/{document-id}.md` 仍是 canonical reading version。`docs/zh-CN/` 和 `docs/en-US/` 用于阅读入口、摘要、术语对齐和协作导航，不替代 source chapters。

完整翻译版本只有在对应 canonical 文档稳定后再创建。创建完整翻译时，必须在 `docs/i18n/document-map.md` 记录路径、状态和更新责任。
