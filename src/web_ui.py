"""
TechFlow Support Bot - Web Interface
====================================
A Gradio-based web UI for the RAG customer support bot.

Run with: python web_ui.py
Then open: http://localhost:7860
"""

import gradio as gr
import sys
from pathlib import Path

# Add src directory to path if needed
sys.path.insert(0, str(Path(__file__).parent))

from qa_chain import answer_question
from retriever import get_client, COLLECTION_NAME


def check_system_ready() -> bool:
    """Check if the RAG system is ready (documents ingested)."""
    try:
        client = get_client()
        collection_info = client.get_collection(COLLECTION_NAME)
        return collection_info.points_count > 0
    except Exception:
        return False


def ask_question(question: str, history: list) -> tuple:
    """
    Process a question and return the answer with sources.

    Args:
        question: User's question
        history: Chat history (not used but required by Gradio)

    Returns:
        Tuple of (history, sources_text)
    """
    if not question.strip():
        return history, ""

    try:
        # Get answer from RAG system
        result = answer_question(question, top_k=5)

        answer = result["answer"]
        sources = result.get("sources", [])

        # Format sources
        if sources:
            sources_text = "**Sources:** " + ", ".join(sources)
        else:
            sources_text = ""

        # Add to history
        history.append((question, answer))

        return history, sources_text

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        history.append((question, error_msg))
        return history, ""


def create_demo():
    """Create the Gradio interface."""

    # Check if system is ready
    system_ready = check_system_ready()

    with gr.Blocks(title="TechFlow Support Bot") as demo:

        # Header
        gr.Markdown("""
        # TechFlow Support Bot

        Ask any question about TechFlow - our AI will search the documentation and answer!

        **Try these questions:**
        - How do I reset my password?
        - What's included in the Pro plan?
        - How do I create a task via the API?
        - Does TechFlow have a mobile app?
        """)

        # Status indicator
        if not system_ready:
            gr.Markdown("""
            > **Setup Required:** The document database is empty. Run the ingestion script first:
            > ```
            > python -c "from ingest import process_documents; from embeddings import embed_chunks; from retriever import store_embeddings, initialize_collection, get_client; client = get_client(); initialize_collection(client, recreate=True); chunks = process_documents('../data/sample_docs'); chunks = embed_chunks(chunks); store_embeddings(chunks)"
            > ```
            """)

        # Chat interface
        chatbot = gr.Chatbot(
            label="Chat",
            height=400,
            show_label=False,
            avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=techflow"),
        )

        # Sources display
        sources_display = gr.Markdown(label="Sources")

        # Input row
        with gr.Row():
            question_input = gr.Textbox(
                placeholder="Ask a question about TechFlow...",
                label="Your Question",
                show_label=False,
                scale=4,
                container=False,
            )
            submit_btn = gr.Button("Ask", variant="primary", scale=1)

        # Example questions
        gr.Examples(
            examples=[
                "How do I reset my password?",
                "What's included in the Pro plan?",
                "My account is locked, what do I do?",
                "How do I create a task via the API?",
                "What's the rate limit for API requests?",
                "Does TechFlow have a mobile app?",
                "How do I set up Slack integration?",
                "What file types can I upload?",
            ],
            inputs=question_input,
            label="Example Questions",
        )

        # Clear button
        clear_btn = gr.Button("Clear Chat", variant="secondary")

        # Event handlers
        submit_btn.click(
            fn=ask_question,
            inputs=[question_input, chatbot],
            outputs=[chatbot, sources_display],
        ).then(
            fn=lambda: "",
            outputs=question_input,
        )

        question_input.submit(
            fn=ask_question,
            inputs=[question_input, chatbot],
            outputs=[chatbot, sources_display],
        ).then(
            fn=lambda: "",
            outputs=question_input,
        )

        clear_btn.click(
            fn=lambda: ([], ""),
            outputs=[chatbot, sources_display],
        )

        # Footer
        gr.Markdown("""
        ---
        *Built with RAG (Retrieval-Augmented Generation) |
        [View Challenge](https://github.com/techlearn-center/rag-document-qa)*
        """)

    return demo


if __name__ == "__main__":
    import os

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n" + "=" * 60)
        print("ERROR: OPENAI_API_KEY environment variable not set!")
        print("=" * 60)
        print("\nSet it with:")
        print("  Windows PowerShell: $env:OPENAI_API_KEY='your-key'")
        print("  Mac/Linux: export OPENAI_API_KEY='your-key'")
        print()
        exit(1)

    print("\n" + "=" * 60)
    print("  TechFlow Support Bot - Web Interface")
    print("=" * 60)
    print("\nStarting server...")
    print("Open your browser to: http://localhost:7861")
    print("\nPress Ctrl+C to stop.\n")

    demo = create_demo()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True,
        theme=gr.themes.Soft(primary_hue="blue"),
    )
