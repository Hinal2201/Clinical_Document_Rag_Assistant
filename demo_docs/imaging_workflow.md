# Synthetic Demo Note: Document Processing Workflow

This is synthetic training content for a software prototype. It is not clinical guidance.

## Document ingestion
The demonstration assistant accepts PDF files that contain selectable text, UTF-8 text files, and Markdown files. Each PDF page is extracted independently so the page can be included in a source reference. Text-only Markdown and TXT files are treated as a single source document.

Scanned PDFs may produce no extracted text because the prototype does not include optical character recognition (OCR). A future version could add OCR after checking the user's document permissions and quality requirements.

## Chunking
The application splits source text into overlapping chunks. The sample uses a chunk size of approximately 900 characters and a 150-character overlap. Chunking helps fit long documents into retrieval and language-model context windows. Chunk size is a tunable parameter rather than a universal best value.

## Embeddings and vector storage
The application sends each text chunk to an embedding model, which transforms the text into a numerical vector. Chroma stores the vectors, source metadata, and original chunk text in a local persistent database folder. Similarity search returns chunks whose vectors are close to the question vector.

## Question answering
When a user asks a question, the application embeds the question, retrieves a small number of relevant chunks, and passes those chunks as context to a language model through LangChain. The assistant is instructed to answer from the provided context and cite labels such as [S1]. If the documents do not contain the answer, it should say that it could not find enough evidence.
