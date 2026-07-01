from datetime import datetime
from .site_context import build_site_context
from dotenv import load_dotenv

from .auditor import audit_page
from .crawler import crawl
from .llm import openai_provider
from .models import AuditResult
from .parser import parse

load_dotenv()


def get_grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"


class SEOExtract:
    @staticmethod
    def audit(
        url: str,
        max_pages: int = 20,
        model: str = "gpt-4o-mini",
    ) -> AuditResult:
        audit_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        pages = [parse(page) for page in crawl(url, max_pages)]
        llm = openai_provider(model=model)
        site_context = build_site_context(pages[0], llm) if pages else {}
        page_audits = []

        for page in pages:
            audit = audit_page(page, llm, site_context=site_context)
            page.page_score = audit.page_score
            page_audits.append(audit)

        site_score = (
            round(sum(page.page_score for page in pages) / len(pages), 1)
            if pages
            else 0.0
        )

        all_issues = []
        for audit in page_audits:
            all_issues.extend(audit.issues)

        return AuditResult(
            url=url,
            audit_date=audit_date,
            pages_crawled=len(pages),
            site_score=site_score,
            grade=get_grade(site_score),
            total_issues=len(all_issues),
            critical_count=sum(1 for i in all_issues if i.severity.upper() == "CRITICAL"),
            warning_count=sum(1 for i in all_issues if i.severity.upper() == "WARNING"),
            info_count=sum(1 for i in all_issues if i.severity.upper() == "INFO"),
            pages=pages,
            page_audits=page_audits,
        )