from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
LLM_MODEL = "gpt-4o-mini"

def perform_web_search(query):
    response = client.responses.create(
        model=LLM_MODEL,
        tools=[{"type": "web_search_preview"}],
        input=query
    )
    # print("Response from LLM Web Search:", response.output_text.strip())
    return response.output_text.strip()
