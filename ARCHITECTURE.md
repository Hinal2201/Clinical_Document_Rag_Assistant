# Architecture and Decision Log

## High-level flow

```text
PDF / TXT / Markdown
        |
        v
Parser + source metadata (filename, optional page)
        |
        v
RecursiveCharacterTextSplitter (900 chunk / 150 overlap)
        |
        v
OpenAI Embeddings (text-embedding-3-small)
        |
        v
Chroma persistent vector store (data/chroma_db)

User question
        |
        v
Question embedding
        |
        v
Chroma top-k similarity retrieval
        |
        v
LangChain prompt + retrieved chunks + question
        |
        v
Chat model (gpt-4.1-mini by default)
        |
        v
Answer with [S1]-style citations + retrieved source excerpts
```

## Decisions

| Decision | Reason | Trade-off / next step |
|---|---|---|
| Streamlit instead of a React/API split | Faster working demo; fewer services to run locally | Split frontend/backend if multiple clients or independent scaling are required |
| Chroma local persistent DB | No remote vector service needs to be provisioned | Local storage is not a security boundary; add backup, encryption, authorization and data lifecycle controls for production |
| OpenAI embedding API | Simple, strong baseline and small dependency surface | Requires network/API key and sends source text to provider; evaluate a locally hosted embedding model when privacy or data residency requires it |
| `text-embedding-3-small` | Practical low-complexity semantic search baseline | Evaluate against real query/document pairs before accepting retrieval quality |
| 900-character chunks / 150 overlap | A clear baseline balancing context size and passage detail | Tune chunking using Recall@k and answer metrics; character count is not token count |
| PDF/TXT/MD only | Keeps parsing simple during a hackathon | Add DOCX, HTML, OCR or DICOM only when the product requirement needs them |
| Citation labels plus excerpt viewer | Makes retrieval inspectable | A model can still attach an incorrect citation; test that every cited label corresponds to actual supporting evidence |
| Prompt-level untrusted context warning | Basic protection against following instructions embedded in retrieved documents | Prompting alone is not a complete prompt-injection defense; use controlled tools and strong separation of data/instructions |

## Production gaps

Authentication and per-tenant isolation, authorization filters, key management, privacy review, encryption, audit logs, monitoring, request limits, content scanning, document deletion/versioning, vector-store backups, prompt-injection evaluation, RAG evaluation dataset, model/cost/latency tracking, approved cloud architecture, and domain review.
