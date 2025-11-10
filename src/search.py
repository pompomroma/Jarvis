"""Simple web search helper built on DuckDuckGo."""

from __future__ import annotations

from duckduckgo_search import DDGS


def run_web_search(query: str, max_results: int = 3) -> list[dict]:
    if not query.strip():
        return []

    results: list[dict] = []
    with DDGS() as ddgs:
        for entry in ddgs.text(query, max_results=max_results):
            results.append(
                {
                    "title": entry.get("title") or "",
                    "body": entry.get("body") or "",
                    "href": entry.get("href") or "",
                }
            )
    return results


def format_search_results(results: list[dict]) -> str:
    if not results:
        return "No relevant web results were found."

    lines: list[str] = []
    for idx, result in enumerate(results, start=1):
        body = result["body"].strip().replace("\n", " ")
        snippet = body[:240] + ("…" if len(body) > 240 else "")
        lines.append(
            f"{idx}. {result['title'].strip()}\n   URL: {result['href']}\n   Snippet: {snippet}"
        )
    return "\n".join(lines)
