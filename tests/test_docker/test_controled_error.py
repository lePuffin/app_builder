from src.workspace.docker_runner import run_code

code = """
raise Exception("test error")
"""

def test_controlled_error():
    output = run_code(code)
    assert "test error" in output