from sandbox.runner import run_code

code = """
print("Hello from sandbox")
"""

def execute(code: str):
    print("Executing code in sandbox...")
    return run_code(code)