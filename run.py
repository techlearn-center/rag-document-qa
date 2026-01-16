#!/usr/bin/env python3
"""
RAG Challenge Runner
====================
Run this script to see your progress and test your implementation.

Usage:
    python run.py          # Check progress on all steps
    python run.py --step 3 # Test only step 3 (chunking)
    python run.py --demo   # Run the full Q&A demo
"""

import subprocess
import sys
import os
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

# For Windows compatibility
if sys.platform == 'win32':
    os.system('color')  # Enable ANSI colors on Windows
    # Fix Unicode encoding on Windows
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

STEPS = [
    {
        "number": 1,
        "name": "Environment Setup",
        "description": "Docker + Dependencies",
        "test": None,  # Manual check
        "check_func": "check_environment"
    },
    {
        "number": 2,
        "name": "Understanding RAG",
        "description": "Read the concepts",
        "test": None,  # No test, just reading
        "check_func": None
    },
    {
        "number": 3,
        "name": "Document Chunking",
        "description": "Implement chunk_document()",
        "test": "tests/test_chunking.py",
        "file": "src/ingest.py",
        "function": "chunk_document"
    },
    {
        "number": 4,
        "name": "Generate Embeddings",
        "description": "Implement generate_embeddings()",
        "test": "tests/test_embeddings.py",
        "file": "src/embeddings.py",
        "function": "generate_embeddings"
    },
    {
        "number": 5,
        "name": "Store Vectors",
        "description": "Implement store_embeddings()",
        "test": "tests/test_retriever.py::TestStoreEmbeddings",
        "file": "src/retriever.py",
        "function": "store_embeddings"
    },
    {
        "number": 6,
        "name": "Vector Search",
        "description": "Implement search()",
        "test": "tests/test_retriever.py::TestSearch",
        "file": "src/retriever.py",
        "function": "search"
    },
    {
        "number": 7,
        "name": "Q&A Chain",
        "description": "Implement answer_question()",
        "test": "tests/test_qa.py",
        "file": "src/qa_chain.py",
        "function": "answer_question"
    },
]


def print_header():
    """Print the challenge header."""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  🎯 RAG Document Q&A Challenge{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")


def print_step_status(step, status, message=""):
    """Print a step's status with color."""
    icons = {
        "pass": f"{Colors.GREEN}✅{Colors.END}",
        "fail": f"{Colors.RED}❌{Colors.END}",
        "skip": f"{Colors.YELLOW}⏭️{Colors.END}",
        "pending": f"{Colors.YELLOW}⏳{Colors.END}",
    }
    icon = icons.get(status, "❓")

    step_num = f"[Step {step['number']}]"
    print(f"  {icon} {Colors.BOLD}{step_num}{Colors.END} {step['name']}: {step['description']}")
    if message:
        print(f"      {Colors.YELLOW}→ {message}{Colors.END}")


def check_environment():
    """Check if Docker and Qdrant are running."""
    # Check Docker
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            return False, "Docker not found"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, "Docker not installed or not in PATH"

    # Check Qdrant container
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=rag-qdrant", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "rag-qdrant" not in result.stdout:
            return False, "Qdrant not running. Run: docker-compose up -d"
    except:
        return False, "Could not check Docker containers"

    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        return False, "OPENAI_API_KEY not set"

    return True, "Environment ready!"


def check_function_implemented(file_path, function_name):
    """Check if a function has been implemented (not just raising NotImplementedError)."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Look for the function and check if it still raises NotImplementedError
        # This is a simple heuristic
        import re
        pattern = rf'def {function_name}\([^)]*\).*?(?=\ndef |\Z)'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            func_body = match.group(0)
            if 'raise NotImplementedError' in func_body:
                return False, "Not implemented yet"

        return True, "Implemented"
    except FileNotFoundError:
        return False, f"File not found: {file_path}"


def run_tests(test_path):
    """Run pytest for a specific test file/class."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short", "-q"],
            capture_output=True,
            text=True,
            timeout=120
        )

        # Parse output for pass/fail count
        output = result.stdout + result.stderr

        if result.returncode == 0:
            return True, "All tests passed!"
        else:
            # Try to extract failure count
            import re
            match = re.search(r'(\d+) passed', output)
            passed = int(match.group(1)) if match else 0
            match = re.search(r'(\d+) failed', output)
            failed = int(match.group(1)) if match else 0

            if failed > 0:
                return False, f"{passed} passed, {failed} failed"
            else:
                return False, "Tests failed (check output below)"

    except subprocess.TimeoutExpired:
        return False, "Tests timed out"
    except Exception as e:
        return False, f"Error running tests: {e}"


def check_all_steps():
    """Check progress on all steps."""
    print_header()
    print(f"  {Colors.BOLD}Checking your progress...{Colors.END}\n")

    results = []
    completed = 0
    total_testable = 0

    for step in STEPS:
        if step.get("check_func") == "check_environment":
            success, message = check_environment()
            status = "pass" if success else "fail"
            results.append((step, status, message))
            if success:
                completed += 1
            total_testable += 1

        elif step.get("test") is None:
            # No automated test (reading step)
            results.append((step, "skip", "Manual step"))

        else:
            # First check if function is implemented
            file_path = step.get("file", "")
            func_name = step.get("function", "")

            if file_path and func_name:
                impl_check, impl_msg = check_function_implemented(file_path, func_name)
                if not impl_check:
                    results.append((step, "pending", impl_msg))
                    total_testable += 1
                    continue

            # Run the tests
            success, message = run_tests(step["test"])
            status = "pass" if success else "fail"
            results.append((step, status, message))

            if success:
                completed += 1
            total_testable += 1

    # Print results
    print(f"  {Colors.BOLD}Progress:{Colors.END}\n")
    for step, status, message in results:
        print_step_status(step, status, message if status != "pass" else "")

    # Print progress bar
    print(f"\n  {Colors.BOLD}Overall Progress:{Colors.END}")
    progress_pct = int((completed / total_testable) * 100) if total_testable > 0 else 0
    bar_filled = int(progress_pct / 5)  # 20 chars total
    bar_empty = 20 - bar_filled

    bar_color = Colors.GREEN if progress_pct == 100 else Colors.YELLOW
    print(f"  {bar_color}{'█' * bar_filled}{'░' * bar_empty}{Colors.END} {progress_pct}% ({completed}/{total_testable} steps)")

    if progress_pct == 100:
        print(f"\n  {Colors.GREEN}{Colors.BOLD}🎉 CHALLENGE COMPLETE! You built a RAG system!{Colors.END}")
        print(f"  {Colors.CYAN}Run 'python run.py --demo' to try it out!{Colors.END}")
    else:
        # Find next step to work on
        for step, status, _ in results:
            if status in ["pending", "fail"]:
                print(f"\n  {Colors.CYAN}Next step: {step['name']}{Colors.END}")
                if step.get("file"):
                    print(f"  {Colors.CYAN}Edit: {step['file']}{Colors.END}")
                break

    print()
    return completed == total_testable


def run_demo():
    """Run the full Q&A demo."""
    print_header()
    print(f"  {Colors.BOLD}Running Q&A Demo...{Colors.END}\n")

    # Check environment first
    success, message = check_environment()
    if not success:
        print(f"  {Colors.RED}❌ {message}{Colors.END}")
        print(f"  {Colors.YELLOW}Please complete the setup first.{Colors.END}\n")
        return

    # Check if all steps are complete
    print(f"  {Colors.CYAN}Checking if RAG system is ready...{Colors.END}")

    try:
        # Try importing and running
        sys.path.insert(0, str(Path(__file__).parent / "src"))

        from ingest import process_documents
        from embeddings import embed_chunks
        from retriever import store_embeddings, initialize_collection, get_client, search
        from qa_chain import answer_question

        # Initialize
        print(f"  {Colors.CYAN}Initializing database...{Colors.END}")
        client = get_client()
        initialize_collection(client, recreate=True)

        # Process documents
        print(f"  {Colors.CYAN}Loading documents...{Colors.END}")
        chunks = process_documents(str(Path(__file__).parent / "data" / "sample_docs"))
        print(f"  {Colors.GREEN}✓ Created {len(chunks)} chunks{Colors.END}")

        # Generate embeddings
        print(f"  {Colors.CYAN}Generating embeddings (this may take a moment)...{Colors.END}")
        chunks = embed_chunks(chunks)
        print(f"  {Colors.GREEN}✓ Embeddings generated{Colors.END}")

        # Store
        print(f"  {Colors.CYAN}Storing in vector database...{Colors.END}")
        count = store_embeddings(chunks)
        print(f"  {Colors.GREEN}✓ Stored {count} vectors{Colors.END}")

        print(f"\n  {Colors.GREEN}{Colors.BOLD}🚀 RAG System Ready!{Colors.END}\n")
        print(f"  {Colors.CYAN}{'─'*50}{Colors.END}")
        print(f"  {Colors.BOLD}Ask questions about the documents.{Colors.END}")
        print(f"  {Colors.BOLD}Type 'quit' to exit.{Colors.END}")
        print(f"  {Colors.CYAN}{'─'*50}{Colors.END}\n")

        # Interactive Q&A
        while True:
            try:
                question = input(f"  {Colors.BOLD}Your question:{Colors.END} ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if question.lower() in ['quit', 'exit', 'q', '']:
                break

            print(f"\n  {Colors.CYAN}Searching and generating answer...{Colors.END}\n")

            try:
                result = answer_question(question)

                print(f"  {Colors.GREEN}{Colors.BOLD}Answer:{Colors.END}")
                # Wrap answer text
                answer_lines = result['answer'].split('\n')
                for line in answer_lines:
                    print(f"  {line}")

                if result.get('sources'):
                    print(f"\n  {Colors.YELLOW}Sources: {', '.join(result['sources'])}{Colors.END}")

                print()

            except Exception as e:
                print(f"  {Colors.RED}Error: {e}{Colors.END}\n")

        print(f"\n  {Colors.CYAN}Thanks for trying the RAG Q&A system!{Colors.END}\n")

    except NotImplementedError as e:
        print(f"\n  {Colors.RED}❌ Some functions are not implemented yet.{Colors.END}")
        print(f"  {Colors.YELLOW}Complete all steps first, then run the demo.{Colors.END}")
        print(f"  {Colors.YELLOW}Run 'python run.py' to check your progress.{Colors.END}\n")

    except Exception as e:
        print(f"\n  {Colors.RED}❌ Error: {e}{Colors.END}")
        print(f"  {Colors.YELLOW}Make sure all steps are complete and tests pass.{Colors.END}\n")


def run_single_step(step_num):
    """Run tests for a single step."""
    print_header()

    step = None
    for s in STEPS:
        if s["number"] == step_num:
            step = s
            break

    if not step:
        print(f"  {Colors.RED}❌ Invalid step number: {step_num}{Colors.END}")
        print(f"  {Colors.YELLOW}Valid steps: 1-7{Colors.END}\n")
        return

    print(f"  {Colors.BOLD}Testing Step {step_num}: {step['name']}{Colors.END}\n")

    if step.get("check_func") == "check_environment":
        success, message = check_environment()
        if success:
            print(f"  {Colors.GREEN}✅ {message}{Colors.END}\n")
        else:
            print(f"  {Colors.RED}❌ {message}{Colors.END}\n")
        return

    if step.get("test") is None:
        print(f"  {Colors.YELLOW}This is a manual step (no automated tests).{Colors.END}\n")
        return

    # Run pytest with full output
    print(f"  {Colors.CYAN}Running: pytest {step['test']} -v{Colors.END}\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", step["test"], "-v", "--tb=short"],
        cwd=str(Path(__file__).parent)
    )

    print()
    if result.returncode == 0:
        print(f"  {Colors.GREEN}✅ Step {step_num} COMPLETE!{Colors.END}")
        if step_num < 7:
            next_step = STEPS[step_num]  # step_num is 1-indexed, list is 0-indexed
            print(f"  {Colors.CYAN}Next: Step {next_step['number']} - {next_step['name']}{Colors.END}")
    else:
        print(f"  {Colors.RED}❌ Some tests failed. Check the output above.{Colors.END}")
        print(f"  {Colors.YELLOW}Hint: Look at the 'Common Mistakes' section in README.md{Colors.END}")
    print()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="RAG Challenge Runner")
    parser.add_argument("--step", type=int, help="Run tests for a specific step (1-7)")
    parser.add_argument("--demo", action="store_true", help="Run the full Q&A demo")

    args = parser.parse_args()

    os.chdir(Path(__file__).parent)

    if args.demo:
        run_demo()
    elif args.step:
        run_single_step(args.step)
    else:
        check_all_steps()


if __name__ == "__main__":
    main()
