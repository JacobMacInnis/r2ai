def ingest_node(state):
    print("[r2ai] Ingesting code...")
    # print(f"[r2ai] State keys: {list(state.keys())}")
    # print(f"[r2ai] state['code'] = {repr(state.get('code'))}")

    filename = state.get("filename", "unknown_file.py")
    code = state.get("code", "")

    if not code.strip():  # <- this is the actual check
        raise ValueError("[r2ai] No code found in input state.")

    print(f"[r2ai] Loaded {len(code.strip().splitlines())} lines from {filename}")

    return {**state, "filename": filename}
