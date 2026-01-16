"""
Document Ingestion Module
=========================
This module handles loading and chunking documents for the RAG pipeline.

Your Task (Step 3):
- Implement the `chunk_document()` function
- Documents should be split into overlapping chunks
- Recommended: 500 characters per chunk, 100 character overlap
"""

import os
from typing import List, Dict
from pathlib import Path


def load_documents(docs_path: str) -> List[Dict]:
    """
    Load all text documents from the specified directory.

    Args:
        docs_path: Path to directory containing .txt files

    Returns:
        List of document dicts with 'content' and 'metadata' keys
    """
    documents = []
    docs_dir = Path(docs_path)

    for file_path in docs_dir.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            documents.append({
                "content": content,
                "metadata": {
                    "source": file_path.name,
                    "path": str(file_path)
                }
            })

    return documents


def chunk_document(content: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Split a document into overlapping chunks.

    TODO: Implement this function!

    Args:
        content: The full text content to chunk
        chunk_size: Maximum size of each chunk (default: 500 chars)
        overlap: Number of characters to overlap between chunks (default: 100)

    Returns:
        List of text chunks

    Example:
        >>> text = "Hello world. This is a test document for chunking."
        >>> chunks = chunk_document(text, chunk_size=20, overlap=5)
        >>> len(chunks) > 1
        True

    Hints:
        - Use a sliding window approach
        - Handle edge cases: empty content, content shorter than chunk_size
        - Ensure no chunk exceeds chunk_size
        - The last chunk may be smaller than chunk_size
    """
    if not content:
        return []

    if len(content) <= chunk_size:
        return [content]

    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(content):
        end = start + chunk_size
        chunk = content[start:end]
        chunks.append(chunk)
        start += step

    return chunks


def process_documents(docs_path: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict]:
    """
    Load documents and split them into chunks with metadata.

    Args:
        docs_path: Path to documents directory
        chunk_size: Size of each chunk
        overlap: Overlap between chunks

    Returns:
        List of chunk dicts with 'content' and 'metadata' keys
    """
    documents = load_documents(docs_path)
    all_chunks = []

    for doc in documents:
        chunks = chunk_document(doc["content"], chunk_size, overlap)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "content": chunk,
                "metadata": {
                    **doc["metadata"],
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            })

    return all_chunks


if __name__ == "__main__":
    # Test with sample documents
    import sys

    docs_path = sys.argv[1] if len(sys.argv) > 1 else "../data/sample_docs"

    print("Loading and chunking documents...")
    chunks = process_documents(docs_path)
    print(f"Created {len(chunks)} chunks from documents")

    if chunks:
        print(f"\nFirst chunk preview:")
        print(f"  Content: {chunks[0]['content'][:100]}...")
        print(f"  Source: {chunks[0]['metadata']['source']}")
