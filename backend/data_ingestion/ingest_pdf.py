import os
import hashlib
import json
import pickle
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent  # backend/ingestion
PROJECT_ROOT = BASE_DIR.parent.parent       # DO33_Final/

PDF_ROOT = PROJECT_ROOT / "Data" / "PDF"
HASH_FILE = BASE_DIR / "pdf_hashes.json"
DOCS_OUTPUT = BASE_DIR / "pdf_docs.pkl"

def get_all_pdf_files(root):
    return [str(p) for p in Path(root).rglob("*.pdf")]

def hash_file(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def load_previous_hashes():
    if HASH_FILE.exists():
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    os.makedirs(HASH_FILE.parent, exist_ok=True)
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=2)

def load_documents(pdf_paths):
    docs = []
    # Approximate 800 words ≈ 4000 characters, 200 words ≈ 1000 characters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    for path in pdf_paths:
        loader = PyPDFLoader(path)
        pages = loader.load()
        full_text = "\n".join(page.page_content for page in pages)
        relative_path = os.path.relpath(path, PDF_ROOT)
        file_name = os.path.basename(path)
        parent_pdf_id = relative_path  

        # Split into chunks with metadata
        chunks = text_splitter.create_documents(
            [full_text],
            metadatas=[{
                "source": file_name,
                "relative_path": relative_path,
                "parent_pdf_id": parent_pdf_id
            }]
        )
        docs.extend(chunks)
    return docs


if __name__ == "__main__":
    print("📂 Scanning for PDF changes...")
    pdf_paths = get_all_pdf_files(PDF_ROOT)
    current_hashes = {path: hash_file(path) for path in pdf_paths}
    previous_hashes = load_previous_hashes()

    if current_hashes != previous_hashes:
        print("🔄 Changes detected. Re-ingesting PDFs...")
        docs = load_documents(pdf_paths)

        os.makedirs(DOCS_OUTPUT.parent, exist_ok=True)
        with open(DOCS_OUTPUT, "wb") as f:
            pickle.dump(docs, f)

        save_hashes(current_hashes)
        print(f"✅ Stored {len(docs)} documents to {DOCS_OUTPUT.name}")
    else:
        print("✅ No changes found. PDFs are up-to-date.")


