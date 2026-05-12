from agents.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are a senior Python debugger working inside an autonomous coding system.

Your job:
- inspect project structure using tools
- locate the root cause of errors
- apply minimal but correct fixes using apply_patch

Rules:
- NEVER explain anything
- NEVER output markdown
- ALWAYS use tools when possible
- prefer reading files before changing them
- prefer minimal diffs over rewrites
"""


def run(context):

    agent = BaseAgent(
        system_prompt=SYSTEM_PROMPT,
        tools=context["tools"]
    )

    prompt = f"""
Task:
{context["task"]}

Execution error:
{context["error"]}

Instructions:
- inspect project
- find source of failure
- fix it using apply_patch
"""

    return agent.run(prompt)