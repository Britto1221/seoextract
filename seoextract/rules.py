from .models import PageData, SEOIssue, IssueType, Severity

TITLE_MIN        = 50
TITLE_MAX        = 60
META_MIN         = 50
META_MAX         = 160
THIN_CONTENT     = 300
MIN_INTERNAL     = 2


def _check_title(page: PageData) -> list[SEOIssue]:
    issues = []

    if not page.title:
        issues.append(SEOIssue(
            page_url      = page.url,
            issue_type    = IssueType.MISSING_TITLE,
            severity      = Severity.CRITICAL,
            current_value = "",
            suggestion    = "Add a descriptive <title> tag between 30–60 characters.",
        ))
    elif page.title_length < TITLE_MIN:
        issues.append(SEOIssue(
            page_url      = page.url,
            issue_type    = IssueType.TITLE_TOO_SHORT,
            severity      = Severity.WARNING,
            current_value = page.title,
            suggestion = f"Title is {page.title_length} chars. Expand to at least {TITLE_MIN} characters.",
        ))
    elif page.title_length > TITLE_MAX:
        issues.append(SEOIssue(
            page_url      = page.url,
            issue_type    = IssueType.TITLE_TOO_LONG,
            severity      = Severity.WARNING,
            current_value = page.title,
            suggestion    = f"Title is {page.title_length} chars. Trim to under {TITLE_MAX} characters.",
        ))

    return issues

def _check_duplicate_meta_descriptions(pages: list[PageData]) -> list[SEOIssue]:
    issues = []
    seen = {}

    for page in pages:
        if not page.meta_description:
            continue

        meta_lower = page.meta_description.strip().lower()

        if meta_lower in seen:
            issues.append(SEOIssue(
                page_url=page.url,
                issue_type=IssueType.DUPLICATE_META,
                severity=Severity.WARNING,
                current_value=page.meta_description,
                suggestion=f"This meta description duplicates '{seen[meta_lower]}'. Each page should have a unique meta description.",
            ))
        else:
            seen[meta_lower] = page.url

    return issues

def _check_meta(page: PageData) -> list[SEOIssue]:
    issues = []

    if not page.meta_description:
        issues.append(SEOIssue(
            page_url=page.url,
            issue_type=IssueType.MISSING_META,
            severity=Severity.WARNING,
            current_value="",
            suggestion="Add a meta description between 50–160 characters summarising the page.",
        ))

    elif page.meta_description_length < META_MIN:
        issues.append(SEOIssue(
            page_url=page.url,
            issue_type=IssueType.META_TOO_SHORT,
            severity=Severity.WARNING,
            current_value=page.meta_description,
            suggestion=f"Meta description is only {page.meta_description_length} chars. Expand to at least {META_MIN}.",
        ))

    elif page.meta_description_length > META_MAX:
        issues.append(SEOIssue(
            page_url=page.url,
            issue_type=IssueType.META_TOO_LONG,
            severity=Severity.WARNING,
            current_value=page.meta_description,
            suggestion=f"Meta description is {page.meta_description_length} chars. Trim to under {META_MAX}.",
        ))

    return issues


def _check_headings(page: PageData) -> list[SEOIssue]:
    issues = []

    if page.h1_count == 0:
        issues.append(SEOIssue(
            page_url      = page.url,
            issue_type    = IssueType.MISSING_H1,
            severity      = Severity.CRITICAL,
            current_value = "0 H1 tags found",
            suggestion    = "Add exactly one <h1> tag that describes the main topic of this page.",
        ))
    elif page.h1_count > 1:
        issues.append(SEOIssue(
            page_url      = page.url,
            issue_type    = IssueType.MULTIPLE_H1,
            severity      = Severity.WARNING,
            current_value = f"{page.h1_count} H1 tags: {page.h1_tags}",
            suggestion    = f"Reduce to one H1 tag. Found: {page.h1_tags}",
        ))

    return issues

def _check_status_code(page: PageData) -> list[SEOIssue]:
    issues = []

    if page.status_code >= 400 or page.status_code == 0:
        issues.append(SEOIssue(
            page_url=page.url,
            issue_type=IssueType.BROKEN_LINK,
            severity=Severity.CRITICAL,
            current_value=str(page.status_code),
            suggestion="Fix this page because it does not return a successful HTTP 200 response.",
        ))

    return issues

def _check_content(page: PageData) -> list[SEOIssue]:
    issues = []

    if page.word_count < THIN_CONTENT and page.status_code == 200:
        issues.append(SEOIssue(
            page_url      = page.url,
            issue_type    = IssueType.THIN_CONTENT,
            severity      = Severity.WARNING,
            current_value = f"{page.word_count} words",
            suggestion    = f"Page has only {page.word_count} words. Aim for at least {THIN_CONTENT} words of meaningful content.",
        ))

    return issues


def _check_images(page: PageData) -> list[SEOIssue]:
    issues = []

    if page.images_missing_alt > 0:
        issues.append(SEOIssue(
            page_url      = page.url,
            issue_type    = IssueType.MISSING_ALT_TEXT,
            severity      = Severity.WARNING,
            current_value = f"{page.images_missing_alt} of {page.total_images} images missing alt text",
            suggestion    = f"Add descriptive alt text to all {page.images_missing_alt} images missing it.",
        ))

    return issues


def _check_canonical(page: PageData) -> list[SEOIssue]:
    issues = []

    if not page.canonical and page.status_code == 200:
        issues.append(SEOIssue(
            page_url      = page.url,
            issue_type    = IssueType.MISSING_CANONICAL,
            severity      = Severity.INFO,
            current_value = "",
            suggestion    = "Add a <link rel='canonical'> tag to prevent duplicate content issues.",
        ))

    return issues


def _check_internal_linking(page: PageData) -> list[SEOIssue]:
    issues = []

    if page.internal_count < MIN_INTERNAL and page.status_code == 200:
        issues.append(SEOIssue(
            page_url      = page.url,
            issue_type    = IssueType.POOR_INTERNAL_LINKING,
            severity      = Severity.INFO,
            current_value = f"{page.internal_count} internal links",
            suggestion    = f"Add at least {MIN_INTERNAL} internal links to help search engines discover related pages.",
        ))

    return issues


def _check_schema(page: PageData) -> list[SEOIssue]:
    issues = []

    if not page.schema_found and page.status_code == 200:
        issues.append(SEOIssue(
            page_url      = page.url,
            issue_type    = IssueType.NO_SCHEMA,
            severity      = Severity.INFO,
            current_value = "No JSON-LD schema found",
            suggestion    = "Add Schema.org structured data (JSON-LD) to improve search result appearance.",
        ))

    return issues


# ── Duplicate Title Check (site-level) ───────────────────────────────────────

def _check_duplicate_titles(pages: list[PageData]) -> list[SEOIssue]:
    issues    = []
    seen      = {}  # title → first page url

    for page in pages:
        if not page.title:
            continue
        title_lower = page.title.strip().lower()
        if title_lower in seen:
            issues.append(SEOIssue(
                page_url      = page.url,
                issue_type    = IssueType.DUPLICATE_TITLE,
                severity      = Severity.CRITICAL,
                current_value = page.title,
                suggestion    = f"This title duplicates '{seen[title_lower]}'. Each page needs a unique title.",
            ))
        else:
            seen[title_lower] = page.url

    return issues

def _check_viewport(page: PageData) -> list[SEOIssue]:
    issues = []

    if not page.viewport and page.status_code == 200:
        issues.append(SEOIssue(
            page_url=page.url,
            issue_type=IssueType.MISSING_VIEWPORT,
            severity=Severity.WARNING,
            current_value="",
            suggestion="Add a viewport meta tag for mobile responsiveness.",
        ))

    return issues

def detect_issues(pages: list[PageData]) -> list[SEOIssue]:
    all_issues = []

    for page in pages:
        all_issues.extend(_check_status_code(page))

        # skip SEO checks if page failed
        if page.status_code != 200:
            continue

        all_issues.extend(_check_title(page))
        all_issues.extend(_check_meta(page))
        all_issues.extend(_check_headings(page))
        all_issues.extend(_check_content(page))
        all_issues.extend(_check_images(page))
        all_issues.extend(_check_canonical(page))
        all_issues.extend(_check_internal_linking(page))
        all_issues.extend(_check_schema(page))
        all_issues.extend(_check_duplicate_titles(pages))
        all_issues.extend(_check_duplicate_meta_descriptions(pages))
        all_issues.extend(_check_duplicate_titles(pages))
        all_issues.extend(_check_viewport(page))

    return all_issues