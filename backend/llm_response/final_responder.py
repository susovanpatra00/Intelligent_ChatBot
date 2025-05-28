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

    # prompt = "\n\n".join(sections) + "\n\nYou are a helpful assistant. Answer **only** using the information provided above. If the answer is not clearly present in the provided data, reply with: 'I’m sorry, I couldn’t find relevant information in the provided documents or data sources.'. Mention the source of each insight. If from 'web-search' then also mention the source urls. Also make the response more attractive and engaging for the user. And ask if they need any further assistance with some follow-up questions. Use emojis to make the response more engaging."
#     prompt = "\n\n".join(sections) + """

# You are a helpful assistant. Answer **only** using the information provided above. 
# If the answer is not clearly present in the provided data, reply with: 
# 'I’m sorry, I couldn’t find relevant information in the provided documents or data sources.'

# - Mention the source of each insight. If from 'web-search', include source URLs.
# - Use symbols and emojis (if needed) to make the response more engaging.
# - Make the response attractive and engaging using user-friendly language and emojis.
# - If relevant information is found, end with a friendly message and suggest follow-up questions or keywords to explore.
# - If no relevant information is found, do **not** add any follow-up questions or keyword suggestions.
# - Only include a “🗂 Want to Explore More?” section when relevant information is available.
# """

    prompt = "\n\n".join(sections) + """

You are a helpful and knowledgeable assistant. Answer the user's query using **only** the information provided above.

🛑 If the answer is not clearly available in the provided data, respond with **exactly** this sentence:
'I’m sorry, I couldn’t find relevant information in the provided documents or data sources.'

✅ When answering:
- Clearly cite the **source** of each insight. If the source is 'web-search', include the source **URL**.
- Use engaging and reader-friendly language, with **symbols** and **emojis** to enhance readability.
- Structure your response well, using **bullet points**, **highlights**, or **subheadings** when helpful.

📌 IMPORTANT:
- Do **not** guess or infer beyond the data given.
- Do **not** include the exploration section below if your response includes the “I’m sorry” sentence.

✨ At the end of your answer (only if a valid answer was given), include this:
🗂 **Want to Explore More?**
- 🔍 *Similar Keywords:* (List 3–5 related keywords)
- ❓ *Related Questions:* (List 2–3 related, relevant questions)

"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()
