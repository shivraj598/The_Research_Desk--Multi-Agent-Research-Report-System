from app.llm import get_llm_response


ORCHESTRATOR_SYSTEM_PROMPT = """You are a research Orchestrator. Your job is to break down a user's research topic into 4-6 specific, well-defined subtasks that can be researched independently.

For each subtask, provide:
- A clear, searchable query (1-2 sentences)
- The specific angle or aspect to investigate

Output your response as a numbered list of subtask descriptions.

CRITICAL RULES:
- Never generate more than 6 subtasks
- Each subtask must be independently researchable
- Cover different angles of the topic
- Output ONLY the numbered list, nothing else"""


SIMPLE_QUERY_KEYWORDS = [
    "write a short", "write about", "introduction about",
    "in one sentence", "briefly", "summarize",
]

CURRENT_EVENT_KEYWORDS = [
    "current", "today", "latest", "recent", "breaking",
    "now", "as of", "update", "this week", "this month",
    "2025", "2026", "2027",
]


def _is_simple_query(topic: str) -> bool:
    lower = topic.lower()
    if any(kw in lower for kw in CURRENT_EVENT_KEYWORDS):
        return False
    if len(topic.split()) < 4:
        return True
    return any(kw in lower for kw in SIMPLE_QUERY_KEYWORDS)


def orchestrator_agent(state: dict) -> dict:
    topic = state.get("topic", "")
    if not topic:
        state["error"] = "No topic provided"
        return state

    if _is_simple_query(topic):
        state["simple_query"] = True
        state["subtasks"] = [topic]
        return state

    response = get_llm_response(ORCHESTRATOR_SYSTEM_PROMPT, f"Research topic: {topic}\n\nBreak this topic into 4-6 research subtasks.")

    if not response or response.startswith("Error"):
        state["error"] = f"Orchestrator failed: {response}"
        return state

    lines = [line.strip() for line in response.strip().splitlines() if line.strip()]
    subtasks = []
    for line in lines:
        cleaned = line.lstrip("0123456789.)- ")
        if cleaned and len(cleaned) > 10:
            subtasks.append(cleaned)

    state["subtasks"] = subtasks[:6]
    return state
