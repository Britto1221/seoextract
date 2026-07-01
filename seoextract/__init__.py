__version__ = "0.1.2"

from datetime import datetime
from dotenv import load_dotenv

from .crawler import crawl
from .parser import parse
from .models import AuditResult
from .auditor import audit_page
from .llm import openai_provider

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
    def audit(url: str, max_pages: int = 20) -> AuditResult:
        audit_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        pages = [parse(page) for page in crawl(url, max_pages)]

        llm = openai_provider()

        page_audits = []

        for page in pages:
            audit = audit_page(page, llm)
            page.page_score = audit.get("page_score", 0)
            page_audits.append(audit)

        site_score = (
            round(sum(page.page_score for page in pages) / len(pages), 1)
            if pages
            else 0.0
        )

        all_issues = []
        for audit in page_audits:
            all_issues.extend(audit.get("issues", []))

        return AuditResult(
            url=url,
            audit_date=audit_date,
            pages_crawled=len(pages),
            site_score=site_score,
            grade=get_grade(site_score),
            total_issues=len(all_issues),
            critical_count=sum(
                1 for issue in all_issues
                if issue.get("severity", "").upper() == "CRITICAL"
            ),
            warning_count=sum(
                1 for issue in all_issues
                if issue.get("severity", "").upper() == "WARNING"
            ),
            info_count=sum(
                1 for issue in all_issues
                if issue.get("severity", "").upper() == "INFO"
            ),
            pages=pages,
            page_audits=page_audits,
        )