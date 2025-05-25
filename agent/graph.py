# agent/graph.py
from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from agent.llm import get_llm
from typing import TypedDict, Optional

# Importing nodes
from agent.nodes.ingest_node import ingest_node
from agent.nodes.analyze_node import analyze_node
from agent.nodes.refactor_node import make_refactor_node
from agent.nodes.review_node import review_node
from agent.nodes.post_refactor_analyze_node import post_refactor_analyze_node
from agent.nodes.pr_node import pr_node


# 👇 Explicit state
class AgentState(TypedDict, total=False):
    code: str
    filename: str
    model: str
    needs_refactor: bool
    ruff_output: str
    refactored_code: str
    post_ruff_output: str
    accepted: bool
    human_feedback: Optional[str]
    refactor_file: str
    __end__: bool


def build_graph(
    model_choice: str,
) -> Runnable:
    graph = StateGraph(AgentState)

    llm = get_llm(model_choice)
    refactor_node = make_refactor_node(llm)

    def analyze_decision(state):
        return "refactor" if state.get("needs_refactor") else "pull_request"

    def review_decision(state):
        if state.get("accepted"):
            return "pull_request"
        elif state.get("human_feedback"):
            return "refactor"
        else:
            return "__end__"

    # Adding nodes to the graph
    graph.add_node("ingest", ingest_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("refactor", refactor_node)
    graph.add_node("post_refactor_analyze", post_refactor_analyze_node)
    graph.add_node("human_review", review_node)
    graph.add_node("pull_request", pr_node)

    # Setting up the graph structure
    graph.set_entry_point("ingest")
    graph.add_edge("ingest", "analyze")
    graph.add_edge("analyze", "refactor")
    graph.add_conditional_edges(
        "analyze",
        analyze_decision,
        {"refactor": "refactor", "pull_request": "pull_request"},
    )
    # graph.add_edge("refactor", "human_review")
    graph.add_edge("refactor", "post_refactor_analyze")
    graph.add_edge("post_refactor_analyze", "human_review")

    graph.add_conditional_edges(
        "human_review",
        review_decision,
        {
            "refactor": "refactor",
            "pull_request": "pull_request",
            "__end__": END,
        },
    )

    # graph.add_edge("human_review", "pull_request")
    graph.add_edge("pull_request", END)

    return graph.compile(checkpointer=None)
