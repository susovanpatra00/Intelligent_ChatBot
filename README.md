# 📚 Intelligence Assistant (DO33 Bot)

An intelligent assistant that allows users to query PDF and Excel documents using natural language. Built using **React + Vite + TypeScript** on the frontend and **Flask + LangChain + OpenAI** on the backend. The system supports contextual retrieval, optional reasoning, and web search.

---

## 🚀 Features

- ✅ Natural language queries on PDFs and Excel files
- 🔍 Internal document retrieval using vector search (FAISS)
- 🧠 Optional LLM-based reasoning
- 🌐 Optional real-time web search via OpenAI
- 📎 Source file traceability and download support
- 🧾 Feedback system for likes/dislikes with logging
- 🎙️ Voice-to-text input (speech recognition)
- 📁 Modular ingestion: Add new file types easily

---

## 📁 Folder Structure

```

DO33\_Final/
├── backend/                     # All backend code
│   ├── app.py                   # Flask API server
│   ├── config.py                # Global config and flags
│   ├── ingestion/               # Data ingestion logic
│   │   ├── ingest\_pdf.py
│   │   ├── ingest\_excel.py
│   ├── vectorstore/             # Stored FAISS indexes
│   ├── retrieval/
│   ├── reasoning/
│   ├── websearch/
│   ├── llm\_response/
│   ├── utils/
│   └── data/                    # Embedded document metadata (pkl, json)
├── Data/                        # Raw files
│   ├── PDF/
│   └── EXCEL/
├── frontend/                    # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.ts
├── .env
├── .gitignore
└── requirements.txt


````

---

## ⚙️ Setup Instructions

### 1. 🧠 Backend Setup

#### a. Create a Python virtual environment

```bash
python -m venv do33_env
source do33_env/bin/activate  # or do33_env\Scripts\activate on Windows
````

#### b. Install dependencies

```bash
pip install -r requirements.txt
```

#### c. Add OpenAI API Key

Create a `.env` file in the backend root:

```env
OPENAI_API_KEY=your_openai_api_key
```

#### d. Run ingestion scripts

```bash
python data_ingestion/generate_embeddings.py
```

#### e. Start the Flask server

```bash
python backend\app.py
```

Server will run at: `http://localhost:5001`

---

### 2. 💻 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at: `http://localhost:8080`

---

## 🧪 Example Usage

* Ask: *"What is the problem with the XYZ component and how was it solved?"*
* Enable reasoning or web search (optional)
* Receive a structured answer with source file buttons
* Click source buttons to open documents
* Leave feedback via 👍 / 👎

---

## 🛠 Config Options

Inside `backend/config.py`:

```python
ENABLE_PDF = True
ENABLE_EXCEL = True
```

---

## 📦 Dependencies

* **Frontend**: React, Vite, TypeScript, Tailwind CSS, Shadcn-UI
* **Backend**: Flask, OpenAI, LangChain, FAISS, Pandas
* **Embeddings**: BAAI/bge-base-en-v1.5 via HuggingFace
* **LLM**: GPT-4o or GPT-3.5-turbo (OpenAI)

---

## 🧠 Future Improvements

* Role-based access and authentication
* Add support for CSV/Docx ingestion
* Summary and analytics dashboard
* Row-level preview for Excel rows used in answers
