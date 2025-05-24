def make_refactor_node(llm):
    # This function creates a refactor node that uses the provided LLM to refactor code.
    def refactor_node(state):
        print("[r2ai] Refactoring code...")

        human_feedback = state.get("human_feedback")
        feedback_clause = (
            f"Apply this human feedback: {human_feedback}\n" if human_feedback else ""
        )

        prompt = (
            "Refactor the following Python code to improve style, clarity, and readability. "
            "Keep the exact same functionality. Respond ONLY with raw valid Python code — no explanation, no markdown, no indentation padding, no formatting comments.\n\n"
            f"{feedback_clause}"
            f"{state['code']}\n\n"
        )

        response = llm.invoke(prompt)

        # ✅ Remove markdown-style triple backticks
        lines = response.strip().splitlines()

        # Remove ``` or ```python from start
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        # Remove closing ```
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

        print("[r2ai] Model responded with:")
        print(cleaned)

        return {**state, "refactored_code": cleaned, "human_feedback": None}

    return refactor_node
