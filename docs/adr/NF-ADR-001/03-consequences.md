# 3. Consequences

## 3.1 Positive Consequences

- 长文档可以逐章维护。
- 文档结构适合 Git diff 和 Review。
- AI/RAG 可以按章节稳定切片。
- 后续可自动生成 Markdown、PDF、JSON、YAML 和网站。
- 每个文档可拥有独立章节索引。

## 3.2 Negative Consequences

- 当前没有自动构建脚本时，canonical 文件和章节源文件可能漂移。
- 文档数量增加，目录结构更复杂。
- 作者必须理解 canonical 与 source chapters 的关系。

## 3.3 Mitigations

- README 必须登记 canonical 文档。
- 每个章节目录必须包含 README.md。
- 后续应创建构建脚本，将 source chapters 合并成 canonical 文档。
- Validation 应检查 Front Matter、document_id、占位符和章节完整性。
