import json 
from tools import TOOLS 
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
MAX_STEPS = 5 # atmost 
MODEL = "gpt-4o-mini"
SYSTEM_PROMPT = """
You are an AI research agent.

Your goal is to research a company and provide a reliable, 
structured report based on information obtained through your tools.

You have access to the following tools:

1. search_web
   - Search the web for relevant information.

2. calculator
   - Perform mathematical calculations.

3. get_stock_price
   - Get stock information for a company.

4. get_company_info
   - Get financial/company information.

5. fetch_webpage
   - Fetch and read information from a specific webpage.

6. save_report
   - Save the final research report.
7. search_knowledge_base
   - Search the knowledge base for relevant information.

When you need to use a tool, output ONLY a JSON action:

{
    "action": "tool_name",
    "action_input": {
        "parameter": "value"
    }
}

Examples:

{
    "action": "search_web",
    "action_input": {
        "query": "latest NVIDIA revenue"
    }
}

{
    "action": "calculator",
    "action_input": {
        "expression1": "100",
        "expression2": "80",
        "operand": "-"
    }
}

{
    "action": "get_stock_price",
    "action_input": {
        "company_name": "NVIDIA",
        "year": "2026"
    }
}

{
    "action": "get_company_info",
    "action_input": {
        "company_name": "NVIDIA"
    }
}

{
    "action": "fetch_webpage",
    "action_input": {
        "url": "https://example.com"
    }
}

{
    "action": "save_report",
    "action_input": {
        "information": "Final research report..."
    }
}
{
    "action": "search_knowledge_base",
    "action_input": {
        "query": "NVIDIA latest revenue"
    }
}

IMPORTANT RULES:

1. Do not invent information.
2. Do not generate an observation yourself.
3. An observation will only be provided after a tool has actually been executed.
4. After receiving an observation, decide whether:
   - another tool is required, or
   - the research is complete.
5. If a tool returns no useful information, try another appropriate
   tool or search query before asking the user.
6. When sufficient information has been collected, provide the final answer.
"""


messages = [
    {
        "role" : "system" , 
        "content" : SYSTEM_PROMPT 
    }, 
    {
        "role" : "user" , 
        "content" : "Find the latest revenue of NVIDIA."
    }
]
# this part was used when i didnt use the langchain 
# response = client.chat.completions.create(
#     model = MODEL , 
#     messages = messages 
# )

#after introducing the langchain 
llm = ChatOpenAI(
    MODEL = ChatOpenAI(
        model = "gpt-4o-mini", 
        temprature = 0 
    )
)
response = llm.invoke("Explain MAML ")
#after introducing the langchain 
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using the provided research context."),
    ("human", "{question}\n\nContext:\n{context}")
])
# AGENT LOOP    
MAX_STEPS = 5

for step in range(MAX_STEPS):

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    assistant_message = response.choices[0].message.content

    print("\nAGENT:")
    print(assistant_message)

    action = json.loads(assistant_message)

    tool_name = action["action"]
    arguments = action["action_input"]

    # STEP 8: stop condition
    if tool_name == "final_answer":
        print("\nFINAL ANSWER:")
        print(arguments["answer"])
        break

    # STEP 6: execute tool outside LLM
    tool_function = TOOLS[tool_name]
    observation = tool_function(**arguments)

    print("\nOBSERVATION:")
    print(observation)

    # STEP 7: maintain state
    messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    messages.append({
        "role": "user",
        "content": f"OBSERVATION:\n{observation}"
    })

else:
    print("Agent stopped: maximum number of steps reached.")