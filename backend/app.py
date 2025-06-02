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
import csv
from datetime import datetime
from utils.file_helpers import get_location

LOG_FILE = "chat_log.csv"
spell = SpellChecker()
FEEDBACK_LOG = "feedback_log.csv"

def log_feedback(session_id, ip, message_id, feedback):
    with open(FEEDBACK_LOG, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            session_id,
            ip,
            message_id,
            feedback  
        ])
        
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



def log_interaction(session_id, ip, country, query, answer):
    with open(LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            session_id,
            ip,
            country,
            query,
            answer
        ])
    
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
        history_strings = [
            f"User: {item['Query']} Bot: {item['Bot Reply']}" for item in history
        ]
        print(f"\nHistory Got: {history_strings}")
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
            
            session_id = session.get("session_id", "unknown")
            ip = request.remote_addr
            country = get_location(ip)
            log_interaction(session_id, ip, country, query, final_answer)

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

            history.append({"Query": standalone_query, "Bot Reply": final_answer})
            history = history[-4:]
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
        print("❌ Error:", e)
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

    # -------------------------------------------------------------------------
    session_id = session.get("session_id", "unknown")
    ip = request.remote_addr
    message_id = data.get("message_id", "unknown")
    feedback_type = "like" if liked else "dislike" if disliked else "none"
    log_feedback(session_id, ip, message_id, feedback_type)
    # -------------------------------------------------------------------------
    
    return jsonify({"message": "Feedback recorded", "likes": likes, "dislikes": dislikes})

if __name__ == "__main__":
    app.run(debug=False, port=5001)
