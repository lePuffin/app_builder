# src/main.py

from orchestrator.core import Orchestrator

if __name__ == "__main__":

    task = """
    Write a Python script to compute Fibonacci, loop from 1 to 10 and print Fibonacci of each number"
    """

    orchestrator = Orchestrator()
    result = orchestrator.run(task)

    print("\nFINAL RESULT:\n", result)