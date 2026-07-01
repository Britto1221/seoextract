from seoextract.models import PageData
from seoextract.prompts import site_context_prompt
from seoextract.utils import parse_llm_json


def build_site_context(homepage: PageData, llm) -> dict:
    homepage_data = homepage.model_dump()

    query = site_context_prompt(homepage_data)
    response = llm.invoke(query)

    return parse_llm_json(response.content)