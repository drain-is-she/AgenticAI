from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


DEFAULT_KNOWLEDGE_DIR = Path(__file__).resolve().parents[1] / "knowledge"


def load_documents(folder=None):
    """Load PDFs from the bundled directory or an explicit caller-supplied path."""
    directory = DEFAULT_KNOWLEDGE_DIR if folder is None else Path(folder)
    if not directory.exists():
        raise FileNotFoundError(f"Knowledge directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Knowledge path is not a directory: {directory}")

    pdfs = sorted(path for path in directory.glob("*.pdf") if path.is_file())
    if not pdfs:
        raise ValueError(f"No PDF files found in knowledge directory: {directory}")

    documents = []
    for pdf in pdfs:
        loader = PyPDFLoader(str(pdf))
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = pdf.name
        documents.extend(docs)

    if not documents:
        raise ValueError(f"PDF files yielded no pages in knowledge directory: {directory}")
    return documents
