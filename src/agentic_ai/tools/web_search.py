"""Web search as a tool.

Search is the tool that makes an agent useful on anything that happened after
the model's training cutoff, and the one that most often ruins a context
window. The defaults here reflect that: few results, short snippets, and a
formatted block that tells the model where each claim came from so it can cite
rather than assert.

Provider is behind one function. Tavily is the default because its free tier is
enough to finish every lab in this repo.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentic_ai.errors import ConfigError, ToolExecutionError
from agentic_ai.settings import get_settings
from agentic_ai.tools.registry import tool


@dataclass(frozen=True, slots=True)
class SearchResult:
    """One hit, trimmed to what a model can act on."""

    title: str
    url: str
    snippet: str

    def render(self) -> str:
        """Format for inclusion in a prompt, URL included so answers can cite."""
        return f"### {self.title}\n{self.url}\n{self.snippet}"


def search(query: str, max_results: int = 5) -> list[SearchResult]:
    """Run a web search and return structured results.

    Args:
        query: The search query.
        max_results: How many results to return. Keep it small; ten mediocre
            results crowd out the two good ones.

    Returns:
        Results in provider-ranked order.

    Raises:
        ConfigError: No ``TAVILY_API_KEY`` configured.
        ToolExecutionError: The search provider failed.
    """
    try:
        from tavily import TavilyClient
    except ImportError as exc:  # pragma: no cover - depends on optional extra
        raise ConfigError("web search needs the 'labs' extra: uv sync --extra labs") from exc

    api_key = get_settings().key_for("tavily")
    try:
        response = TavilyClient(api_key=api_key).search(
            query=query,
            max_results=max_results,
            search_depth="basic",
        )
    except Exception as exc:
        raise ToolExecutionError("search_web", f"search provider failed: {exc}") from exc

    return [
        SearchResult(
            title=str(hit.get("title", "untitled")),
            url=str(hit.get("url", "")),
            # Snippets arrive at wildly varying lengths; cap so that one
            # verbose result cannot dominate the agent's context.
            snippet=str(hit.get("content", ""))[:700],
        )
        for hit in response.get("results", [])
    ]


@tool
def search_web(query: str, max_results: int = 5) -> str:
    """Search the public web for current information and return ranked results.

    Use this when the answer depends on recent events, specific numbers, or
    anything you are not confident about from memory. Prefer several narrow
    queries over one broad one.

    Args:
        query: A focused search query. Narrow queries beat broad ones.
        max_results: Number of results, 1 to 10.
    """
    results = search(query, max_results=max(1, min(max_results, 10)))
    if not results:
        return f"No results for {query!r}. Try different wording or a broader query."
    return "\n\n".join(r.render() for r in results)
