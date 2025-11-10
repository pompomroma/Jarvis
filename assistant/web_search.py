"""Basic web search integration via DuckDuckGo."""

from __future__ import annotations

from typing import List

from duckduckgo_search import DDGS


def search_snippets(query: str, *, max_results: int = 3) -> List[str]:
    """Return concise snippets for the given query."""

    results: List[str] = []
    try:
        with DDGS(timeout=10) as search:
            for item in search.text(query, max_results=max_results):
                title = item.get("title", "").strip()
                snippet = item.get("body", "").strip()
                url = item.get("href") or item.get("link") or ""
                if not snippet:
                    continue
                formatted = f"{title}: {snippet} ({url})".strip()
                results.append(formatted)
    except Exception as exc:  # pragma: no cover - dependent on network
        results.append(f"[Search unavailable: {exc}]")
    return results
