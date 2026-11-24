import os
import json
import platform
import subprocess

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

# 1. Initialize LLM
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL_TOOL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0,
)

# 2. Define the terminal execution tool
@tool
def execute_command(command: str) -> str:
    """Execute a shell command in the terminal and return its result."""
    print(f"[AGENT] $ {command}", flush=True)

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return json.dumps({
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode,
        })
    except subprocess.TimeoutExpired:
        return json.dumps({
            "success": False, "output": "",
            "error": "Command timed out after 60 seconds", "return_code": -1,
        })
    except Exception as e:
        return json.dumps({
            "success": False, "output": "", "error": str(e), "return_code": -1,
        })

# 3. Register the tool
tools = [execute_command]

# 4. Create the agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        f"You are an autonomous terminal command execution agent.\n"
        f"Operating system: {platform.system()}\n"
        f"Shell: {'cmd.exe (Windows)' if platform.system() == 'Windows' else '/bin/sh'}\n\n"
        "RULES:\n"
        "1. ALWAYS call the `execute_command` tool to actually run a command. "
        "NEVER print a command as text and stop — if you write shell code, "
        "you MUST pass it to the tool in the same turn.\n"
        "2. If a command fails, read the `error` field and call "
        "`execute_command` AGAIN with a corrected command. Keep retrying "
        "(up to a few times) until it works or you are truly stuck.\n"
        "3. `cd` does NOT persist between calls. Chain steps with `&&` "
        "or use full paths (e.g. `cd test && mkdir x`).\n"
        "4. On Windows use native commands, NOT bash: "
        "`dir` (not ls), `mkdir` (not touch), "
        "create empty file with `type nul > file.txt`, "
        "loop with `for /L %i in (1,1,10) do type nul > test\\req%i.txt`.\n"
        "5. Never run destructive commands (rm -rf, mkfs, dd, shutdown) "
        "without explicit user confirmation."
    ),
)

# 5. Chat loop
print("Terminal Agent ready. Type 'exit' or 'quit' to leave.\n")
while True:
    userinput = input("User: ").strip()
    if userinput.lower() in {"exit", "quit"}:
        break
    if not userinput:
        continue

    result = agent.invoke({
        "messages": [{"role": "user", "content": userinput}]
    })

    final_message = result["messages"][-1]
    print(f"Agent: {final_message.content}\n")