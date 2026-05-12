from openai import OpenAI
import os
import json
from dotenv import load_dotenv

from schemas.planner import Plan

load_dotenv(override=True)

client = OpenAI(
    base_url=os.getenv("GITHUB_URL"),
    api_key=os.getenv("GITHUB_TOKEN")
)

SYSTEM = """
You are a software planning agent.

Your job:
- Break tasks into small executable steps
- Output ONLY JSON:
  {
    "steps": ["step 1", "step 2", ...]
  }
- No explanations
"""


def run(task: str):

    response = client.chat.completions.create(
        model=os.getenv("GITHUB_MODEL"),
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": task},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content.strip()

    data = json.loads(content)

    validated = Plan(**data)

    return validated.steps