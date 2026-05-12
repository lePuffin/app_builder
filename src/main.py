from orchestrator.core import Orchestrator

task = """
Create a small Python todo app with a simple UI. The app should allow users to add, view, and delete tasks. Use the following files for the project:
- main.py
- storage.py
- create requirements.md and include dependencies
"""

orchestrator = Orchestrator()

result = orchestrator.run(task)

print(result)