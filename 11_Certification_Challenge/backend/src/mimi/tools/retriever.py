from langchain_qdrant import QdrantVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
import threading

from mimi.config.models import MULTI_QUERY_LLM_MODEL, EMBEDDING_MODEL
from mimi.config.retrieval import PERSIST_DIR
from mimi.config.variant_defaults import CHUNKER_TYPE, RETRIEVER_TYPE

# Global client instance with thread lock
_qdrant_client = None
_client_lock = threading.Lock()

def get_qdrant_client():
    """Get a singleton Qdrant client instance"""
    global _qdrant_client
    if _qdrant_client is None:
        with _client_lock:
            if _qdrant_client is None:
                _qdrant_client = QdrantClient(path=PERSIST_DIR)
    return _qdrant_client

def get_retriever(chunker_type: str = CHUNKER_TYPE, retriever_type: str = RETRIEVER_TYPE, **kwargs):
    """
    Get a retriever from the pre-populated Qdrant vector database.
    
    Args:
        persist_dir: Directory where the vector database is stored
        **kwargs: Additional arguments to pass to as_retriever()
    
    Returns:
        A retriever instance
    """
    embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    # Use singleton client instance
    client = get_qdrant_client()
    vectorstore = QdrantVectorStore(
        collection_name=chunker_type,
        embedding=embedding_model,
        client=client
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever(**kwargs)

    # Use multi-query retriever if retriever_type is set to "multi_query"
    if retriever_type == "multi_query":
        chat_model = ChatOpenAI(model=MULTI_QUERY_LLM_MODEL)
        retriever = MultiQueryRetriever.from_llm(
            retriever=retriever, llm=chat_model
        )

    return retriever
