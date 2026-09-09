from openai import OpenAI
import json 
company  = input("Enter the company name")

goal = "Find the latest available revenue of the given company "
client = OpenAI() 
def search_web(query):
    return f"search results for :{query}"
def calculation(expression ) :
    return f"result of {expression}"
TOOLS = {
    "search_web" : search_web , 
    "calculator" : calculation 
}

tools = [
    {
    "type" : "function",
    "function" : {
        "name" : "search_web" , 
        "description" : "Search web for information", 
        "parameters" : {
            "type" : "object", 
            "properties":{
                "query" : {
                    "type" : "string", 
                    "description" : "The search query "
                } 
            },
            "required" : ["query "]
        } 
    }
},
{
    "type" : "function", 
    "function": {
        "name" : "calculation" , 
        "description" : "perform calculations" , 
        "parameters" :{
            "type" : "object", 
            "properties" : {
                "type": "string", 
                "description" : 'The mathematical expression'
            }
        },
        "required" : ["expression"]
    }
} 

]
SYSTEM_PROMPT = f"""
You are an AI agent whose goal is : 
{goal}
You have access to the tool named as search_web. 
When you need an external information, use tje search_web tool.
Use the tool to find the information about the company which is reliable 
from the recent year revenue 
Donot makeup the information. 
Deny if no resposne is available. 
After recieving the final output return the answer. 
""" 
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": f"Find the latest revenue of {company}."
    }
]

# agent loop 
MAX_STEPS = 5 
for step in range(MAX_STEPS) : 
    response = client.chat.completions.create(
        model = "gpt-4.0 " , 
        messages = messages , 
        tools = tools
    )
    messages.append(message)
    # if no more tools are required we assume the tasks have been
    # completed 
    if not message.tool_calls : 
        print("Final answer ")
        print(message.content)
        break 

    for tool_call in messages.tool_calls : 
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        tool_function = TOOLS[tool_name]
        result = tool_function(**arguments)

        message.append({
            "role" : "tool", 
            "tool_call_id" : tool_call.id , 
            "content" : result 
        }) 
 
else : 
    print("agent stopped : maximum number of steps reached ")