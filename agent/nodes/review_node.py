import difflib


def review_node(state):
    print("[r2ai] Awaiting human review...")

    original = state.get("code", "").splitlines()
    refactored = state.get("refactored_code", "").splitlines()

    print("\n--- Diff Preview ---")
    diff = difflib.unified_diff(
        original,
        refactored,
        fromfile="original.py",
        tofile="refactored.py",
        lineterm="",
    )
    for line in diff:
        print(line)

    print("\n--- Accept refactor? ---")
    decision = input("[Y]es / [N]o / [E]dit: ").strip().lower()

    if decision == "n":
        print("[r2ai] Human rejected refactor.")
        return {**state, "__end__": True, "accepted": False}

    if decision == "e":
        print("[r2ai] Enter instruction for next refactor (end with a blank line):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        instruction = "\n".join(lines)

        print(f"[r2ai] Re-running refactor with feedback: {instruction}")
        return {**state, "human_feedback": instruction, "__next__": "refactor"}

    print("[r2ai] Refactor accepted.")
    return {**state, "accepted": True}
