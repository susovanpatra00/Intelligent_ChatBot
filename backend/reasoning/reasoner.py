from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
LLM_MODEL = "gpt-4o-mini"

def generate_reasoning(query, retrieved_content):
    prompt = f"""
The following is a question and some context retrieved from documents.

Question:
{query}

Context:
{retrieved_content}

Based on this, provide a well-reasoned explanation or inference.
    """

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}], 
        temperature=0.7
    )
    # print("\nResponse from LLM Reasoning:", response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()
