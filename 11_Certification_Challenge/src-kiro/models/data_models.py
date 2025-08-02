"""
Core data models for the AI Mental Models Advisor.
Based on the design document specifications.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from langchain_core.documents import Document


@dataclass
class MentalModelData:
    """Data class for mental model information."""
    name: str
    description: str
    application_context: str
    source_chunk: Document
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "application_context": self.application_context,
            "source_chunk": self.source_chunk
        }


@dataclass
class WebResult:
    """Data class for web search results."""
    title: str
    url: str
    content: str
    relevance_score: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "relevance_score": self.relevance_score
        }


@dataclass
class ArxivPaper:
    """Data class for Arxiv paper information."""
    title: str
    authors: List[str]
    abstract: str
    url: str
    published_date: str
    relevance_score: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "url": self.url,
            "published_date": self.published_date,
            "relevance_score": self.relevance_score
        }


@dataclass
class FollowUpQuestion:
    """Data class for follow-up questions."""
    question: str
    mental_model: str
    reasoning: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "question": self.question,
            "mental_model": self.mental_model,
            "reasoning": self.reasoning
        }