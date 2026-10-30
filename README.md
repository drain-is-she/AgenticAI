# Research Assistant and Agent Workflow Experiments

A learning repository exploring document retrieval and tool-using research assistants, alongside a roadmap from basic LLM calls to agent orchestration.

## What is implemented

- `RA_langchain/main.py`: loads PDFs, splits them into chunks, builds a vector store, and retrieves relevant passages for a query.
- `RA_langchain/rag/`: document loading, chunking, embedding, vector-store, and retrieval components.
- `RA_langchain/agent.py` and `tools/`: a draft LangChain research-agent integration.
- `complete_agentic_ai_learning_workflow.md`: learning roadmap; its stages are goals, not a list of completed features.
- `autonomus_company_RA/`: a work-in-progress scaffold, with several empty configuration and setup files.

## Current limitations

The agent draft needs fixes before it is ready to run: the input field is spelled `messgaes`, its final response is not printed, and the exit check includes a trailing space. A tested dependency specification and automated checks have not yet been added. API-backed components require separately configured credentials and may incur provider charges.

Keep local credentials in environment variables or an ignored `.env` file. Do not add credentials to source code or notebooks.

## Next milestones

1. Repair and test the query/response loop.
2. Document and pin a verified dependency environment.
3. Add a small retrieval evaluation set and cite source passages in responses.
4. Separate completed examples from planned orchestration experiments.
