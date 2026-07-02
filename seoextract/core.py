from datetime import datetime

from .crawler import crawl
from .models import AuditResult, Severity
from .parser import parse
from .rules import detect_issues
from .scorer import score_site


class SEOExtract:
    @staticmethod
    def audit(url: str, max_pages: int = 20) -> AuditResult:
        audit_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        pages = [parse(page) for page in crawl(url, max_pages)]
        issues = detect_issues(pages)
        site_score, grade = score_site(pages, issues)

        critical_count = sum(i.severity == Severity.CRITICAL for i in issues)
        warning_count = sum(i.severity == Severity.WARNING for i in issues)
        info_count = sum(i.severity == Severity.INFO for i in issues)

        return AuditResult(
            url=url,
            audit_date=audit_date,
            pages_crawled=len(pages),
            site_score=site_score,
            grade=grade,
            total_issues=len(issues),
            critical_count=critical_count,
            warning_count=warning_count,
            info_count=info_count,
            pages=pages,
            issues=issues,
        )