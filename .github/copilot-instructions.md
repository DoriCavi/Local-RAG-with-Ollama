## Quick Context

- Purpose: Local RAG (retrieval-augmented generation) demo that uses Ollama for embeddings and chat models, Chroma for vector storage, and small utilities to convert PDFs → markdown and ingest into a local vector DB.
- Key directories/files:
  - `UI.py` — a Gradio chat UI (appears to be a standalone demo).
  - `3_chatbot.py` — main RAG setup + Gradio/Streamlit UI for querying documents.
  - `2_chunking_embedding_ingestion.py` — ingestion pipeline: chunk documents, create embeddings via `langchain_ollama`, and persist into `chroma_db`.
  - `DocParsing.py` — converts PDFs to markdown (uses `docling`) and writes to `markdown_output/`.
  - `chroma_db/` — persistent Chroma database (contains `chroma.sqlite3`).
  - `markdown_output/` — where `DocParsing` stores markdown outputs (e.g. `ApplePolicy.md`).
  - `.env` — environment variables (models, database location, collection name, Bright Data key).

## Big-picture architecture

- Data flow:
  1. Source PDF(s) or scraped text → `DocParsing.py` (writes markdown to `markdown_output/`).
  2. `2_chunking_embedding_ingestion.py` reads prepared text (via `DATASET_STORAGE_FOLDER` / `datasets/` or `snapshot.txt`), splits text into chunks (RecursiveCharacterTextSplitter), computes embeddings with Ollama (`langchain_ollama.OllamaEmbeddings`), and writes vectors into Chroma at `DATABASE_LOCATION`.
  3. `3_chatbot.py` (or `UI.py`) loads the Chroma vectorstore + Ollama chat model and performs: embed query → similarity search → format context → call chat LLM with a prompt template to generate answers with sources.

- Why these choices:
  - Ollama is used to run models locally (embeddings + chat) instead of a hosted API.
  - Chroma persists embeddings locally as `chroma_db/` for fast similarity search.
  - Small text-splitting chunks (chunk_size=1000, overlap=200) are applied consistently across ingestion and retrieval.

## Project-specific developer workflows (how to run things here)

- Create & activate venv (Windows PowerShell):
  - `python -m venv venv`
  - `.\\.\venv\Scripts\Activate.ps1`

- Install dependencies:
  - `pip install -r requirements.txt`

- Recommended `.env` values (already in repo):
  - `EMBEDDING_MODEL`, `CHAT_MODEL`, `MODEL_PROVIDER` (default: Ollama models). Example in `.env`:
    - `EMBEDDING_MODEL="mxbai-embed-large"`
    - `CHAT_MODEL="llama3.2:1b"`
    - `DATABASE_LOCATION = "chroma_db"`
    - `COLLECTION_NAME = "rag_data"`

- Typical run sequence (safe order):
  1. Convert or prepare source docs: `python DocParsing.py` (this writes markdown to `markdown_output/`).
  2. Create embeddings & (re)ingest: `python 2_chunking_embedding_ingestion.py`.
     - WARNING: `2_chunking_embedding_ingestion.py` will delete the `DATABASE_LOCATION` folder if it exists (it calls `shutil.rmtree`). Running it wipes the Chroma DB and rebuilds it.
  3. Start the app:
     - Streamlit (recommended per README): `streamlit run 3_chatbot.py`.
     - Or run Gradio directly (works for `UI.py` or `3_chatbot.py`): `python 3_chatbot.py` or `python UI.py`.
     - Note: the repo contains both a `UI.py` Gradio demo and `3_chatbot.py` which mixes Streamlit and Gradio; inspect both before choosing.

## Important environment & integrations

- Local Ollama: This project uses `langchain-ollama` and `ollama` Python packages. Ollama typically requires a local Ollama runtime — ensure Ollama is installed and running on the machine if you expect local models to be available.
- Chroma persistence: The vector store persist directory is `DATABASE_LOCATION` (.env default `chroma_db`). The file `chroma_db/chroma.sqlite3` is the persistent DB — do not delete unless you intend to re-ingest.
- Bright Data: optional scraping pipeline keys are referenced in `.env` (BRIGHTDATA_API_KEY). If you use scraping scripts (e.g., `1_scraping_wikipedia.py` if present), populate that key.

## Conventions & patterns to follow when coding here

- Embeddings and chat models are always constructed via environment variables. Use `os.getenv("EMBEDDING_MODEL")` and `os.getenv("CHAT_MODEL")` to keep code consistent with existing files.
- Text splitting: prefer `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)` to stay consistent with ingestion and retrieval granularity.
- Vector store access: code directly references `vector_store._collection` for counts / peeks — follow the same pattern when you need quick diagnostics (but prefer stable APIs where possible).
- IDs: ingestion uses `uuid4()` for document IDs — maintain unique IDs on add.

## Useful code examples (copy/paste)

- Build embeddings and vector store (example from `2_chunking_embedding_ingestion.py`):

```py
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

embeddings = OllamaEmbeddings(model=os.getenv("EMBEDDING_MODEL"))
vector_store = Chroma(collection_name=os.getenv("COLLECTION_NAME"), embedding_function=embeddings, persist_directory=os.getenv("DATABASE_LOCATION"))
```

- Retrieval flow (example from `3_chatbot.py`):

```py
query_embedding = embeddings.embed_query(question)
results = vector_store.similarity_search_by_vector(embedding=query_embedding, k=3)
# format context and call llm
```

## Known issues / quirks to watch for

- Duplicate or inconsistent UI code: `UI.py` is a Gradio app; `3_chatbot.py` mixes Streamlit + Gradio and contains duplicate `if __name__ == "__main__"` blocks. Decide which UI to maintain before refactoring.
- `2_chunking_embedding_ingestion.py` deletes the Chroma folder on start — remember this when running repeatedly.
- Some files (DocParsing, 3_chatbot) print diagnostics and also write files; editing them may change both behavior and file outputs.

## Where to look next when editing

- `3_chatbot.py` — main RAG setup, prompt construction, retrieval + answer pipeline.
- `2_chunking_embedding_ingestion.py` — ingestion pipeline, chunk sizes, and DB persistence behavior.
- `DocParsing.py` — PDF → markdown conversion and storage target `markdown_output/`.
- `requirements.txt` — shows required packages (notably `ollama` and `langchain-ollama`).

---
If anything here is unclear or you'd like the file to emphasise different parts (for example, instructions for running Ollama locally, Docker hints, or CI/test commands), tell me which area to expand and I will update this file.
