from enum import Enum
from pydantic import BaseModel, Field


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"


class IssueType(str, Enum):
    MISSING_VIEWPORT = "Missing Viewport Meta Tag"
    MISSING_TITLE = "Missing Title"
    TITLE_TOO_SHORT = "Title Too Short"
    TITLE_TOO_LONG = "Title Too Long"
    DUPLICATE_TITLE = "Duplicate Title"
    MISSING_META = "Missing Meta Description"
    META_TOO_SHORT = "Meta Description Too Short"
    META_TOO_LONG = "Meta Description Too Long"
    DUPLICATE_META = "Duplicate Meta Description"
    MISSING_H1 = "Missing H1 Tag"
    MULTIPLE_H1 = "Multiple H1 Tags"
    THIN_CONTENT = "Thin Content"
    MISSING_ALT_TEXT = "Missing Image Alt Text"
    MISSING_CANONICAL = "Missing Canonical Tag"
    POOR_INTERNAL_LINKING = "Poor Internal Linking"
    NO_SCHEMA = "No Schema Markup"
    PAGE_INACCESSIBLE = "Page Inaccessible"


class SEOIssue(BaseModel):
    page_url: str
    issue_type: IssueType
    severity: Severity
    current_value: str = ""
    suggestion: str


class PageData(BaseModel):
    url: str
    response_time_ms: float
    status_code: int = 0
    final_url: str | None = None

    title: str | None = None
    title_length: int = 0
    text: str = ""

    meta_description: str | None = None
    meta_description_length: int = 0

    canonical: str | None = None
    viewport: str | None = None
    robots_meta: str | None = None

    h1_tags: list[str] = Field(default_factory=list)
    h2_tags: list[str] = Field(default_factory=list)
    h3_tags: list[str] = Field(default_factory=list)
    h4_tags: list[str] = Field(default_factory=list)
    h5_tags: list[str] = Field(default_factory=list)
    h6_tags: list[str] = Field(default_factory=list)

    h1_count: int = 0
    h2_count: int = 0
    h3_count: int = 0
    h4_count: int = 0
    h5_count: int = 0
    h6_count: int = 0

    word_count: int = 0

    total_images: int = 0
    images_missing_alt: int = 0
    images: list[dict] = Field(default_factory=list)

    internal_links: list[str] = Field(default_factory=list)
    external_links: list[str] = Field(default_factory=list)
    internal_count: int = 0
    external_count: int = 0

    schema_found: bool = False

    og_title: str | None = None
    og_description: str | None = None

    page_score: float = 0.0
    page_issues_count: int = 0


class AuditResult(BaseModel):
    url: str
    audit_date: str
    pages_crawled: int
    site_score: float
    grade: str

    total_issues: int
    critical_count: int
    warning_count: int
    info_count: int

    pages: list[PageData] = Field(default_factory=list)
    issues: list[SEOIssue] = Field(default_factory=list)