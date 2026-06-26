import os
import requests
from dotenv import load_dotenv

load_dotenv()


def check_safe_browsing(url: str, api_key: str | None = None) -> dict:
    # manual key has first priority
    if api_key is None:
        api_key = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")

    if not api_key:
        return {
            "is_safe": None,
            "threats": [],
            "error": "Google Safe Browsing API key not provided and GOOGLE_SAFE_BROWSING_API_KEY not found in .env",
        }

    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"

    payload = {
        "client": {
            "clientId": "seoextracthf",
            "clientVersion": "1.0.0",
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION",
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        matches = data.get("matches", [])

        if not matches:
            return {"is_safe": True, "threats": [], "error": None}

        return {
            "is_safe": False,
            "threats": [match.get("threatType") for match in matches],
            "error": None,
        }

    except requests.RequestException as e:
        return {
            "is_safe": None,
            "threats": [],
            "error": str(e),
        }