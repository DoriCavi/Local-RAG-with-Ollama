# Apple Watch RAG Chatbot

A simple chatbot that answers questions about Apple Watch using RAG (Retrieval-Augmented Generation).

---

## What Does It Do?

Answers questions about Apple Watch by:
1. Finding relevant information from the user guide
2. Using AI to generate natural answers

**Example:**
- You ask: "How do I set up Apple Pay?"
- Bot finds relevant sections from the guide
- Bot generates a clear answer

---

## How It Works

```
┌─────────────┐
│   User asks │
│  a question │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Search for relevant │
│ info in database    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ AI generates answer │
│ using that info     │
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│ Show answer │
│   to user   │
└─────────────┘
```

---

## What You Need

1. **Python 3.11+**
2. **Ollama** (for running AI models locally)
3. **The code files**

---

## Setup (5 Steps)

### Step 1: Install Ollama

**Mac:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:** Download from https://ollama.ai/download

### Step 2: Get AI Models

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

### Step 3: Install Python Packages

```bash
pip install -r requirements.txt
```

### Step 4: Create .env File

Create a file named `.env`:
```
EMBEDDING_MODEL=nomic-embed-text
CHAT_MODEL=llama3.2
DATABASE_LOCATION=./chroma_db
COLLECTION_NAME=apple_watch_guide
```

### Step 5: Run It

```bash
python app.py
```

Open your browser: http://localhost:7860

---

## File Structure

```
project/
├── app.py           # Main code
├── UI.py                  # User interface
├── DocParsing.py          # Reads documents
├── .env                   # Settings
├── requirements.txt       # Python packages
└── markdown_output/
    └── Apple Watch User Guide.md  # Knowledge source
```

---

## How The System Works

### Simple Diagram

```
┌───────────────────────────────────────────────────────┐
│                    YOUR QUESTION                       │
│              "How do I check battery?"                 │
└────────────────────┬──────────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────────┐
│              STEP 1: FIND INFORMATION                  │
│                                                        │
│  Searches the Apple Watch guide for relevant chunks:  │
│  - "Battery percentage shown in Control Center..."    │
│  - "Swipe up to see battery level..."                 │
│  - "Low Power Mode extends battery life..."           │
└────────────────────┬──────────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────────┐
│              STEP 2: GENERATE ANSWER                   │
│                                                        │
│  AI reads the found information and writes:           │
│  "You can check your Apple Watch battery by           │
│   swiping up from the watch face to open Control      │
│   Center. The battery percentage is displayed at      │
│   the top. You can also enable Low Power Mode..."     │
└────────────────────┬──────────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────────┐
│                  SHOW TO USER                          │
└───────────────────────────────────────────────────────┘
```

---

## The Main Parts

### 1. Document Storage (ChromaDB)

- Stores the Apple Watch guide in small chunks
- Each chunk has a "vector" (numbers that represent the meaning)
- Allows fast searching for relevant information

### 2. Embeddings (nomic-embed-text)

- Converts text into vectors (numbers)
- Questions and document chunks both become vectors
- Similar meanings = similar vectors

### 3. Chat Model (llama3.2)

- Reads the found information
- Generates natural language answers
- Runs locally on your computer

### 4. User Interface (Streamlit)

- Web-based chat interface
- Shows questions and answers
- Easy to use

---

## Key Functions

### `setup_rag()`
Sets up everything when you start the app.

### `retrieve_documents(question, k=3)`
Finds the 3 most relevant pieces of information for your question.

### `answer_with_retrieved_docs(docs, question)`
Uses AI to generate an answer from the found information.

### `ask_question(question)`
Complete process: find info → generate answer → return result.

---

## Common Problems

### "Ollama not running"
**Fix:** 
```bash
ollama serve
```

### "Model not found"
**Fix:**
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### "No answers / empty database"
**Fix:** Delete the database folder and restart:
```bash
rm -rf ./chroma_db
python app.py
```

### "Slow responses"
**Fix:** Use a smaller model:
```
CHAT_MODEL=llama3.2:7b
```

---

## What Each Setting Does

In your `.env` file:

| Setting | What It Does | Default |
|---------|--------------|---------|
| `EMBEDDING_MODEL` | Model that converts text to vectors | nomic-embed-text |
| `CHAT_MODEL` | Model that generates answers | llama3.2 |
| `DATABASE_LOCATION` | Where to save the database | ./chroma_db |
| `COLLECTION_NAME` | Database collection name | apple_watch_guide |

---

## How to Customize

### Use Different Documents

Replace `Apple Watch User Guide.md` with your own document.

### Change Number of Results

In `app.py`, find:
```python
docs = retrieve_documents(vector_store, embeddings, question, k=3)
```

Change `k=3` to `k=5` for more results.

### Change AI Temperature

In `app.py`, find:
```python
llm = ChatOllama(model=os.getenv("CHAT_MODEL"), temperature=0.3)
```

- Lower (0.1): More focused, consistent answers
- Higher (0.7): More creative answers

---

## Requirements

```txt
streamlit
langchain
langchain-chroma
langchain-ollama
chromadb
python-dotenv
```

Install all:
```bash
pip install -r requirements.txt
```

---

## That's It!

Simple RAG chatbot that:
1. ✅ Runs locally (private)
2. ✅ Uses free AI models
3. ✅ Easy to customize
4. ✅ Works with any documents

**Questions?** Check the troubleshooting section above.
