import json

from agents.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are an autonomous Python project generator.

Your responsibilities:
- create complete Python projects
- create all required files
- write correct code
- use tools to inspect and modify the workspace

Rules:
- ALWAYS use write_file tool
- NEVER output markdown
- NEVER explain anything
- prefer simple architectures
- prefer deterministic execution
- avoid infinite loops
"""


def run(context):

    agent = BaseAgent(
        system_prompt=SYSTEM_PROMPT,
        tools=context["tools"]
    )

    prompt = f"""
Task:
{context["task"]}

Plan:
{context.get("plan")}

Runtime:
{json.dumps(context.get("runtime", {}), indent=2)}

Instructions:
- adapt the project to runtime capabilities
- if GUI execution is unsupported, avoid launching windows
- if stdin is unsupported, avoid interactive input()
"""

    return agent.run(prompt)