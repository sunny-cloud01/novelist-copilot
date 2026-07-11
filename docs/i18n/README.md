# Bilingual Documentation Policy

This directory defines how Novel Factory maintains complementary Chinese and English documentation.

## Goals

- Preserve the existing canonical document build system.
- Keep complete domain semantics in the canonical specification files.
- Provide English companion navigation and summaries without duplicating unstable source content too early.
- Make translation status explicit and reviewable.
- Avoid uncontrolled parallel documents that drift silently.

## Language Roles

| Role                    | Language                       | Responsibility                                                    |
| ----------------------- | ------------------------------ | ----------------------------------------------------------------- |
| Canonical specification | Chinese-first, bilingual terms | Full domain meaning, constraints, examples, source chapters       |
| English companion       | English                        | Cross-team navigation, technical summaries, terminology alignment |
| Translation map         | Bilingual                      | Pairing, status, ownership and update tracking                    |

## File Organization

```text
docs/
├── zh-CN/
│   └── README.md
├── en-US/
│   └── README.md
├── i18n/
│   ├── README.md
│   └── document-map.md
├── {category}/
│   ├── {document-id}.md
│   └── {document-id}/
│       ├── README.md
│       └── {chapter}.md
```

## Translation Status

Allowed status values:

- `canonical`: primary maintained specification.
- `companion-summary`: English or Chinese summary exists, but not a full translation.
- `needs-translation`: no useful companion content yet.
- `in-review`: translation exists and is being reviewed.
- `aligned`: bilingual versions are considered semantically aligned.
- `outdated`: companion content needs update after canonical change.

## Update Rule

When any canonical document changes:

1. Keep source chapters as the source of truth.
2. Rebuild the canonical document with `python scripts/build_docs.py --write --document DOC-ID`.
3. Check whether English title, abstract, or terminology changed.
4. Update `document-map.md` when translation status or summary changes.
5. Run `python scripts/build_docs.py --check` before finishing.

## Boundary Rule

Do not create full translated copies of every source chapter until the corresponding canonical document is stable enough for review. Before that point, maintain bilingual entry points, abstracts and terminology maps.
