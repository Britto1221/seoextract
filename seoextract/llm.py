import os
from langchain_openai import ChatOpenAI


def openai_provider():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. Add it to your .env file or environment variables."
        )

    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=api_key,
    )