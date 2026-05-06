from src.workspace.docker_runner import run_code

code = """
import os

print(os.system("ls /"))
print("done")
"""

def test_anti_exit():
    output = run_code(code)
    assert "done" in output