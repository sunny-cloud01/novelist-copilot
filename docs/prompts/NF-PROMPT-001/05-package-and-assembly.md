# 5. Package and Assembly

## 5.1 Prompt Package

标准 Prompt Package：

```text
PromptPackage
├── metadata
├── template_ref
├── variables
├── knowledge_refs
├── graph_refs
├── constraints
├── output_contract
├── evaluation_rules
└── assembly_log
```

metadata 必须包含 prompt_package_id、template_id、template_version、task_id、agent_type 和 created_at。

## 5.2 Assembly Flow

Prompt 装配流程：

```text
Generation Goal
↓
Knowledge Query
↓
Story Graph Query
↓
Rule Selection
↓
Template Selection
↓
Variable Binding
↓
Constraint Injection
↓
Output Contract Binding
↓
Prompt Package Export
```
