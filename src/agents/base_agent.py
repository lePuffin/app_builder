from openai import OpenAI
import os
import json
from dotenv import load_dotenv



load_dotenv(override=True)

client = OpenAI(
    base_url=os.getenv("GITHUB_URL"),
    api_key=os.getenv("GITHUB_TOKEN")
)


class BaseAgent:

    def __init__(
        self,
        system_prompt,
        tools=None,
        model=None,
        max_iterations=15
    ):

        self.system_prompt = system_prompt
        self.tools = tools or {}

        self.model = (
            model or os.getenv("GITHUB_MODEL")
        )

        self.max_iterations = max_iterations

    # ==========================================
    # TOOL SCHEMAS
    # ==========================================

    def build_tool_schemas(self):

        return [
            tool.schema
            for tool in self.tools.values()
        ]

    # ==========================================
    # EXECUTE TOOL (WITH VALIDATION)
    # ==========================================

    def execute_tool_call(
        self,
        tool_name,
        arguments
    ):

        tool = self.tools[tool_name]

        fn = tool.function
        model = tool.model

        # 🔥 Pydantic validation
        validated = model(**arguments)

        result = fn(**validated.model_dump())

        return result

    # ==========================================
    # MAIN LOOP
    # ==========================================

    def run(self, user_prompt):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        iterations = 0

        while iterations < self.max_iterations:

            iterations += 1

            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.build_tool_schemas(),
                tool_choice="auto",
                temperature=0.1,
            )

            message = response.choices[0].message

            # ======================================
            # TOOL CALLS
            # ======================================

            if message.tool_calls:

                messages.append(message)

                for tool_call in message.tool_calls:

                    tool_name = tool_call.function.name

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    print(f"🔧 tool: {tool_name}")

                    try:

                        result = self.execute_tool_call(
                            tool_name,
                            arguments
                        )

                    except Exception as e:

                        result = {
                            "error": str(e)
                        }

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })

                continue

            # ======================================
            # FINAL ANSWER
            # ======================================

            return message.content

        return {
            "error": "max iterations reached"
        }   