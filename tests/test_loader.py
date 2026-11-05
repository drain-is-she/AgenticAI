"""Filesystem behavior tests with PDF parsing replaced by a test double."""
import importlib.util
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]


def load_loader(factory):
    community = ModuleType("langchain_community")
    loaders = ModuleType("langchain_community.document_loaders")
    loaders.PyPDFLoader = factory
    community.document_loaders = loaders
    spec = importlib.util.spec_from_file_location("pdf_loader", ROOT / "RA_langchain/rag/loader.py")
    module = importlib.util.module_from_spec(spec)
    with patch.dict("sys.modules", {"langchain_community": community,
                                    "langchain_community.document_loaders": loaders}):
        spec.loader.exec_module(module)
    return module


class DocumentLoaderTests(unittest.TestCase):
    def setUp(self):
        self.factory = Mock()
        self.factory.return_value.load.side_effect = lambda: [SimpleNamespace(page_content="page", metadata={"page": 0})]
        self.loader = load_loader(self.factory)

    def test_default_is_independent_of_working_directory(self):
        original = Path.cwd()
        with TemporaryDirectory() as folder:
            try:
                os.chdir(folder)
                documents = self.loader.load_documents()
            finally:
                os.chdir(original)
        expected = sorted((ROOT / "RA_langchain/knowledge").glob("*.pdf"))
        self.assertTrue(expected)
        self.assertEqual([Path(c.args[0]) for c in self.factory.call_args_list], expected)
        self.assertEqual([d.metadata["source"] for d in documents], [p.name for p in expected])

    def test_explicit_directory_sorted_files_and_metadata(self):
        with TemporaryDirectory() as folder:
            directory = Path(folder)
            for name in ["z.pdf", "a.pdf", "notes.txt"]:
                (directory / name).touch()
            (directory / "not-a-file.pdf").mkdir()
            documents = self.loader.load_documents(directory)
        self.assertEqual([d.metadata for d in documents], [
            {"page": 0, "source": "a.pdf"}, {"page": 0, "source": "z.pdf"}])

    def test_missing_directory(self):
        with TemporaryDirectory() as folder:
            with self.assertRaisesRegex(FileNotFoundError, "does not exist"):
                self.loader.load_documents(Path(folder) / "missing")
        self.factory.assert_not_called()

    def test_file_is_not_directory(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "file.pdf"
            path.touch()
            with self.assertRaisesRegex(NotADirectoryError, "not a directory"):
                self.loader.load_documents(path)
        self.factory.assert_not_called()

    def test_empty_directory(self):
        with TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "No PDF files"):
                self.loader.load_documents(folder)
        self.factory.assert_not_called()

    def test_no_pages(self):
        self.factory.return_value.load.side_effect = None
        self.factory.return_value.load.return_value = []
        with TemporaryDirectory() as folder:
            (Path(folder) / "empty.pdf").touch()
            with self.assertRaisesRegex(ValueError, "yielded no pages"):
                self.loader.load_documents(folder)


if __name__ == "__main__":
    unittest.main()
