from seoextract.models import PageData
from seoextract.prompts import full_page_audit_prompt
from seoextract.utils import parse_llm_json
def overall_rules(page: PageData, llm):
    page_data = {
    "url": page.url,
    "final_url": page.final_url,
    "response_time_ms": page.response_time_ms,
    "title": page.title or "",
    "title_length": page.title_length,
    "meta_description": page.meta_description or "",
    "meta_description_length": page.meta_description_length,
    "canonical": page.canonical or "",
    "headings": {
        "h1": page.h1_tags,
        "h2": page.h2_tags,
        "h3": page.h3_tags,
        "h4": page.h4_tags,
        "h5": page.h5_tags,
        "h6": page.h6_tags,
    },
    "heading_counts": {
        "h1": page.h1_count,
        "h2": page.h2_count,
        "h3": page.h3_count,
        "h4": page.h4_count,
        "h5": page.h5_count,
        "h6": page.h6_count,
    },
    "word_count": page.word_count,
    "total_images": page.total_images,
    "images_missing_alt": page.images_missing_alt,
    "internal_links": page.internal_links,
    "external_links": page.external_links,
    "internal_count": page.internal_count,
    "external_count": page.external_count,
    "schema_found": page.schema_found,
    "og_title": page.og_title or "",
    "og_description": page.og_description or "",
    "page_score": page.page_score,
}

    query = full_page_audit_prompt(page_data)
    response = llm.invoke(query)
    result = parse_llm_json(response.content)
    return result