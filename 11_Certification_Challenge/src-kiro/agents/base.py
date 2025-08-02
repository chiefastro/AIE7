"""
Base agent interfaces and abstract classes.
Following patterns from Multi_Agent_RAG_LangGraph notebook.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_core.documents import Document
from src.models.state import (
    ConversationState, 
    AgentRoutingDecision, 
    ProcessedWebInfo, 
    AcademicInsights,
    MentalModel
)


class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def process(self, state: ConversationState) -> Dict[str, Any]:
        """Process the current state and return updates."""
        pass


class SupervisorAgent(BaseAgent):
    """Supervisor agent that coordinates subagents."""
    
    def __init__(self):
        super().__init__("supervisor")
    
    @abstractmethod
    def analyze_query(self, query: str) -> AgentRoutingDecision:
        """Analyze query and determine which subagents to use."""
        pass
    
    @abstractmethod
    def coordinate_subagents(self, routing: AgentRoutingDecision, state: ConversationState) -> ConversationState:
        """Coordinate execution of selected subagents."""
        pass


class VectorRAGSubagent(BaseAgent):
    """Subagent for vector-based RAG retrieval."""
    
    def __init__(self):
        super().__init__("vector_rag")
    
    @abstractmethod
    def retrieve_mental_models(self, query: str) -> List[Document]:
        """Retrieve relevant mental models from vector store."""
        pass
    
    @abstractmethod
    def extract_applicable_models(self, docs: List[Document]) -> List[MentalModel]:
        """Extract and identify applicable mental models."""
        pass


class WebSearchSubagent(BaseAgent):
    """Subagent for web search using Tavily."""
    
    def __init__(self):
        super().__init__("web_search")
    
    @abstractmethod
    def search_web(self, query: str) -> List[Dict[str, Any]]:
        """Search web using Tavily API."""
        pass
    
    @abstractmethod
    def process_results(self, results: List[Dict[str, Any]]) -> ProcessedWebInfo:
        """Process and structure web search results."""
        pass


class AcademicSearchSubagent(BaseAgent):
    """Subagent for academic search using Arxiv."""
    
    def __init__(self):
        super().__init__("academic_search")
    
    @abstractmethod
    def search_arxiv(self, query: str) -> List[Dict[str, Any]]:
        """Search academic papers using Arxiv API."""
        pass
    
    @abstractmethod
    def extract_insights(self, papers: List[Dict[str, Any]]) -> AcademicInsights:
        """Extract insights from academic papers."""
        pass