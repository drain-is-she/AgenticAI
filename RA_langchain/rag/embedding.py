from langchain_openai import OpenAIEmbeddings


def get_embeddings():
    return OpenAIEmbeddings(
        model="text-embedding-3-small"
    )