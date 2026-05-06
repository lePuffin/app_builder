# src/orchestrator/core.py

from agents.planner import run as planner
from agents.coder import run as coder
from agents.evaluator import run as evaluator
from sandbox.runner import run_code


class Orchestrator:

    def run(self, task: str):

        print("\n🧭 PLANNING PHASE")

        steps = planner(task)

        print("Plan:", steps)

        results = []

        for i, step in enumerate(steps):

            print(f"\n🔁 STEP {i+1}: {step}")

            context = {
                "task": step,
                "error": None
            }

            success = False

            for attempt in range(3):

                print("  🧑‍💻 coding...")

                code = coder(context)

                print("  🐳 running...")

                result = run_code(code)

                context["result"] = result

                decision = evaluator(context)

                print("  🔍", decision["status"])

                if decision["status"] == "success":
                    success = True
                    results.append(code)
                    break

                context["error"] = decision["error"]

            if not success:
                print("❌ step failed:", step)
                return None

        print("\n🎉 ALL STEPS COMPLETED")
        return results