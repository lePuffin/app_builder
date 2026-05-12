from agents.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are a senior Python refactoring agent.

Your job:
- improve code quality
- improve structure
- improve readability
- preserve behavior

Rules:
- ALWAYS use tools
- NEVER explain
- NEVER output markdown
- prefer minimal safe refactors
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
- inspect project
- improve code quality
- preserve behavior
"""

    return agent.run(prompt)