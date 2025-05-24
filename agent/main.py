import argparse
import os
from agent.graph import build_graph


def gather_python_files(path: str) -> list[str]:
    if os.path.isfile(path) and path.endswith(".py"):
        return [path]
    elif os.path.isdir(path):
        return [
            os.path.join(root, file)
            for root, _, files in os.walk(path)
            for file in files
            if file.endswith(".py")
        ]
    else:
        print(f"[r2ai] Invalid path: {path}")
        return []


def run_single_file(graph, model: str, filepath: str) -> None:
    print(f"\n🔹 Processing: {filepath}")
    try:
        with open(filepath, "r") as f:
            code = f.read().strip()
    except FileNotFoundError:
        print(f"[r2ai] File not found: {filepath}")
        return

    state = {
        "code": code,
        "model": model,
        "filename": filepath,
    }

    result = graph.invoke(state)

    if result.get("__end__"):
        print(f"[r2ai] ❌ Skipped or rejected: {filepath}")
    else:
        print(f"[r2ai] ✅ Completed: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Run R2AI Code Refactor Agent")
    parser.add_argument(
        "--model",
        choices=["ollama", "gpt"],
        default="ollama",
        help="Which LLM backend to use",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path", help="Path to a folder of Python files")
    group.add_argument("--file", help="Path to a single Python file")

    args = parser.parse_args()

    print(f"[r2ai] Using model: {args.model}")
    print(f"[r2ai] Target path: {args.path}")

    if args.file:
        files = [args.file]
    elif args.path:
        files = gather_python_files(args.path)
    else:
        files = []

    if not files:
        print("[r2ai] No valid Python files found.")
        return

    graph = build_graph(model_choice=args.model)

    for file_path in files:
        run_single_file(graph, args.model, file_path)


if __name__ == "__main__":
    main()
