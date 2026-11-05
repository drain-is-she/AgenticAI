def build_agent():
    from langchain.agents import create_agent
    from langchain_openai import ChatOpenAI
    from rag.loader import load_documents
    from rag.chunking import chunk_documents
    from rag.embedding import get_embeddings
    from rag.vector_store import create_vector_store
    from rag.retrieval import create_retriever
    from tools.tools import create_research_tool


    documents = load_documents()
    chunks = chunk_documents(documents)
    embeddings = get_embeddings()
    vector_store = create_vector_store(chunks , embeddings)
    retriever = create_retriever(vector_store)
    research_tool = create_research_tool(retriever)     

    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
    )

    agent = create_agent(
        model = model , 
        tools = [research_tool], 
        system_prompt= """
     You are an autonomous research assistant. You have access to a tool that allows you to search through a collection of research PDFs for information relevant to a given query. Use this tool to find the most relevant information and provide concise, accurate answers based on the retrieved content. If the information is not available in the documents, respond accordingly."""
    )
    return agent 


def run_chat(agent, input_fn=input, output_fn=print):
    """Run independent research queries against an already-built agent."""
    while True:
        try:
            query = input_fn("\n You : ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if query.lower() == "exit":
            break
        if not query:
            continue

        result = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        final_message = result["messages"][-1]
        output_fn(final_message.content)


def main():
    run_chat(build_agent())


if __name__ == "__main__":
    main()
