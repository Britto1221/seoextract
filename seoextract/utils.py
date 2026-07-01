import json
import re


def parse_llm_json(content: str) -> dict:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return {
            "page_score": 0,
            "grade": "F",
            "summary": "LLM response was not valid JSON.",
            "issues": [
                {
                    "category": "LLM",
                    "title": "Invalid JSON response",
                    "severity": "INFO",
                    "reason": "The LLM returned text that could not be parsed as JSON.",
                    "recommendation": content,
                }
            ],
            "strengths": [],
            "priority_actions": [],
        }