from seoextract.models import IssueType, PageData, SEOIssue, Severity
from meta_rules import meta_rules
from title_rules import title_rules
from heading_rules import heading_rules
from content_rules import content_rules
from technical_rules import technical_rules
from link_rules import link_rules
from image_rules import image_rules
from seoextract.llm import openai_provider
from overall_rules import overall_rules
def detect_issues(pages: list[PageData]) -> list[dict]:
    issues = []
    llm = openai_provider()

    for page in pages:
        issues.append(meta_rules(page, llm))
        issues.append(title_rules(page, llm))
        issues.append(heading_rules(page, llm))
        issues.append(content_rules(page, llm))
        issues.append(technical_rules(page, llm))
        issues.append(link_rules(page, llm))
        issues.append(image_rules(page, llm))
        issues.append(overall_rules(page, llm))

    return issues