import asyncio

from app.state import AppState
from app.tools.tavily_search import search_subtopic, MAX_SEARCHES_PER_TASK
from app.tools.scraper import scrape_urls


def researcher_agent(state: AppState) -> AppState:
    state.research_cycle_count += 1

    for subtask in state.subtasks:
        if subtask in state.raw_sources:
            continue

        results = search_subtopic(subtask, max_results=5)
        urls = [r.get("url") for r in results if r.get("url")]

        scraped = asyncio.run(scrape_urls(urls))

        sources = []
        for r, s in zip(results, scraped):
            sources.append({
                "url": r.get("url"),
                "title": r.get("title"),
                "content": s.get("content") or r.get("content", ""),
            })

        state.raw_sources[subtask] = sources

    return state
