from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(
    base_url=os.getenv("GITHUB_URL"),
    api_key=os.getenv("GITHUB_TOKEN")
)

SYSTEM = """
You are a software planning agent.

Your job:
- Break tasks into small executable steps
- Output ONLY a valid JSON in this format:
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

    try:
        data = json.loads(content)

        from schemas.planner import Plan

        validated = Plan(**data)

        return validated.steps
    
    except Exception as e:
        # fallback safety
        print("Planner validation failed:", e)
        return [task]