
import os
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain.tools import tool

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

tools = [get_admin_name]
# 3. Bind tool to LLM
llm_with_tools = llm.bind_tools(tools)


# 4. Send user query
response = llm_with_tools.invoke(
    "Who is admin"
)


# 5. Inspect LLM response
print("\n--- LLM RESPONSE ---")
print(response.content)

print("\n--- TOOL CALLS ---")
print(response.tool_calls)
