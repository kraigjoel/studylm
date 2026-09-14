# StudyLM

A locally hosted, NotebookLM-inspired study assistant that uses **Retrieval-Augmented Generation (RAG)** to answer questions from user-provided documents.

StudyLM combines document ingestion, semantic retrieval, and a locally running language model through Ollama to generate answers grounded in the supplied study material.

> The goal is to build a practical understanding of how document-based AI assistants work, from ingestion and retrieval through to answer generation.

## Features

* Local LLM inference using Ollama
* Document ingestion and processing
* Text chunking for retrieval
* Semantic search over document content
* Retrieval-Augmented Generation (RAG)
* Context-grounded question answering
* Modular Python application structure
* Fully local processing without requiring a cloud LLM API

## Architecture

```text
                    ┌──────────────────┐
                    │  User Documents  │
                    │  PDFs / Text     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Document Loader  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Text Splitter   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Embeddings /     │
                    │ Vector Storage   │
                    └────────┬─────────┘
                             │
                             ▼
User Question ─────► ┌──────────────────┐
                     │    Retriever     │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Relevant Context │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   Ollama LLM     │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Grounded Answer  │
                     └──────────────────┘
```

## Tech Stack

* **Python** – Application development
* **Ollama** – Local language model inference
* **LangChain** – LLM and retrieval integration
* **Vector database / vector storage** – Semantic document retrieval
* **RAG** – Grounding model responses in retrieved document context

## How It Works

StudyLM follows a Retrieval-Augmented Generation pipeline:

1. User documents are loaded into the application.
2. Documents are split into smaller text chunks.
3. Chunks are processed and stored for semantic retrieval.
4. The user submits a question.
5. The retriever identifies the most relevant document chunks.
6. The retrieved content is passed into the LLM as context.
7. Ollama generates an answer based on the retrieved information.

This allows the model to answer questions using the user's documents rather than relying entirely on its pretrained knowledge.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/kraigjoel/studylm.git
cd studylm
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama from:

https://ollama.com

Pull the required model:

```bash
ollama pull llama3.1:8b
```

Make sure Ollama is running before launching the application.

## Usage

Run the application from the project root:

```bash
python -m app.main
```

Follow the application prompts to load documents and ask questions about their content.

> The exact execution flow may change as the project develops.

## Example

Example interaction:

```text
User:
What is the function of mitochondria?

StudyLM:
Mitochondria are organelles responsible for producing ATP
through cellular respiration. They are often described as
the powerhouse of the cell.
```

The answer is generated using relevant retrieved document context rather than simply asking the model a general question.

## Project Structure

```text
studylm/
│
├── app/
│   ├── ingestion/       # Document loading and processing
│   ├── rag/             # Retrieval and RAG pipeline
│   └── main.py          # Application entry point
│
├── data/                # Input documents / local data
├── requirements.txt     # Python dependencies
├── LICENSE              # MIT License
└── README.md
```

## Current Limitations

* The application is currently in active development.
* Retrieval quality depends on document chunking and embedding configuration.
* The system relies on locally available Ollama models.
* The current implementation is focused on core RAG functionality rather than a fully polished user interface.
* Answer quality may vary depending on the quality and relevance of retrieved context.

## Development Notes

This project is also being used to explore and document the practical debugging process involved in building a RAG application.

Common challenges include:

* Python package and import structure
* Document processing
* Retrieval configuration
* Passing retrieved context into the LLM
* Prompt construction
* Ensuring generated answers remain grounded in source material

See [`studylm_rag_debugging_process.md`](studylm_rag_debugging_process.md) for a documented debugging walkthrough.

## Future Improvements

* [ ] Improve retrieval accuracy
* [ ] Add support for more document formats
* [ ] Add source references to generated answers
* [ ] Support multiple documents and collections
* [ ] Improve conversation history
* [ ] Add a graphical user interface
* [ ] Add automated tests
* [ ] Add retrieval and answer-quality evaluation
* [ ] Improve error handling and user feedback

## License

This project is licensed under the MIT License.
