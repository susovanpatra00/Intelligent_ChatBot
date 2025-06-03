import os
import csv
import logging
import sys
from pathlib import Path
from urllib.parse import quote
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_session import Session
from concurrent.futures import ThreadPoolExecutor
sys.path.append(str(Path(__file__).resolve().parent.parent))

from retrieval.query_handler import search_similar_documents, generate_direct_answer
from reasoning.reasoner import generate_reasoning
from websearch.web_search import perform_web_search
from llm_response.final_responder import generate_final_answer
from rewrite.rewrite_query import rewrite_standalone_query
from spellchecker import SpellChecker
# ============================================================ #
from utils.file_helpers import log_interaction
import socket
import traceback
# ============================================================ #


spell = SpellChecker()
        
def correct_query(query):
    corrected_words = []
    for word in query.split():
        # Skip correction for all-uppercase or capitalized words
        if word.isupper() or word[0].isupper():
            corrected_words.append(word)
        else:
            correction = spell.correction(word)
            corrected_words.append(correction if correction is not None else word)
    return ' '.join(corrected_words)


    
# === Logging Setup ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
MAX_HISTORY = 4

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Or 'redis', 'mongodb', etc.
app.config['SECRET_KEY'] = 'secret-key'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
Session(app)
CORS(app, supports_credentials=True)


# === Directories ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
PDF_DIR = DATA_DIR / "PDF"
EXCEL_DIR = DATA_DIR / "EXCEL"
FEEDBACK_FILE = BASE_DIR / "feedback_log.csv"

# === Static File Routes ===
@app.route('/pdfs/<path:relative_path>')
def serve_pdf(relative_path):
    full_path = PDF_DIR / relative_path
    return send_from_directory(full_path.parent, full_path.name) if full_path.exists() else ("PDF not found", 404)

# @app.route('/excels/<path:relative_path>')
# def serve_excel(relative_path):
#     full_path = EXCEL_DIR / relative_path
#     return send_from_directory(full_path.parent, full_path.name) if full_path.exists() else ("Excel not found", 404)

@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.pop("history", None)
    return jsonify({"message": "Session history cleared."})



# === Chat Route ===
@app.route("/chat", methods=["POST"])
def chat():
    if "session_id" not in session:
        import uuid
        session["session_id"] = str(uuid.uuid4())

    data = request.json
    query = data.get("query", "")
    query = correct_query(query)
    use_reasoning = data.get("reasoning", False)
    use_web = data.get("web", False)

    if not query:
        return jsonify({"error": "Missing query"}), 400
    

    try:
        # --------------- modified ------------------- #
        history = session.get("history", [])
        history_strings = [f"{item['role'].capitalize()}: {item['content']}" for item in history]

        standalone_query = rewrite_standalone_query(history_strings, query)
        print(f"\nActual Query: {query} \nStandalone Query: {standalone_query}\n")
        # -------------------------------------------- #
        web = None
        retrieval_answer = None
        reasoning = None
        top_docs = []

        if use_web:
            with ThreadPoolExecutor() as executor:
                web = executor.submit(perform_web_search, query).result()
            final_answer = generate_final_answer(standalone_query, retrieval_answer, reasoning, web)
            
            # ============================================================ #
            try:
                log_interaction(query=query, answer=final_answer)
            except Exception as e:
                logger.error(f"Logging failed: {e}")
            # ============================================================ #

            return jsonify({
                "retrieval": None,
                "reasoning": None,
                "web": web,
                "final": final_answer,
                "sources": []
            })
        else:
            top_docs = search_similar_documents(standalone_query, k=5)
            retrieval_answer = generate_direct_answer(standalone_query, top_docs)
            if not use_reasoning:
                final_answer = retrieval_answer
            else:
                reasoning = generate_reasoning(query, retrieval_answer) 
                final_answer = generate_final_answer(standalone_query, retrieval_answer, reasoning)

            # ============================================================ #
            try:
                log_interaction(query=query, answer=final_answer)
            except Exception as e:
                logger.error(f"Logging failed: {e}")
            # ============================================================ #

            history.append({"role": "user", "content": query})
            history.append({"role": "assistant", "content": final_answer})
            history = history[-8:]
            session["history"] = history
            
            # Build source download links
            source_buttons = []
            for doc in top_docs:
                file_path = Path(doc["FileLocation"]).resolve()
                file_name = doc["FileName"]
    
                if PDF_DIR in file_path.parents:
                    base = PDF_DIR
                    route = "pdfs"
                else:
                    continue
    
                relative = file_path.relative_to(base)
                encoded_path = quote(str(relative).replace("\\", "/"))
                url = f"http://10.245.146.157:8789/{route}/{encoded_path}"
    
                row_note = ""
    
                source_buttons.append({
                    "file": f"{file_name}{row_note}",
                    "url": url
                })
    
            return jsonify({
                "retrieval": retrieval_answer,
                "reasoning": reasoning,
                "web": web,
                "final": final_answer,
                "sources": source_buttons
            })

    except Exception as e:
        # print("❌ Error:", e)
        # return jsonify({"error": "Server error", "details": str(e)}), 500
        print("❌ Error:", e)
        traceback.print_exc()  # This will show the full error stack trace
        return jsonify({"error": "Server error", "details": str(e)}), 500



















# === Feedback Logging ===
@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    liked = data.get("liked", False)
    disliked = data.get("disliked", False)

    # Initialize file if missing
    if not FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Likes", "Dislikes"])
            writer.writeheader()
            writer.writerow({"Likes": 0, "Dislikes": 0})

    # Read current feedback
    with open(FEEDBACK_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        row = next(reader)

    likes = int(row["Likes"])
    dislikes = int(row["Dislikes"])

    # Update
    if liked: likes += 1
    if disliked: dislikes += 1

    with open(FEEDBACK_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Likes", "Dislikes"])
        writer.writeheader()
        writer.writerow({"Likes": likes, "Dislikes": dislikes})
    
    return jsonify({"message": "Feedback recorded", "likes": likes, "dislikes": dislikes})

if __name__ == "__main__":
    app.run(debug=False, port=5001)
