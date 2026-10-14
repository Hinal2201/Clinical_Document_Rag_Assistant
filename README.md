# Clinical Document AI Workbench

**An AI-powered document question-answering prototype built with Python, LangChain, Retrieval-Augmented Generation (RAG), OpenAI embeddings, ChromaDB, and Streamlit.**

Upload documents, search their content using semantic similarity, and ask questions in natural language. The application generates answers using retrieved document passages and displays source references so users can inspect the supporting evidence.

> **Disclaimer:** This is a learning and demonstration project. It is not a medical device, diagnostic tool, or clinically validated system. Use synthetic or non-sensitive documents only. Do not upload patient records, protected health information, or confidential company documents.

## Key Features

- **Document ingestion:** Upload PDF, TXT, and Markdown files.
- **Text extraction:** Extract selectable text from PDFs while retaining page metadata.
- **Text chunking:** Split documents into smaller, overlapping passages using LangChain.
- **Embeddings:** Convert document chunks into numerical vectors using OpenAI's embedding model.
- **Vector database:** Store document vectors, text chunks, and metadata in a persistent local ChromaDB database.
- **Semantic search:** Retrieve passages relevant to a user's question.
- **LLM-powered answers:** Generate context-aware responses using a LangChain pipeline and an OpenAI chat model.
- **Source references:** Display source filenames, PDF page numbers when available, and retrieved excerpts.
- **Interactive interface:** Upload documents, manage indexing, ask questions, and inspect results through Streamlit.
- **Bundled demo documents:** Explore the application using synthetic workflow, privacy, and troubleshooting notes.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and RAG pipeline |
| Streamlit | Interactive web interface |
| LangChain | Document processing, text splitting, prompts, and model orchestration |
| OpenAI Embeddings | Convert text into vector representations |
| ChromaDB | Persistent vector storage and similarity search |
| OpenAI chat model | Generate answers based on retrieved context |
| PyPDF | Extract text and page information from PDF documents |
| Pytest | Test core application functions |

## How It Works

The application follows a Retrieval-Augmented Generation (RAG) workflow.

1. **Document ingestion:** Upload a PDF, TXT, or Markdown document.
2. **Text extraction:** Read the text and attach source metadata.
3. **Chunking:** Split long documents into overlapping passages.
4. **Embedding generation:** Convert each chunk into a vector representation.
5. **Vector storage:** Save embeddings, text, and metadata in ChromaDB.
6. **Retrieval:** Embed the user's question and retrieve the most relevant passages.
7. **Answer generation:** Pass the question and retrieved context to an LLM through LangChain.
8. **Source inspection:** Display the generated answer alongside the passages used to produce it.

The goal of RAG is to ground generated responses in a selected document collection. However, retrieval and citations do not guarantee that an answer is correct. Retrieved evidence and generated answers must still be evaluated.

## Architecture

```text
PDF / TXT / Markdown Documents
              |
              v
       Text Extraction
              |
              v
      Document Chunking
              |
              v
     OpenAI Embeddings
              |
              v
     ChromaDB Vector Store
              |
              v
        User Question
              |
              v
      Semantic Retrieval
              |
              v
   Retrieved Source Passages
              |
              v
     LangChain Prompt Chain
              |
              v
       OpenAI Chat Model
              |
              v
    Answer + Source Evidence
              |
              v
       Streamlit Interface
```

## Getting Started

### Prerequisites

- Python 3.13 recommended
- VS Code or another Python development environment
- An OpenAI API key with access to the selected embedding and chat models
- Internet access for API calls

API usage may incur charges. Review your provider's pricing and usage limits before indexing documents.

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/clinical-document-rag-assistant.git
cd clinical-document-rag-assistant
```

Replace `<your-username>` with your GitHub username.

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If the `py` command is unavailable, use the full path to your installed Python 3.13 executable.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure the API key

Copy `.env.example` to `.env` and configure your API settings:

```dotenv
OPENAI_API_KEY=your_api_key_here
OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Alternatively, enter the API key into the application's sidebar.

**Never commit your API key or `.env` file to GitHub.** The repository's `.gitignore` excludes secrets, the virtual environment, and the local vector database.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL printed in your terminal, usually:

http://localhost:8501

## Try the Demo

1. Enter your OpenAI API key.
2. Open the **Document Library** tab.
3. Select **Index bundled demo documents**.
4. Open **Ask Your Documents**.
5. Ask questions such as:
   - How does the document retrieval pipeline work?
   - What happens when a PDF contains no selectable text?
   - What privacy considerations are important for a production system?
6. Expand **Retrieved Source Passages** to inspect the evidence behind the answer.
7. Upload a non-sensitive document and ask a question based on its content.

## Configuration

| Setting | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | Not configured | API key used for embeddings and answer generation |
| `OPENAI_CHAT_MODEL` | `gpt-4.1-mini` | Language model used to generate answers |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Model used to generate embeddings |
| Retrieved chunks | 4 | Number of document passages retrieved per question |
| Chunk size | 900 characters | Approximate size of each text chunk |
| Chunk overlap | 150 characters | Overlap between consecutive chunks |

These values provide a starting configuration. Chunk size, overlap, and retrieval settings should be evaluated against representative questions and expected source documents.

## Project Structure

```text
clinical-document-rag-assistant/
├── app.py
├── rag_engine.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── demo_docs/
│   ├── data_handling.md
│   ├── imaging_workflow.md
│   └── troubleshooting.md
├── data/
│   └── chroma_db/
├── tests/
│   └── test_core.py
├── ARCHITECTURE.md
├── INTERVIEW_PLAYBOOK.md
└── README.md
```

- `app.py` — Streamlit user interface.
- `rag_engine.py` — document loading, chunking, embedding, ChromaDB indexing, retrieval, and answer generation.
- `demo_docs/` — synthetic demonstration documents.
- `data/chroma_db/` — local persistent vector data generated when indexing documents.
- `tests/` — tests for core text-processing and source-display behavior.
- `ARCHITECTURE.md` — architecture and technical decision log.
- `INTERVIEW_PLAYBOOK.md` — demo walkthrough and interview preparation.

## Run the Tests

Activate your virtual environment, then run:

```bash
python -m pytest -q
```

The included tests cover document chunking, source metadata preservation, and source-label formatting. They do not establish end-to-end retrieval accuracy, answer correctness, or production readiness.

## Current Limitations

- Scanned PDFs without selectable text are not processed because OCR is not implemented.
- DOCX, HTML, DICOM, and image-based document ingestion are outside the current scope.
- Embedding and answer generation require an API key and internet access.
- Document content is sent to the embedding API during indexing, and retrieved context is sent to the chat API during question answering.
- Authentication, per-user document isolation, audit logging, and production security controls are not implemented.
- Source references help users inspect evidence but cannot guarantee that a generated answer is correct.
- The application is not validated for medical or clinical decision-making.

## Future Improvements

- Add a labelled evaluation dataset and measure retrieval quality using Recall@k and Mean Reciprocal Rank (MRR).
- Compare embedding models, chunking strategies, and retrieval parameters.
- Add OCR support for scanned documents.
- Implement document deletion, versioning, and duplicate detection.
- Evaluate hybrid keyword and vector retrieval or reranking.
- Add authentication, document-level permissions, audit trails, and monitoring.
- Evaluate latency, token usage, API cost, retrieval relevance, and answer groundedness.

## Responsible Use and Security

- Use synthetic or approved non-sensitive documents only.
- Keep API keys and secrets out of source control.
- Do not expose the prototype as a public document service without appropriate security controls.
- Treat uploaded documents and retrieved passages as untrusted input. Prompt instructions alone are not a complete defense against prompt injection.
- Any real clinical deployment requires appropriate privacy, security, validation, domain-expert, and regulatory review.

## Learning Objectives

This project demonstrates practical implementation of:

- Document ingestion and text preprocessing
- Embeddings and vector databases
- Semantic search and retrieval
- Retrieval-Augmented Generation using LangChain
- LLM integration and evidence-grounded responses
- Source attribution and testing
- Technical decision-making for AI applications

## License

No license has been specified. Add a `LICENSE` file before inviting others to reuse or contribute to the project.

---

**Built as an AI engineering learning project exploring document-grounded question answering with RAG.**