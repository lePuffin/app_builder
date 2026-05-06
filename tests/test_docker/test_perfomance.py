from sandbox.runner import run_code

code = """
print(sum(range(100000)))
"""

def test_performance():
    output = run_code(code)
    assert "999950000" in output