import subprocess
import tempfile
import os
import ast


def post_refactor_analyze_node(state):
    print("[r2ai] Re-analyzing refactored code with Ruff...")

    code = state.get("refactored_code", "")
    if not code:
        print("[r2ai] No refactored code found.")
        return {**state, "post_ruff_output": "No code"}

    # ✅ Syntax safeguard BEFORE Ruff runs
    try:
        ast.parse(code)
    except SyntaxError as e:
        print("[r2ai] ❌ Syntax error in refactored code before Ruff:")
        print(e)
        return {**state, "post_ruff_output": f"SyntaxError: {e}"}

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["ruff", "check", tmp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output = result.stdout.strip()

        if output:
            print("[r2ai] Ruff still found issues after refactor:")
            print(output)
        else:
            print("[r2ai] ✅ Refactored code is clean!")

        return {**state, "post_ruff_output": output}

    finally:
        os.unlink(tmp_path)
