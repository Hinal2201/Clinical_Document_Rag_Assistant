# Synthetic Demo Note: Troubleshooting and Support Workflow

This is synthetic training content for a software prototype. It is not clinical or operational authority.

## First checks when indexing fails
1. Confirm that an API key is configured and is authorized for the selected embedding model.
2. Confirm that the machine has network access to the API provider.
3. Check whether the PDF contains selectable text. Scanned PDFs may require OCR, which is not implemented in this demo.
4. Check the terminal output for the first error message rather than relying only on the last error line.
5. Confirm that the correct Python virtual environment is active and that the project dependencies installed successfully.

## First checks when the assistant cannot answer
1. Confirm that at least one document has been indexed.
2. Inspect the retrieved source passages to see whether the relevant text is present.
3. Try a more specific question using wording from the document.
4. If the expected passage is not retrieved, evaluate chunk size, overlap, embedding model, and the number of retrieved chunks.
5. If the passage is retrieved but the answer is incorrect, review the prompt, model behavior, context length, and test set.

## Retrieval evaluation
A useful evaluation set contains realistic questions, expected supporting documents, and a note explaining what a correct answer should include. Measure whether the correct source appears in the retrieved results before measuring answer quality. Do not judge RAG quality only by whether a response sounds fluent.
