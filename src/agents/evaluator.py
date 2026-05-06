from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from schemas.evaluator import Evaluation

load_dotenv(override=True)

client = OpenAI(
    base_url=os.getenv("GITHUB_URL"),
    api_key=os.getenv("GITHUB_TOKEN")
)

SYSTEM = """
You are an evaluation agent.

Your job:
- Decide if code execution was successful or not
- Only respond in JSON

Return format:
{
  "status": "success" or "retry",
  "error": "error message or null"
}

Rules:
- If exit_code == 0 and no obvious error → success
- Otherwise → retry
"""


def run(context: dict):
    result = context.get("result") or {}

    prompt = f"""
                stdout:
                {result.get('stdout', '')}

                stderr:
                {result.get('stderr', '')}

                exit_code:
                {result.get('exit_code', 1)}
                """

    response = client.chat.completions.create(
        model=os.getenv("GITHUB_MODEL"),
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)

        # 🔥 schema validation
        validated = Evaluation(**data)

        return validated.model_dump()

    except Exception as e:
        # fallback seguro (nunca crasha o system)
        return {
            "status": "retry",
            "error": str(e)
        }
