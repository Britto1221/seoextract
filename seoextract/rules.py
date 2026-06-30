from .models import IssueType, PageData, SEOIssue, Severity

TITLE_MIN, TITLE_MAX = 50, 60
META_MIN, META_MAX = 50, 160
THIN_CONTENT, MIN_INTERNAL = 300, 2


def issue(page: PageData, issue_type: IssueType, severity: Severity, current_value: str, suggestion: str) -> SEOIssue:
    return SEOIssue(page_url=page.url, issue_type=issue_type, severity=severity, current_value=current_value, suggestion=suggestion)


def _check_page(page: PageData) -> list[SEOIssue]:
    issues = []

    if page.status_code >= 400 or page.status_code == 0:
        return [issue(page, IssueType.BROKEN_LINK, Severity.CRITICAL, str(page.status_code), "Fix this page because it does not return a successful HTTP 200 response.")]

    checks = [
        (not page.title, IssueType.MISSING_TITLE, Severity.CRITICAL, "", "Add a descriptive <title> tag between 30–60 characters."),
        (page.title and page.title_length < TITLE_MIN, IssueType.TITLE_TOO_SHORT, Severity.WARNING, page.title or "", f"Title is {page.title_length} chars. Expand to at least {TITLE_MIN} characters."),
        (page.title and page.title_length > TITLE_MAX, IssueType.TITLE_TOO_LONG, Severity.WARNING, page.title or "", f"Title is {page.title_length} chars. Trim to under {TITLE_MAX} characters."),
        (not page.meta_description, IssueType.MISSING_META, Severity.WARNING, "", "Add a meta description between 50–160 characters summarising the page."),
        (page.meta_description and page.meta_description_length < META_MIN, IssueType.META_TOO_SHORT, Severity.WARNING, page.meta_description or "", f"Meta description is only {page.meta_description_length} chars. Expand to at least {META_MIN}."),
        (page.meta_description and page.meta_description_length > META_MAX, IssueType.META_TOO_LONG, Severity.WARNING, page.meta_description or "", f"Meta description is {page.meta_description_length} chars. Trim to under {META_MAX}."),
        (page.h1_count == 0, IssueType.MISSING_H1, Severity.CRITICAL, "0 H1 tags found", "Add exactly one <h1> tag that describes the main topic of this page."),
        (page.h1_count > 1, IssueType.MULTIPLE_H1, Severity.WARNING, f"{page.h1_count} H1 tags: {page.h1_tags}", f"Reduce to one H1 tag. Found: {page.h1_tags}"),
        (page.word_count < THIN_CONTENT, IssueType.THIN_CONTENT, Severity.WARNING, f"{page.word_count} words", f"Page has only {page.word_count} words. Aim for at least {THIN_CONTENT} words of meaningful content."),
        (page.images_missing_alt > 0, IssueType.MISSING_ALT_TEXT, Severity.WARNING, f"{page.images_missing_alt} of {page.total_images} images missing alt text", f"Add descriptive alt text to all {page.images_missing_alt} images missing it."),
        (not page.canonical, IssueType.MISSING_CANONICAL, Severity.INFO, "", "Add a <link rel='canonical'> tag to prevent duplicate content issues."),
        (page.internal_count < MIN_INTERNAL, IssueType.POOR_INTERNAL_LINKING, Severity.INFO, f"{page.internal_count} internal links", f"Add at least {MIN_INTERNAL} internal links to help search engines discover related pages."),
        (not page.schema_found, IssueType.NO_SCHEMA, Severity.INFO, "No JSON-LD schema found", "Add Schema.org structured data (JSON-LD) to improve search result appearance."),
        (not page.viewport, IssueType.MISSING_VIEWPORT, Severity.WARNING, "", "Add a viewport meta tag for mobile responsiveness."),
    ]
    return [issue(page, it, sev, val, sug) for ok, it, sev, val, sug in checks if ok]


def _duplicates(pages: list[PageData], attr: str, issue_type: IssueType, severity: Severity, label: str) -> list[SEOIssue]:
    seen, issues = {}, []
    for page in pages:
        value = getattr(page, attr)
        if not value:
            continue
        key = value.strip().lower()
        if key in seen:
            issues.append(issue(page, issue_type, severity, value, f"This {label} duplicates '{seen[key]}'. Each page should have a unique {label}."))
        else:
            seen[key] = page.url
    return issues


def detect_issues(pages: list[PageData]) -> list[SEOIssue]:
    issues = [seo_issue for page in pages for seo_issue in _check_page(page)]
    issues += _duplicates(pages, "title", IssueType.DUPLICATE_TITLE, Severity.CRITICAL, "title")
    issues += _duplicates(pages, "meta_description", IssueType.DUPLICATE_META, Severity.WARNING, "meta description")
    return issues
