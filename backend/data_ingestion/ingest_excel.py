import os
import json
import pickle
import hashlib
import pandas as pd
from pathlib import Path
from langchain_core.documents import Document

EXCEL_DIR = "Data/EXCEL"
HASH_FILE = "data_ingestion/excel_hashes.json"
DOCS_OUTPUT = "data_ingestion/excel_docs.pkl"

def get_all_excel_files(root):
    return [str(p) for p in Path(root).rglob("*.xlsx")]

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def load_previous_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=2)

def load_excel_documents(paths):
    docs = []
    for path in paths:
        try:
            xls = pd.ExcelFile(path)
            for sheet_name in xls.sheet_names:
                df = xls.parse(sheet_name).fillna("")
                for i, row in df.iterrows():
                    content = "\n".join([f"{col}: {row[col]}" for col in df.columns])
                    relative = os.path.relpath(path, EXCEL_DIR)
                    doc = Document(
                        page_content=content,
                        metadata={
                            "source": os.path.basename(path),
                            "relative_path": relative,
                            "sheet": sheet_name,
                            "row": i
                        }
                    )
                    docs.append(doc)
        except Exception as e:
            print(f"❌ Error reading {path}: {e}")
    return docs

if __name__ == "__main__":
    paths = get_all_excel_files(EXCEL_DIR)
    current_hashes = {p: hash_file(p) for p in paths}
    previous_hashes = load_previous_hashes()

    if current_hashes != previous_hashes:
        print("🔄 Change detected in Excel files. Re-ingesting...")
        docs = load_excel_documents(paths)
        with open(DOCS_OUTPUT, "wb") as f:
            pickle.dump(docs, f)
        save_hashes(current_hashes)
        print(f"✅ Stored {len(docs)} documents to {DOCS_OUTPUT}")
    else:
        print("✅ No changes in Excel files.")
