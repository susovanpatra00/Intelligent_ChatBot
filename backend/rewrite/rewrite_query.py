import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
LLM_MODEL = "gpt-4o"



def rewrite_standalone_query(history, query):
    """
    Determines if the query is related to the conversation history using OpenAI API.
    If related, returns a standalone rewritten query for vector search.
    If not related, returns the original query.

    Args:
        history (list of str): List of previous conversation messages.
        query (str): Current user query.
        openai_client: Initialized OpenAI client instance.

    Returns:
        str: Rewritten standalone query or original query.
    """
    # Combine history into a single string
    history_text = "\n".join(history)

    # Prepare prompt for relevance check and rewriting
    prompt = (
        f"Given the conversation history:\n{history_text}\n\n"
        f"Is the following query related to the history? If yes, rewrite it as a standalone query for vector search retrieval. "
        f"If not, return only the original query, with no explanation or extra text.\nQuery: {query}"
    )


    # Call OpenAI API to get the response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    answer = response.choices[0].message.content.strip()

    return answer
