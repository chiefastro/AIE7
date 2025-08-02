from langchain_community.vectorstores import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings

from mimi.config.vectors import PERSIST_DIR, EMBEDDING_MODEL
from mimi.config.variants import variants

def index(chunks):
    embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    # Get collection name from variants config
    collection_name = variants.chunker_type.value
    
    qdrant_vectorstore = Qdrant.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=collection_name,
        path=PERSIST_DIR,
        force_recreate=True  # Overwrite existing collection
    )
    return qdrant_vectorstore