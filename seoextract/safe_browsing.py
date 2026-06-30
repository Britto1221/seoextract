import os
import requests

THREAT_TYPES = ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"]


def check_safe_browsing(url: str, api_key: str | None = None) -> dict:
    api_key = api_key or os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")
    if not api_key:
        return {"is_safe": None, "threats": [], "error": "Google Safe Browsing API key not provided."}

    payload = {
        "client": {"clientId": "seoextracthf", "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": THREAT_TYPES,
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    try:
        response = requests.post(f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}", json=payload, timeout=10)
        response.raise_for_status()
        matches = response.json().get("matches", [])
        return {"is_safe": not matches, "threats": [m.get("threatType") for m in matches], "error": None}
    except requests.RequestException as e:
        return {"is_safe": None, "threats": [], "error": str(e)}
