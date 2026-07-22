from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.state import AppState
from app.agents.orchestrator import orchestrator_agent
from app.agents.researcher import researcher_agent
from app.agents.analyst import analyst_agent
from app.agents.writer import writer_agent
from app.agents.fact_checker import fact_checker_agent

MAX_RESEARCH_CYCLES = 2


def should_continue(state: AppState) -> str:
    if state.error:
        return "error"
    if state.approval_status == "approved":
        return "finalize"
    if state.approval_status == "revision_requested":
        return "revise"
    return "continue"


def error_handler(state: AppState) -> AppState:
    state.final_report = f"An error occurred during research: {state.error}"
    return state


def finalize_report(state: AppState) -> AppState:
    if not state.final_report:
        state.final_report = state.draft_report
    return state


def build_graph() -> StateGraph:
    workflow = StateGraph(AppState)

    workflow.add_node("orchestrator", orchestrator_agent)
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("analyst", analyst_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("fact_checker", fact_checker_agent)
    workflow.add_node("error_handler", error_handler)
    workflow.add_node("finalize", finalize_report)

    workflow.set_entry_point("orchestrator")

    workflow.add_conditional_edges(
        "orchestrator",
        should_continue,
        {"continue": "researcher", "error": "error_handler"},
    )
    workflow.add_conditional_edges(
        "researcher",
        should_continue,
        {"continue": "analyst", "error": "error_handler"},
    )
    workflow.add_conditional_edges(
        "analyst",
        should_continue,
        {"continue": "writer", "error": "error_handler"},
    )
    workflow.add_conditional_edges(
        "writer",
        should_continue,
        {"continue": "fact_checker", "error": "error_handler", "revise": "researcher"},
    )
    workflow.add_conditional_edges(
        "fact_checker",
        should_continue,
        {"continue": "finalize", "error": "error_handler", "revise": "researcher"},
    )

    workflow.add_edge("error_handler", END)
    workflow.add_edge("finalize", END)

    return workflow


def compile_graph():
    graph = build_graph()
    return graph.compile(checkpointer=MemorySaver())
