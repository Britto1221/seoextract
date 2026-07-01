import time

from seoextract.models import PageAudit, PageData
from seoextract.prompts import full_page_audit_prompt
from seoextract.utils import parse_llm_json


def audit_page(page: PageData, llm, site_context: dict | None = None, retries: int = 2) -> PageAudit:
    page_data = {
    "site_context": site_context or {},
    "page_data": page.model_dump(),
}

    query = full_page_audit_prompt(page_data)

    last_error = None

    for attempt in range(retries + 1):
        try:
            response = llm.invoke(query)
            result = parse_llm_json(response.content)

            return PageAudit(
                page_url=page.url,
                page_score=result.get("page_score", 0),
                grade=result.get("grade", "F"),
                summary=result.get("summary", ""),
                issues=result.get("issues", []),
                strengths=result.get("strengths", []),
                priority_actions=result.get("priority_actions", []),
            )

        except Exception as e:
            last_error = e
            time.sleep(2 ** attempt)

    return PageAudit(
        page_url=page.url,
        page_score=0,
        grade="F",
        summary=f"Audit failed: {last_error}",
        issues=[
            {
                "category": "LLM",
                "title": "LLM audit failed",
                "severity": "INFO",
                "reason": str(last_error),
                "recommendation": "Try again later or check your API key/model settings.",
            }
        ],
    )