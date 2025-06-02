import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
LLM_MODEL = "gpt-4o"

def generate_final_answer(query, retrieval, reasoning=None, web=None):
    sections = [
        f"Question: {query}",
        f"Retrieved Answer: {retrieval}"
    ]
    if reasoning:
        sections.append(f"Reasoning Answer: {reasoning}")
    if web:
        sections.append(f"Web Search Result: {web}")

    
    print("\n\nSections for Final Answer Generation:", sections)
    prompt = "\n\n".join(sections) + """

You are a helpful and knowledgeable assistant. Your task is to **ONLY rearrange, rephrase, and format** the information provided above according to the writing standards below. 
**Do NOT add, invent, or infer any new information.** 

✅ When formatting:
- Clearly cite the **source** of each insight. If the source is 'web-search', include the source **URL**.
- Use engaging and reader-friendly language, with **symbols** and **emojis** to enhance readability.
- Structure your response well, using **bullet points**, **highlights**, or **subheadings** when helpful.

📌 IMPORTANT:
- Do **not** guess, add, or infer beyond the data given.
- Do **not** include the exploration section below if your response includes the “I’m sorry” sentence.

✨ At the end of your answer (only if a valid answer was given), include this:
🗂 **Want to Explore More?**
- 🔍 *Similar Keywords:* (List 3–5 related keywords)
- ❓ *Related Questions:* (List 2–3 related, relevant questions)
"""


    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
