from langchain_community.vectorstores import Qdrant
from langchain_qdrant import QdrantVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

from backend.src.mimi.config.models import MULTI_QUERY_LLM_MODEL, EMBEDDING_MODEL
from backend.src.mimi.config.retrieval import PERSIST_DIR
from backend.src.mimi.config.variants import variants, RetrieverType

def get_retriever(**kwargs):
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
    collection_name = variants.chunker_type.value
    
    # Connect to existing vector store
    client = QdrantClient(path=PERSIST_DIR)
    vectorstore = QdrantVectorStore(
        collection_name=collection_name,
        embedding=embedding_model,
        client=client
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever(**kwargs)

    # Use multi-query retriever if retriever_type is set to "multi_query"
    retriever_type = variants.retriever_type.value
    if retriever_type == RetrieverType.MULTI_QUERY:
        chat_model = ChatOpenAI(model=MULTI_QUERY_LLM_MODEL)
        retriever = MultiQueryRetriever.from_llm(
            retriever=retriever, llm=chat_model
        )

    return retriever
