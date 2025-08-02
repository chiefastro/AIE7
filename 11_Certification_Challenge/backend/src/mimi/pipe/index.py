from langchain_community.vectorstores import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings

from mimi.config.vector import COLLECTION_NAME, PERSIST_DIR, EMBEDDING_MODEL

def index(chunks):
    embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    qdrant_vectorstore = Qdrant.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        path=PERSIST_DIR,
        force_recreate=True  # Overwrite existing collection
    )
    return qdrant_vectorstore