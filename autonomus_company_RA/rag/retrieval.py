from rag.embedding import semantic_search


retrieval_tool = semantic_search(
    vector_store,
    word_to_id,
    word_embeddings
)


def search_knowledge_base(query: str):

    results = retrieval_tool.search(
        query,
        top_k=5
    )

    return results