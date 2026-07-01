from seoextract.models import PageData
from seoextract.prompts import image_prompt
from seoextract.utils import parse_llm_json
def image_rules(page: PageData, llm):
    images = page.images or []
    page_text = page.text or ""
    query = image_prompt(
        images,
        page_text
    )
    response = llm.invoke(query)
    result = parse_llm_json(response.content)
    return result