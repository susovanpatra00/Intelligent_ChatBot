import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from backend.data_ingestion.ingest_pdf import (
    get_all_pdf_files,
    load_documents as load_pdf_documents,
    load_previous_hashes as load_pdf_hashes,
    save_hashes as save_pdf_hashes,
    hash_file as hash_pdf_file
)

from backend.data_ingestion.ingest_excel import (
    get_all_excel_files,
    load_excel_documents,
    load_previous_hashes as load_excel_hashes,
    save_hashes as save_excel_hashes,
    hash_file as hash_excel_file
)

# ==== Paths ====
DATA_DIR = "Data"
PDF_DOCS_FILE = "backend/data_ingestion/pdf_docs.pkl"
EXCEL_DOCS_FILE = "backend/data_ingestion/excel_docs.pkl"
PDF_VECTOR_DIR = "backend/vectorstore/vectorstore_pdf"
EXCEL_VECTOR_DIR = "backend/vectorstore/vectorstore_excel"

# ==== Embedding Function ====
def embed_and_store(documents, path):
    embedder = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        encode_kwargs={"normalize_embeddings": True}
    )
    db = FAISS.from_documents(documents, embedder)
    db.save_local(path)
    print(f"✅ Embeddings stored in {path}")

# ==== PDF Embedding ====
pdf_paths = get_all_pdf_files(os.path.join(DATA_DIR, "PDF"))
pdf_current_hashes = {path: hash_pdf_file(path) for path in pdf_paths}
pdf_prev_hashes = load_pdf_hashes()

if pdf_current_hashes != pdf_prev_hashes:
    print("📄 Rebuilding PDF embeddings...")
    pdf_docs = load_pdf_documents(pdf_paths)
    with open(PDF_DOCS_FILE, "wb") as f:
        pickle.dump(pdf_docs, f)
    embed_and_store(pdf_docs, PDF_VECTOR_DIR)
    save_pdf_hashes(pdf_current_hashes)
else:
    print("✅ PDF vectorstore up to date.")

# ==== Excel Embedding ====
excel_paths = get_all_excel_files(os.path.join(DATA_DIR, "EXCEL"))
excel_current_hashes = {path: hash_excel_file(path) for path in excel_paths}
excel_prev_hashes = load_excel_hashes()

if excel_current_hashes != excel_prev_hashes:
    print("📊 Rebuilding Excel embeddings...")
    excel_docs = load_excel_documents(excel_paths)
    with open(EXCEL_DOCS_FILE, "wb") as f:
        pickle.dump(excel_docs, f)
    embed_and_store(excel_docs, EXCEL_VECTOR_DIR)
    save_excel_hashes(excel_current_hashes)
else:
    print("✅ Excel vectorstore up to date.")
