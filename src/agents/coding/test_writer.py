from agents.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are a Python test generation agent.

Your job:
- inspect the project
- generate pytest tests
- create or update tests files

Rules:
- ALWAYS use tools
- ALWAYS write tests using write_file or apply_patch
- NEVER explain
- NEVER output markdown
"""


def run(context):

    agent = BaseAgent(
        system_prompt=SYSTEM_PROMPT,
        tools=context["tools"]
    )

    prompt = f"""
Task:
{context["task"]}

Instructions:
- inspect project files
- create pytest tests
- create tests folder if needed
"""

    return agent.run(prompt)