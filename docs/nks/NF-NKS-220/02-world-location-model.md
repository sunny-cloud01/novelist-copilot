# 2. World and Location Model

## 2.1 Worldview Model

Worldview 表示作品或题材的世界规则集合。

最小字段：

- worldview_id
- genre
- core_rules
- social_structure
- power_system_refs
- faction_refs
- location_refs
- resource_rules
- taboo_rules
- evidence_refs

## 2.2 Location Model

Location 表示事件发生或角色活动的空间节点。

最小字段：

- location_id
- canonical_name
- location_type
- parent_location_id
- worldview_id
- access_rules
- resident_factions
- available_resources
- danger_level
- evidence_refs

## 2.3 Location Hierarchy

Location 必须支持层级结构。

示例：

```text
World
└── Continent
    └── Kingdom
        └── City
            └── Auction House
```

子 Location 必须继承上级 Location 的世界规则，除非存在明确例外规则。
