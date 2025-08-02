from pathlib import Path
from mimi.pipe.load import load_documents
from mimi.pipe.chunk import markdown_chunker
from mimi.pipe.index import index
from dotenv import load_dotenv

load_dotenv()

def pipe(docs):
    print(f"Starting pipeline with docs path: {docs}")
    docs = load_documents(docs)
    print(f"Documents loaded: {len(docs)}")
    
    # Use custom markdown-aware chunking
    chunks = markdown_chunker.split_documents(docs)
    print(f"Chunks created: {len(chunks)}")
    
    if len(chunks) == 0:
        print("ERROR: No chunks created! This will cause the embedding error.")
        return None
        
    vectorstore = index(chunks)
    return vectorstore

if __name__ == "__main__":
    pipe(Path("./data"))