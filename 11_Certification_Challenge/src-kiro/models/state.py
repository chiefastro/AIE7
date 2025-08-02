"""
State schemas for LangGraph workflows.
Based on patterns from Multi_Agent_RAG_LangGraph notebook.
"""

from typing import List, Dict, Optional, Any
from typing_extensions import TypedDict
from langchain_core.documents import Document


class ConversationState(TypedDict):
    """Main state schema for the conversation workflow."""
    query: str
    conversation_history: List[Dict[str, Any]]
    routing_decision: Optional["AgentRoutingDecision"]
    vector_results: Optional[List[Document]]
    web_results: Optional["ProcessedWebInfo"]
    academic_results: Optional["AcademicInsights"]
    final_response: Optional["FinalResponse"]


class AgentRoutingDecision(TypedDict):
    """Schema for supervisor agent routing decisions."""
    use_vector_rag: bool
    use_web_search: bool
    use_academic_search: bool
    reasoning: str


class ProcessedWebInfo(TypedDict):
    """Schema for processed web search results."""
    results: List[Dict[str, Any]]
    summary: str
    sources: List[str]


class AcademicInsights(TypedDict):
    """Schema for academic search results."""
    papers: List[Dict[str, Any]]
    insights: str
    sources: List[str]


class FinalResponse(TypedDict):
    """Schema for the final synthesized response."""
    answer: str
    mental_models_used: List[str]
    sources: List[str]
    follow_up_questions: List[str]


class MentalModel(TypedDict):
    """Schema for mental model data."""
    name: str
    description: str
    application_context: str
    source_chunk: Document


class MultiSourceData(TypedDict):
    """Schema for combining data from multiple sources."""
    mental_models: List[MentalModel]
    web_insights: Optional[ProcessedWebInfo]
    academic_insights: Optional[AcademicInsights]