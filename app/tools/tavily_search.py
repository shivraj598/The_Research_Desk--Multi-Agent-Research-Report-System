import os
from typing import Optional

from tavily import TavilyClient

_client: Optional[TavilyClient] = None


def get_tavily_client() -> TavilyClient:
    global _client
    if _client is None:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not set in environment")
        _client = TavilyClient(api_key=api_key)
    return _client


MAX_SEARCHES_PER_TASK = 3


def search_subtopic(
    query: str,
    max_results: int = 5,
    search_depth: str = "advanced",
) -> list[dict]:
    client = get_tavily_client()
    response = client.search(
        query=query,
        max_results=max_results,
        search_depth=search_depth,
    )
    return response.get("results", [])
