"""Web search tool for the agent.

We use DuckDuckGo's instant answer API here because it is free and requires no
API key. This is simpler than third-party package wrappers, but it is also less
feature-rich and may sometimes return limited or inconsistent results.
"""
import json
from typing import Any

import requests

from tools.base import Tool


class WebSearchTool(Tool):
    name = "web_search"
    description = "Search the web for recent information about a topic."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query to look up."}
        },
        "required": ["query"],
    }

    def run(self, **kwargs) -> str:
        query = kwargs.get("query")
        if not query or not str(query).strip():
            return "Web search failed: a non-empty query is required."

        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_redirect": 1,
            "no_html": 1,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            return f"Web search failed: unable to reach the search service ({exc})."

        results = []

        # Top-level result list when available
        related_topics = data.get("RelatedTopics", [])
        for item in related_topics[:3]:
            if isinstance(item, dict):
                title = item.get("Text") or item.get("Name") or "Result"
                snippet = item.get("Result") or item.get("Snippet") or ""
                if snippet:
                    results.append(f"- {title}: {snippet}")

        # Instant answer fallback
        if not results:
            abstract = data.get("AbstractText") or data.get("Abstract")
            if abstract:
                results.append(f"- {data.get('Heading', 'Summary')}: {abstract}")

        # More direct fallback for the underlying API plus top results
        if not results:
            if data.get("Results"):
                for result in data["Results"][:3]:
                    results.append(f"- {result.get('Text', 'Result')}")

        if not results:
            return f"Web search returned no results for: {query}."

        return "\n".join(results[:5])
