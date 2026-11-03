"""Offline tests of retrieval wiring; LangChain's decorator is a test double."""
import importlib.util
from pathlib import Path
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1] / "RA_langchain"


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_tools():
    # Isolate repository code from the optional framework dependency. Returning
    # the function unchanged tests formatting, not LangChain's schema/decorator.
    core = ModuleType("langchain_core")
    tools = ModuleType("langchain_core.tools")
    tools.tool = lambda function: function
    core.tools = tools
    with patch.dict("sys.modules", {"langchain_core": core, "langchain_core.tools": tools}):
        return load_module("research_tools", "tools/tools.py")


class RetrievalTests(unittest.TestCase):
    def test_import_and_top_five_configuration(self):
        module = load_module("retrieval", "rag/retrieval.py")
        store = Mock()
        retriever = module.create_retriever(store)
        self.assertIs(retriever, store.as_retriever.return_value)
        store.as_retriever.assert_called_once_with(search_kwargs={"k": 5})
        retriever.invoke.assert_not_called()

    def test_tool_creation_does_not_query(self):
        module = load_tools()
        retriever = Mock()
        search = module.create_research_tool(retriever)
        self.assertTrue(callable(search))
        retriever.invoke.assert_not_called()

    def test_passages_keep_their_sources_and_pages(self):
        module = load_tools()
        retriever = Mock()
        retriever.invoke.return_value = [
            SimpleNamespace(metadata={"source": "attention.pdf", "page": 0}, page_content="Attention passage"),
            SimpleNamespace(metadata={"source": "ml.pdf", "page": 7}, page_content="ML passage"),
        ]
        result = module.create_research_tool(retriever)("How does attention work?")
        retriever.invoke.assert_called_once_with("How does attention work?")
        self.assertEqual(result, "Source: attention.pdf, Page: 0\nAttention passage\n\n"
                                 "Source: ml.pdf, Page: 7\nML passage")

    def test_missing_metadata(self):
        module = load_tools()
        retriever = Mock()
        retriever.invoke.return_value = [SimpleNamespace(metadata={}, page_content="Unattributed passage")]
        self.assertEqual(module.create_research_tool(retriever)("query"),
                         "Source: unknown, Page: unknown\nUnattributed passage")

    def test_empty_results(self):
        module = load_tools()
        retriever = Mock()
        retriever.invoke.return_value = []
        self.assertEqual(module.create_research_tool(retriever)("query"), "")


if __name__ == "__main__":
    unittest.main()
