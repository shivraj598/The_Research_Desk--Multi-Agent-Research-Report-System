from typing import TypedDict, Optional


class AppState(TypedDict):
    topic: str
    subtasks: list[str]
    raw_sources: dict[str, list[dict]]
    insights: dict[str, list[dict]]
    draft_report: str
    fact_check_results: list[dict]
    final_report: str
    approval_status: str
    revision_notes: str
    research_cycle_count: int
    simple_query: bool
    error: Optional[str]


def initial_state(topic: str, mode: str = "quick") -> AppState:
    return {
        "topic": topic,
        "subtasks": [],
        "raw_sources": {},
        "insights": {},
        "draft_report": "",
        "fact_check_results": [],
        "final_report": "",
        "approval_status": "pending",
        "revision_notes": "",
        "research_cycle_count": 0,
        "simple_query": mode == "quick",
        "error": None,
    }
