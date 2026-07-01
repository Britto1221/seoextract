from seoextract.models import PageData
from seoextract.prompts import content_prompt
import json
def content_rules(page: PageData, llm):
    page_text = page.text or ""
    query = content_prompt(
        page_text
    )
    response = llm.invoke(query)
    result = json.loads(response.content)
    return result