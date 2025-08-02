from langchain_community.vectorstores import Qdrant
from langchain_qdrant import QdrantVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient

from backend.src.mimi.config.vectors import PERSIST_DIR, EMBEDDING_MODEL
from backend.src.mimi.config.variants import get_variants

def get_retriever(persist_dir=PERSIST_DIR, **kwargs):
    """
    Get a retriever from the pre-populated Qdrant vector database.
    
    Args:
        persist_dir: Directory where the vector database is stored
        **kwargs: Additional arguments to pass to as_retriever()
    
    Returns:
        A retriever instance
    """
    embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    # Get collection name from variants config
    variants = get_variants()
    collection_name = variants.chunker_type.value
    
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
