"""
Tests for Vector Retriever (Steps 5 & 6)
========================================
These tests verify your store_embeddings() and search() implementations.

Run with: pytest tests/test_retriever.py -v

Note: These tests require Qdrant to be running (docker-compose up -d)
"""

import pytest
import os
import sys
sys.path.insert(0, '../src')

from retriever import (
    get_client, initialize_collection, store_embeddings, search,
    COLLECTION_NAME, VECTOR_SIZE
)


# Check if Qdrant is available
def qdrant_available():
    try:
        client = get_client()
        client.get_collections()
        return True
    except:
        return False


pytestmark = pytest.mark.skipif(
    not qdrant_available(),
    reason="Qdrant not available - run 'docker-compose up -d'"
)


class TestQdrantConnection:
    """Tests for Qdrant connection."""

    def test_connection(self):
        """Test that we can connect to Qdrant."""
        client = get_client()
        collections = client.get_collections()
        assert collections is not None, "Should get collections response"

    def test_initialize_collection(self):
        """Test collection initialization."""
        client = get_client()
        initialize_collection(client, recreate=True)

        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]

        assert COLLECTION_NAME in collection_names, \
            f"Collection '{COLLECTION_NAME}' should exist"


class TestStoreEmbeddings:
    """Tests for the store_embeddings function."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset collection before each test."""
        client = get_client()
        initialize_collection(client, recreate=True)

    def test_store_single_chunk(self):
        """Test storing a single chunk."""
        chunks = [{
            "content": "This is test content.",
            "embedding": [0.1] * VECTOR_SIZE,
            "metadata": {"source": "test.txt", "chunk_index": 0}
        }]

        count = store_embeddings(chunks)
        assert count == 1, "Should store 1 point"

    def test_store_multiple_chunks(self):
        """Test storing multiple chunks."""
        chunks = [
            {
                "content": f"Content {i}",
                "embedding": [0.1 * (i + 1)] * VECTOR_SIZE,
                "metadata": {"source": "test.txt", "chunk_index": i}
            }
            for i in range(5)
        ]

        count = store_embeddings(chunks)
        assert count == 5, "Should store 5 points"

    def test_store_empty_list(self):
        """Test storing empty list."""
        count = store_embeddings([])
        assert count == 0, "Should store 0 points for empty input"


class TestSearch:
    """Tests for the search function."""

    @pytest.fixture(autouse=True)
    def setup_data(self):
        """Set up test data before each test."""
        client = get_client()
        initialize_collection(client, recreate=True)

        # Store test documents with different topics
        chunks = [
            {
                "content": "Machine learning is a subset of artificial intelligence.",
                "embedding": [0.9, 0.1, 0.0] + [0.0] * (VECTOR_SIZE - 3),
                "metadata": {"source": "ml.txt", "chunk_index": 0}
            },
            {
                "content": "Deep learning uses neural networks with many layers.",
                "embedding": [0.8, 0.2, 0.0] + [0.0] * (VECTOR_SIZE - 3),
                "metadata": {"source": "dl.txt", "chunk_index": 0}
            },
            {
                "content": "Cooking pasta requires boiling water and salt.",
                "embedding": [0.0, 0.0, 0.9] + [0.0] * (VECTOR_SIZE - 3),
                "metadata": {"source": "cooking.txt", "chunk_index": 0}
            }
        ]
        store_embeddings(chunks)

    def test_search_returns_results(self):
        """Test that search returns results."""
        query_embedding = [0.85, 0.15, 0.0] + [0.0] * (VECTOR_SIZE - 3)
        results = search(query_embedding, top_k=2)

        assert len(results) == 2, "Should return 2 results"

    def test_search_result_structure(self):
        """Test that search results have correct structure."""
        query_embedding = [0.85, 0.15, 0.0] + [0.0] * (VECTOR_SIZE - 3)
        results = search(query_embedding, top_k=1)

        assert len(results) >= 1, "Should have at least 1 result"
        result = results[0]

        assert "content" in result, "Result should have content"
        assert "metadata" in result, "Result should have metadata"
        assert "score" in result, "Result should have score"

    def test_search_relevance(self):
        """Test that search returns relevant results first."""
        # Query similar to ML content
        query_embedding = [0.85, 0.15, 0.0] + [0.0] * (VECTOR_SIZE - 3)
        results = search(query_embedding, top_k=3)

        # ML-related content should rank higher than cooking
        assert "machine learning" in results[0]["content"].lower() or \
               "deep learning" in results[0]["content"].lower(), \
               "ML content should be most relevant"

        # Cooking should be least relevant
        assert "cooking" in results[-1]["content"].lower() or \
               "pasta" in results[-1]["content"].lower(), \
               "Cooking content should be least relevant"

    def test_search_top_k_limit(self):
        """Test that search respects top_k limit."""
        query_embedding = [0.5] * VECTOR_SIZE
        results = search(query_embedding, top_k=1)

        assert len(results) == 1, "Should return only 1 result when top_k=1"

    def test_search_scores_ordered(self):
        """Test that results are ordered by score (descending)."""
        query_embedding = [0.5, 0.3, 0.2] + [0.0] * (VECTOR_SIZE - 3)
        results = search(query_embedding, top_k=3)

        scores = [r["score"] for r in results]
        assert scores == sorted(scores, reverse=True), \
            "Results should be ordered by score descending"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
