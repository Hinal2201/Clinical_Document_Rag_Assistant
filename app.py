from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from rag_engine import (
    DEMO_DOCS_DIR,
    VECTOR_DB_DIR,
    get_index_stats,
    index_documents,
    load_demo_documents,
    load_uploaded_documents,
    query_rag,
)

load_dotenv()

st.set_page_config(
    page_title="Clinical Document AI | RAG Workbench",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """
    <style>
      .main-title {font-size: 2.15rem; font-weight: 750; margin-bottom: .1rem;}
      .sub-title {color: #64748b; margin-bottom: 1.1rem;}
      div[data-testid="stMetric"] {border: 1px solid rgba(128,128,128,.25); padding: 12px; border-radius: 12px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Clinical Document AI Workbench</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload documents, index their meaning in a persistent vector database, and ask questions with source-grounded RAG.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "OpenAI API key",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
        help="Used for embeddings and answer generation. Keep this secret; never commit it to GitHub.",
    )
    chat_model = st.text_input(
        "Chat model",
        value=os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini"),
        help="Change this to a model available to your API account.",
    )
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    top_k = st.slider("Retrieved chunks per question", min_value=2, max_value=8, value=4)
    st.caption(f"Embedding model: `{embedding_model}`")
    st.caption(f"Vector database: `{VECTOR_DB_DIR.relative_to(Path.cwd()) if VECTOR_DB_DIR.is_relative_to(Path.cwd()) else VECTOR_DB_DIR}`")
    st.divider()
    st.markdown("**Data safety**")
    st.caption("Use synthetic or non-sensitive demo documents only. This sample app is not approved for patient data or clinical decision-making.")

chat_tab, docs_tab, architecture_tab = st.tabs(["💬 Ask your documents", "📚 Document library", "⚙️ How it works"])

with docs_tab:
    left, right = st.columns([1.1, 1])
    with left:
        st.subheader("Add documents")
        uploads = st.file_uploader(
            "Upload PDF, TXT, or Markdown files",
            type=["pdf", "txt", "md", "markdown"],
            accept_multiple_files=True,
            help="PDFs must contain selectable text. OCR for scanned PDFs is not included in this prototype.",
        )
        if st.button("Index uploaded documents", type="primary", disabled=not bool(uploads), use_container_width=True):
            if not api_key.strip():
                st.error("Enter an OpenAI API key in the sidebar first. Embeddings are needed to build the vector index.")
            else:
                try:
                    docs = load_uploaded_documents(uploads)
                    if not docs:
                        st.warning("No readable text was found. A scanned PDF may need OCR first.")
                    else:
                        with st.spinner("Splitting documents, creating embeddings, and writing to Chroma..."):
                            chunk_count = index_documents(docs, api_key=api_key.strip(), embedding_model=embedding_model)
                        st.success(f"Indexed {len(docs)} document page(s)/text file(s) into {chunk_count} chunks.")
                        st.rerun()
                except Exception as exc:
                    st.error(f"Indexing failed: {exc}")
                    st.caption("Check the API key, network connection, and that the PDF contains extractable text.")

        st.markdown("#### Quick-start sample documents")
        st.write("Load the bundled synthetic workflow, data-handling, and troubleshooting notes to practise without using real clinical material.")
        if st.button("Index bundled demo documents", use_container_width=True):
            if not api_key.strip():
                st.error("Enter an OpenAI API key in the sidebar first.")
            else:
                try:
                    docs = load_demo_documents()
                    with st.spinner("Embedding demo notes and saving to Chroma..."):
                        chunk_count = index_documents(docs, api_key=api_key.strip(), embedding_model=embedding_model)
                    st.success(f"Indexed the bundled notes into {chunk_count} chunks.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Demo indexing failed: {exc}")

    with right:
        st.subheader("Indexed collection")
        if not api_key.strip():
            st.info("Add an API key to connect to the embedding model and inspect the indexed collection.")
        else:
            try:
                stats = get_index_stats(api_key=api_key.strip(), embedding_model=embedding_model)
                m1, m2 = st.columns(2)
                m1.metric("Indexed chunks", stats["chunk_count"])
                m2.metric("Source files", stats["source_count"])
                if stats["sources"]:
                    st.markdown("**Sources in Chroma**")
                    for src in stats["sources"]:
                        st.write(f"• {src}")
                else:
                    st.caption("No documents indexed yet. Add the demo notes or upload a file.")
            except Exception as exc:
                st.warning(f"The vector collection isn't available yet: {exc}")

with chat_tab:
    st.subheader("Ask a question grounded in your documents")
    st.caption("Answers use retrieved chunks from the local Chroma database and show the passages that informed the response.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    control1, control2 = st.columns([1, 6])
    with control1:
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("sources"):
                with st.expander("Retrieved source passages"):
                    for source in message["sources"]:
                        st.markdown(f"**{source['label']}**")
                        st.caption(source["metadata"])
                        st.write(source["excerpt"])

    question = st.chat_input("For example: What steps are used to prepare a document for retrieval?")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            if not api_key.strip():
                response = "Enter an OpenAI API key in the sidebar, then index the bundled demo documents or upload your own documents to start asking questions."
                st.info(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "sources": []})
            else:
                try:
                    with st.spinner("Searching Chroma and generating a grounded answer..."):
                        result = query_rag(
                            question=question,
                            api_key=api_key.strip(),
                            chat_model=chat_model.strip() or "gpt-4.1-mini",
                            embedding_model=embedding_model,
                            top_k=top_k,
                        )
                    st.markdown(result["answer"])
                    with st.expander("Retrieved source passages", expanded=True):
                        for source in result["sources"]:
                            st.markdown(f"**{source['label']}**")
                            st.caption(source["metadata"])
                            st.write(source["excerpt"])
                    st.session_state.messages.append(
                        {"role": "assistant", "content": result["answer"], "sources": result["sources"]}
                    )
                except Exception as exc:
                    response = f"I couldn't complete the retrieval request: {exc}"
                    st.error(response)
                    st.caption("Make sure documents have been indexed and the model names/API key are valid.")
                    st.session_state.messages.append({"role": "assistant", "content": response, "sources": []})

with architecture_tab:
    st.subheader("End-to-end RAG architecture")
    flow = [
        ("1. Ingest", "Read selectable text from PDF/TXT/Markdown and attach source metadata."),
        ("2. Chunk", "Split long documents into overlapping passages to fit retrieval and model context windows."),
        ("3. Embed", f"Convert passages to vectors using `{embedding_model}`."),
        ("4. Store", "Persist chunk text, vectors, and metadata in a local Chroma vector database."),
        ("5. Retrieve", "Embed the user's question and retrieve the most similar passages."),
        ("6. Generate", f"Use LangChain and `{chat_model or 'gpt-4.1-mini'}` to answer from the retrieved context."),
        ("7. Ground", "Display source filenames/page numbers and the actual retrieved passages for inspection."),
    ]
    for title, detail in flow:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(detail)
    st.warning("Prototype boundary: this is a document Q&A demo. It is not a diagnostic system, is not validated for clinical use, and should not be used with protected health information.")

st.divider()
st.caption("Practice prototype • Local Chroma persistence • LangChain retrieval pipeline • Use synthetic, non-sensitive documents only")
