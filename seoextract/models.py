from pydantic import BaseModel, HttpUrl
from typing import Optional
from enum import Enum


# ── Severity Levels ──────────────────────────────────────────────────────────

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING  = "WARNING"
    INFO     = "INFO"

class SafeBrowsingResult(BaseModel):
    is_safe: bool | None
    threats: list[str] = []
    error: str | None = None
# ── Issue Types ───────────────────────────────────────────────────────────────

class IssueType(str, Enum):
    MISSING_VIEWPORT = "Missing Viewport Meta Tag"
    META_TOO_SHORT = "Meta Description Too Short"
    MISSING_TITLE         = "Missing Title"
    TITLE_TOO_SHORT       = "Title Too Short"
    TITLE_TOO_LONG        = "Title Too Long"
    DUPLICATE_TITLE       = "Duplicate Title"
    MISSING_META          = "Missing Meta Description"
    META_TOO_LONG         = "Meta Description Too Long"
    MISSING_H1            = "Missing H1 Tag"
    MULTIPLE_H1           = "Multiple H1 Tags"
    THIN_CONTENT          = "Thin Content"
    MISSING_ALT_TEXT      = "Missing Image Alt Text"
    BROKEN_LINK           = "Broken Internal Link"
    MISSING_CANONICAL     = "Missing Canonical Tag"
    POOR_INTERNAL_LINKING = "Poor Internal Linking"
    NO_SCHEMA             = "No Schema Markup"
    MISSING_ROBOTS_META   = "Missing Robots Meta Tag"
    DUPLICATE_META = "Duplicate Meta Description"


# ── Single SEO Issue ──────────────────────────────────────────────────────────

class SEOIssue(BaseModel):
    page_url      : str
    issue_type    : IssueType
    severity      : Severity
    current_value : str        # what was found (or empty string if missing)
    suggestion    : str        # one-line hint for fixing it


# ── Per-Page Extracted Data ───────────────────────────────────────────────────

class PageData(BaseModel):
    url              : str
    status_code      : int
    response_time_ms : float

    # Title
    title            : Optional[str] = None
    title_length     : int = 0

    # Meta
    meta_description        : Optional[str] = None
    meta_description_length : int = 0

    # Robots + Canonical
    robots_meta : Optional[str] = None   # e.g. "noindex, nofollow"
    canonical   : Optional[str] = None

    # Headings
    h1_tags : list[str] = []
    h2_tags : list[str] = []
    h3_tags : list[str] = []
    h1_count: int = 0
    h2_count: int = 0
    h3_count: int = 0

    # Content
    word_count: int = 0

    # Images
    total_images        : int = 0
    images_missing_alt  : int = 0

    # Links
    internal_links : list[str] = []
    external_links : list[str] = []
    internal_count : int = 0
    external_count : int = 0

    # Schema
    schema_found : bool = False

    # Open Graph
    og_title       : Optional[str] = None
    og_description : Optional[str] = None

    # Scoring
    page_score : float = 0.0

    final_url: Optional[str] = None

    viewport: Optional[str] = None

class AuditResult(BaseModel):
    url           : str
    audit_date    : str
    pages_crawled : int
    site_score    : float
    grade         : str          # A / B / C / D / F
    total_issues  : int
    critical_count: int
    warning_count : int
    info_count    : int
    pages         : list[PageData]
    issues        : list[SEOIssue]
    safe_browsing: SafeBrowsingResult