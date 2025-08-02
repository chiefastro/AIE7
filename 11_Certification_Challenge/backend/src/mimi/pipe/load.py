"""Load .md files from data directory into a list of documents"""

from pathlib import Path
from typing import List
from langchain.schema import Document

def load_documents(directory: Path) -> List[Document]:
    """Load .md files from data directory into a list of documents"""
    print(f"Searching for .md files in: {directory.absolute()}")
    documents = []
    md_files = list(directory.glob("*.md"))
    print(f"Found {len(md_files)} .md files: {[f.name for f in md_files]}")
    
    for file in md_files:
        print(f"Loading file: {file.name}")
        with open(file, "r") as f:
            content = f.read()
            print(f"  - Content length: {len(content)} characters")
            documents.append(Document(page_content=content, metadata={"source": file.name}))
    
    print(f"Total documents loaded: {len(documents)}")
    return documents