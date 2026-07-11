# 6. Tool Boundary

Tool access must be scoped by Agent role.

- Ingestion Agent may access source import and preprocessing tools.
- Extraction Agent may access text analysis and knowledge extraction tools.
- Graph Agent may access graph validation tools.
- Generation Agent may access LLM generation tools and Prompt Engine output.
- Review Agent may access quality checks and consistency reports.
- Feedback Agent may access feedback analytics and ranking tools.

No Agent may directly modify Approved or Frozen knowledge without review workflow.
