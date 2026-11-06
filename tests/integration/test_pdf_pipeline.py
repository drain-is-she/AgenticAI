"""Real PDF/parser and tool-wrapper checks, without embeddings or model calls."""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


loader = load_module("real_pdf_loader", "RA_langchain/rag/loader.py")
tools = load_module("real_research_tools", "RA_langchain/tools/tools.py")


def write_fixture(path):
    """Write an original one-page PDF with searchable text and valid offsets."""
    stream = b"BT /F1 12 Tf 72 720 Td (Offline research fixture.) Tj ET"
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    data = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f"{number} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(data)
    data.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        data.extend(f"{offset:010d} 00000 n \n".encode())
    data.extend(f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    path.write_bytes(data)


class PDFPipelineTests(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        write_fixture(Path(self.folder.name) / "fixture.pdf")
        # Fail if these supposedly offline operations try opening a connection.
        guard = patch("socket.socket.connect", side_effect=AssertionError("Network access forbidden"))
        guard.start()
        self.addCleanup(guard.stop)

    def test_real_parser_extracts_text_and_page_metadata(self):
        documents = loader.load_documents(self.folder.name)
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0].page_content.strip(), "Offline research fixture.")
        self.assertEqual(documents[0].metadata["source"], "fixture.pdf")
        self.assertEqual(documents[0].metadata["page"], 0)

    def test_real_tool_wrapper_returns_parsed_evidence(self):
        documents = loader.load_documents(self.folder.name)
        retriever = Mock()
        retriever.invoke.return_value = documents
        search = tools.create_research_tool(retriever)
        result = search.invoke({"query": "What does the fixture say?"})
        retriever.invoke.assert_called_once_with("What does the fixture say?")
        self.assertIn("Source: fixture.pdf, Page: 0", result)
        self.assertIn("Offline research fixture.", result)


if __name__ == "__main__":
    unittest.main()
