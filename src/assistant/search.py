import os
from dataclasses import dataclass
from typing import List, Optional

import requests


class SearchUnavailable(RuntimeError):
    """Raised when a search request is attempted without a configured provider."""


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


class TavilySearchClient:
    """Thin wrapper around the Tavily web search API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise SearchUnavailable(
                "No Tavily API key found. Set TAVILY_API_KEY to enable web search integration."
            )

    def search(self, query: str, max_results: int = 3) -> List[SearchResult]:
        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        response = requests.post(
            "https://api.tavily.com/search",
            json={"query": query, "max_results": max_results, "include_answer": True},
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        hits = data.get("results", [])
        results = []
        for hit in hits[:max_results]:
            results.append(
                SearchResult(
                    title=hit.get("title", "Untitled"),
                    url=hit.get("url", ""),
                    snippet=hit.get("content", "")[:500],
                )
            )
        if not results and data.get("answer"):
            results.append(
                SearchResult(
                    title="Tavily Summary",
                    url="",
                    snippet=data["answer"],
                )
            )
        return results


def format_results(results: List[SearchResult]) -> str:
    """Render search results into a compact string for prompt injection."""
    formatted = []
    for idx, item in enumerate(results, start=1):
        formatted.append(f"{idx}. {item.title}\n   {item.url}\n   {item.snippet}")
    return "\n".join(formatted)
