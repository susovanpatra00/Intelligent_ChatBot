import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))



import os
import pickle
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not found in environment!"

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

# ==== Base Path ====
BASE_DIR = Path(__file__).resolve().parent.parent.parent 

DATA_DIR = BASE_DIR / "Data"
PDF_DIR = DATA_DIR / "PDF"
EXCEL_DIR = DATA_DIR / "EXCEL"

PDF_DOCS_FILE = BASE_DIR / "backend" / "data_ingestion" / "pdf_docs.pkl"
EXCEL_DOCS_FILE = BASE_DIR / "backend" / "data_ingestion" / "excel_docs.pkl"
PDF_VECTOR_DIR = BASE_DIR / "backend" / "vectorstore" / "vectorstore_pdf"
EXCEL_VECTOR_DIR = BASE_DIR / "backend" / "vectorstore" / "vectorstore_excel"

# ==== Embedding Function ====
# def embed_and_store(documents, path):
#     embedder = OpenAIEmbeddings(model="text-embedding-3-large")
#     db = FAISS.from_documents(documents, embedder)
#     db.save_local(str(path))
#     print(f"✅ Embeddings stored in {path}")


def embed_and_store(documents, path, batch_size=100):
    embedder = OpenAIEmbeddings(model="text-embedding-3-small")
    all_texts = [doc.page_content for doc in documents]
    all_metadatas = [doc.metadata for doc in documents]

    # Split into batches
    db = None
    for i in range(0, len(all_texts), batch_size):
        batch_texts = all_texts[i:i+batch_size]
        batch_metadatas = all_metadatas[i:i+batch_size]
        batch_docs = [Document(page_content=t, metadata=m) for t, m in zip(batch_texts, batch_metadatas)]
        if db is None:
            db = FAISS.from_documents(batch_docs, embedder)
        else:
            db.add_documents(batch_docs)
    db.save_local(str(path))
    print(f"✅ Embeddings stored in {path}")



# ==== PDF Embedding ====
pdf_paths = get_all_pdf_files(PDF_DIR)
pdf_current_hashes = {str(path): hash_pdf_file(path) for path in pdf_paths}
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
excel_paths = get_all_excel_files(EXCEL_DIR)
excel_current_hashes = {str(path): hash_excel_file(path) for path in excel_paths}
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
