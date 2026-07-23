from datetime import date

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.state import AppState
from app.agents.orchestrator import orchestrator_agent
from app.agents.researcher import researcher_agent
from app.agents.analyst import analyst_agent
from app.agents.writer import writer_agent
from app.agents.fact_checker import fact_checker_agent
from app.llm import get_llm_response
from app.tools.web_search import search_web

TODAY = date.today().isoformat()


def error_handler(state: dict) -> dict:
    state["final_report"] = f"An error occurred during research: {state.get('error', 'unknown error')}"
    return state


def finalize_report(state: dict) -> dict:
    if not state.get("final_report"):
        state["final_report"] = state.get("draft_report", "")
    return state


def direct_writer(state: dict) -> dict:
    topic = state.get("topic", "")
    results = search_web(topic, max_results=5, scrape_content=True)

    if not results:
        state["draft_report"] = f'I couldn\'t find any current search results for "{topic}". Try rephrasing or using Deep Research mode.'
        return state

    sources_text = ""
    for r in results:
        url = r.get("url", "unknown")
        content = r.get("content", "")
        if content:
            sources_text += f"\nSource ({url}):\n{content[:2000]}\n"

    response = get_llm_response(
        f"Today is {TODAY}. You are a research assistant. Summarize the search results below to answer the user's question.\n"
        "CRITICAL: Do NOT use any of your own knowledge or training data. Only use information from the search results.\n"
        "If the search results do not contain relevant information, say so.\n"
        "Cite source URLs inline where possible.",
        f"Question: {topic}\n\nSearch Results:{sources_text[:10000]}\n\n"
        "Write a concise paragraph answering the question using ONLY the search results above.",
        max_tokens=1024,
    )
    if response and not response.startswith("Error"):
        state["draft_report"] = response
    else:
        state["draft_report"] = "I couldn't generate a response from the search results. Please try Deep Research mode."
    return state


def should_continue(state: dict) -> str:
    if state.get("error"):
        return "error"
    if state.get("simple_query"):
        return "direct"
    return "continue"


def should_continue_writer(state: dict) -> str:
    if state.get("error"):
        return "error"
    if state.get("approval_status") == "approved":
        return "finalize"
    if state.get("approval_status") == "revision_requested":
        return "revise"
    if state.get("simple_query"):
        return "finalize"
    return "continue"


def build_graph() -> StateGraph:
    workflow = StateGraph(AppState)

    workflow.add_node("orchestrator", orchestrator_agent)
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("analyst", analyst_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("fact_checker", fact_checker_agent)
    workflow.add_node("direct_writer", direct_writer)
    workflow.add_node("error_handler", error_handler)
    workflow.add_node("finalize", finalize_report)

    workflow.set_entry_point("orchestrator")

    workflow.add_conditional_edges(
        "orchestrator",
        should_continue,
        {"continue": "researcher", "direct": "direct_writer", "error": "error_handler"},
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
        should_continue_writer,
        {"continue": "fact_checker", "finalize": "finalize", "error": "error_handler", "revise": "researcher"},
    )
    workflow.add_conditional_edges(
        "fact_checker",
        should_continue,
        {"continue": "finalize", "error": "error_handler"},
    )
    workflow.add_edge("direct_writer", "finalize")
    workflow.add_edge("error_handler", END)
    workflow.add_edge("finalize", END)

    return workflow


def compile_graph():
    graph = build_graph()
    return graph.compile(checkpointer=MemorySaver())
