import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def openai_provider(model: str | None = None):
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. Add it to your .env file or environment variables."
        )

    return ChatOpenAI(
        model=model_name,
        temperature=0,
        api_key=api_key,
    )