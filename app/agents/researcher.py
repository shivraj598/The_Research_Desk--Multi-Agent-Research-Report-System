from app.tools.tavily_search import search_subtopic
from app.tools.scraper import scrape_urls


def researcher_agent(state: dict) -> dict:
    state["research_cycle_count"] = state.get("research_cycle_count", 0) + 1
    raw_sources = state.get("raw_sources", {})

    for subtask in state.get("subtasks", []):
        if subtask in raw_sources:
            continue

        results = search_subtopic(subtask, max_results=5)
        urls = [r.get("url") for r in results if r.get("url")]

        scraped = scrape_urls(urls)

        sources = []
        for r, s in zip(results, scraped):
            sources.append({
                "url": r.get("url"),
                "title": r.get("title"),
                "content": s.get("content") or r.get("content", ""),
            })

        raw_sources[subtask] = sources

    state["raw_sources"] = raw_sources
    return state
