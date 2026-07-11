# 2. Decision

Novel Factory 采用 Documentation Project Architecture。

每个正式文档同时维护：

```text
docs/{category}/{document-id}.md
docs/{category}/{document-id}/README.md
docs/{category}/{document-id}/{chapter}.md
```

语义约定：

- `{document-id}.md` 是 canonical 汇总文档和正式阅读版。
- `{document-id}/` 下的章节文件是 source chapters，用于局部维护和后续自动构建。
- 当前阶段允许人工同步 canonical 与 source chapters。
- 后续应引入 build script，使 source chapters 成为自动生成 canonical 文档的来源。
