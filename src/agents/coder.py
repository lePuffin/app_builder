# src/agents/coder.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(
    base_url=os.getenv("GITHUB_URL"),
    api_key=os.getenv("GITHUB_TOKEN")
)

SYSTEM_PROMPT = """
You are a Python developer.

Return ONLY valid Python code.
No explanations.
No markdown.
"""

def run(context: dict):
    prompt = f"""
Task:
{context['task']}

Previous error (if any):
{context.get('error', '')}

Plan:
{context.get('plan', '')}
"""
    response = client.chat.completions.create(
        model=os.getenv("GITHUB_MODEL"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
