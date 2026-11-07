"""Real FAISS retrieval with deterministic vectors, not semantic-quality metrics."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

ROOT = Path(__file__).resolve().parents[2]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vector_store = load_module("real_vector_store", "RA_langchain/rag/vector_store.py")
retrieval = load_module("real_retrieval", "RA_langchain/rag/retrieval.py")
research_tools = load_module("vector_research_tools", "RA_langchain/tools/tools.py")


class CoordinateEmbeddings(Embeddings):
    """Encode numeric fixture text as a point on a line; no learned model."""
    def embed_documents(self, texts):
        return [[float(text), 0.0] for text in texts]

    def embed_query(self, text):
        return [float(text), 0.0]


class VectorPipelineTests(unittest.TestCase):
    def setUp(self):
        guard = patch("socket.socket.connect", side_effect=AssertionError("Network access forbidden"))
        guard.start()
        self.addCleanup(guard.stop)
        # Deliberately unsorted: insertion order must not masquerade as ranking.
        self.documents = [Document(page_content=str(n), metadata={
            "source": f"fixture-{n}.pdf", "page": n,
        }) for n in [6, 0, 4, 1, 5, 2, 3]]

    def make_retriever(self, documents):
        store = vector_store.create_vector_store(documents, CoordinateEmbeddings())
        return retrieval.create_retriever(store)

    def test_top_five_are_ranked_by_distance(self):
        retriever = self.make_retriever(self.documents)
        results = retriever.invoke("0")
        self.assertEqual([d.page_content for d in results], ["0", "1", "2", "3", "4"])
        self.assertEqual([d.metadata for d in results], [
            {"source": f"fixture-{n}.pdf", "page": n} for n in range(5)
        ])
        # Changing query must change ranking rather than returning a fixed list.
        self.assertEqual([d.page_content for d in retriever.invoke("6")],
                         ["6", "5", "4", "3", "2"])

    def test_small_corpus_returns_only_available_documents(self):
        results = self.make_retriever(self.documents[:2]).invoke("0")
        self.assertEqual([d.page_content for d in results], ["0", "6"])

    def test_real_tool_exposes_retrieved_sources(self):
        search = research_tools.create_research_tool(self.make_retriever(self.documents))
        result = search.invoke({"query": "0"})
        self.assertEqual(result, "\n\n".join(
            f"Source: fixture-{n}.pdf, Page: {n}\n{n}" for n in range(5)
        ))


if __name__ == "__main__":
    unittest.main()
