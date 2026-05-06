from sandbox.runner import run_code

code = """
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

print(fib(10))
"""

def test_real_code():
    output = run_code(code)
    assert "55" in output