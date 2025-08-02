"""
Configuration settings for the AI Mental Models Advisor.
"""

import os
from typing import Dict, Any


class Config:
    """Configuration class for application settings."""
    
    # LLM Configuration
    OPENAI_MODEL = "gpt-4.1-nano"
    EMBEDDING_MODEL = "text-embedding-3-small"
    
    # Vector Store Configuration
    VECTOR_STORE_LOCATION = ":memory:"  # In-memory for development
    COLLECTION_NAME = "mental_models"
    
    # Retrieval Configuration
    DEFAULT_K = 10  # Number of documents to retrieve
    RERANK_TOP_K = 5  # Number of documents after reranking
    
    # API Keys (from environment)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    
    # Chunking Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Get LLM configuration."""
        return {
            "model": cls.OPENAI_MODEL,
            "temperature": 0.1,
            "max_tokens": 1000
        }
    
    @classmethod
    def get_embedding_config(cls) -> Dict[str, Any]:
        """Get embedding model configuration."""
        return {
            "model": cls.EMBEDDING_MODEL
        }
    
    @classmethod
    def validate_api_keys(cls) -> bool:
        """Validate that required API keys are present."""
        required_keys = [cls.OPENAI_API_KEY]
        return all(key is not None for key in required_keys)