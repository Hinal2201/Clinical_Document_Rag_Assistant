from langchain_core.documents import Document

from rag_engine import _basename, _source_label, split_documents


def test_basename_removes_path_components():
    assert _basename(r"C:\private\patient_notes.txt") == "patient_notes.txt"


def test_split_documents_preserves_source_metadata():
    text = ("Document processing retrieves evidence from chunked text. " * 60).strip()
    docs = [Document(page_content=text, metadata={"source": "sample.md", "page": 2})]
    chunks = split_documents(docs)
    assert len(chunks) > 1
    assert all(chunk.metadata["source"] == "sample.md" for chunk in chunks)
    assert all(chunk.metadata["page"] == 2 for chunk in chunks)
    assert all(chunk.page_content.strip() for chunk in chunks)


def test_source_label_displays_pdf_page_and_excerpt():
    doc = Document(page_content="A relevant retrieved passage.", metadata={"source": "report.pdf", "page": 3})
    result = _source_label(doc, 1)
    assert result["label"] == "[S1] report.pdf, page 3"
    assert "Page: 3" in result["metadata"]
    assert result["excerpt"] == "A relevant retrieved passage."
