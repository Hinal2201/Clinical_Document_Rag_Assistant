# Interview Playbook — Clinical Document AI Workbench

## 30–45 second explanation

“I built a document-grounded AI assistant using LangChain, Chroma, embeddings, and RAG. Users can upload PDFs, text files, and Markdown notes. I extract the text and retain page metadata, split it into overlapping chunks, generate embeddings, and persist those vectors with the chunks in Chroma. At question time, I embed the question, retrieve the most relevant chunks, pass only those passages and the question to a chat model through a LangChain prompt chain, and show source references and excerpts. I chose a local persistent vector database to keep the demo easy to run, and a small embedding model for a straightforward baseline. The current project uses synthetic notes and isn't intended for clinical decisions.”

## Architecture by component

- **UI — Streamlit:** file upload, API configuration, indexing controls, chat window, sources and collection stats.
- **Document parsing — pypdf / Python text decoding:** PDF pages are kept separate to preserve page references; TXT and Markdown are accepted.
- **Chunking — RecursiveCharacterTextSplitter:** 900-character chunks and 150-character overlap are an initial baseline. The correct size should be selected by evaluation, not guesswork.
- **Embeddings — OpenAI `text-embedding-3-small`:** convert chunks/questions to vectors. Indexing sends document text to the provider.
- **Vector DB — Chroma:** persist embeddings, text chunks and metadata on disk. It makes semantic similarity search possible without running a remote DB.
- **Retrieval — Chroma similarity search:** return top-k chunks for the query. This is the evidence retrieval step.
- **Generation — LangChain prompt + ChatOpenAI:** generate an answer using the retrieved context; prompt requests inline source labels and abstention when evidence is insufficient.
- **UI grounding — citations and excerpt panel:** lets a reviewer check which retrieved passages were provided to the model.

## High-probability questions and answer ideas

### Why RAG instead of fine-tuning?
RAG is better for a document assistant whose source material changes. Documents can be indexed without retraining model weights, and retrieved excerpts give a reviewer a way to inspect the evidence. Fine-tuning might improve style or a specialized behavior, but it is not the first choice for keeping a model up to date with changing reference documents.

### What is the role of embeddings?
An embedding model turns text into a numerical vector. Similar concepts can have vectors near each other even when the wording differs. We embed the document chunks once at indexing time and embed each question at query time, then search for nearby vectors.

### Why Chroma?
For the prototype it is a simple persistent vector store that runs locally and integrates with LangChain. At production scale, I would compare managed options such as Azure AI Search, PostgreSQL with pgvector, or a managed vector database based on the organisation's infrastructure, access patterns, filtering requirements, scale, and security needs.

### Why LangChain?
It standardizes document objects, chunking, embedding interfaces, vector store access, prompt templates, and model invocation. It speeds up integration, but I still need to understand and test each step instead of treating the framework as a black box.

### How do you reduce hallucination?
Retrieve evidence first, send only selected passages to the model, request citations, instruct it to acknowledge missing evidence, and display the retrieved excerpts. This reduces risk but does not eliminate hallucinations. I would test supported and unsupported questions and review citation correctness.

### How would you evaluate retrieval quality?
Create a representative question set with expected source documents or chunks. Measure Recall@k or whether the correct evidence is present among the top-k results. Then separately evaluate answer correctness, groundedness, source citation accuracy, latency, cost, and refusal behavior on unsupported questions.

### What happens if the PDF is scanned?
The current parser extracts embedded text, so an image-only PDF may return no text. I would detect low or empty extraction and provide a clear message. If OCR were in scope, I would add a suitable OCR pipeline and test extraction quality rather than silently indexing an empty page.

### How do you avoid duplicate indexing?
This prototype deletes existing chunks by source filename before adding fresh chunks. For production, source identity should be more robust than filename alone: use stable IDs, content hashes, version metadata, and deletion/update workflows.

### What are the security gaps?
This is a local learning app, not a secure multi-user service. Source text is sent to an external API for embeddings and retrieved context is sent for generation. Before any sensitive deployment, I would review provider terms/data handling, use approved infrastructure, add authentication/authorization, isolate users or tenants, secure secrets, encrypt data in transit and at rest, audit access, and define retention/deletion procedures. I would never use real patient data in this demo.

### Why not use agents?
The current problem is document question answering, which is well served by a transparent retrieval pipeline. An agent adds autonomy and tool selection, which can introduce complexity and risks without clear value. I would add an agent only if a user workflow requires multi-step planning or controlled tool use.

## Demo script (about 3 minutes)

1. Explain the intended user: someone who needs answers grounded in technical reference documents.
2. In Document Library, index the three synthetic sample docs.
3. Ask: “What happens if a PDF is scanned and has no selectable text?”
4. Expand Retrieved Source Passages and show the source label plus excerpt.
5. Ask: “What security controls would be needed before a real deployment?”
6. Ask an unsupported question and discuss why evidence thresholds and abstention should be evaluated.
7. Close with a next step: build a labelled evaluation set and compare chunking/retrieval settings before choosing production infrastructure.

## 90-minute hackathon prioritization

- 0–10 min: clarify user, pain point, success criterion, and constraints.
- 10–20 min: create the smallest architecture and run a first vertical slice.
- 20–50 min: implement ingestion/retrieval/UI happy path.
- 50–65 min: add source citations and one important validation/failure state.
- 65–80 min: run realistic tests and fix the biggest issue.
- 80–90 min: prepare a live demo and explain what is incomplete.

## Honest positioning

Use this project to discuss your design and implementation practice. Do not say this exact prototype was deployed at Vena Medical unless that is accurate. Describe your actual Vena work separately and use only details you can personally substantiate.
