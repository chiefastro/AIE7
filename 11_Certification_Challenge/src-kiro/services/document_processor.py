"""
Document processing service for mental models content.
Handles chunking and embedding of markdown documents.
"""

from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import VectorStore


class DocumentProcessor(ABC):
    """Abstract base class for document processing."""
    
    @abstractmethod
    def chunk_markdown(self, content: str) -> List[Document]:
        """
        Chunk markdown content while preserving structure.
        
        Args:
            content: Raw markdown content
            
        Returns:
            List of chunked documents with preserved context
        """
        pass
    
    @abstractmethod
    def embed_chunks(self, chunks: List[Document]) -> VectorStore:
        """
        Create embeddings and store in vector database.
        
        Args:
            chunks: List of document chunks
            
        Returns:
            Configured vector store with embedded documents
        """
        pass


class MarkdownChunker:
    """Specialized chunker for markdown content that preserves structure."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_with_context(self, content: str, source_metadata: dict = None) -> List[Document]:
        """
        Chunk markdown while maintaining heading context.
        
        Args:
            content: Markdown content to chunk
            source_metadata: Optional metadata to include
            
        Returns:
            List of documents with contextual information
        """
        # Implementation will be added in later tasks
        pass