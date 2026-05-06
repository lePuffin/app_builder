from sandbox.runner import run_code

code = """
for i in range(5):
    print("line", i)
"""

def test_multiple_line():
    output = run_code(code)
    assert "line 0" in output
    assert "line 1" in output
    assert "line 2" in output
    assert "line 3" in output
    assert "line 4" in output