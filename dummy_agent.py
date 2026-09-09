import os 
from huggingface_hub import InterferenceClient 

client = InterferenceClient(model = "moonshotai/Kimi-K2.5")

output = client.chat.completions.create(
    messages = [{"role":"user", "content": "The capital of France is "},
                ], 
                stream = False ,
                max_tokens = 1024, 
                extra_body = {'thinking ': {'type':'disabled'}} ,  
)
print(output.choices[0].message.content)

SYSTEM_PROMPT = """Answer the following questions as best as you can.You have access to the : get_weather = Get current weather in a give location 
The best way you use the tools is by specifying the JSON blob. 
Specifically, this json should have an 'action' key(with the name of the tool to use)and 
the only values that should be in the "action" feild are : 
get_weather : Get the current weather in a given location , args : {"location":{"ty}}"""