"""Streamlit interface for the contract review agent."""

import sys
import uuid
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from contract_review.agent.graph import build_graph  # noqa: E402
from contract_review.config import settings  # noqa: E402
from contract_review.rag.chunker import chunk_pages  # noqa: E402
from contract_review.rag.document_loader import load_upload  # noqa: E402
from contract_review.rag.ingestion import store_chunks  # noqa: E402
from contract_review.rag.vector_store import create_session_collection  # noqa: E402

st.set_page_config(page_title="Contract Review Agent", page_icon="⚖️", layout="wide")
st.title("⚖️ Contract Review Agent")
st.caption("Ask questions about uploaded agreements and inspect the clauses that support each answer.")
st.warning("Educational aid only, not legal advice. Have a qualified lawyer verify findings before acting.")

with st.sidebar:
    st.header("1 · Upload contracts")
    uploads = st.file_uploader("PDF, DOCX, or TXT", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    process = st.button("Process contracts", type="primary", disabled=not uploads)
    st.divider()
    st.markdown("**Example questions**")
    st.markdown("- Can the vendor increase the price?\n- How can either party terminate?\n- Is liability capped?\n- What happens if delivery is late?")

if process and uploads:
    pages, errors = [], []
    for upload in uploads:
        try:
            pages.extend(load_upload(upload.name, upload.getvalue()))
        except Exception as exc:
            errors.append(f"{upload.name}: {exc}")
    for error in errors:
        st.error(error)
    chunks = chunk_pages(pages, settings.chunk_size, settings.chunk_overlap)
    if chunks:
        collection = create_session_collection(uuid.uuid4().hex)
        store_chunks(chunks, collection)
        st.session_state.collection = collection
        st.session_state.document_names = [upload.name for upload in uploads]
        st.success(f"Indexed {len(pages)} sections into {len(chunks)} searchable chunks.")
    else:
        st.session_state.pop("collection", None)
        st.warning("No readable text was found. Scanned PDFs need OCR before they can be searched.")

collection = st.session_state.get("collection")
if collection is None:
    st.subheader("How it works")
    st.write("Upload a contract, process it, and ask a question. The agent retrieves relevant passages, drafts an evidence-based answer, and displays the source pages.")
else:
    st.subheader("2 · Ask about the documents")
    st.caption("Loaded: " + ", ".join(st.session_state.get("document_names", [])))
    with st.form("ask_form"):
        question = st.text_input("Question", placeholder="Can the vendor increase the price?")
        submitted = st.form_submit_button("Ask")
    if submitted and question.strip():
        graph = build_graph(collection)
        with st.spinner("Reviewing relevant clauses…"):
            state = graph.invoke({"question": question.strip()})
        st.markdown("### Answer")
        st.markdown(state.get("answer", "No answer was generated."))
        if state.get("demo_mode"):
            st.caption("No LLM configured: showing retrieved evidence. Set LLM_PROVIDER and credentials in .env for synthesized answers.")
        if state.get("chunks"):
            st.markdown("### Supporting clauses")
            for number, chunk in enumerate(state["chunks"], start=1):
                with st.expander(f"[{number}] {chunk.source} · {chunk.location} · distance {chunk.distance:.3f}"):
                    st.write(chunk.text)
