from app.tools.web_search import search_web


def researcher_agent(state: dict) -> dict:
    state["research_cycle_count"] = state.get("research_cycle_count", 0) + 1
    raw_sources = state.get("raw_sources", {})

    for subtask in state.get("subtasks", []):
        if subtask in raw_sources:
            continue

        results = search_web(subtask, max_results=5, scrape_content=True)
        sources = []
        for r in results:
            sources.append({
                "url": r.get("url", ""),
                "title": r.get("title", ""),
                "content": r.get("content", ""),
            })

        raw_sources[subtask] = sources

    state["raw_sources"] = raw_sources
    return state
