from src.workspace.docker_runner import run_code

def test_basic():
    output = run_code("print('hello sandbox')")
    assert "hello" in output