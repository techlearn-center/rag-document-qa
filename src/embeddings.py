"""
Embeddings Module
=================
This module generates vector embeddings for text chunks.

Your Task (Step 4):
- Implement the `generate_embeddings()` function
- Use OpenAI's embedding API (text-embedding-3-small)
- Handle batching for efficiency
"""

import os
from typing import List, Dict, Optional
from openai import OpenAI


# Initialize OpenAI client - requires OPENAI_API_KEY environment variable
client: Optional[OpenAI] = None


def get_client() -> OpenAI:
    """Get or create OpenAI client."""
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set.\n"
                "Get your API key from: https://platform.openai.com/api-keys\n"
                "Then run: export OPENAI_API_KEY='your-key-here'"
            )
        client = OpenAI(api_key=api_key)
    return client


def generate_embeddings(
    texts: List[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 100
) -> List[List[float]]:
    """
    Generate embeddings for a list of text strings.

    TODO: Implement this function!

    Args:
        texts: List of text strings to embed
        model: OpenAI embedding model to use (default: text-embedding-3-small)
        batch_size: Number of texts to embed in each API call (default: 100)

    Returns:
        List of embedding vectors (each is a list of floats)

    Example:
        >>> embeddings = generate_embeddings(["Hello world", "Test text"])
        >>> len(embeddings) == 2
        True
        >>> len(embeddings[0]) == 1536  # text-embedding-3-small dimension
        True

    Hints:
        - Use get_client() to get the OpenAI client
        - Call client.embeddings.create(input=batch, model=model)
        - Process in batches to handle large lists efficiently
        - The response has .data attribute, each item has .embedding
    """
    if not texts:
        return []

    client = get_client()
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(input=batch, model=model)
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)

    return all_embeddings


def embed_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Add embeddings to chunk dictionaries.

    Args:
        chunks: List of chunk dicts with 'content' key

    Returns:
        Same chunks with 'embedding' key added
    """
    texts = [chunk["content"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    return chunks


if __name__ == "__main__":
    # Test embedding generation
    print("Testing embedding generation...")

    test_texts = [
        "What is machine learning?",
        "How do neural networks work?",
        "Explain deep learning concepts."
    ]

    try:
        embeddings = generate_embeddings(test_texts)
        print(f"Generated {len(embeddings)} embeddings")
        print(f"Embedding dimension: {len(embeddings[0])}")
        print("Embedding generation working!")
    except NotImplementedError as e:
        print(f"Not implemented yet: {e}")
    except Exception as e:
        print(f"Error: {e}")
