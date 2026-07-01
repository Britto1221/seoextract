__version__ = "0.1.2"
from datetime import datetime
from .crawler import crawl
from .models import AuditResult,Severity
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
        counts = {severity: sum(i.severity == severity for i in issues) for severity in Severity}

        return AuditResult(
            url=url,
            audit_date=audit_date,
            pages_crawled=len(pages),
            site_score=site_score,
            grade=grade,
            total_issues=len(issues),
            critical_count=counts[Severity.CRITICAL],
            warning_count=counts[Severity.WARNING],
            info_count=counts[Severity.INFO],
            pages=pages,
            issues=issues,
            safe_browsing=safe_browsing,
        )


