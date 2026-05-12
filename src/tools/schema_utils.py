def pydantic_to_tool(
    model,
    name,
    description
):

    return {
        "type": "function",

        "function": {
            "name": name,
            "description": description,
            "parameters": model.model_json_schema()
        }
    }