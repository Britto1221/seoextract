from seoextract.models import PageData
from seoextract.prompts import links_prompt
from seoextract.utils import parse_llm_json
def link_rules(page: PageData, llm):
    internal_links = page.internal_links or []
    external_links = page.external_links or []
    page_text = page.text or ""

    query = links_prompt(
        internal_links,
        external_links,
        page_text
    )
    response = llm.invoke(query)
    result = parse_llm_json(response.content)
    return result