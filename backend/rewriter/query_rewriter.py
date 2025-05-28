from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# Load environment variables (ensure OPENAI_API_KEY is set in .env)
load_dotenv()

# Define prompt template
PROMPT_TEMPLATE = """
You are a helpful AI assistant. You are given the current user question and chat history.

Your task is to rewrite the current user question to be a standalone question that captures the context of the conversation.

Chat History:
{chat_history}

Current User Question:
{user_question}

Standalone Question:
"""

# Initialize the model and pipeline
prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
llm = ChatOpenAI(model="gpt-4", temperature=0)
output_parser = StrOutputParser()
query_rewriter_chain = prompt | llm | output_parser

def rewrite_query(user_question: str, chat_history: list[str]) -> str:
    """
    Rewrites a follow-up user question into a standalone question using context from chat history.
    
    Parameters:
        user_question (str): The latest user question.
        chat_history (list[str]): List of previous chat messages in order (alternating User/Assistant).
    
    Returns:
        str: A standalone, contextually complete version of the user question.
    """
    history_str = "\n".join(chat_history[-6:])  # Only use last 6 turns to keep it relevant
    return query_rewriter_chain.invoke({
        "chat_history": history_str,
        "user_question": user_question
    })
