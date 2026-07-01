from seoextract.models import PageData
from seoextract.prompts import full_page_audit_prompt
from seoextract.utils import parse_llm_json


def audit_page(page: PageData, llm) -> dict:
    page_data = page.model_dump()

    query = full_page_audit_prompt(page_data)

    response = llm.invoke(query)
    result = parse_llm_json(response.content)

    return {
        "page_url": page.url,
        "page_score": result.get("page_score", 0),
        "grade": result.get("grade", "F"),
        "summary": result.get("summary", ""),
        "issues": result.get("issues", []),
        "strengths": result.get("strengths", []),
        "priority_actions": result.get("priority_actions", []),
        "raw": result,
    }