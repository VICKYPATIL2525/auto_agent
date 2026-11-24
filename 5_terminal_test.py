import subprocess
from langchain.tools import tool

command = "dir"  # Windows command

result = subprocess.run(
    command,
    shell=True,
    capture_output=True,
    text=True
)

print("OUTPUT:")
print(result.stdout)

print("ERROR:")
print(result.stderr)

print("RETURN CODE:", result.returncode)


import subprocess
@tool
def execute_command(command: str):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }

    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "return_code": -1
        }


# Usage
response = execute_command("python --version")
print(response)

response = execute_command("dir")
print(response)

