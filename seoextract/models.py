from pydantic import BaseModel, Field

class AuditIssue(BaseModel):
    category: str = ""
    title: str = ""
    severity: str = "INFO"
    reason: str = ""
    recommendation: str = ""


class PageAudit(BaseModel):
    page_url: str = ""
    page_score: float = 0.0
    grade: str = "F"
    summary: str = ""
    issues: list[AuditIssue] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    priority_actions: list[str] = Field(default_factory=list)

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
    page_audits: list[PageAudit] = Field(default_factory=list)