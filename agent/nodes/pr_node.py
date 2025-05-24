def pr_node(state):
    print("[r2ai] Simulating pull request...")

    refactored = state.get("refactored_code", "")
    original = state.get("code", "")
    filename = state.get("filename", "output.py")

    out_path = f"{filename.rsplit('.', 1)[0]}_refactored.py"

    with open(out_path, "w") as f:
        f.write(refactored)

    print(f"[r2ai] ✅ Refactored code written to: {out_path}")

    # Optional: show a pretend PR description
    print("\n--- Simulated PR Message ---")
    print(f"Refactored `{filename}` for improved readability and style.")
    if state.get("ruff_output"):
        print("Lint issues addressed:\n")
        print(state["ruff_output"])
    else:
        print("No specific issues found by Ruff.")
    print("-----------------------------")

    return {**state, "refactor_file": out_path}
