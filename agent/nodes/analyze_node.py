import subprocess
import tempfile
import os


def analyze_node(state):
    print("[r2ai] Analyzing code with ruff...")

    # Run ruff as a subprocess on the input code
    code = state["code"]

    # Write code to temp file for linting
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
        lint_output = result.stdout.strip()
        if lint_output:
            print("[r2ai] Ruff found issues:")
            print(lint_output)
            return {**state, "needs_refactor": True, "ruff_output": lint_output}
        else:
            print("[r2ai] Code is clean — no refactor needed.")
            return {**state, "needs_refactor": False}
    finally:
        os.unlink(tmp_path)
