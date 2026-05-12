from agents.planner import run as planner
from agents.evaluator import run as evaluator
from agents.coding.dependency_resolver import run as dependency_resolver

from agents.coding.debugger import run as debugger
from agents.coding.test_writer import run as test_writer
from agents.coding.refactorer import run as refactorer
from agents.coding.project_generator import run as project_generator

from config.runtime_profiles import (
    RUNTIME_PROFILES
)

from sandbox.runner import run_project
from workspace.manager import WorkspaceManager
from tools.registry import ToolRegistry



class Orchestrator:

    def __init__(self):
        self.workspace = WorkspaceManager()

    def run(self, task: str):

        # ==========================================
        # WORKSPACE
        # ==========================================

        workspace = self.workspace.create()
        workspace_path = workspace["path"]

        print("📁 workspace:", workspace_path)

        # ==========================================
        # RUNTIME CONTEXT
        # ==========================================

        runtime = {
            "environment": "docker",
            "headless": True,

            "supports_gui_code_generation": True,
            "supports_gui_execution": False,

            "allowed_frameworks": [
                "fastapi",
                "textual",
                "flet"
            ],

            "forbidden_frameworks": [
                "tkinter"
            ],
            
            "supports_stdin": False,
            "supports_interactive_input": False,
            "network_enabled": True,
            "python_version": "3.14",
            "os": "linux"
        }

        # ==========================================
        # TOOLS (single source of truth)
        # ==========================================

        tools = ToolRegistry(
            self.workspace,
            workspace_path
        ).get_tools()

        # ==========================================
        # PLANNING (reasoning only)
        # ==========================================

        print("\n🧭 planning...")
        plan =  planner({
            "task": task,
            "runtime": runtime
        })
        print(plan)

        # ==========================================
        # PROJECT GENERATION (writes workspace)
        # ==========================================

        print("\n🏗 generating project...")

        project_generator({
            "task": task,
            "plan": plan,
            "runtime": runtime,
            "tools": tools
        })

        entrypoint = "main.py"

        # ==========================================
        # EXECUTION LOOP
        # ==========================================

        success = False

        for attempt in range(5):

            print(f"\n🔁 execution attempt {attempt+1}")

            # ==========================================
            # DEPENDENCIES (reasoning only)
            # ==========================================

            deps = dependency_resolver({
                "files": self.workspace.read_project(workspace_path)
            })

            dependencies = deps["dependencies"]

            print("📦 dependencies:", dependencies)

            result = run_project(
                workspace_path,
                entrypoint,
                dependencies
            )

            decision = evaluator({
                "result": result
            })

            print(decision)

            if decision["status"] == "success":
                success = True
                print("✅ execution succeeded")
                break

            # ======================================
            # DEBUGGER (mutates workspace)
            # ======================================

            print("🐞 debugging...")

            debugger({
                "task": task,
                "error": decision["error"],
                "runtime": runtime,
                "tools": tools
            })

        # ==========================================
        # FAILURE
        # ==========================================

        if not success:
            print("❌ max retries reached")
            return None

        # ==========================================
        # TEST GENERATION (mutates workspace)
        # ==========================================

        print("\n🧪 generating tests...")

        test_writer({
            "task": task,
            "runtime": runtime,
            "tools": tools
        })

        # ==========================================
        # REFACTORING (mutates workspace)
        # ==========================================

        print("\n♻️ refactoring project...")

        refactorer({
            "task": task,
            "tools": tools
        })

        # ==========================================
        # DONE
        # ==========================================

        print("\n🎉 project complete")

        return {
            "workspace": str(workspace_path),
            "plan": plan
        }