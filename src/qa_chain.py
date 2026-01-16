"""
Question Answering Chain Module
===============================
This module connects retrieval with LLM generation for Q&A.

Your Task (Step 7):
- Implement `answer_question()` to create the full RAG pipeline
- Retrieve relevant context and generate answers with GPT
"""

import os
from typing import List, Dict, Optional
from openai import OpenAI

from retriever import search_with_text
from embeddings import get_client as get_openai_client


def build_context(results: List[Dict], max_context_length: int = 3000) -> str:
    """
    Build context string from search results.

    Args:
        results: List of search results with 'content' and 'metadata'
        max_context_length: Maximum total context length

    Returns:
        Formatted context string
    """
    context_parts = []
    total_length = 0

    for i, result in enumerate(results, 1):
        content = result["content"]
        source = result.get("metadata", {}).get("source", "Unknown")

        part = f"[Source {i}: {source}]\n{content}\n"

        if total_length + len(part) > max_context_length:
            break

        context_parts.append(part)
        total_length += len(part)

    return "\n".join(context_parts)


def answer_question(
    question: str,
    top_k: int = 5,
    model: str = "gpt-4o-mini",
    temperature: float = 0.3
) -> Dict:
    """
    Answer a question using RAG (Retrieval-Augmented Generation).

    TODO: Implement this function!

    Args:
        question: The user's question
        top_k: Number of documents to retrieve for context
        model: OpenAI model to use for generation
        temperature: Generation temperature (lower = more focused)

    Returns:
        Dict with 'answer', 'sources', and 'context_used' keys

    Example:
        >>> result = answer_question("What is machine learning?")
        >>> 'answer' in result
        True
        >>> 'sources' in result
        True

    Steps to implement:
        1. Use search_with_text(question, top_k) to retrieve relevant chunks
        2. Use build_context(results) to format the context
        3. Create a prompt that includes the context and question
        4. Call OpenAI API to generate the answer
        5. Return structured response

    Prompt template suggestion:
        "You are a helpful assistant. Answer the question based ONLY on the
         provided context. If the context doesn't contain the answer, say
         'I don't have enough information to answer this question.'

         Context:
         {context}

         Question: {question}

         Answer:"

    Hints:
        - Use get_openai_client() for the OpenAI client
        - Call client.chat.completions.create(model=model, messages=[...])
        - Extract answer from response.choices[0].message.content
        - Include sources in the response for transparency
    """
    # 1. Retrieve relevant chunks
    results = search_with_text(question, top_k)

    # 2. Build context
    context = build_context(results)

    # 3. Create prompt
    prompt = f"""You are a helpful assistant. Answer the question based ONLY on the provided context.
If the context doesn't contain the answer, say "I don't have enough information to answer this question."

Context:
{context}

Question: {question}

Answer:"""

    # 4. Call GPT
    client = get_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    answer = response.choices[0].message.content

    # 5. Return structured response
    sources = [r.get("metadata", {}).get("source", "Unknown") for r in results]

    return {
        "answer": answer,
        "sources": list(set(sources)),  # Unique sources
        "context_used": context
    }


def interactive_qa():
    """Run interactive Q&A session."""
    print("\n" + "=" * 50)
    print("RAG Document Q&A System")
    print("=" * 50)
    print("Ask questions about your documents.")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            print("\nSearching documents and generating answer...")
            result = answer_question(question)

            print(f"\nAnswer: {result['answer']}")

            if result.get('sources'):
                print(f"\nSources used:")
                for source in result['sources']:
                    print(f"  - {source}")

            print()

        except NotImplementedError as e:
            print(f"\nNot implemented yet: {e}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    interactive_qa()
