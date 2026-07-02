from .models import PageData, SEOIssue, Severity


SEVERITY_PENALTY = {
    Severity.CRITICAL: 20,
    Severity.WARNING: 8,
    Severity.INFO: 3,
}


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


def score_site(pages: list[PageData], issues: list[SEOIssue]) -> tuple[float, str]:
    issues_by_page: dict[str, list[SEOIssue]] = {}

    for issue in issues:
        issues_by_page.setdefault(issue.page_url, []).append(issue)

    for page in pages:
        page_issue_list = issues_by_page.get(page.url, [])
        page.page_issues_count = len(page_issue_list)

        if page.status_code != 200:
            page.page_score = 0.0
            continue

        score = 100.0
        for issue in page_issue_list:
            score -= SEVERITY_PENALTY.get(issue.severity, 0)

        page.page_score = max(0.0, round(score, 1))

    if not pages:
        return 0.0, "F"

    site_score = round(sum(page.page_score for page in pages) / len(pages), 1)
    return site_score, get_grade(site_score)