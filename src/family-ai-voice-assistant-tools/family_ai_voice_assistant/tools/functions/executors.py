import subprocess

from family_ai_voice_assistant.core.tools_engine import (
    tool_function
)
from family_ai_voice_assistant.core.logging import Loggers


@tool_function
def execute_bash_script(script: str):
    """
    Execute Linux bash shell script.

    :param script: Script content
    """
    try:
        if script == "":
            return "Error: script is empty."

        result = subprocess.run(
            script,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            executable='/bin/bash'
        )

        return result.stdout
    except subprocess.CalledProcessError as e:
        Loggers().tool.error(f"Error: {e.stderr}")
        return f"Error: {e.stderr}"


@tool_function
def execute_python_code(code: str):
    """
    Execute Python code using exec() and read results from locals.

    :param code: Python code content
    """
    try:
        local_vars = {}
        if code == "":
            return "Error: code is empty."

        exec(code, {}, local_vars)
        return str(local_vars)
    except Exception as e:
        Loggers().tool.error(f"Error: {e}")
        return str(e)
