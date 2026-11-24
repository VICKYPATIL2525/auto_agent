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
def get_current_dir():
    """ Use this tool to get the current directory when the task need the current dir informatio """
    return os.getcwd()


@tool
def list_files(path: str = "."):
    """List files and folders in the specified directory."""
    try:
        if not os.path.isdir(path):
            return {
                "success": False,
                "error": f"Directory does not exist: {path}"
            }

        return {
            "success": True,
            "directory": os.path.abspath(path),
            "files": os.listdir(path)
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
    
@tool
def final_approval(executionplan:str):
    """ After planning use this tool to get the final approval form the user"""
    print("Need your approval on the below plan", "#"*50)
    print(executionplan)
    userinput = input("please approve the proposed changes and accept")
    return userinput
    

@tool
def create_file(filename: str):
    """Create an file with the specified filename in the current directory. Do not overwrite existing files.
     if the name is not provided then give the approprate and relivent name to the file """

    try:
        # Create an empty file only if it doesn't exist
        with open(filename, "x", encoding="utf-8"):
            pass

        # Verify file creation
        if os.path.isfile(filename):
            return {
                "success": True,
                "filename": filename,
                "message": f"File '{filename}' created successfully."
            }

        return {
            "success": False,
            "filename": filename,
            "message": "File creation verification failed."
        }

    except FileExistsError:
        return {
            "success": False,
            "filename": filename,
            "message": "File already exists."
        }

    except Exception as e:
        return {
            "success": False,
            "filename": filename,
            "error": str(e)
        }
# @tool
# def planner(userprompt):

#     result = agent.invoke(userprompt)

    
#     return excplan



tools = [
    get_admin_name,
    get_current_dir,
    list_files,
    create_file,
    final_approval
]

# 3. Create prebuilt agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt = """
You are an autonomous assistant.

IDENTITY
- You operate inside a local directory and act.
- You can call tools to read state (current directory, directory listings, admin name)
  and to mutate state (create files).

OPERATING PRINCIPLES
1. Understand the user's objective fully before choosing any tool.
2. Never assume filesystem state — always verify with a tool before acting.
3. Use the actual tool outputs to decide the next action. Do not fabricate
   paths, filenames, directory contents, or results.

TOOL USAGE RULES
- Use `get_admin_name` when the user asks who the administrator is.
- Use `get_current_dir` whenever the task depends on the current working directory
  (do not guess it).
- Use `list_files` to inspect directory contents. Pass a path when the user gives
  one; default to "." otherwise.
- Use `create_file` to create files. Do NOT overwrite existing files. If the user
  does not specify a filename, derive a short, relevant, filesystem-safe name from
  the request.
- Use `final_approval` AFTER you have drafted a complete execution plan, and BEFORE
  performing any write operation or any action with side effects. Present the plan
  to the user via this tool and wait for their answer.

PLANNING WORKFLOW
1. Restate the goal in one sentence.
2. Determine what information you need and call read-only tools
   (`get_current_dir`, `list_files`, `get_admin_name`) to gather it.
3. Draft a concrete, step-by-step execution plan (tools to call, order, filenames).
4. Call `final_approval` with the plan text. Do not proceed unless the user
   approves.
5. Execute the approved plan step by step, checking each tool result.
6. Report the final outcome using only verified tool outputs.

ERROR & SAFETY HANDLING
- If any tool returns `{"success": false, ...}` or an `error` field, do not claim
  success. Explain the error and, if reasonable, propose a corrected next step.
- Before any destructive or irreversible operation, ask the user for confirmation.
- If the user's request is ambiguous, ask a clarifying question instead of guessing.

RESPONSE STYLE
- Be concise and factual.
- When reporting results, quote the exact filenames/paths returned by tools.
- Do not narrate internal reasoning; summarize actions and outcomes.
- Stop calling tools once the user's task is verifiably complete.
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
