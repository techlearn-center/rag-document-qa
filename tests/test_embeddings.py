"""
Tests for Embeddings (Step 4)
=============================
These tests verify your generate_embeddings() implementation.

Run with: pytest tests/test_embeddings.py -v

Note: These tests require a valid OPENAI_API_KEY environment variable.
"""

import pytest
import os
import sys
sys.path.insert(0, '../src')

from embeddings import generate_embeddings, embed_chunks


# Skip all tests if no API key
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set"
)


class TestGenerateEmbeddings:
    """Tests for the generate_embeddings function."""

    def test_single_text(self):
        """Test embedding a single text."""
        texts = ["Hello, world!"]
        embeddings = generate_embeddings(texts)

        assert len(embeddings) == 1, "Should return one embedding"
        assert len(embeddings[0]) == 1536, "text-embedding-3-small has 1536 dimensions"

    def test_multiple_texts(self):
        """Test embedding multiple texts."""
        texts = [
            "What is machine learning?",
            "How do neural networks work?",
            "Explain deep learning."
        ]
        embeddings = generate_embeddings(texts)

        assert len(embeddings) == 3, "Should return three embeddings"
        assert all(len(e) == 1536 for e in embeddings), "All embeddings should be 1536-dim"

    def test_empty_list(self):
        """Test handling of empty input list."""
        embeddings = generate_embeddings([])

        assert embeddings == [], "Empty input should return empty list"

    def test_embeddings_are_floats(self):
        """Test that embeddings contain float values."""
        embeddings = generate_embeddings(["Test text"])

        assert all(isinstance(v, float) for v in embeddings[0]), \
            "Embedding values should be floats"

    def test_similar_texts_similar_embeddings(self):
        """Test that similar texts have similar embeddings."""
        texts = [
            "The cat sat on the mat.",
            "The cat was sitting on the mat.",
            "Quantum physics explains particle behavior."
        ]
        embeddings = generate_embeddings(texts)

        # Calculate cosine similarity
        def cosine_sim(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(x * x for x in b) ** 0.5
            return dot / (norm_a * norm_b)

        sim_similar = cosine_sim(embeddings[0], embeddings[1])
        sim_different = cosine_sim(embeddings[0], embeddings[2])

        assert sim_similar > sim_different, \
            "Similar texts should have higher cosine similarity"

    def test_batching_large_input(self):
        """Test that large inputs are handled (batched properly)."""
        texts = [f"Text number {i}" for i in range(150)]  # More than typical batch size
        embeddings = generate_embeddings(texts, batch_size=50)

        assert len(embeddings) == 150, "Should return all 150 embeddings"


class TestEmbedChunks:
    """Tests for the embed_chunks helper function."""

    def test_embed_chunks_adds_embeddings(self):
        """Test that embed_chunks adds embedding key to chunks."""
        chunks = [
            {"content": "First chunk", "metadata": {"source": "test.txt"}},
            {"content": "Second chunk", "metadata": {"source": "test.txt"}}
        ]

        result = embed_chunks(chunks)

        assert len(result) == 2, "Should return same number of chunks"
        assert all("embedding" in c for c in result), "Each chunk should have embedding"
        assert all(len(c["embedding"]) == 1536 for c in result), "Embeddings should be 1536-dim"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
