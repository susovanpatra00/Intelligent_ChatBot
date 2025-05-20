# # Version 1.0
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from Retrieval.query_handler import search_similar_documents, generate_direct_answer
# from Reasoning.reasoner import generate_reasoning
# from WebSearch.web_search import perform_web_search
# from LLM_Response.final_responder import generate_final_answer
# from urllib.parse import quote
# from pathlib import Path
# from concurrent.futures import ThreadPoolExecutor

# app = Flask(__name__)
# CORS(app)

# DATA_DIR = "Data"

# @app.route('/pdfs/<path:relative_path>')
# def serve_nested_pdf(relative_path):
#     # full_path = os.path.join(DATA_DIR, relative_path)
#     full_path = Path(DATA_DIR, relative_path).resolve()
#     print(f"📂 Requested file: {full_path}")  
#     if not os.path.isfile(full_path):
#         print("❌ File not found:", full_path)
#         return "File not found", 404

#     directory = os.path.dirname(full_path)
#     filename = os.path.basename(full_path)
#     return send_from_directory(directory, filename)



# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.json
#     query = data.get("query", "")
#     use_reasoning = data.get("reasoning", False)
#     use_web = data.get("web", False)

#     if not query:
#         return jsonify({"error": "Missing query"}), 400

#     try:
#         # Step 1: Retrieve documents
#         top_docs = search_similar_documents(query)

#         # Step 2: Always get retrieval-based answer
#         retrieval_answer = generate_direct_answer(query, top_docs)

#         # Step 3: Optional reasoning and web
#         with ThreadPoolExecutor() as executor:
#             web_future = executor.submit(perform_web_search, query) if use_web else None
#             reasoning_future = executor.submit(generate_reasoning, query, retrieval_answer) if use_reasoning else None

#         web = web_future.result() if web_future else None
#         reasoning = reasoning_future.result() if reasoning_future else None

#         # Step 4: Final combined answer
#         final_answer = generate_final_answer(
#             query=query,
#             retrieval=retrieval_answer,
#             reasoning=reasoning,
#             web=web
#         )

#         # Step 5: Build source file links
#         source_buttons = []
#         for doc in top_docs:
#             full_path = doc["FileLocation"]
#             relative_path = os.path.relpath(full_path, DATA_DIR).replace("\\", "/")
#             encoded_path = quote(relative_path)
#             url = f"http://localhost:5001/pdfs/{encoded_path}"
#             source_buttons.append({
#                 "file": doc["FileName"],
#                 "url": url
#             })

#         return jsonify({
#             "retrieval": retrieval_answer,
#             "reasoning": reasoning,
#             "web": web,
#             "final": final_answer,
#             "sources": source_buttons
#         })

#     except Exception as e:
#         print("❌ Error:", e)
#         return jsonify({"error": "Server error", "details": str(e)}), 500
    

# if __name__ == "__main__":
#     app.run(debug=False, port=5001)
# # --------------------------------------------------------------------------------- #






























# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from Retrieval.query_handler import search_similar_documents, generate_direct_answer
# from Reasoning.reasoner import generate_reasoning
# from WebSearch.web_search import perform_web_search
# from LLM_Response.final_responder import generate_final_answer
# from urllib.parse import quote
# from pathlib import Path

# app = Flask(__name__)
# CORS(app)

# DATA_DIR = "Data/PDF"

# @app.route('/pdfs/<path:relative_path>')
# def serve_nested_pdf(relative_path):
#     full_path = Path(DATA_DIR, relative_path).resolve()
#     print(f"📂 Requested file: {full_path}")

#     if not full_path.exists() or not full_path.is_file():
#         print("❌ File not found:", full_path)
#         return "File not found", 404

#     return send_from_directory(full_path.parent, full_path.name)

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.json
#     query = data.get("query", "")
#     use_reasoning = data.get("reasoning", False)
#     use_web = data.get("web", False)

#     if not query:
#         return jsonify({"error": "Missing query"}), 400

#     try:
#         # Step 1: Retrieve documents (PDF + Excel)
#         top_docs = search_similar_documents(query, k=5)

#         # Step 2: Always get retrieval-based answer
#         retrieval_answer = generate_direct_answer(query, top_docs)

#         # Step 3: Optional reasoning + web search (parallel web)
#         reasoning = generate_reasoning(query, retrieval_answer) if use_reasoning else None

#         web = None
#         if use_web:
#             from concurrent.futures import ThreadPoolExecutor
#             with ThreadPoolExecutor() as executor:
#                 web_future = executor.submit(perform_web_search, query)
#                 web = web_future.result()

#         # Step 4: Final answer
#         final_answer = generate_final_answer(
#             query=query,
#             retrieval=retrieval_answer,
#             reasoning=reasoning,
#             web=web
#         )

#         # Step 5: Source file links
#         source_buttons = []
#         for doc in top_docs:
#             full_path = Path(doc["FileLocation"])
#             relative_path = full_path.relative_to(DATA_DIR)
#             encoded_path = quote(str(relative_path).replace("\\", "/"))
#             url = f"http://localhost:5000/pdfs/{encoded_path}"
#             source_buttons.append({
#                 "file": doc["FileName"],
#                 "url": url
#             })

#         return jsonify({
#             "retrieval": retrieval_answer,
#             "reasoning": reasoning,
#             "web": web,
#             "final": final_answer,
#             "sources": source_buttons
#         })

#     except Exception as e:
#         print("❌ Error:", e)
#         return jsonify({"error": "Server error", "details": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=False, port=5001)




































import sys
import os
from pathlib import Path
from urllib.parse import quote

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from retrieval.query_handler import search_similar_documents, generate_direct_answer
from reasoning.reasoner import generate_reasoning
from websearch.web_search import perform_web_search
from llm_response.final_responder import generate_final_answer
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

PDF_DIR = Path("Data/PDF").resolve()
EXCEL_DIR = Path("Data/EXCEL").resolve()
FEEDBACK_FILE = "feedback_log.csv"

# === PDF File Serving ===
@app.route('/pdfs/<path:relative_path>')
def serve_pdf(relative_path):
    full_path = PDF_DIR / relative_path
    # print(f"📄 Requested PDF: {full_path}")

    if not full_path.exists() or not full_path.is_file():
        return "PDF file not found", 404

    return send_from_directory(full_path.parent, full_path.name)

# === Excel File Serving ===
@app.route('/excels/<path:relative_path>')
def serve_excel(relative_path):
    full_path = EXCEL_DIR / relative_path
    # print(f"📊 Requested Excel: {full_path}")

    if not full_path.exists() or not full_path.is_file():
        return "Excel file not found", 404

    return send_from_directory(full_path.parent, full_path.name)

# === Chat Endpoint ===
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "")
    use_reasoning = data.get("reasoning", False)
    use_web = data.get("web", False)

    if not query:
        return jsonify({"error": "Missing query"}), 400

    try:
        # Step 1: Retrieve documents (PDF + Excel)
        top_docs = search_similar_documents(query, k=5)

        # Step 2: Always get retrieval-based answer
        retrieval_answer = generate_direct_answer(query, top_docs)

        # Step 3: Optional reasoning and web (parallel web)
        reasoning = generate_reasoning(query, retrieval_answer) if use_reasoning else None
        web = None
        if use_web:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor() as executor:
                web_future = executor.submit(perform_web_search, query)
                web = web_future.result()

        # Step 4: Final LLM synthesis
        final_answer = generate_final_answer(
            query=query,
            retrieval=retrieval_answer,
            reasoning=reasoning,
            web=web
        )

        # Step 5: Build file download/view links
        source_buttons = []
        for doc in top_docs:
            file_path = Path(doc["FileLocation"]).resolve()
            file_name = doc["FileName"]

            if PDF_DIR in file_path.parents:
                base = PDF_DIR
                route = "pdfs"
            elif EXCEL_DIR in file_path.parents:
                base = EXCEL_DIR
                route = "excels"
            else:
                continue

            relative = file_path.relative_to(base)
            encoded_path = quote(str(relative).replace("\\", "/"))
            url = f"http://localhost:5001/{route}/{encoded_path}"

            # Add row number if Excel
            row_note = ""
            if route == "excels":
                metadata = doc.get("metadata", {})
                row = metadata.get("row")
                if row is not None:
                    row_note = f" (row {row})"

            source_buttons.append({
                "file": f"{file_name}{row_note}",
                "url": url
            })


        # print("🔗 Source buttons:", source_buttons)
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


@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    liked = data.get("liked", False)
    disliked = data.get("disliked", False)

    # Ensure file exists and has headers
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Likes", "Dislikes"])
            writer.writeheader()
            writer.writerow({"Likes": 0, "Dislikes": 0})

    # Read current values
    with open(FEEDBACK_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        row = next(reader)

    likes = int(row["Likes"])
    dislikes = int(row["Dislikes"])

    # Update counts
    if liked:
        likes += 1
    if disliked:
        dislikes += 1

    # Write back updated values
    with open(FEEDBACK_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Likes", "Dislikes"])
        writer.writeheader()
        writer.writerow({"Likes": likes, "Dislikes": dislikes})

    return jsonify({"message": "Feedback recorded", "likes": likes, "dislikes": dislikes})

if __name__ == "__main__":
    app.run(debug=False, port=5001)
