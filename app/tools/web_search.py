import os
import re
import time
from typing import Optional

import httpx
from bs4 import BeautifulSoup

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)

_client: Optional[httpx.Client] = None


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(
            follow_redirects=True,
            timeout=15.0,
            headers={"User-Agent": USER_AGENT},
        )
    return _client


def _extract_text(html: str, max_chars: int = 3000) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text[:max_chars]


def _search_tavily(query: str, max_results: int = 5) -> Optional[list[dict]]:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=max_results)
        results = response.get("results", [])
        return [
            {
                "url": r.get("url", ""),
                "title": r.get("title", ""),
                "content": r.get("content", ""),
            }
            for r in results
        ]
    except Exception:
        return None


def _search_duckduckgo(query: str, max_results: int = 5) -> Optional[list[dict]]:
    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "url": r.get("href", ""),
                    "title": r.get("title", ""),
                    "content": r.get("body", ""),
                })
        return results if results else None
    except Exception:
        return None


def scrape_page(url: str, max_chars: int = 3000) -> Optional[str]:
    try:
        client = _get_client()
        resp = client.get(url)
        resp.raise_for_status()
        return _extract_text(resp.text, max_chars)
    except Exception:
        return None


def search_web(
    query: str,
    max_results: int = 5,
    scrape_content: bool = True,
    max_content_chars: int = 3000,
) -> list[dict]:
    results = _search_tavily(query, max_results=max_results)

    if results is None:
        results = _search_duckduckgo(query, max_results=max_results)

    if results is None:
        return []

    if scrape_content:
        for r in results:
            url = r.get("url", "")
            if not url:
                continue
            if r.get("content"):
                continue
            content = scrape_page(url, max_chars=max_content_chars)
            if content:
                r["content"] = content
            time.sleep(0.3)

    return results
