"""Utilities to compare LangGraph agents and measure cache performance.

Functions here are notebook-friendly and avoid external dependencies.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional, Tuple

from langchain_core.messages import BaseMessage, AIMessage, HumanMessage


def _is_helpfulness_marker(message: BaseMessage) -> bool:
    content = getattr(message, "content", "")
    return isinstance(content, str) and content.startswith("HELPFULNESS:")


def extract_helpfulness_decision(messages: List[BaseMessage]) -> Optional[str]:
    """Return 'Y', 'N', 'END', or None if no helpfulness marker is present."""
    for message in reversed(messages):
        if _is_helpfulness_marker(message):
            text = str(getattr(message, "content", ""))
            if text == "HELPFULNESS:END":
                return "END"
            if "HELPFULNESS:Y" in text:
                return "Y"
            if "HELPFULNESS:N" in text:
                return "N"
    return None


def extract_final_ai_message(messages: List[BaseMessage]) -> Optional[AIMessage]:
    """Return the last AIMessage excluding helpfulness markers, if any."""
    for message in reversed(messages):
        if isinstance(message, AIMessage) and not _is_helpfulness_marker(message):
            return message
    return None


def count_tool_calls(messages: List[BaseMessage]) -> int:
    """Count tool calls by summing tool_calls in AI messages across the trace."""
    total = 0
    for message in messages:
        if isinstance(message, AIMessage):
            tool_calls = getattr(message, "tool_calls", None)
            if isinstance(tool_calls, list):
                total += len(tool_calls)
    return total


def invoke_agent(agent: Any, query: str) -> Tuple[Dict[str, Any], float]:
    """Invoke a compiled LangGraph agent with a single HumanMessage and measure time."""
    from langchain_core.messages import HumanMessage  # local import to keep deps light

    messages = [HumanMessage(content=query)]
    start = time.perf_counter()
    response = agent.invoke({"messages": messages})
    elapsed = time.perf_counter() - start
    return response, elapsed


def summarize_response(response: Dict[str, Any], elapsed_s: float) -> Dict[str, Any]:
    """Summarize key metrics from an agent invocation response."""
    messages: List[BaseMessage] = response.get("messages", [])  # type: ignore
    final_ai = extract_final_ai_message(messages)
    helpfulness = extract_helpfulness_decision(messages)
    tool_calls = count_tool_calls(messages)

    return {
        "elapsed_s": elapsed_s,
        "num_messages": len(messages),
        "tool_calls": tool_calls,
        "helpfulness": helpfulness,
        "final_text": getattr(final_ai, "content", ""),
    }


def compare_agents_on_query(agent_a: Any, agent_b: Any, query: str, name_a: str = "agent_a", name_b: str = "agent_b") -> Dict[str, Any]:
    """Run both agents on the same query and return a side-by-side summary dict."""
    resp_a, t_a = invoke_agent(agent_a, query)
    resp_b, t_b = invoke_agent(agent_b, query)

    summary_a = summarize_response(resp_a, t_a)
    summary_b = summarize_response(resp_b, t_b)

    return {
        "query": query,
        name_a: summary_a,
        name_b: summary_b,
    }


def compare_agents_on_queries(agent_a: Any, agent_b: Any, queries: List[str], name_a: str = "agent_a", name_b: str = "agent_b") -> List[Dict[str, Any]]:
    """Batch compare two agents across multiple queries; returns list of comparison dicts."""
    results: List[Dict[str, Any]] = []
    for q in queries:
        results.append(compare_agents_on_query(agent_a, agent_b, q, name_a, name_b))
    return results


def measure_cache_performance(agent: Any, query: str, repeats: int = 3) -> Dict[str, Any]:
    """Invoke the same query multiple times to observe timing and potential cache effects."""
    timings: List[float] = []
    texts: List[str] = []
    for _ in range(max(1, repeats)):
        resp, t = invoke_agent(agent, query)
        timings.append(t)
        texts.append(str(summarize_response(resp, t).get("final_text", "")))
    return {
        "query": query,
        "repeats": repeats,
        "timings_s": timings,
        "min_s": min(timings) if timings else None,
        "max_s": max(timings) if timings else None,
        "first_s": timings[0] if timings else None,
        "last_s": timings[-1] if timings else None,
        "responses_identical": len(set(texts)) == 1 if texts else None,
    }


def get_directory_size_bytes(path: str) -> int:
    """Compute total size of files under a directory tree."""
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total


def human_readable_bytes(num: int) -> str:
    """Convert bytes to a human readable string."""
    step = 1024.0
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < step:
            return f"{num:0.2f} {unit}"
        num /= step
    return f"{num:0.2f} PB"


__all__ = [
    "extract_helpfulness_decision",
    "extract_final_ai_message",
    "count_tool_calls",
    "invoke_agent",
    "summarize_response",
    "compare_agents_on_query",
    "compare_agents_on_queries",
    "measure_cache_performance",
    "get_directory_size_bytes",
    "human_readable_bytes",
]


