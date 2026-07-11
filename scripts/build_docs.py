#!/usr/bin/env python3
"""Build canonical Markdown documents from chapter source files."""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path


DOCUMENT_PREFIXES = ("NFES-", "NF-")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def split_front_matter(content: str) -> tuple[str, str]:
    if not content.startswith("---\n"):
        return "", content

    marker = "\n---\n"
    end = content.find(marker, 4)
    if end == -1:
        return "", content

    front_matter = content[: end + len(marker)]
    body = content[end + len(marker) :]
    return front_matter, body


def extract_title_block(body: str) -> str:
    lines = body.splitlines()
    headings: list[str] = []
    index = 0

    while index < len(lines) and lines[index] == "":
        index += 1

    while index < len(lines) and len(headings) < 2:
        if not lines[index].startswith("# "):
            break
        headings.append(lines[index])
        index += 1
        while index < len(lines) and lines[index] == "":
            index += 1

    if not headings:
        return ""
    return "\n\n".join(headings) + "\n\n"


def source_chapter_files(source_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in source_dir.glob("*.md")
        if path.name != "README.md" and path.is_file()
    )


def build_document(canonical_path: Path, source_dir: Path) -> str:
    canonical = read_text(canonical_path)
    front_matter, body = split_front_matter(canonical)
    title_block = extract_title_block(body)

    chapters: list[str] = []
    for chapter_path in source_chapter_files(source_dir):
        chapter = read_text(chapter_path).strip() + "\n"
        chapters.append(chapter)

    rendered = ""
    if front_matter:
        rendered += front_matter.rstrip() + "\n\n"
    rendered += title_block
    rendered += "\n".join(chapters)
    return rendered.rstrip() + "\n"


def check_document(canonical_path: Path, source_dir: Path, show_diff: bool = False) -> bool:
    expected = build_document(canonical_path, source_dir)
    actual = read_text(canonical_path)
    if actual == expected:
        return True

    if show_diff:
        diff = difflib.unified_diff(
            actual.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile=str(canonical_path),
            tofile=f"{source_dir}/",
        )
        sys.stdout.writelines(diff)
    return False


def discover_documents(root: Path) -> list[tuple[Path, Path]]:
    docs_root = root / "docs"
    if not docs_root.exists():
        return []

    documents: list[tuple[Path, Path]] = []
    for canonical_path in sorted(docs_root.glob("*/*.md")):
        if canonical_path.name == "README.md":
            continue
        if not canonical_path.name.startswith(DOCUMENT_PREFIXES):
            continue
        source_dir = canonical_path.with_suffix("")
        if source_dir.is_dir():
            documents.append((canonical_path, source_dir))
    return documents


def select_documents(root: Path, document_ids: list[str]) -> list[tuple[Path, Path]]:
    documents = discover_documents(root)
    if not document_ids:
        return documents

    wanted = set(document_ids)
    selected = [item for item in documents if item[0].stem in wanted]
    found = {item[0].stem for item in selected}
    missing = sorted(wanted - found)
    if missing:
        raise SystemExit(f"Unknown document id(s): {', '.join(missing)}")
    return selected


def command_list(documents: list[tuple[Path, Path]]) -> int:
    for canonical_path, source_dir in documents:
        print(f"{canonical_path} <- {source_dir}/")
    return 0


def command_check(documents: list[tuple[Path, Path]]) -> int:
    failed = []
    for canonical_path, source_dir in documents:
        if check_document(canonical_path, source_dir, show_diff=True):
            print(f"OK {canonical_path}")
        else:
            failed.append(canonical_path)

    if failed:
        print("\nOut of sync:")
        for path in failed:
            print(f"- {path}")
        return 1
    return 0


def command_write(documents: list[tuple[Path, Path]]) -> int:
    for canonical_path, source_dir in documents:
        rendered = build_document(canonical_path, source_dir)
        write_text(canonical_path, rendered)
        print(f"WROTE {canonical_path}")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--document", action="append", default=[], help="Build/check one document id, e.g. NF-NKS-100. Can be repeated.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true", help="List discovered canonical documents and source directories.")
    mode.add_argument("--check", action="store_true", help="Check whether canonical documents match source chapters.")
    mode.add_argument("--write", action="store_true", help="Regenerate canonical documents from source chapters.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).resolve()
    documents = select_documents(root, args.document)

    if args.list:
        return command_list(documents)
    if args.check:
        return command_check(documents)
    if args.write:
        return command_write(documents)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
