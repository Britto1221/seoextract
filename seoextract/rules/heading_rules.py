from seoextract.models import PageData
from seoextract.prompts import heading_prompt
import json
def heading_rules(page: PageData, llm):
    headings = {
        "h1": page.h1_tags or [],
        "h2": page.h2_tags or [],
        "h3": page.h3_tags or [],
        "h4": page.h4_tags or [],
        "h5": page.h5_tags or [],
        "h6": page.h6_tags or [],
    }
    page_text = page.text or ""
    query = heading_prompt(
        headings,
        page_text
    )
    response = llm.invoke(query)
    result = json.loads(response.content)
    return result