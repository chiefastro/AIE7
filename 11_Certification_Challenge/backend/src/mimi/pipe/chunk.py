import tiktoken
import re
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from mimi.config.variants import ChunkerType

def tiktoken_len(text):
    tokens = tiktoken.encoding_for_model("gpt-4o").encode(
        text,
    )
    return len(tokens)

class MarkdownAwareTextSplitter:
    """
    Custom text splitter that leverages the structure of markdown documents.
    Creates granular chunks: each bullet point, table row, paragraph, and quote becomes a separate chunk,
    while retaining headers for context.
    
    Implements the same interface as RecursiveCharacterTextSplitter.
    """
    
    def __init__(self, chunk_size: int = 750, chunk_overlap: int = 0, length_function=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function or tiktoken_len
        
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents using markdown-aware chunking.
        Matches the interface of RecursiveCharacterTextSplitter.split_documents()
        """
        all_chunks = []
        
        for doc in documents:
            # Use custom chunker for markdown content
            text_chunks = self.split_text(doc.page_content)
            
            # Convert text chunks back to Document objects with metadata
            for i, chunk_text in enumerate(text_chunks):
                chunk_doc = Document(
                    page_content=chunk_text,
                    metadata={
                        **doc.metadata,
                        "chunk_index": i,
                        "total_chunks": len(text_chunks)
                    }
                )
                all_chunks.append(chunk_doc)
        
        return all_chunks
    
    def split_text(self, text: str) -> List[str]:
        """
        Split text using markdown-aware chunking.
        """
        return self._split_markdown(text)
    
    def _split_markdown(self, text: str) -> List[str]:
        """
        Split markdown text into granular chunks while preserving headers for context.
        """
        lines = text.split('\n')
        chunks = []
        current_header = ""
        current_chunk_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Handle headers
            if re.match(r'^#{1,6}\s+', line):
                # Save previous chunk if it exists
                if current_chunk_lines:
                    chunk_text = self._create_chunk_with_header(current_header, current_chunk_lines)
                    if chunk_text.strip():
                        chunks.append(chunk_text)
                
                # Start new section with this header
                current_header = line
                current_chunk_lines = []
                i += 1
                continue
            
            # Handle blockquotes
            if line.startswith('>'):
                # Save previous chunk if it exists
                if current_chunk_lines:
                    chunk_text = self._create_chunk_with_header(current_header, current_chunk_lines)
                    if chunk_text.strip():
                        chunks.append(chunk_text)
                
                # Collect the entire blockquote
                quote_lines = []
                while i < len(lines) and lines[i].strip().startswith('>'):
                    quote_lines.append(lines[i])
                    i += 1
                
                # Create chunk for the blockquote
                if quote_lines:
                    chunk_text = self._create_chunk_with_header(current_header, quote_lines)
                    if chunk_text.strip():
                        chunks.append(chunk_text)
                continue
            
            # Handle bullet points and numbered lists
            if re.match(r'^[\*\-+]\s+', line) or re.match(r'^\d+\.\s+', line):
                # Save previous chunk if it exists
                if current_chunk_lines:
                    chunk_text = self._create_chunk_with_header(current_header, current_chunk_lines)
                    if chunk_text.strip():
                        chunks.append(chunk_text)
                
                # Create chunk for this bullet point
                chunk_text = self._create_chunk_with_header(current_header, [lines[i]])
                if chunk_text.strip():
                    chunks.append(chunk_text)
                
                current_chunk_lines = []
                i += 1
                continue
            
            # Handle table rows
            if '|' in line and not re.match(r'^[\|\-\s]+$', line):
                # Save previous chunk if it exists
                if current_chunk_lines:
                    chunk_text = self._create_chunk_with_header(current_header, current_chunk_lines)
                    if chunk_text.strip():
                        chunks.append(chunk_text)
                
                # Create chunk for this table row
                chunk_text = self._create_chunk_with_header(current_header, [lines[i]])
                if chunk_text.strip():
                    chunks.append(chunk_text)
                
                current_chunk_lines = []
                i += 1
                continue
            
            # Handle table separators
            if re.match(r'^[\|\-\s]+$', line):
                # Skip table separators
                i += 1
                continue
            
            # Handle empty lines
            if not line:
                # Save previous chunk if it exists
                if current_chunk_lines:
                    chunk_text = self._create_chunk_with_header(current_header, current_chunk_lines)
                    if chunk_text.strip():
                        chunks.append(chunk_text)
                    current_chunk_lines = []
                i += 1
                continue
            
            # Regular paragraph text
            current_chunk_lines.append(lines[i])
            i += 1
        
        # Save final chunk
        if current_chunk_lines:
            chunk_text = self._create_chunk_with_header(current_header, current_chunk_lines)
            if chunk_text.strip():
                chunks.append(chunk_text)
        
        return chunks
    
    def _create_chunk_with_header(self, header: str, content_lines: List[str]) -> str:
        """
        Create a chunk with header context.
        """
        if not content_lines:
            return ""
        
        # If we have a header, include it
        if header:
            return f"{header}\n\n{chr(10).join(content_lines)}"
        else:
            return chr(10).join(content_lines)

# Initialize the custom chunker
markdown_chunker = MarkdownAwareTextSplitter(
    chunk_size=750,
    chunk_overlap=0
)

# Keep the original text splitter as fallback
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 750,
    chunk_overlap = 0,
    length_function = tiktoken_len,
)

def get_chunker(chunker_type: ChunkerType):
    if chunker_type == ChunkerType.MARKDOWN_CHUNKER:
        return markdown_chunker
    elif chunker_type == ChunkerType.NAIVE_CHUNKER:
        return text_splitter
    else:
        raise ValueError(f"Invalid chunker type: {chunker_type}")


def test_chunker():
    """Test the custom chunker with the mental models document."""
    
    # Load the test document
    doc_path = Path("../../../../data/Mental-Models-for-the-Intelligence-Age-Skillenai.md")
    
    if not doc_path.exists():
        print(f"Error: Test document not found at {doc_path}")
        return
    
    with open(doc_path, 'r') as f:
        content = f.read()
    
    print(f"Original document length: {len(content)} characters")
    print(f"Original document starts with: {content[:100]}...")
    print("-" * 80)
    
    # Test the custom chunker
    print("Testing custom markdown-aware chunker:")
    chunks = markdown_chunker.split_text(content)
    
    print(f"Created {len(chunks)} chunks:")
    print("-" * 80)
    
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1} ({len(chunk)} chars):")
        print("-" * 40)
        print(chunk[:300] + "..." if len(chunk) > 300 else chunk)
        print("-" * 40)
        
        # Check if chunk contains headers
        if '##' in chunk:
            print("✓ Contains section header")
        
        # Check if chunk contains bullet points
        if any(line.strip().startswith('*') for line in chunk.split('\n')):
            print("✓ Contains bullet points")
        
        # Check if chunk contains tables
        if '|' in chunk and '---' in chunk:
            print("✓ Contains table")
        
        # Check if chunk contains quotes
        if chunk.strip().startswith('>'):
            print("✓ Contains quote")
        
        # Check chunk size
        if len(chunk) < 100:
            print("✓ Small chunk")
        elif len(chunk) < 500:
            print("✓ Medium chunk")
        else:
            print("⚠ Large chunk")
    
    print("\n" + "=" * 80)
    print("Chunking analysis complete!")
    
    # Test the fallback chunker for comparison
    print("\nTesting fallback chunker for comparison:")
    fallback_chunks = text_splitter.split_text(content)
    print(f"Fallback created {len(fallback_chunks)} chunks")
    
    # Show a sample fallback chunk
    if fallback_chunks:
        print(f"\nSample fallback chunk ({len(fallback_chunks[0])} chars):")
        print("-" * 40)
        print(fallback_chunks[0][:200] + "..." if len(fallback_chunks[0]) > 200 else fallback_chunks[0])

if __name__ == "__main__":
    from pathlib import Path
    test_chunker()
