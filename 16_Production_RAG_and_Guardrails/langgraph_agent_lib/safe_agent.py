"""LangGraph agent with input/output Guardrails integration."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import os

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools.arxiv.tool import ArxivQueryRun

from .models import get_openai_model
from .rag import ProductionRAGChain
from .guardrails import SafetyGuards, build_default_guards


class SafeAgentState(TypedDict):
    """State schema for guarded agent graphs."""

    messages: Annotated[List[BaseMessage], add_messages]
    retry_count: int
    blocked: bool


def create_rag_tool(rag_chain: ProductionRAGChain):
    """Create a RAG tool from a ProductionRAGChain."""

    @tool
    def retrieve_information(query: str) -> str:
        """Use Retrieval Augmented Generation to retrieve information from the student loan documents."""
        try:
            result = rag_chain.invoke(query)
            return result.content if hasattr(result, "content") else str(result)
        except Exception as exc:  # pragma: no cover
            return f"Error retrieving information: {str(exc)}"

    return retrieve_information


def get_default_tools(rag_chain: Optional[ProductionRAGChain] = None) -> List:
    """Get default tools for the agent (Tavily, Arxiv, and optional RAG)."""
    tools: List[Any] = []
    if os.getenv("TAVILY_API_KEY"):
        tools.append(TavilySearchResults(max_results=5))
    tools.append(ArxivQueryRun())
    if rag_chain:
        tools.append(create_rag_tool(rag_chain))
    return tools


def create_safe_langgraph_agent(
    model_name: str = "gpt-4",
    temperature: float = 0.1,
    tools: Optional[List] = None,
    rag_chain: Optional[ProductionRAGChain] = None,
    guards: Optional[SafetyGuards] = None,
    max_refinements: int = 1,
):
    """Create a LangGraph agent with Guardrails-based input/output validation.

    Flow: input_guard -> agent -> (tools)* -> output_guard -> (refine <= max_refinements)
    """

    if tools is None:
        tools = get_default_tools(rag_chain)

    if guards is None:
        guards = build_default_guards()

    # Bind model and tools
    model = get_openai_model(model_name=model_name, temperature=temperature)
    model_with_tools = model.bind_tools(tools)

    def input_guard_node(state: SafeAgentState) -> Dict[str, Any]:
        messages = state["messages"]
        last_human = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                last_human = msg
                break
        if last_human is None:
            return {"blocked": False}

        result = guards.run_input(last_human.content)

        if result.validated_text != last_human.content:
            # Replace last human message with redacted text
            redacted = HumanMessage(content=result.validated_text)
            return {"messages": [redacted], "blocked": not result.passed}

        if not result.passed:
            refusal = AIMessage(
                content=(
                    "I cannot assist with that request. Please keep questions on student loans "
                    "and avoid unsafe content or attempts to bypass safeguards."
                )
            )
            return {"messages": [refusal], "blocked": True}

        return {"blocked": False}

    def call_model(state: SafeAgentState) -> Dict[str, Any]:
        messages = state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    def should_route_after_input(state: SafeAgentState):
        return END if state.get("blocked", False) else "agent"

    def should_continue(state: SafeAgentState):
        last_message = state["messages"][-1]
        if getattr(last_message, "tool_calls", None):
            return "action"
        return "output_guard"

    def output_guard_node(state: SafeAgentState) -> Dict[str, Any]:
        last_ai = None
        for msg in reversed(state["messages"]):
            if isinstance(msg, AIMessage):
                last_ai = msg
                break
        if last_ai is None:
            return {}

        result = guards.run_output(last_ai.content)
        if result.passed:
            return {"retry_count": state.get("retry_count", 0)}

        # Add critique and request refinement
        critique = SystemMessage(
            content=(
                "Your previous reply failed safety checks. Regenerate a safe, on-topic, factual, "
                "and PII-free answer. Do not include disallowed content."
            )
        )
        return {"messages": [critique], "retry_count": state.get("retry_count", 0) + 1}

    def should_refine_or_end(state: SafeAgentState):
        # If last message is a SystemMessage critique we should refine; otherwise end
        last = state["messages"][-1]
        if isinstance(last, SystemMessage):
            current_retries = state.get("retry_count", 0)
            if current_retries < max_refinements:
                return "agent"
        return END

    # Build graph
    graph = StateGraph(SafeAgentState)
    tool_node = ToolNode(tools)

    graph.add_node("input_guard", input_guard_node)
    graph.add_node("agent", call_model)
    graph.add_node("action", tool_node)
    graph.add_node("output_guard", output_guard_node)

    graph.set_entry_point("input_guard")
    graph.add_conditional_edges("input_guard", should_route_after_input, {"agent": "agent", END: END})
    graph.add_conditional_edges("agent", should_continue, {"action": "action", "output_guard": "output_guard"})
    graph.add_edge("action", "agent")
    graph.add_conditional_edges("output_guard", should_refine_or_end, {"agent": "agent", END: END})

    return graph.compile()


__all__ = ["create_safe_langgraph_agent", "SafeAgentState"]


