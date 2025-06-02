import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not found in environment!"
from openai import OpenAI
from config import ENABLE_PDF, ENABLE_EXCEL

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Path Setup ===
BASE_DIR = Path(__file__).resolve().parent.parent
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

PDF_VECTORSTORE = VECTORSTORE_DIR / "vectorstore_pdf"
EXCEL_VECTORSTORE = VECTORSTORE_DIR / "vectorstore_excel"
DATA_DIR = BASE_DIR.parent / "Data"  # go up to DO33_Final/
PDF_DATA_DIR = DATA_DIR / "PDF"
EXCEL_DATA_DIR = DATA_DIR / "EXCEL"

SCORE_THRESHOLD = 0.99

EMBEDDER = OpenAIEmbeddings(model="text-embedding-3-large")
print("Using OpenAI Embedding model:", EMBEDDER.model)
client = OpenAI(api_key=OPENAI_API_KEY)
LLM_MODEL = "gpt-4o-mini"

# === Load Vector Stores (conditional) ===
pdf_vectordb = FAISS.load_local(str(PDF_VECTORSTORE), EMBEDDER, allow_dangerous_deserialization=True) if ENABLE_PDF and PDF_VECTORSTORE.exists() else None
excel_vectordb = FAISS.load_local(str(EXCEL_VECTORSTORE), EMBEDDER, allow_dangerous_deserialization=True) if ENABLE_EXCEL and EXCEL_VECTORSTORE.exists() else None

def get_all_pdf_chunks(parent_pdf_id, vectordb):
    '''
    This function fetches all chunks from the same PDF using parent_pdf_id
    '''

    all_chunks = []
    for doc in vectordb.docstore._dict.values():
        if doc.metadata.get("parent_pdf_id") == parent_pdf_id:
            all_chunks.append(doc)
    # Optionally, sort by chunk index if you added it
    all_chunks.sort(key=lambda d: d.metadata.get("chunk_index", 0))
    return all_chunks

def search_similar_documents(query, k=10):
    all_docs = []

    if pdf_vectordb:
        pdf_results = pdf_vectordb.similarity_search_with_score(query, k=k)
        added_pdf_ids = set()
        print("Top-matching PDF chunks:")
        for doc, score in pdf_results:
            if score <= SCORE_THRESHOLD:
                parent_pdf_id = doc.metadata.get("parent_pdf_id")
                print(f"  Chunk from PDF: {doc.metadata.get('source')} | parent_pdf_id: {parent_pdf_id} | Score: {score:.4f}")
                if parent_pdf_id and parent_pdf_id not in added_pdf_ids:
                    # Fetch all chunks from this PDF
                    pdf_chunks = get_all_pdf_chunks(parent_pdf_id, pdf_vectordb)
                    combined_content = "\n\n".join(chunk.page_content for chunk in pdf_chunks)
                    all_docs.append({
                        "FileName": doc.metadata.get("source", "Unknown"),
                        "FileLocation": str(PDF_DATA_DIR / doc.metadata.get("relative_path", "")),
                        "Content": combined_content,
                        "score": score,
                        "metadata": doc.metadata
                    })
                    added_pdf_ids.add(parent_pdf_id)

    if excel_vectordb:
        excel_results = excel_vectordb.similarity_search_with_score(query, k=k)
        for doc, score in excel_results:
            if score <= SCORE_THRESHOLD:
                all_docs.append({
                    "FileName": doc.metadata.get("source", "Unknown"),
                    "FileLocation": str(EXCEL_DATA_DIR / doc.metadata.get("relative_path", "")),
                    "Content": doc.page_content,
                    "score": score,
                    "metadata": doc.metadata
                })

    return sorted(all_docs, key=lambda d: d["score"])[:k]

def generate_direct_answer(query, top_docs):
    context = ""
    for doc in top_docs:
        context += f"{doc['Content']}\n\n"


    prompt = f"""
You are a helpful assistant. 
Answer the user's question strictly based on the information provided below. 
If the information is incomplete, answer as best you can using what is available, "DO NOT USE YOUR OWN KNOWLEDGE"
Only reply "I’m sorry, I couldn’t find relevant information in the provided documents." if the information below is completely unrelated or empty.

Format your answer clearly and engagingly:
- **Bold** important terms or phrases.
- *Italicize* for emphasis.
- Use bullet points or numbered lists if helpful.
- Do NOT mention document numbers, file names, or scores.

Information:
{context}

Question:
{query}
    """

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
