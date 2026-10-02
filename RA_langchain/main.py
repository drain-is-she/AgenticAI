from rag.loader import load_documents
from rag.chunking import chunk_documents
from rag.embedding import get_embeddings
from rag.vector_store import create_vector_store
from rag.retrieval import create_retriever


def main():

    documents = load_documents("knowledge")

    print("Documents:", len(documents))

    chunks = chunk_documents(documents)

    print("Chunks:", len(chunks))

    embeddings = get_embeddings()

    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    retriever = create_retriever(
        vector_store
    )

    query = input("Query: ")

    results = retriever.invoke(query)

    for i, doc in enumerate(results):

        print("\n")
        print("RESULT:", i + 1)
        print("SOURCE:", doc.metadata.get("source"))
        print("PAGE:", doc.metadata.get("page"))
        print(doc.page_content)


if __name__ == "__main__":
    main()