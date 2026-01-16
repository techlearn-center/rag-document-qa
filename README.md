# Build a RAG Document Q&A System

> **What you'll create:** A system that can answer questions about any documents you give it - like having a personal assistant who has read all your files.

---

## Quick Start (For DevOps Students)

If you're in a DevOps class, follow this workflow:

```bash
# 1. Fork this repo to your GitHub account (click "Fork" button)

# 2. Clone YOUR fork
git clone https://github.com/YOUR-USERNAME/rag-document-qa.git
cd rag-document-qa

# 3. Set up and code (see steps below)

# 4. Push your changes
git add .
git commit -m "Implement RAG challenge"
git push origin main

# 5. Check GitHub Actions tab - see your score!
```

**Important:** Add your OpenAI API key to GitHub Secrets (see [Setup GitHub Secrets](#setup-github-secrets) below).

---

## What is This Challenge?

Imagine you have 100 PDF documents and want to ask: *"What did the contract say about payment terms?"*

Instead of reading all 100 documents, a **RAG system** (Retrieval-Augmented Generation) finds the relevant parts and answers your question using AI.

**By the end of this challenge, you will have built this system yourself.**

---

## Do I Need to Know How to Code?

**You need basic Python knowledge:**
- ✅ You know what variables, functions, and loops are
- ✅ You can read Python code and understand what it does
- ✅ You've written simple Python scripts before

**You DON'T need to:**
- ❌ Be an expert programmer
- ❌ Know anything about AI/ML
- ❌ Have used Docker before
- ❌ Know what "embeddings" or "vectors" are (we'll teach you!)

---

## How Does This Challenge Work?

### Your Main Assignment

You will implement **4 functions** across 4 Python files. Each function is a building block of the RAG system:

| Step | File | Function | What It Does |
|------|------|----------|--------------|
| 3 | `ingest.py` | `chunk_document()` | Splits documents into small pieces |
| 4 | `embeddings.py` | `generate_embeddings()` | Converts text to numbers for search |
| 5-6 | `retriever.py` | `store_embeddings()` + `search()` | Saves and finds documents |
| 7 | `qa_chain.py` | `answer_question()` | Connects everything to answer questions |

### How You're Guided

Each function has:
1. **Clear instructions** - What the function should do
2. **Example inputs/outputs** - So you know what to expect
3. **Hints** - Specific tips if you're stuck
4. **Tests** - Run them to check if your code works

### Track Your Progress

Run this command anytime to see your progress:

```bash
python run.py
```

You'll see something like this:

```
  ============================================================
    🎯 RAG Document Q&A Challenge
  ============================================================

  Checking your progress...

  Progress:

  ✅ [Step 1] Environment Setup: Docker + Dependencies
  ⏭️  [Step 2] Understanding RAG: Read the concepts
  ✅ [Step 3] Document Chunking: Implement chunk_document()
  ⏳ [Step 4] Generate Embeddings: Implement generate_embeddings()
      → Not implemented yet
  ⏳ [Step 5] Store Vectors: Implement store_embeddings()
  ⏳ [Step 6] Vector Search: Implement search()
  ⏳ [Step 7] Q&A Chain: Implement answer_question()

  Overall Progress:
  ████████░░░░░░░░░░░░ 40% (2/5 steps)

  Next step: Generate Embeddings
  Edit: src/embeddings.py
```

### How Do I Know I'm Right?

After implementing each function:

```bash
# Test a specific step
python run.py --step 3   # Test chunking
python run.py --step 4   # Test embeddings
# ... etc

# Or run all tests
python run.py
```

When tests pass, you'll see ✅. When they fail, you'll see exactly what went wrong.

### What's the Final Result?

When all steps are complete:

```bash
python run.py --demo
```

This launches an **interactive Q&A session** where you can ask questions about the sample documents and see YOUR system answer them!

```
  🚀 RAG System Ready!

  ──────────────────────────────────────────────────
  Ask questions about the documents.
  Type 'quit' to exit.
  ──────────────────────────────────────────────────

  Your question: What is machine learning?

  Searching and generating answer...

  Answer:
  Machine learning is a subset of artificial intelligence (AI)
  that enables systems to learn and improve from experience
  without being explicitly programmed...

  Sources: machine_learning_basics.txt
```

### What If You're Stuck?

**Don't worry!** At each step, we provide:

- 🎯 **"Common Mistakes"** - Problems most beginners hit
- 💡 **"If you see this error..."** - Solutions to specific errors
- 🆘 **"Still stuck?"** - Expandable full solutions (it's OK to look!)

---

## Step 0: Install Everything You Need

> ⏱️ **Time:** 15-30 minutes (one-time setup)

### 0.1 Install Python

**Check if Python is installed:**
```bash
python --version
```

If you see `Python 3.9` or higher, skip to 0.2!

**If not installed:**

<details>
<summary>🪟 Windows</summary>

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.11 (click the big yellow button)
3. **IMPORTANT:** Check ✅ "Add Python to PATH" during installation
4. Click "Install Now"
5. Restart your terminal and verify: `python --version`

</details>

<details>
<summary>🍎 Mac</summary>

1. Open Terminal
2. Install Homebrew (if you don't have it):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python@3.11
   ```
4. Verify: `python3 --version`

**Note:** On Mac, use `python3` instead of `python`

</details>

<details>
<summary>🐧 Linux</summary>

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

Verify: `python3 --version`

</details>

---

### 0.2 Install UV (Modern Python Package Manager)

**UV** is a fast, modern tool for managing Python projects. It replaces `pip` and `venv`.

**Install UV:**

<details>
<summary>🪟 Windows (PowerShell)</summary>

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then restart your terminal.

</details>

<details>
<summary>🍎 Mac / 🐧 Linux</summary>

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal or run: `source $HOME/.local/bin/env`

</details>

**Verify UV is installed:**
```bash
uv --version
```

You should see something like `uv 0.4.x`

---

### 0.3 Install Docker

Docker runs the **vector database** (Qdrant) that stores your document embeddings.

**Think of Docker as:** A way to run pre-packaged software without installing it directly on your computer.

<details>
<summary>🪟 Windows</summary>

1. Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Download "Docker Desktop for Windows"
3. Run the installer
4. Restart your computer
5. Open Docker Desktop (it should start automatically)
6. Wait for "Docker is running" in the system tray

**Verify:**
```bash
docker --version
```

</details>

<details>
<summary>🍎 Mac</summary>

1. Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Download "Docker Desktop for Mac" (choose Apple Silicon or Intel based on your Mac)
3. Drag to Applications folder
4. Open Docker Desktop
5. Wait for "Docker is running"

**Verify:**
```bash
docker --version
```

</details>

<details>
<summary>🐧 Linux</summary>

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Allow running Docker without sudo
sudo usermod -aG docker $USER

# Log out and back in, then verify:
docker --version
```

</details>

---

### 0.4 Get an OpenAI API Key

You need an API key to use OpenAI's embedding and chat models.

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. **Save it somewhere safe** - you won't be able to see it again!

**Cost:** This challenge uses ~$0.10-0.50 of API credits. New accounts get $5 free.

---

## Step 1: Set Up This Project

> ⏱️ **Time:** 5 minutes

### 1.1 Open Terminal in This Folder

Navigate to the challenge folder:
```bash
cd path/to/challenges/rag-document-qa
```

### 1.2 Create a Virtual Environment with UV

A **virtual environment** keeps this project's packages separate from your other Python projects.

```bash
# Create the environment
uv venv

# Activate it
# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate
```

**You'll know it worked when you see** `(.venv)` at the start of your terminal prompt.

### 1.3 Install Dependencies

```bash
uv pip install -r requirements.txt
```

This installs:
- `openai` - For embeddings and chat
- `qdrant-client` - For the vector database
- `pytest` - For running tests

### 1.4 Set Your OpenAI API Key

<details>
<summary>🪟 Windows (PowerShell)</summary>

```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

</details>

<details>
<summary>🪟 Windows (Command Prompt)</summary>

```cmd
set OPENAI_API_KEY=sk-your-key-here
```

</details>

<details>
<summary>🍎 Mac / 🐧 Linux</summary>

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

</details>

**Tip:** You'll need to set this every time you open a new terminal. To make it permanent, add the line to your shell profile (`~/.bashrc`, `~/.zshrc`, or Windows Environment Variables).

### 1.5 Start the Vector Database

```bash
docker-compose up -d
```

**What this does:** Starts Qdrant (the vector database) in the background.

**Verify it's running:**
```bash
curl http://localhost:6333/
```

You should see: `{"title":"qdrant - vector search engine"...}`

<details>
<summary>🔧 If curl doesn't work on Windows</summary>

Open your browser and go to: http://localhost:6333/

You should see JSON output with "qdrant" in it.

</details>

---

## Step 2: Understand What You're Building

> ⏱️ **Time:** 10 minutes (reading)

Before writing code, let's understand **why** each piece exists.

### The Problem

You have documents. You want to ask questions. But:
- ChatGPT doesn't know about YOUR documents
- Documents are too long to paste into ChatGPT
- You need to find the RIGHT parts of documents to answer each question

### The Solution: RAG

**RAG = Retrieval-Augmented Generation**

```
Your Question: "What are the payment terms?"
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  1. RETRIEVE: Find document chunks about "payment"      │
│  2. AUGMENT: Add those chunks to the AI prompt          │
│  3. GENERATE: AI writes answer using those chunks       │
└─────────────────────────────────────────────────────────┘
        │
        ▼
Answer: "According to section 3.2, payment is due within 30 days..."
```

### Your 4 Building Blocks

```
Documents → [CHUNK] → Pieces → [EMBED] → Vectors → [STORE] → Database
                                                        │
Question → [EMBED] → Vector → [SEARCH] ─────────────────┘
                                  │
                                  ▼
                        Relevant Pieces → [GENERATE] → Answer
```

| Block | What It Does | Analogy |
|-------|--------------|---------|
| **Chunk** | Split documents into pieces | Cutting a book into paragraphs |
| **Embed** | Convert text to numbers | Creating a "fingerprint" for each paragraph |
| **Store/Search** | Save and find by similarity | A library that finds books by meaning, not title |
| **Generate** | Write answer from context | A researcher who summarizes what they found |

### Read the Sample Documents

Look at the files in `data/sample_docs/`. These are what your system will answer questions about:
- `machine_learning_basics.txt`
- `deep_learning_intro.txt`
- `rag_explained.txt`

---

## Step 3: Implement Document Chunking

> ⏱️ **Time:** 20-30 minutes

### What You're Building

A function that splits a long document into smaller overlapping pieces.

**Why overlap?** If a sentence is cut in half, important information might be lost. Overlap ensures no information falls through the cracks.

### Example

```
Original: "The quick brown fox jumps over the lazy dog."

Chunks (size=20, overlap=5):
  Chunk 1: "The quick brown fox "
  Chunk 2: " fox jumps over the "
  Chunk 3: " the lazy dog."

Notice how "fox" and "the" appear in two chunks each!
```

### Your Task

Open `src/ingest.py` and find the `chunk_document()` function.

**Current code:**
```python
def chunk_document(content: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    # TODO: Your implementation here
    raise NotImplementedError("Implement chunk_document() - See hints above!")
```

**Replace it with your implementation.**

### Step-by-Step Guide

<details>
<summary>💡 Hint 1: The Algorithm</summary>

Use a **sliding window**:
1. Start at position 0
2. Take `chunk_size` characters
3. Move forward by `chunk_size - overlap` characters
4. Repeat until you reach the end

```
Text: [===========================================]
       |--- chunk 1 ---|
                  |--- chunk 2 ---|
                             |--- chunk 3 ---|
       ^          ^
       |          |
     start    start + (chunk_size - overlap)
```

</details>

<details>
<summary>💡 Hint 2: Handle Edge Cases</summary>

- **Empty string:** Return empty list `[]`
- **Short string:** If content is shorter than `chunk_size`, return `[content]`
- **Last chunk:** It might be smaller than `chunk_size` - that's OK!

</details>

<details>
<summary>💡 Hint 3: Python Code Structure</summary>

```python
def chunk_document(content: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    if not content:
        return []

    if len(content) <= chunk_size:
        return [content]

    chunks = []
    start = 0

    while start < len(content):
        end = start + chunk_size
        chunk = content[start:end]
        chunks.append(chunk)
        start += ???  # What should this be?

    return chunks
```

</details>

<details>
<summary>🎯 Full Solution (Only if completely stuck!)</summary>

```python
def chunk_document(content: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
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
```

</details>

### Test Your Code

```bash
cd tests
pytest test_chunking.py -v
```

**Expected output:**
```
test_basic_chunking PASSED
test_overlap_exists PASSED
test_short_content PASSED
test_empty_content PASSED
...
```

### Common Mistakes

| Error | Cause | Fix |
|-------|-------|-----|
| `IndexError` | Going past end of string | Python slicing handles this automatically - `s[0:1000]` works even if `s` is short |
| Infinite loop | `start` never increases | Make sure `step > 0`. If `overlap >= chunk_size`, you have a problem! |
| Missing last chunk | Loop ends too early | Use `while start < len(content)` not `<=` |

---

## Step 4: Generate Embeddings

> ⏱️ **Time:** 20-30 minutes

### What You're Building

A function that converts text into numbers (vectors) using OpenAI's API.

### Why Numbers?

Computers can't understand that "dog" and "puppy" are similar. But if we convert them to number lists:
- "dog" → [0.2, 0.8, 0.1, ...]
- "puppy" → [0.21, 0.79, 0.12, ...]
- "car" → [0.9, 0.1, 0.7, ...]

Now we can mathematically see that "dog" and "puppy" have similar numbers!

### Your Task

Open `src/embeddings.py` and implement `generate_embeddings()`.

### Step-by-Step Guide

<details>
<summary>💡 Hint 1: OpenAI API Call</summary>

The OpenAI embedding API works like this:

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY from environment
response = client.embeddings.create(
    input=["Hello world", "Another text"],
    model="text-embedding-3-small"
)

# response.data is a list of embedding objects
# Each has an .embedding attribute (list of floats)
```

</details>

<details>
<summary>💡 Hint 2: Extract Embeddings</summary>

```python
embeddings = [item.embedding for item in response.data]
```

</details>

<details>
<summary>💡 Hint 3: Handle Batching</summary>

OpenAI can process many texts at once, but there's a limit. For safety, process in batches:

```python
all_embeddings = []
for i in range(0, len(texts), batch_size):
    batch = texts[i:i + batch_size]
    # Call API for this batch
    # Add results to all_embeddings
```

</details>

<details>
<summary>🎯 Full Solution</summary>

```python
def generate_embeddings(
    texts: List[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 100
) -> List[List[float]]:
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
```

</details>

### Test Your Code

```bash
pytest test_embeddings.py -v
```

### Common Mistakes

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthenticationError` | API key not set | Set `OPENAI_API_KEY` environment variable |
| `RateLimitError` | Too many requests | Add a small delay between batches |
| Empty result | Empty input list | Handle `if not texts: return []` |

---

## Step 5: Store Embeddings in Qdrant

> ⏱️ **Time:** 15-20 minutes

### What You're Building

A function that saves your embeddings to a database so you can search them later.

### Your Task

Open `src/retriever.py` and implement `store_embeddings()`.

### Step-by-Step Guide

<details>
<summary>💡 Hint 1: Qdrant Point Structure</summary>

Qdrant stores data as "points". Each point has:
- **id:** A unique number
- **vector:** The embedding (list of floats)
- **payload:** Extra data (like the text content and source file)

```python
from qdrant_client.models import PointStruct

point = PointStruct(
    id=1,
    vector=[0.1, 0.2, 0.3, ...],
    payload={"content": "Hello world", "source": "doc.txt"}
)
```

</details>

<details>
<summary>💡 Hint 2: Insert Points</summary>

```python
client.upsert(
    collection_name="documents",
    points=[point1, point2, point3, ...]
)
```

</details>

<details>
<summary>🎯 Full Solution</summary>

```python
def store_embeddings(chunks: List[Dict], client: Optional[QdrantClient] = None) -> int:
    if not chunks:
        return 0

    if client is None:
        client = get_client()

    initialize_collection(client)

    points = []
    for i, chunk in enumerate(chunks):
        point = PointStruct(
            id=i,
            vector=chunk["embedding"],
            payload={
                "content": chunk["content"],
                "metadata": chunk.get("metadata", {})
            }
        )
        points.append(point)

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)
```

</details>

### Test Your Code

```bash
pytest test_retriever.py::TestStoreEmbeddings -v
```

---

## Step 6: Implement Search

> ⏱️ **Time:** 15-20 minutes

### What You're Building

A function that finds the most similar documents to a query.

### Your Task

Still in `src/retriever.py`, implement `search()`.

### Step-by-Step Guide

<details>
<summary>💡 Hint 1: Qdrant Search</summary>

```python
results = client.search(
    collection_name="documents",
    query_vector=[0.1, 0.2, ...],  # Your query embedding
    limit=5  # How many results
)
```

</details>

<details>
<summary>💡 Hint 2: Process Results</summary>

Each result has:
- `result.payload` - Your stored data (content, metadata)
- `result.score` - How similar (0 to 1, higher = more similar)

```python
processed = []
for result in results:
    processed.append({
        "content": result.payload["content"],
        "metadata": result.payload.get("metadata", {}),
        "score": result.score
    })
```

</details>

<details>
<summary>🎯 Full Solution</summary>

```python
def search(
    query_embedding: List[float],
    top_k: int = 5,
    client: Optional[QdrantClient] = None
) -> List[Dict]:
    if client is None:
        client = get_client()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k
    )

    processed = []
    for result in results:
        processed.append({
            "content": result.payload["content"],
            "metadata": result.payload.get("metadata", {}),
            "score": result.score
        })

    return processed
```

</details>

### Test Your Code

```bash
pytest test_retriever.py::TestSearch -v
```

---

## Step 7: Build the Q&A Chain

> ⏱️ **Time:** 25-35 minutes

### What You're Building

The final piece! A function that:
1. Takes a question
2. Finds relevant document chunks
3. Sends them + the question to GPT
4. Returns the answer

### Your Task

Open `src/qa_chain.py` and implement `answer_question()`.

### Step-by-Step Guide

<details>
<summary>💡 Hint 1: The Flow</summary>

```python
# 1. Search for relevant chunks
results = search_with_text(question, top_k=5)

# 2. Build context from results
context = build_context(results)

# 3. Create prompt
prompt = f"""Answer based on this context:

{context}

Question: {question}

Answer:"""

# 4. Call GPT
# 5. Return answer + sources
```

</details>

<details>
<summary>💡 Hint 2: Call GPT</summary>

```python
client = get_openai_client()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Answer based only on the provided context."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)
answer = response.choices[0].message.content
```

</details>

<details>
<summary>🎯 Full Solution</summary>

```python
def answer_question(
    question: str,
    top_k: int = 5,
    model: str = "gpt-4o-mini",
    temperature: float = 0.3
) -> Dict:
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
```

</details>

### Test Your Code

```bash
pytest test_qa.py -v
```

---

## Step 8: Run the Full System!

> ⏱️ **Time:** 10 minutes

### 8.1 Ingest the Documents

```bash
cd src
python -c "
from ingest import process_documents
from embeddings import embed_chunks
from retriever import store_embeddings, initialize_collection, get_client

# Initialize database
client = get_client()
initialize_collection(client, recreate=True)

# Process documents
print('Loading and chunking documents...')
chunks = process_documents('../data/sample_docs')
print(f'Created {len(chunks)} chunks')

# Generate embeddings
print('Generating embeddings (this may take a minute)...')
chunks = embed_chunks(chunks)
print('Embeddings generated!')

# Store in database
count = store_embeddings(chunks)
print(f'Stored {count} vectors in database')

print('\nReady to answer questions!')
"
```

### 8.2 Try It Out!

```bash
python qa_chain.py
```

**Try these questions:**
- "What is machine learning?"
- "What's the difference between supervised and unsupervised learning?"
- "How does RAG work?"
- "What is backpropagation?"

### 8.3 Run All Tests

```bash
cd tests
pytest -v
```

**All tests passing = You completed the challenge!** 🎉

---

## Understanding CI/CD (For DevOps Students)

> **This section teaches you what CI/CD is and how it works.** Don't skip it!

### What is CI/CD?

**CI/CD** stands for **Continuous Integration / Continuous Deployment**.

- **CI (Continuous Integration):** Automatically test code every time someone pushes
- **CD (Continuous Deployment):** Automatically deploy code that passes tests

**In this challenge:** When you push code, GitHub automatically runs your tests. This is CI.

### Why Does This Matter?

Without CI/CD (the old way):
```
Developer writes code → Manually runs tests → Forgets to test → Pushes broken code → 💥
```

With CI/CD (the modern way):
```
Developer writes code → Pushes → Tests run automatically → Broken code blocked → ✅
```

**Every company uses CI/CD.** You'll see it in job interviews.

### What is GitHub Actions?

GitHub Actions is GitHub's built-in CI/CD system. It:
- Runs automatically when you push code
- Executes commands in a fresh virtual machine
- Reports pass/fail status

### How Our Workflow Works

Look at the file `.github/workflows/grade.yml` in this repo. Here's what each part does:

```yaml
# 1. WHEN does this run?
on:
  push:
    branches: [main]    # Runs when you push to main branch

# 2. WHAT runs?
jobs:
  grade:
    runs-on: ubuntu-latest    # Use a fresh Ubuntu Linux machine

    # 3. SERVICES - Start dependencies (like our vector database)
    services:
      qdrant:
        image: qdrant/qdrant:latest    # Pull Docker image
        ports:
          - 6333:6333                   # Expose port

    # 4. STEPS - Commands to run in order
    steps:
      - name: Checkout code            # Get your code
        uses: actions/checkout@v4

      - name: Set up Python            # Install Python
        uses: actions/setup-python@v5

      - name: Install dependencies     # pip install
        run: pip install -r requirements.txt

      - name: Run tests                # pytest
        run: pytest tests/ -v
```

### Hands-On: Read the Workflow File

**Exercise:** Open `.github/workflows/grade.yml` and answer these questions:

1. What triggers the workflow to run? (Hint: look at `on:`)
2. What Docker image is used for the vector database?
3. What Python version is installed?
4. What happens if a test fails?

<details>
<summary>Answers</summary>

1. Push to `main` or `master` branch, or pull requests, or manual trigger (`workflow_dispatch`)
2. `qdrant/qdrant:latest`
3. Python 3.11
4. The step shows ❌ FAILED and the job continues (because of `continue-on-error: true`) so you can see all results

</details>

### Key CI/CD Concepts You're Learning

| Concept | What It Means | Where You See It |
|---------|---------------|------------------|
| **Trigger** | Event that starts the workflow | `on: push` |
| **Runner** | Machine that runs your code | `runs-on: ubuntu-latest` |
| **Job** | Group of steps that run together | `jobs: grade:` |
| **Step** | Single command or action | `- name: Run tests` |
| **Service** | Background container (databases, etc) | `services: qdrant:` |
| **Secret** | Encrypted variable (API keys) | `${{ secrets.OPENAI_API_KEY }}` |
| **Artifact** | Files saved from the build | (not used here, but common) |

### What Happens When You Push

```
┌─────────────────────────────────────────────────────────────────┐
│  YOU: git push origin main                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  GITHUB: "I see a push! Let me check for workflows..."          │
│                                                                  │
│  Found: .github/workflows/grade.yml                             │
│  Trigger matches: push to main ✓                                │
│                                                                  │
│  Starting workflow...                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  GITHUB RUNNER (fresh Ubuntu VM):                                │
│                                                                  │
│  1. git clone your-repo                                         │
│  2. docker run qdrant/qdrant (start database)                   │
│  3. Install Python 3.11                                         │
│  4. pip install -r requirements.txt                             │
│  5. pytest tests/test_chunking.py                               │
│  6. pytest tests/test_embeddings.py                             │
│  7. ... more tests ...                                          │
│  8. Calculate score, write summary                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  YOU: Check Actions tab → See results!                          │
│                                                                  │
│  🎯 Total Score: 80/100                                         │
│  ❌ Step 7 failed - check the logs                              │
└─────────────────────────────────────────────────────────────────┘
```

### Reading CI Logs (Important Skill!)

When a test fails, you need to read the logs to debug. Here's how:

1. Go to **Actions** tab in your repo
2. Click on the failed workflow run
3. Click on the failed job (red ❌)
4. Expand the failed step
5. Read the error message

**Example error log:**
```
tests/test_chunking.py::TestChunkDocument::test_overlap_exists FAILED

E       AssertionError: Chunk 1 should overlap with chunk 0
E       assert 'fox ' in 'jumps over the lazy'

=========================== short test summary ===========================
FAILED tests/test_chunking.py::test_overlap_exists - AssertionError
```

**How to read this:**
- Test name: `test_overlap_exists`
- What failed: Chunks don't overlap properly
- Expected: The word "fox " should appear in the next chunk
- Your code: The next chunk starts with "jumps" (no overlap!)

### Try It: Break Something On Purpose

**Learning exercise:** Make a test fail intentionally to practice reading logs.

1. In `src/ingest.py`, change your `chunk_document()` to always return `["broken"]`
2. Commit and push
3. Watch the workflow fail
4. Read the error logs
5. Fix it and push again

This teaches you the **debug cycle** that real developers use daily.

---

## Setup GitHub Secrets

To run the full grading workflow, you need to add your OpenAI API key as a secret.

### Why Secrets?

Your API key is sensitive - you don't want it in your code!

**Bad (NEVER do this):**
```python
api_key = "sk-abc123..."  # 😱 Anyone can see this!
```

**Good (use secrets):**
```python
api_key = os.getenv("OPENAI_API_KEY")  # ✅ Loaded from environment
```

GitHub Secrets encrypts your key and only exposes it during workflow runs.

### How to Add Your API Key

1. Go to your **forked repository** on GitHub
2. Click **Settings** (tab at the top)
3. Click **Secrets and variables** → **Actions** (left sidebar)
4. Click **New repository secret**
5. Fill in:
   - **Name:** `OPENAI_API_KEY`
   - **Secret:** `sk-your-actual-api-key`
6. Click **Add secret**

### How Secrets Work in the Workflow

In `.github/workflows/grade.yml`:

```yaml
- name: Run tests
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}  # Inject secret
  run: pytest tests/
```

The `${{ secrets.OPENAI_API_KEY }}` syntax tells GitHub to:
1. Decrypt your secret
2. Set it as an environment variable
3. Only for this step
4. Never print it in logs (shows `***` instead)

### What You'll See in GitHub Actions

After pushing your code, go to the **Actions** tab to see your results:

```
🎯 Grade Challenge

  ✅ Step 3: Document Chunking     - 20/20 points
  ✅ Step 4: Generate Embeddings   - 20/20 points
  ✅ Step 5: Store Vectors         - 20/20 points
  ✅ Step 6: Vector Search         - 20/20 points
  ✅ Step 7: Q&A Chain             - 20/20 points

  ─────────────────────────────────────────────
  🎯 Total Score: 100/100

  🎉 CHALLENGE COMPLETE!
```

If tests fail, expand the failed step to see detailed error messages.

---

## Troubleshooting

<details>
<summary>❌ "OPENAI_API_KEY not set"</summary>

Set your API key:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key"

# Mac/Linux
export OPENAI_API_KEY="sk-your-key"
```

</details>

<details>
<summary>❌ "Connection refused" to Qdrant</summary>

Make sure Docker is running and Qdrant is started:
```bash
docker-compose up -d
docker ps  # Should show qdrant container
```

</details>

<details>
<summary>❌ "ModuleNotFoundError"</summary>

Make sure you're in the virtual environment:
```bash
# Should see (.venv) in your prompt
# If not, activate it:
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

</details>

<details>
<summary>❌ Tests failing</summary>

Read the error message carefully. Common issues:
- **AssertionError:** Your output doesn't match expected. Check the test to see what's expected.
- **NotImplementedError:** You haven't implemented the function yet.
- **TypeError:** Wrong data types. Make sure you return `List[str]` not `str`, etc.

</details>

---

## What You Learned

By completing this challenge, you now understand:

- ✅ **Document Chunking** - How to split text for retrieval
- ✅ **Text Embeddings** - Converting text to searchable vectors
- ✅ **Vector Databases** - Storing and searching by meaning
- ✅ **RAG Architecture** - How modern AI assistants access external knowledge
- ✅ **Prompt Engineering** - Structuring prompts for accurate answers

**This is the same technology powering:**
- ChatGPT with file uploads
- Enterprise knowledge bases
- AI-powered search engines
- Customer support chatbots

---

## Next Steps

Want to go further? Try:

1. **Add your own documents** - Put PDFs or text files in `data/sample_docs/`
2. **Improve chunking** - Split on sentences instead of characters
3. **Add metadata filtering** - Search only specific document types
4. **Build a web UI** - Create a simple chat interface

---

## Need Help?

If you're stuck and the hints don't help:

1. **Re-read the hints** - They contain the answer, broken into steps
2. **Check the error message** - It usually tells you exactly what's wrong
3. **Look at the test** - Tests show expected inputs and outputs
4. **Use the solution** - It's OK to learn by reading working code!

Good luck! 🚀
