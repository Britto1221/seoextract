from collections import Counter

from .models import IssueType, PageData, SEOIssue, Severity


def _issue(
    page_url: str,
    issue_type: IssueType,
    severity: Severity,
    current_value: str,
    suggestion: str,
) -> SEOIssue:
    return SEOIssue(
        page_url=page_url,
        issue_type=issue_type,
        severity=severity,
        current_value=current_value,
        suggestion=suggestion,
    )


def _page_key(page: PageData) -> str:
    return (page.final_url or page.url).rstrip("/")


def detect_issues(pages: list[PageData]) -> list[SEOIssue]:
    issues: list[SEOIssue] = []

    # Deduplicate page identity when checking duplicate titles/meta
    unique_title_pages: dict[str, str] = {}
    unique_meta_pages: dict[str, str] = {}

    for page in pages:
        key = _page_key(page)

        title = (page.title or "").strip().lower()
        if title and key not in unique_title_pages:
            unique_title_pages[key] = title

        meta = (page.meta_description or "").strip().lower()
        if meta and key not in unique_meta_pages:
            unique_meta_pages[key] = meta

    title_counter = Counter(unique_title_pages.values())
    meta_counter = Counter(unique_meta_pages.values())

    for page in pages:
        if page.status_code != 200:
            issues.append(
                _issue(
                    page.url,
                    IssueType.PAGE_INACCESSIBLE,
                    Severity.CRITICAL,
                    f"HTTP {page.status_code}",
                    "The page could not be accessed successfully. Fix timeout, redirect, DNS, SSL, or server issues before auditing on-page SEO.",
                )
            )
            continue

        # title rules
        if not page.title:
            issues.append(
                _issue(
                    page.url,
                    IssueType.MISSING_TITLE,
                    Severity.WARNING,
                    "",
                    "Add a descriptive HTML title tag for the page.",
                )
            )
        else:
            if page.title_length < 30:
                issues.append(
                    _issue(
                        page.url,
                        IssueType.TITLE_TOO_SHORT,
                        Severity.WARNING,
                        f"{page.title_length} characters",
                        "Expand the title to around 30–60 characters while keeping it specific and relevant.",
                    )
                )

            if page.title_length > 60:
                issues.append(
                    _issue(
                        page.url,
                        IssueType.TITLE_TOO_LONG,
                        Severity.INFO,
                        f"{page.title_length} characters",
                        "Shorten the title to around 30–60 characters to reduce truncation risk in search results.",
                    )
                )

            if title_counter[(page.title or "").strip().lower()] > 1:
                issues.append(
                    _issue(
                        page.url,
                        IssueType.DUPLICATE_TITLE,
                        Severity.WARNING,
                        page.title,
                        "Use a unique title for this page so search engines can distinguish it from other pages.",
                    )
                )

        # meta description rules
        if not page.meta_description:
            issues.append(
                _issue(
                    page.url,
                    IssueType.MISSING_META,
                    Severity.WARNING,
                    "",
                    "Add a meta description summarizing the page in roughly 50–160 characters.",
                )
            )
        else:
            if page.meta_description_length < 50:
                issues.append(
                    _issue(
                        page.url,
                        IssueType.META_TOO_SHORT,
                        Severity.INFO,
                        f"{page.meta_description_length} characters",
                        "Expand the meta description to better explain the page and improve search snippet quality.",
                    )
                )

            if page.meta_description_length > 160:
                issues.append(
                    _issue(
                        page.url,
                        IssueType.META_TOO_LONG,
                        Severity.INFO,
                        f"{page.meta_description_length} characters",
                        "Shorten the meta description to around 50–160 characters to reduce truncation.",
                    )
                )

            if meta_counter[(page.meta_description or "").strip().lower()] > 1:
                issues.append(
                    _issue(
                        page.url,
                        IssueType.DUPLICATE_META,
                        Severity.INFO,
                        page.meta_description,
                        "Write a unique meta description for this page.",
                    )
                )

        # heading rules
        if page.h1_count == 0:
            issues.append(
                _issue(
                    page.url,
                    IssueType.MISSING_H1,
                    Severity.WARNING,
                    "0 H1 tags",
                    "Add a single clear H1 heading describing the main topic of the page.",
                )
            )
        elif page.h1_count > 1:
            issues.append(
                _issue(
                    page.url,
                    IssueType.MULTIPLE_H1,
                    Severity.INFO,
                    f"{page.h1_count} H1 tags",
                    "Use one primary H1 where possible and move other headings into H2/H3 levels.",
                )
            )

        # content rules
        if page.word_count < 300:
            issues.append(
                _issue(
                    page.url,
                    IssueType.THIN_CONTENT,
                    Severity.WARNING,
                    f"{page.word_count} words",
                    "Add more useful page content. Aim for at least 300 words where appropriate.",
                )
            )

        # image rules
        if page.images_missing_alt > 0:
            issues.append(
                _issue(
                    page.url,
                    IssueType.MISSING_ALT_TEXT,
                    Severity.INFO,
                    f"{page.images_missing_alt} images missing alt text",
                    "Add descriptive alt text to important images for accessibility and image SEO.",
                )
            )

        # internal linking
        if page.internal_count < 2:
            issues.append(
                _issue(
                    page.url,
                    IssueType.POOR_INTERNAL_LINKING,
                    Severity.INFO,
                    f"{page.internal_count} internal links",
                    "Add more relevant internal links to related pages to improve crawlability and site structure.",
                )
            )

        # canonical
        if not page.canonical:
            issues.append(
                _issue(
                    page.url,
                    IssueType.MISSING_CANONICAL,
                    Severity.INFO,
                    "",
                    "Add a canonical tag to indicate the preferred version of the page.",
                )
            )

        # viewport
        if not page.viewport:
            issues.append(
                _issue(
                    page.url,
                    IssueType.MISSING_VIEWPORT,
                    Severity.INFO,
                    "",
                    "Add a viewport meta tag for mobile responsiveness.",
                )
            )

        # schema
        if not page.schema_found:
            issues.append(
                _issue(
                    page.url,
                    IssueType.NO_SCHEMA,
                    Severity.INFO,
                    "",
                    "Add relevant Schema.org structured data where appropriate.",
                )
            )

    return issues