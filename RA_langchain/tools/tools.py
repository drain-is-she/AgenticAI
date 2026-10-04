from langchain_core.tools import tool


def create_research_tool(retriever):

    @tool
    def research_search(query: str) -> str:
        """Search the research PDFs for information relevant to the query."""

        documents = retriever.invoke(query)

        results = []

        for doc in documents:
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "unknown")

            results.append(
                f"Source: {source}, Page: {page}\n"
                f"{doc.page_content}"
            )

        return "\n\n".join(results)

    return research_search
research_tool = create_research_tool(retriever)