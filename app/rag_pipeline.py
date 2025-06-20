from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  # ✅ Updated import


def chunk_pages(pages):
    texts = [p["text"] for p in pages]
    metadatas = [{"page": p["page"]} for p in pages]

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.create_documents(texts, metadatas=metadatas)
    return docs


def create_vectorstore(docs):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # ✅ Fixed model name
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore
