from langchain_community.vectorstores import Qdrant
from langchain_qdrant import QdrantVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient

from mimi.config.vector import COLLECTION_NAME, PERSIST_DIR, EMBEDDING_MODEL

def get_retriever(collection_name=COLLECTION_NAME, persist_dir=PERSIST_DIR, **kwargs):
    """
    Get a retriever from the pre-populated Qdrant vector database.
    
    Args:
        collection_name: Name of the Qdrant collection
        persist_dir: Directory where the vector database is stored
        **kwargs: Additional arguments to pass to as_retriever()
    
    Returns:
        A retriever instance
    """
    embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    # Connect to existing vector store
    client = QdrantClient(path=persist_dir)
    vectorstore = QdrantVectorStore(
        collection_name=collection_name,
        embedding=embedding_model,
        client=client
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever(**kwargs)
    return retriever
