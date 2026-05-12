from openai import OpenAI

import os
import json
import ast
import sys
import importlib.util
import sysconfig

from dotenv import load_dotenv

from schemas.coder import DependencyResolution

load_dotenv(override=True)

client = OpenAI(
    base_url=os.getenv("GITHUB_URL"),
    api_key=os.getenv("GITHUB_TOKEN")
)

SYSTEM = """
You are a Python dependency analysis agent.

Your job:
- detect external python dependencies
- ignore standard library modules
- ignore local project imports

Return ONLY valid JSON:

{
  "dependencies": ["requests", "numpy"]
}
"""

STDLIB_PATH = sysconfig.get_paths()["stdlib"]

def extract_imports(code: str):

    imports = set()

    try:

        tree = ast.parse(code)

    except Exception:
        return imports

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for name in node.names:

                imports.add(
                    name.name.split(".")[0]
                )

        elif isinstance(node, ast.ImportFrom):

            if node.module:

                imports.add(
                    node.module.split(".")[0]
                )

    return imports


# ==========================================
# MAIN
# ==========================================

def run(context: dict):

    files = context.get("files", [])

    # ==========================================
    # VALIDATE FORMAT
    # ==========================================

    if not isinstance(files, list):

        return {
            "dependencies": []
        }

    # ==========================================
    # RUNTIME MODULE CLASSIFICATION
    # ==========================================

    STDLIB_MODULES = set(sys.stdlib_module_names)


    def is_stdlib_module(module_name: str) -> bool:

        return module_name in STDLIB_MODULES


    def is_builtin_or_system(module_name: str) -> bool:

        try:

            spec = importlib.util.find_spec(module_name)

            if spec is None:
                return False

            # builtins
            if spec.origin == "built-in":
                return True

            # frozen modules
            if spec.origin == "frozen":
                return True

            # stdlib path detection
            if (
                spec.origin
                and spec.origin.startswith(STDLIB_PATH)
            ):
                return True

            return False

        except Exception:
            return False
    
    # ==========================================
    # FILTER PYTHON FILES
    # ==========================================

    python_files = []

    for file in files:

        path = file.get("path", "")

        if not path.endswith(".py"):
            continue

        if path.startswith("tests/"):
            continue

        python_files.append(file)

    # ==========================================
    # LOCAL MODULES
    # ==========================================

    local_modules = set()

    for file in python_files:

        path = file.get("path", "")

        if not path.endswith(".py"):
            continue

        module = (
            path
            .replace(".py", "")
            .replace("/", ".")
        )

        local_modules.add(module)

        # also top-level module name
        local_modules.add(
            module.split(".")[0]
        )

    # ==========================================
    # STATIC IMPORT ANALYSIS
    # ==========================================

    detected = set()

    for file in python_files:

        content = file.get("content", "")

        imports = extract_imports(content)

        detected.update(imports)

    # ==========================================
    # FILTERS
    # ==========================================

    filtered = set()

    for dep in detected:

        # local project module
        if dep in local_modules:
            continue

        # stdlib
        if is_stdlib_module(dep):
            continue

        # builtin/system/runtime module
        if is_builtin_or_system(dep):
            continue

        filtered.add(dep)

    detected = filtered

    # ==========================================
    # AI VALIDATION LAYER
    # ==========================================

    summarized_code = "\n\n".join([
        f"FILE: {f['path']}\n{f['content']}"
        for f in python_files
    ])

    response = client.chat.completions.create(
        model=os.getenv("GITHUB_MODEL"),
        messages=[
            {
                "role": "system",
                "content": SYSTEM
            },
            {
                "role": "user",
                "content": summarized_code
            },
        ],
        temperature=0,
        response_format={
            "type": "json_object"
        },
    )

    data = json.loads(
        response.choices[0].message.content
    )

    validated = DependencyResolution(**data)

    ai_dependencies = set(
        validated.dependencies
    )

    # ==========================================
    # MERGE RESULTS
    # ==========================================

    final_dependencies = sorted(
        detected.union(ai_dependencies)
    )

    return {
        "dependencies": final_dependencies
    }