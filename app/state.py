from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AppState:
    topic: str = ""
    subtasks: list[str] = field(default_factory=list)
    raw_sources: dict[str, list[dict]] = field(default_factory=dict)
    insights: dict[str, list[dict]] = field(default_factory=dict)
    draft_report: str = ""
    fact_check_results: list[dict] = field(default_factory=list)
    final_report: str = ""
    approval_status: str = "pending"
    revision_notes: str = ""
    research_cycle_count: int = 0
    error: Optional[str] = None
