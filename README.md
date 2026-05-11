# Tech Giants Strategic Assistant (RAG)

A small retrieval-augmented generation (RAG) demo that answers questions using only your local documents. It uses [LangGraph](https://github.com/langchain-ai/langgraph) for a two-step pipeline (retrieve, then generate), [Chroma](https://www.trychroma.com/) as the vector store, and [Ollama](https://ollama.com/) for embeddings and the chat model.

## How it works

1. **Retrieve** (`graph.py`): The user question is passed to a Chroma retriever configured with similarity score threshold search (`k=5`, `score_threshold=0.5`).
2. **Generate** (`graph.py`): If any chunks pass the threshold, they are formatted with source file names and sent to the LLM with strict instructions to answer only from that context and to cite sources. If nothing is retrieved, the app returns a fixed apology message and disclaimer.

The CLI entry point is `main.py`, which loads the compiled LangGraph `app` from `graph.py`.

## Prerequisites

- Python 3.10 or newer (recommended)
- [Ollama](https://ollama.com/) installed and running locally
- Pull the models used in code (names must match what is in the repo):

  ```bash
  ollama pull llama3.2:latest
  ollama pull mxbai-embed-large:latest
  ```

- A populated Chroma database at `./chroma_db` (see indexing below)

## Project layout

| Path | Role |
|------|------|
| `main.py` | Interactive loop: questions in, printed answers out (`q` to quit) |
| `graph.py` | LangGraph state, retrieve/generate nodes, workflow wiring |
| `tools.py` | Chroma client, embeddings, retriever configuration |
| `ingestion.py` | Intended script to load documents from `knowledge_base/`, chunk, and build `chroma_db/` |
| `knowledge_base/` | Put source `.txt` (and optionally PDF) files here before indexing |
| `chroma_db/` | Persistent vector store (created after a successful ingest) |

## Setup

1. Clone the repository and enter the project directory.

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   ```

   Activate it (Windows PowerShell):

   ```bash
   .\venv\Scripts\Activate.ps1
   ```

   Install packages (adjust versions if you pin them elsewhere):

   ```bash
   pip install langchain-ollama langgraph langchain-chroma langchain-community langchain-text-splitters chromadb
   ```

3. Ensure Ollama is running and the models above are available.

4. Create `knowledge_base` if it does not exist and add your `.txt` documents.

5. Build or refresh the vector store so `./chroma_db` exists before you run the assistant. The project includes `ingestion.py` for that purpose; it must define everything it uses (for example `embeddings` and any PDF loader) so the script runs without `NameError`. After a successful run, `chroma_db` will contain the indexed chunks.

## Run the assistant

From the project root (with the virtual environment activated):

```bash
python main.py
```

Type your question at the prompt. Type `q` and press Enter to exit.

## Configuration notes

- **Retriever** (`tools.py`): `search_type="similarity_score_threshold"` with `k=5` and `score_threshold=0.5`. Changing the threshold affects how strict retrieval is relative to embedding similarity.
- **LLM** (`graph.py`): `OllamaLLM(model="llama3.2:latest")`.
- **Embeddings** (`tools.py`): `OllamaEmbeddings(model="mxbai-embed-large:latest")`. Use the same embedding model for ingestion and retrieval, or rebuild the index after you change it.


