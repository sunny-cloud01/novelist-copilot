# 4. Prompt Variable Model

Prompt 变量必须包含以下元数据：

- variable_name
- source_document
- source_object_type
- source_id
- required
- default_value
- validation_rule

变量命名规则：

- 使用 snake_case。
- 不使用含糊名称。
- 引用 NKS 对象时必须保留 source_id。

示例变量：

- character_profile
- faction_context
- location_context
- active_rules
- unresolved_hooks
- rhythm_target
- chapter_goal
- forbidden_changes
