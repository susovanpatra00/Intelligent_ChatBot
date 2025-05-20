import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
LLM_MODEL = "gpt-4o-mini"

def generate_final_answer(query, retrieval, reasoning=None, web=None):
    sections = [
        f"Question: {query}",
        f"Retrieved Answer: {retrieval}"
    ]
    if reasoning:
        sections.append(f"Reasoning Answer: {reasoning}")
    if web:
        sections.append(f"Web Search Result: {web}")

    prompt = "\n\n".join(sections) + "\n\nYou are a helpful assistant. Answer **only** using the information provided above. If the answer is not clearly present in the provided data, reply with: 'I’m sorry, I couldn’t find relevant information in the provided documents or data sources.'. Mention the source of each insight."

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()
