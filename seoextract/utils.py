import json


def parse_llm_json(content: str) -> dict:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "issue_found": True,
            "severity": "INFO",
            "reason": "LLM response was not valid JSON.",
            "recommendation": content,
        }