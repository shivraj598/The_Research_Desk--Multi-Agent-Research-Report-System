from typing import Optional

import httpx
from bs4 import BeautifulSoup

MAX_SCRAPE_PER_TASK = 5


def fetch_page_content(url: str, timeout: float = 15.0) -> Optional[str]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            resp = client.get(url, headers=headers)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            lines = [line for line in text.splitlines() if len(line) > 40]
            return "\n".join(lines[:200])
    except Exception:
        return None


def scrape_urls(urls: list[str]) -> list[dict]:
    results = []
    for url in urls[:MAX_SCRAPE_PER_TASK]:
        content = fetch_page_content(url)
        if content:
            results.append({"url": url, "content": content})
        else:
            results.append({"url": url, "content": None, "error": "failed to fetch"})
    return results
