from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_documents(folder="knowledge"):
    documents = []

    for pdf in Path(folder).glob("*.pdf"):
        loader = PyPDFLoader(str(pdf))
        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = pdf.name

        documents.extend(docs)

    return documents