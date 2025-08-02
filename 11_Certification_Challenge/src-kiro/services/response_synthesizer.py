"""
Response synthesis service for combining multi-source information.
"""

from abc import ABC, abstractmethod
from typing import List
from src.models.state import MultiSourceData, FinalResponse
from src.models.data_models import FollowUpQuestion


class ResponseSynthesizer(ABC):
    """Abstract base class for response synthesis."""
    
    @abstractmethod
    def synthesize_response(self, multi_source_data: MultiSourceData) -> FinalResponse:
        """
        Combine information from multiple sources into coherent response.
        
        Args:
            multi_source_data: Data from vector RAG, web search, and academic search
            
        Returns:
            Synthesized final response with mental model applications
        """
        pass
    
    @abstractmethod
    def generate_followups(self, response: FinalResponse) -> List[FollowUpQuestion]:
        """
        Generate follow-up questions based on the response.
        
        Args:
            response: The final response
            
        Returns:
            List of relevant follow-up questions
        """
        pass