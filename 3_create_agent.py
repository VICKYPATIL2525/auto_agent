
import os
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
import json


load_dotenv()

# 1. Initialize LLM
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL_TOOL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0
)


# 2. Define a tool
@tool
def get_admin_name() -> str:
    """Returns the name of the system administrator."""
    print(">>> TOOL EXECUTED")
    return "Vicky Vijay Patil"

@tool
def add(num1, num2) -> int:
    """ This tool is to add 2 number"""
    return num1 +num2+5

@tool
def sub(num1, num2) -> int:
    """ This tool is for substracting 2 numbers"""
    return num1-num2-5

@tool
def greeting(name: str) -> str:
    """Generate a greeting for the given user name."""
    print(">>> GREETING TOOL EXECUTED")
    return f"Good morning {name}"


@tool
def countchar(string: str) -> str:
    """Count characters in the string received and return that many stars."""
    print(">>> COUNTCHAR TOOL EXECUTED")
    output = len(string)
    return "*" * output


@tool
def code(output: str) -> str:
    """Generate the final secret code using the star string received from countchar."""
    print(">>> CODE TOOL EXECUTED")
    return output[:-1] + "hh"


@tool
def get_customer_data() -> str:
    """Fetch all customer records from the customers.json file.
    Use this tool whenever the user asks questions about customers.
    """
    with open("customers.json", "r") as file:
        customers = json.load(file)

    return json.dumps(customers, indent=2)

    
tools = [get_admin_name, add, sub, greeting, countchar, code, get_customer_data]

# 3. Create prebuilt agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt ="""
You are a helpful assistant.

CUSTOMER DATA RULES:

1. Whenever the user asks anything about customers,
   call get_customer_data.
2. Wait for the tool response.
3. Read the customer records returned by the tool.
4. Answer the user's question using the retrieved data.
5. Never invent customer information.

SECRET CODE RULES:

When the user asks for a greeting and secret code:

1. First call greeting.
2. Pass its actual output to countchar.
3. Pass the actual countchar output to code.
4. Wait for each tool result before calling the next tool.
5. Return the final result.
"""
)

while True:
    userinput = input("User: ")
    result = agent.invoke({
    "messages": [
        {"role": "user", "content": userinput}
    ]
})
    print(result)


# # 4. Invoke agent
# result = agent.invoke()
