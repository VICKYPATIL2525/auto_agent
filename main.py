
import os
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

# 1. LLM
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0
)


# 2. Tool
@tool
def admin_name() -> str:
    """Return the system administrator's name."""
    print(">>> ADMIN TOOL EXECUTED")
    return "Vicky Vijay Patil"


# 3. Test direct tool calling
llm_with_tools = llm.bind_tools([admin_name])

debug = llm_with_tools.invoke(
    "You must use the admin_name tool to answer: Who is the admin?"
)

print("\n--- DIRECT TOOL TEST ---")
print("Tool calls:", debug.tool_calls)
print("Content:", debug.content)


# 4. Create agent
agent = create_agent(
    model=llm,
    tools=[admin_name],
    system_prompt="""
    You are a helpful assistant.

    IMPORTANT:
    Whenever the user asks who the administrator is,
    you MUST call the admin_name tool.

    Never invent or guess the administrator's name.
    Always use the tool result.
    """
)


# 5. Invoke
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "Who is the admin?"}
    ]
})


# 6. Execution trace
print("\n--- AGENT EXECUTION TRACE ---")

for message in result["messages"]:

    print(f"\n[{message.type}]")
    print("Content:", message.content)

    tool_calls = getattr(message, "tool_calls", [])

    if tool_calls:
        print("Tool calls:", tool_calls)

    if message.type == "tool":
        print("Tool result:", message.content)


# 7. Final answer
print("\n--- FINAL ANSWER ---")
print(result["messages"][-1].content)
