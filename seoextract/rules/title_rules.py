from seoextract.models import PageData
from seoextract.prompts import title_prompt
import json
def title_rules(page: PageData, llm):
    title = page.title or ""
    page_text = page.text or ""
    query = title_prompt(
        title,
        page_text
    )
    response = llm.invoke(query)
    result = json.loads(response.content)
    return result