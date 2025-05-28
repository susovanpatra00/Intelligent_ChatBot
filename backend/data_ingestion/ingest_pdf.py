# import os
# import hashlib
# import json
# from pathlib import Path
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_core.documents import Document
# import pickle

# PDF_ROOT = "Data/PDF"
# HASH_FILE = "data_ingestion/pdf_hashes.json"

# def get_all_pdf_files(root):
#     return [str(p) for p in Path(root).rglob("*.pdf")]

# def hash_file(filepath):
#     with open(filepath, "rb") as f:
#         return hashlib.md5(f.read()).hexdigest()

# def load_previous_hashes():
#     if os.path.exists(HASH_FILE):
#         with open(HASH_FILE, "r") as f:
#             return json.load(f)
#     return {}

# def save_hashes(hashes):
#     with open(HASH_FILE, "w") as f:
#         json.dump(hashes, f, indent=2)

# def load_documents(pdf_paths):
#     docs = []
#     for path in pdf_paths:
#         loader = PyPDFLoader(path)
#         pages = loader.load()
#         full_text = "\n".join(page.page_content for page in pages)
#         relative_path = os.path.relpath(path, PDF_ROOT)
#         doc = Document(
#             page_content=full_text,
#             metadata={
#                 "source": os.path.basename(path),
#                 "relative_path": relative_path
#             }
#         )
#         docs.append(doc)
#     return docs

# if __name__ == "__main__":
#     print("📂 Scanning for PDF changes...")
#     pdf_paths = get_all_pdf_files(PDF_ROOT)
#     current_hashes = {path: hash_file(path) for path in pdf_paths}
#     previous_hashes = load_previous_hashes()

#     if current_hashes != previous_hashes:
#         print("🔄 Changes detected. Re-ingesting PDFs...")
#         docs = load_documents(pdf_paths)

#         with open("Data_Ingestion/pdf_docs.pkl", "wb") as f:
#             pickle.dump(docs, f)

#         save_hashes(current_hashes)
#         print(f"✅ Stored {len(docs)} documents to pdf_docs.pkl")
#     else:
#         print("✅ No changes found. PDFs are up-to-date.")







# Version 2.0
import os
import hashlib
import json
import pickle
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

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
    for path in pdf_paths:
        loader = PyPDFLoader(path)
        pages = loader.load()
        full_text = "\n".join(page.page_content for page in pages)
        relative_path = os.path.relpath(path, PDF_ROOT)
        doc = Document(
            page_content=full_text,
            metadata={
                "source": os.path.basename(path),
                "relative_path": relative_path
            }
        )
        docs.append(doc)
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
