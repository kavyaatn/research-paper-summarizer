# main.py
# Set environment variables and patch modules before importing anything
import os
os.environ["STREAMLIT_WATCHER_IGNORE_MODULES"] = "torch,torchaudio,torchvision"

# Initialize asyncio loop first
import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Create empty torch.classes to prevent errors
import sys
import types
import torch
if not hasattr(torch, 'classes'):
    torch.classes = types.ModuleType('torch.classes')
    sys.modules['torch.classes'] = torch.classes

# Now import remaining modules
import streamlit as st
from app.pdf_utils import extract_text_from_pdf
from app.rag_pipeline import chunk_pages, create_vectorstore
from app.summarizer import summarize_with_citations
import warnings

# 🩹 Patch for torch.classes error
if not hasattr(torch, "classes"):
    torch.classes = type("classes", (), {})()

# 🛠️ Fix for asyncio error
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

warnings.filterwarnings("ignore", category=UserWarning)

st.set_page_config(page_title="HF Research Summarizer", layout="wide")
st.title("📄 Research Paper Summarizer")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    st.write("File uploaded:", uploaded_file.name)
    
    with st.spinner("📄 Extracting text from PDF..."):
        pages = extract_text_from_pdf(uploaded_file)
        st.write(f"Extracted {len(pages)} pages from PDF")
        if len(pages) > 0:
            st.write("Preview of first page:", pages[0]["text"][:200] + "...")

    with st.spinner("🧱 Chunking text and creating vector store..."):
        docs = chunk_pages(pages)
        st.write(f"Created {len(docs)} chunks from the text")
        vs = create_vectorstore(docs)
        retriever = vs.as_retriever()
        relevant_chunks = retriever.invoke("Summarize this paper.")
        st.write(f"Retrieved {len(relevant_chunks)} relevant chunks for summarization")

    if st.button("🧠 Summarize"):
        with st.spinner("📡 Sending to Hugging Face API..."):
            try:
                summary = summarize_with_citations(relevant_chunks, "Summarize this paper.")
                st.subheader("📌 Summary")
                st.markdown(summary)
            except Exception as e:
                st.error(f"❌ Summary failed: {str(e)}")
                st.error("Full error:")
                st.exception(e)
