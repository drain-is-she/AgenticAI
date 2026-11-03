def create_retriever(vector_store):
    return vector_store.as_retriever(
        search_kwargs={
            "k": 5
        }
    )
