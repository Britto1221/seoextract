from seoextract.models import PageData
from seoextract.prompts import technical_prompt
import json
def technical_rules(page: PageData, llm):
    technical_data = {
        "url": page.url,
        "canonical": page.canonical,
        "viewport": page.viewport,
        "robots_meta": page.robots_meta,
        "schema_present": page.schema_present,
        "https": page.url.startswith("https://"),
        "status_code": page.status_code,
    }
    query = technical_prompt(
        technical_data,
    )
    response = llm.invoke(query)
    result = json.loads(response.content)
    return result