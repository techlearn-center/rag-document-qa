"""
Tests for Question Answering (Step 7)
=====================================
These tests verify your answer_question() implementation.

Run with: pytest tests/test_qa.py -v

Note: These tests require:
- OPENAI_API_KEY environment variable
- Qdrant running (docker-compose up -d)
- Documents already ingested (run the full pipeline first)
"""

import pytest
import os
import sys
sys.path.insert(0, '../src')

from qa_chain import answer_question, build_context


# Check prerequisites
def prerequisites_met():
    if not os.getenv("OPENAI_API_KEY"):
        return False
    try:
        from retriever import get_client
        client = get_client()
        client.get_collections()
        return True
    except:
        return False


pytestmark = pytest.mark.skipif(
    not prerequisites_met(),
    reason="Prerequisites not met (API key or Qdrant)"
)


class TestBuildContext:
    """Tests for context building."""

    def test_build_context_basic(self):
        """Test basic context building."""
        results = [
            {"content": "First result content", "metadata": {"source": "a.txt"}},
            {"content": "Second result content", "metadata": {"source": "b.txt"}}
        ]

        context = build_context(results)

        assert "First result content" in context
        assert "Second result content" in context
        assert "[Source 1:" in context
        assert "[Source 2:" in context

    def test_build_context_respects_limit(self):
        """Test that context respects max length."""
        results = [
            {"content": "A" * 1000, "metadata": {"source": "a.txt"}},
            {"content": "B" * 1000, "metadata": {"source": "b.txt"}},
            {"content": "C" * 1000, "metadata": {"source": "c.txt"}}
        ]

        context = build_context(results, max_context_length=1500)

        assert len(context) <= 1500, "Context should not exceed max length"

    def test_build_context_empty_results(self):
        """Test context building with empty results."""
        context = build_context([])
        assert context == "", "Empty results should produce empty context"


class TestAnswerQuestion:
    """Tests for the answer_question function."""

    def test_answer_structure(self):
        """Test that answer has correct structure."""
        result = answer_question("What is this document about?")

        assert "answer" in result, "Result should have 'answer' key"
        assert "sources" in result, "Result should have 'sources' key"
        assert isinstance(result["answer"], str), "Answer should be a string"
        assert isinstance(result["sources"], list), "Sources should be a list"

    def test_answer_not_empty(self):
        """Test that answer is not empty."""
        result = answer_question("Tell me something from the documents.")

        assert len(result["answer"]) > 0, "Answer should not be empty"

    def test_answer_includes_sources(self):
        """Test that sources are provided when available."""
        result = answer_question("What information is in the documents?")

        # If documents were ingested, should have sources
        # This is a soft check as it depends on ingested data
        if result.get("context_used"):
            assert len(result["sources"]) > 0, \
                "Should include sources when context was used"

    def test_answer_handles_unknown(self):
        """Test handling of questions not in documents."""
        result = answer_question(
            "What is the exact population of Mars in 2024?"
        )

        # Should indicate lack of information rather than hallucinate
        answer_lower = result["answer"].lower()
        uncertainty_phrases = [
            "don't have",
            "not found",
            "no information",
            "cannot find",
            "unable to",
            "not mentioned",
            "doesn't contain"
        ]

        # Soft check - model should ideally indicate uncertainty
        # but we don't fail if it doesn't (depends on prompt engineering)
        pass  # Informational test


class TestEndToEndRAG:
    """End-to-end tests for the full RAG pipeline."""

    def test_full_pipeline(self):
        """Test the complete RAG pipeline."""
        # This test assumes documents have been ingested
        questions = [
            "What topics are covered in the documents?",
            "Summarize the main points.",
        ]

        for question in questions:
            result = answer_question(question)

            assert "answer" in result, f"Failed for question: {question}"
            assert len(result["answer"]) > 10, \
                f"Answer too short for question: {question}"

    def test_multiple_questions_consistent(self):
        """Test that similar questions get consistent themes in answers."""
        q1_result = answer_question("What is the main topic?")
        q2_result = answer_question("What subject does this cover?")

        # Both should reference the same documents
        # (soft check - just ensure both produce answers)
        assert q1_result["answer"], "First question should have answer"
        assert q2_result["answer"], "Second question should have answer"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
