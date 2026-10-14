# Synthetic Demo Note: Data Handling and Privacy

This is synthetic training content for a software prototype. It is not legal, regulatory, or security advice.

## Prototype data boundary
Use synthetic or non-sensitive documents during demonstrations. Do not upload patient records, identifiable health information, confidential company documents, access tokens, or other restricted information.

## External API boundary
The prototype uses an external embedding API to convert documents and questions into vectors, and an external chat API to generate responses. That means document text sent for indexing and retrieved context sent for answering leave the local computer. A real organization must review its security, privacy, contractual, residency, retention, and access-control requirements before choosing a provider or sending data.

## Local vector database
Chroma persists the indexed chunks and metadata in the project's data/chroma_db folder. These local files should be treated as sensitive if non-public documents are ever indexed. The sample .gitignore excludes this folder from Git.

## Production considerations
A production implementation should include authenticated users, per-user or per-tenant authorization, encrypted storage and transport, audit logging, secrets management, retention/deletion workflows, monitoring, safe backups, and an approved deployment environment. Access filters must be enforced on the server rather than trusted to the language model.
