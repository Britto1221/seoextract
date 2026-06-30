from .models import PageData, SEOIssue, Severity

PENALTY = {Severity.CRITICAL: 20, Severity.WARNING: 8, Severity.INFO: 3}


def _grade(score: float) -> str:
    return "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F"


def score_page(page: PageData, issues: list[SEOIssue]) -> float:
    if page.status_code != 200:
        return 0.0
    penalty = sum(PENALTY[i.severity] for i in issues if i.page_url == page.url)
    return round(max(100.0 - penalty, 0.0), 1)


def score_site(pages: list[PageData], issues: list[SEOIssue]) -> tuple[float, str]:
    if not pages:
        return 0.0, "F"
    for page in pages:
        page.page_score = score_page(page, issues)
    site_score = round(sum(page.page_score for page in pages) / len(pages), 1)
    return site_score, _grade(site_score)
