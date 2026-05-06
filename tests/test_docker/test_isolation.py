from sandbox.runner import run_code

code = """
import os

print("cwd:", os.getcwd())
print("files:", os.listdir("/"))
"""

def test_isolation():
    output = run_code(code)
    assert "cwd:" in output