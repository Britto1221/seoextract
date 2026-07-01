from seoextract.models import PageData
from seoextract.prompts import full_page_audit_prompt
import json
def overall_rules(page: PageData, llm):
    page_data = {
        "url": page.url,
        "title": page.title or "",
        "meta_description": page.meta_description or "",
        "headings": {
            "h1": page.h1_tags or [],
            "h2": page.h2_tags or [],
            "h3": page.h3_tags or [],
            "h4": page.h4_tags or [],
            "h5": page.h5_tags or [],
            "h6": page.h6_tags or [],
        },
        "text": page.text or "",
        "word_count": page.word_count,
        "images": page.images or [],
        "total_images": page.total_images,
        "internal_links": page.internal_links or [],
        "external_links": page.external_links or [],
        "canonical": page.canonical or "",
        "viewport": page.viewport or "",
        "robots_meta": page.robots_meta or "",
        "schema_present": page.schema_present,
        "status_code": page.status_code,
        "https": page.url.startswith("https://"),
    }

    query = full_page_audit_prompt(page_data)
    response = llm.invoke(query)
    result = json.loads(response.content)
    return result