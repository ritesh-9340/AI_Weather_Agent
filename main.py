from sample import agentic_weather
from dotenv import load_dotenv
from groq import Groq
import os
import json


load_dotenv()
client=Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
MODEL="openai/gpt-oss-20b"

weather_agent = agentic_weather()
temperature = weather_agent.get_weather("New York")



with open("tools.json", "r") as file:
    TOOLS = json.load(file)

TOOL_FUNCTIONS = {
    "get_weather" :weather_agent.get_weather,
    "suggest_activity":weather_agent.suggest_activity
    
}

MESSAGES = [
    {
        "role": "user",
        "content": "How is the weather in New York City?"
    }
]
res = client.chat.completions.create(
    model = MODEL,
    max_tokens = 1000,
    tools= TOOLS,
    messages= MESSAGES
)


#appending the mag to MESSAGE so that LLM should know that we first got the msg and then we already made a tool call

MESSAGES.append(res.choices[0].message)

#Execute tool to send back observation to Model

for call in res.choices[0].message.tool_calls:
    tool_id = call.id
    func_name =call.function.name
    _args = json.loads(call.function.arguments)
    # json.loads(call.function.arguments)

    #get_weather(city='Denver')
    tool_output = TOOL_FUNCTIONS[func_name](**_args)

    MESSAGES.append( {"role": "tool", "content": str(tool_output) , "tool_call_id": tool_id, "name": func_name})



#Call LLM for processing the output
res = client.chat.completions.create(
    model = MODEL,
    max_tokens = 1000,
    tools= TOOLS,
    messages= MESSAGES
)


message = res.choices[0].message

if message.tool_calls:
    for call in message.tool_calls:
        func_name = call.function.name
        args = json.loads(call.function.arguments)

        tool_output = TOOL_FUNCTIONS[func_name](**args)

        print(tool_output)

else:
    print(message.content)


    