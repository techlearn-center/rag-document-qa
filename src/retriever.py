"""
Vector Retriever Module
=======================
This module handles storing and retrieving documents from the vector database.

Your Task (Step 5 & 6):
- Implement `store_embeddings()` to insert vectors into Qdrant
- Implement `search()` to find similar documents
"""

import os
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


# Qdrant connection settings
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_NAME = "documents"
VECTOR_SIZE = 1536  # text-embedding-3-small dimension


def get_client() -> QdrantClient:
    """Create Qdrant client connection."""
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def initialize_collection(client: QdrantClient, recreate: bool = False) -> None:
    """
    Initialize the Qdrant collection for document storage.

    Args:
        client: Qdrant client instance
        recreate: If True, delete and recreate the collection
    """
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME in collection_names:
        if recreate:
            client.delete_collection(COLLECTION_NAME)
        else:
            return  # Collection already exists

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )
    print(f"Created collection: {COLLECTION_NAME}")


def store_embeddings(chunks: List[Dict], client: Optional[QdrantClient] = None) -> int:
    """
    Store document chunks with embeddings in Qdrant.

    TODO: Implement this function!

    Args:
        chunks: List of chunk dicts with 'content', 'embedding', and 'metadata' keys
        client: Optional Qdrant client (creates new one if not provided)

    Returns:
        Number of points stored

    Example:
        >>> chunks = [
        ...     {"content": "Hello", "embedding": [0.1] * 1536, "metadata": {"source": "test.txt"}}
        ... ]
        >>> count = store_embeddings(chunks)
        >>> count == 1
        True

    Hints:
        - Use get_client() if client is None
        - Call initialize_collection() first
        - Create PointStruct objects for each chunk
        - Use client.upsert(collection_name=COLLECTION_NAME, points=points)
        - PointStruct needs: id (int), vector (list), payload (dict with content + metadata)
    """
    # TODO: Your implementation here
    # Remove the line below and implement the storage logic
    raise NotImplementedError("Implement store_embeddings() - See hints above!")


def search(
    query_embedding: List[float],
    top_k: int = 5,
    client: Optional[QdrantClient] = None
) -> List[Dict]:
    """
    Search for similar documents using a query embedding.

    TODO: Implement this function!

    Args:
        query_embedding: The embedding vector of the query
        top_k: Number of results to return (default: 5)
        client: Optional Qdrant client

    Returns:
        List of result dicts with 'content', 'metadata', and 'score' keys

    Example:
        >>> query_emb = [0.1] * 1536
        >>> results = search(query_emb, top_k=3)
        >>> len(results) <= 3
        True
        >>> 'content' in results[0] and 'score' in results[0]
        True

    Hints:
        - Use get_client() if client is None
        - Call client.search(collection_name=COLLECTION_NAME, query_vector=..., limit=...)
        - Each result has .payload (dict) and .score (float)
        - Extract content and metadata from payload
    """
    # TODO: Your implementation here
    # Remove the line below and implement the search logic
    raise NotImplementedError("Implement search() - See hints above!")


def search_with_text(query: str, top_k: int = 5) -> List[Dict]:
    """
    Search using a text query (generates embedding automatically).

    Args:
        query: Text query string
        top_k: Number of results

    Returns:
        List of search results
    """
    from embeddings import generate_embeddings

    query_embedding = generate_embeddings([query])[0]
    return search(query_embedding, top_k)


if __name__ == "__main__":
    # Test connection to Qdrant
    print(f"Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}...")

    try:
        client = get_client()
        collections = client.get_collections()
        print(f"Connected! Collections: {[c.name for c in collections.collections]}")

        # Initialize collection
        initialize_collection(client)
        print("Collection initialized successfully!")

    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        print("\nMake sure Qdrant is running:")
        print("  docker-compose up -d")
