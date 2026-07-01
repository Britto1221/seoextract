from seoextract.models import PageData
from seoextract.prompts import meta_description_prompt
import json
def meta_rules(page: PageData, llm):
    meta_description = page.meta_description or ""
    page_text = page.text or ""
    query = meta_description_prompt(
        meta_description,
        page_text
    )
    response = llm.invoke(query)
    result = json.loads(response.content)
    return result