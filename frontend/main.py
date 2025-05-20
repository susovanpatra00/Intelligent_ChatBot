import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
import torch
torch.classes.__path__ = [] 
import streamlit as st
from Retrieval.query_handler import search_similar_documents, generate_direct_answer
from Reasoning.reasoner import generate_reasoning
from WebSearch.web_search import perform_web_search
from LLM_Response.final_responder import generate_final_answer




st.set_page_config(page_title="Nexus Bot", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Quicksand', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; font-size: 40px;'>
        🤖 NexusBot: Your PDF Intelligence Assistant
    </h1>
    <hr>
    """, 
    unsafe_allow_html=True
)


# === Session Initialization ===
if "submit" not in st.session_state:
    st.session_state.submit = False
if "top_docs" not in st.session_state:
    st.session_state.top_docs = []
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "context_text" not in st.session_state:
    st.session_state.context_text = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "reasoning" not in st.session_state:
    st.session_state.reasoning = ""
if "web" not in st.session_state:
    st.session_state.web = ""
if "final_answer" not in st.session_state:
    st.session_state.final_answer = ""

# === Reset Logic ===
if st.button("Reset"):
    st.session_state.submit = False
    st.session_state.top_docs = []
    st.session_state.last_query = ""
    st.session_state.context_text = ""
    st.session_state.answer = ""
    st.session_state.reasoning = ""
    st.session_state.web = ""
    st.session_state.final_answer = ""
    st.rerun()

query = st.text_input("Enter your question:")

# === Query Execution ===
reasoning_option = st.checkbox("🔍 Use Reasoning")
web_search_option = st.checkbox("🌐 Use Web Search")

if reasoning_option and web_search_option:
    st.warning("Please select only one of the options: Reasoning or Web Search.")
    st.stop()

if st.button("Submit"):
    st.session_state.submit = True
    st.session_state.last_query = query

    with st.spinner("🔎 Retrieving relevant documents..."):
        top_docs = search_similar_documents(query)
        st.session_state.top_docs = top_docs

        context_text = "\n\n".join([
            f"Document {i+1} (File: {doc['FileName']}, Score: {doc['score']:.4f}):\n{doc['Content'][:1000]}..."
            for i, doc in enumerate(top_docs)
        ])
        st.session_state.context_text = context_text
        print(f"\n\n\033[96mContext Text: \n{st.session_state.context_text} \033[0m\n\n\n")  

    # Always generate answer from retrieval
    with st.spinner("📘 Generating Retrieval Answer..."):
        st.session_state.answer = generate_direct_answer(query, st.session_state.top_docs)

    if not st.session_state.answer and not reasoning_option and not web_search_option:
        st.warning("No relevant documents found. Please try a different query.")
        st.stop()

    if not reasoning_option and not web_search_option:
        st.session_state.reasoning = ""
        st.session_state.web = ""
        st.session_state.final_answer = ""
    else:
        if reasoning_option:
            with st.spinner("🧠 Generating Reasoning..."):
                st.session_state.reasoning = generate_reasoning(query, st.session_state.context_text)
        if web_search_option:
            with st.spinner("🌍 Performing Web Search..."):
                st.session_state.web = perform_web_search(query)

        with st.spinner("🎯 Generating Final Answer..."):
            st.session_state.final_answer = generate_final_answer(
                query=query,
                retrieval=st.session_state.answer,  # Use the LLM-processed answer from retrieval
                reasoning=st.session_state.reasoning if reasoning_option else None,
                web=st.session_state.web if web_search_option else None
            )

# === Output ===
if st.session_state.answer:
    st.markdown("### 📘 <span style='color:#3498db'>Retrieval Answer</span>", unsafe_allow_html=True)
    with st.expander("📘 Retrieved Answer", expanded=True):
        st.markdown(st.session_state.answer, unsafe_allow_html=True)

if st.session_state.reasoning:
    st.markdown("### 🧠 <span style='color:#8e44ad'>Reasoning</span>", unsafe_allow_html=True)
    with st.expander("🧠 LLM Reasoning", expanded=True):
        st.markdown(st.session_state.reasoning, unsafe_allow_html=True)

if st.session_state.web:
    st.markdown("### 🌍 <span style='color:#16a085'>Web Search</span>", unsafe_allow_html=True)
    with st.expander("🌍 Web Search Result", expanded=True):
        st.markdown(st.session_state.web, unsafe_allow_html=True)

if st.session_state.final_answer:
    st.markdown("### 🎯 <span style='color:#e67e22'>Final Answer</span>", unsafe_allow_html=True)
    with st.expander("🎯 Synthesized Answer", expanded=True):
        st.markdown(
            st.session_state.final_answer, unsafe_allow_html=True)

# === Downloads ===
if st.session_state.top_docs:
    st.subheader("📁 Source Files")
    for doc in st.session_state.top_docs:
        abs_path = os.path.abspath(doc['FileLocation'])
        file_name = doc['FileName']
        with open(abs_path, "rb") as file:
            st.download_button(
                label=f"Download {file_name}",
                data=file.read(),
                file_name=file_name,
                mime="application/pdf",
                key=f"download_{file_name}"
            )
