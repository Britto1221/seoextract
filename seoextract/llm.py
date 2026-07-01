from langchain_openai import ChatOpenai
from dotenv import load_dotenv
load_dotenv()
import os

def openai_provider():
    return ChatOpenai(
        model = "gpt4o-mini",
        api_key = os.getenv("OPENAI_API_KEY"),
        temperature = 0
    )