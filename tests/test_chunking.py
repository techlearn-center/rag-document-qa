"""
Tests for Document Chunking (Step 3)
====================================
These tests verify your chunk_document() implementation.

Run with: pytest tests/test_chunking.py -v
"""

import pytest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ingest import chunk_document, load_documents, process_documents

# Get the path to sample_docs relative to test file
SAMPLE_DOCS_PATH = str(Path(__file__).parent.parent / 'data' / 'sample_docs')


class TestChunkDocument:
    """Tests for the chunk_document function."""

    def test_basic_chunking(self):
        """Test basic chunking with default parameters."""
        text = "A" * 1000  # 1000 character string
        chunks = chunk_document(text, chunk_size=500, overlap=100)

        assert len(chunks) >= 2, "Should create multiple chunks for long text"
        assert all(len(c) <= 500 for c in chunks), "No chunk should exceed chunk_size"

    def test_overlap_exists(self):
        """Test that chunks have proper overlap."""
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 50  # Long enough for multiple chunks
        chunks = chunk_document(text, chunk_size=100, overlap=20)

        if len(chunks) >= 2:
            # Check that end of chunk N appears at start of chunk N+1
            for i in range(len(chunks) - 1):
                end_of_current = chunks[i][-20:] if len(chunks[i]) >= 20 else chunks[i]
                assert end_of_current in chunks[i + 1], \
                    f"Chunk {i+1} should overlap with chunk {i}"

    def test_short_content(self):
        """Test handling of content shorter than chunk_size."""
        text = "Short text"
        chunks = chunk_document(text, chunk_size=500, overlap=100)

        assert len(chunks) == 1, "Short content should produce single chunk"
        assert chunks[0] == text, "Short content chunk should match original"

    def test_empty_content(self):
        """Test handling of empty content."""
        chunks = chunk_document("", chunk_size=500, overlap=100)

        assert len(chunks) == 0 or chunks == [""], \
            "Empty content should produce empty list or single empty string"

    def test_exact_chunk_size(self):
        """Test content exactly equal to chunk_size."""
        text = "X" * 500
        chunks = chunk_document(text, chunk_size=500, overlap=100)

        assert len(chunks) == 1, "Content equal to chunk_size should be single chunk"

    def test_no_content_loss(self):
        """Test that all original content is preserved in chunks."""
        text = "The quick brown fox jumps over the lazy dog. " * 50
        chunks = chunk_document(text, chunk_size=100, overlap=20)

        # Reconstruct (approximately) by taking non-overlapping parts
        # This is a softer check - we mainly want no data loss
        all_chars = set(text)
        chunk_chars = set("".join(chunks))

        assert all_chars == chunk_chars, "All characters should be preserved"

    def test_chunk_count_reasonable(self):
        """Test that chunk count is reasonable for given parameters."""
        text = "A" * 1000
        chunks = chunk_document(text, chunk_size=200, overlap=50)

        # With 200 char chunks and 50 overlap, step size is 150
        # For 1000 chars: ceil(1000/150) ≈ 7 chunks expected
        assert 5 <= len(chunks) <= 10, \
            f"Expected 5-10 chunks, got {len(chunks)}"


class TestLoadDocuments:
    """Tests for document loading."""

    def test_load_sample_docs(self):
        """Test loading sample documents."""
        docs = load_documents(SAMPLE_DOCS_PATH)

        assert len(docs) > 0, "Should load at least one document"
        assert all("content" in d for d in docs), "Each doc should have content"
        assert all("metadata" in d for d in docs), "Each doc should have metadata"


class TestProcessDocuments:
    """Tests for full document processing pipeline."""

    def test_process_creates_chunks(self):
        """Test that process_documents creates chunks with metadata."""
        chunks = process_documents(SAMPLE_DOCS_PATH, chunk_size=200, overlap=50)

        assert len(chunks) > 0, "Should create chunks"
        for chunk in chunks:
            assert "content" in chunk, "Each chunk should have content"
            assert "metadata" in chunk, "Each chunk should have metadata"
            assert "source" in chunk["metadata"], "Metadata should include source"
            assert "chunk_index" in chunk["metadata"], "Metadata should include chunk_index"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
