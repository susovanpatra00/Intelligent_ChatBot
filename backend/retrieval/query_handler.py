# import os
# import hashlib
# import json
# from pathlib import Path
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# load_dotenv()
# from config import ENABLE_PDF, ENABLE_EXCEL

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # === Embedding + LLM Setup ===
# EMBEDDER = HuggingFaceEmbeddings(
#     model_name="BAAI/bge-base-en-v1.5",
#     encode_kwargs={"normalize_embeddings": True}
# )
# LLM_MODEL = "gpt-4o-mini"
# client = OpenAI(api_key=OPENAI_API_KEY)

# # === Vector Store Paths ===
# PDF_VECTORSTORE = "backend/vectorstore/vectorstore_pdf"
# EXCEL_VECTORSTORE = "backend/vectorstore/vectorstore_excel"
# SCORE_THRESHOLD = 0.7

# # === Load Vector Stores (optional based on flags) ===
# pdf_vectordb = FAISS.load_local(PDF_VECTORSTORE, EMBEDDER, allow_dangerous_deserialization=True) if ENABLE_PDF and Path(PDF_VECTORSTORE).exists() else None
# excel_vectordb = FAISS.load_local(EXCEL_VECTORSTORE, EMBEDDER, allow_dangerous_deserialization=True) if ENABLE_EXCEL and Path(EXCEL_VECTORSTORE).exists() else None

# def search_similar_documents(query, k=5):
#     all_docs = []

#     if pdf_vectordb:
#         pdf_results = pdf_vectordb.similarity_search_with_score(query, k=k)
#         for doc, score in pdf_results:
#             if score <= SCORE_THRESHOLD:
#                 all_docs.append({
#                     "FileName": doc.metadata.get("source", "Unknown"),
#                     "FileLocation": str(Path("Data/PDF") / doc.metadata.get("relative_path", "")),
#                     "Content": doc.page_content,
#                     "score": score,
#                     "metadata": doc.metadata
#                 })

#     if excel_vectordb:
#         excel_results = excel_vectordb.similarity_search_with_score(query, k=k)
#         for doc, score in excel_results:
#             if score <= SCORE_THRESHOLD:
#                 all_docs.append({
#                     "FileName": doc.metadata.get("source", "Unknown"),
#                     "FileLocation": str(Path("Data/EXCEL") / doc.metadata.get("relative_path", "")),
#                     "Content": doc.page_content,
#                     "score": score,
#                     "metadata": doc.metadata
#                 })

#     # Sort all combined results by score
#     return sorted(all_docs, key=lambda d: d["score"])[:k]

# def generate_direct_answer(query, top_docs):
#     context = ""
#     for i, doc in enumerate(top_docs, 1):
#         context += f"Document {i} (File: {doc['FileName']}, Score: {doc['score']:.4f}):\n{doc['Content']}\n\n"

#     prompt = f"""
# You are a helpful assistant that answers strictly **based on the provided document content**. 
# If the context does not contain relevant information, respond with:
# "I’m sorry, I couldn’t find relevant information in the provided documents."

# Ensure your response is clear, organized, and engaging by using the following formatting:

# 1. **Bold** important terms or phrases.
# 2. *Italic* for emphasis.
# 3. Use bullet points or numbered lists for structure.
# 4. Leave space between sections.

# Context:
# {context}

# Question:
# {query}
#     """

#     response = client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.3
#     )
#     # print("\nResponse from LLM Direct Answer:", response.choices[0].message.content.strip())
#     return response.choices[0].message.content.strip()











# Version 2.0
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
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

SCORE_THRESHOLD = 0.75

# === Embedding + LLM Setup ===
EMBEDDER = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5",
    encode_kwargs={"normalize_embeddings": True}
)
client = OpenAI(api_key=OPENAI_API_KEY)
LLM_MODEL = "gpt-4o-mini"

# === Load Vector Stores (conditional) ===
pdf_vectordb = FAISS.load_local(str(PDF_VECTORSTORE), EMBEDDER, allow_dangerous_deserialization=True) if ENABLE_PDF and PDF_VECTORSTORE.exists() else None
excel_vectordb = FAISS.load_local(str(EXCEL_VECTORSTORE), EMBEDDER, allow_dangerous_deserialization=True) if ENABLE_EXCEL and EXCEL_VECTORSTORE.exists() else None

def search_similar_documents(query, k=5):
    all_docs = []

    if pdf_vectordb:
        pdf_results = pdf_vectordb.similarity_search_with_score(query, k=k)
        for doc, score in pdf_results:
            if score <= SCORE_THRESHOLD:
                all_docs.append({
                    "FileName": doc.metadata.get("source", "Unknown"),
                    "FileLocation": str(PDF_DATA_DIR / doc.metadata.get("relative_path", "")),
                    "Content": doc.page_content,
                    "score": score,
                    "metadata": doc.metadata
                })

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
    for i, doc in enumerate(top_docs, 1):
        context += f"Document {i} (File: {doc['FileName']}, Score: {doc['score']:.4f}):\n{doc['Content']}\n\n"

    prompt = f"""
You are a helpful assistant that answers strictly **based on the provided document content**. 
If the context does not contain relevant information, respond with:
"I’m sorry, I couldn’t find relevant information in the provided documents."

Ensure your response is clear, organized, and engaging by using the following formatting:

1. **Bold** important terms or phrases.
2. *Italic* for emphasis.
3. Use bullet points or numbered lists for structure.
4. Leave space between sections.

Context:
{context}

Question:
{query}
    """

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
