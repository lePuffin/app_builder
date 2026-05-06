from sandbox.runner import run_code

def test_basic():
    output = run_code("print('hello sandbox')")
    assert "hello" in output