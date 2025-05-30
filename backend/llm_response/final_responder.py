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

    # prompt = "\n\n".join(sections) + "\n\nYou are a helpful assistant. Answer **only** using the information provided above. If the answer is not clearly present in the provided data, reply with: 'I’m sorry, I couldn’t find relevant information in the provided documents or data sources.'. **Mention the source of each insight.**"
#     prompt = "\n\n".join(sections) + """

# You are a helpful assistant. Answer **only** using the information provided above.

# If the answer is not clearly present in the provided data, reply with exactly this sentence:
# 'I’m sorry, I couldn’t find relevant information in the provided documents or data sources.'

# - Mention the source of each insight. If from 'web-search', include the source URLs.
# - Make the response attractive and engaging using user-friendly language, symbols and emojis.
# - At the end of your response, if and only if you did NOT return the "I'm sorry" message, add:
#   🗂 Want to Explore More? : Here give some *similar keywords* related to the query and also some similar *questions* related to the query.

# - Do NOT add the above section if your answer contains the "I'm sorry" sentence.
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
