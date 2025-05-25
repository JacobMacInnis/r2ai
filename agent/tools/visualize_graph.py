# tools/visualize_graph.py
from agent.graph import build_graph
import pathlib

graph = build_graph("ollama")
mermaid_str = graph.get_graph().draw_mermaid()
with open("graph.mmd", "w") as f:
    f.write(mermaid_str)
print("[r2ai] Mermaid diagram saved to graph.mmd")


# print(f"[r2ai] Graph SVG saved to {output_path}")
