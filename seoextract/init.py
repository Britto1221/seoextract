from datetime import datetime

from .crawler import crawl
from .models import AuditResult, SafeBrowsingResult, Severity
from .parser import parse
from .rules import detect_issues
from .safe_browsing import check_safe_browsing
from .scorer import score_site


class SEOExtract:
    @staticmethod
    def audit(url: str, max_pages: int = 20, safe_browsing_api_key: str | None = None) -> AuditResult:
        safe_browsing = SafeBrowsingResult(**check_safe_browsing(url, safe_browsing_api_key))
        audit_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        if safe_browsing.is_safe is False:
            return AuditResult(
                url=url, audit_date=audit_date, pages_crawled=0, site_score=0.0, grade="F",
                total_issues=0, critical_count=0, warning_count=0, info_count=0,
                safe_browsing=safe_browsing,
            )

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
<<<<<<< HEAD
    

if __name__ == "__main__":
    result = SEOExtract.audit("Your Website")
    print(result.model_dump_json(indent=2))
=======
>>>>>>> f0d241a (seoextract v0.1.2)
