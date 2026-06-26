from .models import PageData, SEOIssue, Severity


# ── Severity Penalty Weights ──────────────────────────────────────────────────

PENALTY = {
    Severity.CRITICAL : 20,
    Severity.WARNING  : 8,
    Severity.INFO     : 3,
}


def _grade(score: float) -> str:
    if score >= 90: return "A"
    if score >= 75: return "B"
    if score >= 60: return "C"
    if score >= 40: return "D"
    return "F"


def score_page(page: PageData, issues: list[SEOIssue]) -> float:
    """
    Calculate a 0–100 score for a single page.
    Starts at 100, deducts points per issue by severity.
    """
    page_issues = [i for i in issues if i.page_url == page.url]
    score = 100.0
    if page.status_code != 200:
        return 0.0
    for issue in page_issues:
        score -= PENALTY[issue.severity]

    return round(max(score, 0.0), 1)


def score_site(pages: list[PageData], issues: list[SEOIssue]) -> tuple[float, str]:
    """
    Calculate site-level score and grade.
    Returns: (site_score, grade)
    """
    if not pages:
        return 0.0, "F"

    for page in pages:
        page.page_score = score_page(page, issues)

    site_score = round(sum(p.page_score for p in pages) / len(pages), 1)
    return site_score, _grade(site_score)