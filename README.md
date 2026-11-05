# Research Assistant and Agent Workflow Experiments

A learning repository exploring document retrieval and tool-using research assistants, alongside a roadmap from basic LLM calls to agent orchestration.

## What is implemented

- `RA_langchain/main.py`: loads PDFs, splits them into chunks, builds a vector store, and retrieves relevant passages for a query.
- `RA_langchain/rag/`: document loading, chunking, embedding, vector-store, and retrieval components.
- `RA_langchain/agent.py` and `tools/`: a draft LangChain research-agent integration.
- `complete_agentic_ai_learning_workflow.md`: learning roadmap; its stages are goals, not a list of completed features.
- `autonomus_company_RA/`: a work-in-progress scaffold, with several empty configuration and setup files.

## Current limitations

The terminal query loop sends the `messages` field, prints the final response content, skips blank input, and accepts `exit` regardless of case or surrounding whitespace. EOF and Ctrl+C at the input prompt also exit cleanly. Each query is independent; conversation memory is not implemented.

A tested dependency specification and end-to-end retrieval/model verification are still needed. API-backed components require separately configured credentials and may incur provider charges. The offline tests below verify terminal-loop behavior and retrieval wiring with test doubles; they do not establish that the full research assistant is ready to run.

Keep local credentials in environment variables or an ignored `.env` file. Do not add credentials to source code or notebooks.

## Document paths

Both research entry points call `load_documents()` to locate the bundled `RA_langchain/knowledge/` directory relative to the loader file, independent of the terminal’s current directory. For a custom location, call `load_documents(path)`; explicit relative paths remain relative to the caller’s working directory. The loader reads top-level `*.pdf` files in sorted order and preserves page metadata while labeling each source with its filename.

Missing directories, paths that are files, directories without PDFs, and PDFs yielding no pages raise clear errors before the embedding/vector-store steps. Dependency setup and actual PDF parsing still need end-to-end verification.

## Offline regression tests

From the repository root, run:

```sh
python -m unittest discover -s tests -v
```

The sixteen tests use fake agents/retrievers and a fake PDF parser and Python’s standard library, with no API keys, network requests, model downloads, or LangChain installation. They cover the request schema, displayed answers, multiple independent queries, blank input, exit variants, and terminal closure. Framework and retrieval imports are deferred until `build_agent()` is called so the terminal loop can be tested independently. Retrieval tests also check import safety, top-five configuration, source/page formatting, missing metadata, and empty results. Loader tests cover default paths from another working directory, custom directories, file ordering, metadata, and invalid/empty input. The LangChain tool decorator and PDF parser are replaced with test doubles; framework schema validation and actual PDF/vector search are not covered.

Retrieval modules define factories without executing example queries at import time. Call `create_retriever(vector_store)` and `create_research_tool(retriever)` with initialized dependencies before searching.

## Next milestones

1. Validate the complete agent setup and add retrieval/tool integration tests.
2. Document and pin a verified dependency environment.
3. Add a small retrieval evaluation set and cite source passages in responses.
4. Separate completed examples from planned orchestration experiments.
