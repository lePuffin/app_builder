def run(context: dict):

    result = context["result"]

    stdout = result.get("stdout", "")
    stderr = result.get("stderr", "")
    exit_code = result.get("exit_code", 1)

    print("\n📤 STDOUT:")
    print(stdout)

    print("\n⚠️ STDERR:")
    print(stderr)

    print("\n🚪 EXIT CODE:", exit_code)

    # ==========================================
    # SUCCESS CONDITIONS
    # ==========================================

    if exit_code == 0 and not stderr.strip():

        return {
            "status": "success",
            "error": None
        }

    # ==========================================
    # FAILURE
    # ==========================================

    error = stderr.strip() or stdout.strip() or "Unknown execution error"

    return {
        "status": "retry",
        "error": error
    }