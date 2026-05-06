from sandbox.runner import run_code

code = """
while True:
    pass
"""

def test_isolation():
    output = run_code(code)
    assert "cwd:" in output