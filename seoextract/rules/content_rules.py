from seoextract.models import PageData
from seoextract.prompts import content_prompt
from seoextract.utils import parse_llm_json
def content_rules(page: PageData, llm):
    page_text = page.text or ""
    query = content_prompt(
        page_text
    )
    response = llm.invoke(query)
    result = parse_llm_json(response.content)
    return result