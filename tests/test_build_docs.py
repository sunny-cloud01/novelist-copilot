import tempfile
import unittest
from pathlib import Path

from scripts.build_docs import build_document, check_document, discover_documents


class BuildDocsTest(unittest.TestCase):
    def test_build_document_preserves_front_matter_and_title_then_appends_numbered_chapters(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            canonical = root / "docs" / "nks" / "NF-NKS-100.md"
            source_dir = root / "docs" / "nks" / "NF-NKS-100"
            source_dir.mkdir(parents=True)
            canonical.parent.mkdir(parents=True, exist_ok=True)
            canonical.write_text(
                "---\n"
                "document_id: NF-NKS-100\n"
                "title: Example\n"
                "---\n\n"
                "# NF-NKS-100\n\n"
                "# Example\n\n"
                "old body\n",
                encoding="utf-8",
            )
            (source_dir / "README.md").write_text("# Index\n", encoding="utf-8")
            (source_dir / "02-second.md").write_text("# 2. Second\n\nBody 2\n", encoding="utf-8")
            (source_dir / "01-first.md").write_text("# 1. First\n\nBody 1\n", encoding="utf-8")

            rendered = build_document(canonical, source_dir)

            self.assertEqual(
                rendered,
                "---\n"
                "document_id: NF-NKS-100\n"
                "title: Example\n"
                "---\n\n"
                "# NF-NKS-100\n\n"
                "# Example\n\n"
                "# 1. First\n\n"
                "Body 1\n\n"
                "# 2. Second\n\n"
                "Body 2\n",
            )

    def test_check_document_reports_when_canonical_differs_from_source_chapters(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            canonical = root / "docs" / "prd" / "NF-PRD-001.md"
            source_dir = root / "docs" / "prd" / "NF-PRD-001"
            source_dir.mkdir(parents=True)
            canonical.parent.mkdir(parents=True, exist_ok=True)
            canonical.write_text(
                "---\ndocument_id: NF-PRD-001\n---\n\n# NF-PRD-001\n\n# Product\n\nstale\n",
                encoding="utf-8",
            )
            (source_dir / "01-purpose.md").write_text("# 1. Purpose\n\nFresh\n", encoding="utf-8")

            self.assertFalse(check_document(canonical, source_dir))

    def test_build_document_does_not_treat_existing_first_chapter_as_title_block(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            canonical = root / "docs" / "nks" / "NF-NKS-200.md"
            source_dir = root / "docs" / "nks" / "NF-NKS-200"
            source_dir.mkdir(parents=True)
            canonical.parent.mkdir(parents=True, exist_ok=True)
            canonical.write_text(
                "---\n"
                "document_id: NF-NKS-200\n"
                "---\n\n"
                "# NF-NKS-200\n\n"
                "# Story Graph Model Specification\n\n"
                "# 1. Purpose and Scope\n\n"
                "Existing generated chapter.\n",
                encoding="utf-8",
            )
            (source_dir / "01-purpose-and-scope.md").write_text(
                "# 1. Purpose and Scope\n\nFresh chapter.\n",
                encoding="utf-8",
            )

            rendered = build_document(canonical, source_dir)

            self.assertEqual(rendered.count("# 1. Purpose and Scope"), 1)

    def test_discover_documents_finds_canonical_with_matching_source_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            canonical = root / "docs" / "api" / "NF-API-001.md"
            source_dir = root / "docs" / "api" / "NF-API-001"
            source_dir.mkdir(parents=True)
            canonical.write_text("---\ndocument_id: NF-API-001\n---\n\n# NF-API-001\n", encoding="utf-8")

            docs = discover_documents(root)

            self.assertEqual(docs, [(canonical, source_dir)])


if __name__ == "__main__":
    unittest.main()
