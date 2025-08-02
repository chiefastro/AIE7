from pathlib import Path
from mimi.pipe.load import load_documents
from mimi.pipe.chunk import get_chunker
from mimi.pipe.index import index
from mimi.config.variants import variants
from dotenv import load_dotenv

load_dotenv()

def pipe(docs):
    print(f"Starting pipeline with docs path: {docs}")
    docs = load_documents(docs)
    print(f"Documents loaded: {len(docs)}")
    
    # Get chunker type from variants config
    chunker_type = variants.chunker_type
    print(f"Using chunker: {chunker_type.value}")
    
    # Get the appropriate chunker
    chunker = get_chunker(chunker_type)
    
    # Use the selected chunker
    chunks = chunker.split_documents(docs)
    print(f"Chunks created: {len(chunks)}")
    
    if len(chunks) == 0:
        print("ERROR: No chunks created! This will cause the embedding error.")
        return None
        
    vectorstore = index(chunks)
    return vectorstore

if __name__ == "__main__":
    pipe(Path("./data"))