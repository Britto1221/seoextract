# SEOExtract

<div align="center">

# Rule-Based SEO Audit Engine for Python

Crawl websites, extract SEO signals, detect on-page SEO issues, and receive structured page-level audit results with scoring and actionable suggestions.

Built for developers, automation pipelines, dashboards, APIs, and AI systems that need clean structured SEO audit data.

</div>

---

## What SEOExtract Does

SEOExtract takes a website URL and runs a structured SEO audit pipeline:

```text
Website URL
    ↓
Crawl pages
    ↓
Parse HTML into structured SEO data
    ↓
Apply rule-based SEO checks
    ↓
Detect issues with severity
    ↓
Score each page and the overall site
    ↓
Return validated Pydantic output
```

---

## Features

- Rule-based SEO auditing
- Website crawler
- Multi-page website analysis
- Technical SEO analysis
- Content quality checks
- Heading structure analysis
- Meta title and description analysis
- Internal link analysis
- Image alt-text analysis
- Schema.org detection
- Open Graph extraction
- Canonical tag detection
- Viewport detection
- Structured JSON output
- Pydantic models
- Page-level scoring
- Site-level scoring
- Severity-based issue detection

---

## Installation

```bash
pip install seoextract
```

Or install from source:

```bash
git clone https://github.com/Britto1221/seoextract.git
cd seoextract
pip install -e .
```

---

## Requirements

- Python 3.10+

---

## Quick Start

```python
from seoextract import SEOExtract

result = SEOExtract.audit("https://example.com")

print(result.site_score)
print(result.grade)
```

---

## CLI Usage

Run an audit from the terminal:

```bash
seoextract audit https://example.com --max-pages 5
```

Show the installed version:

```bash
seoextract version
```

---

## Output

SEOExtract returns a validated `AuditResult` Pydantic object.

```text
AuditResult
│
├── url
├── audit_date
├── pages_crawled
├── site_score
├── grade
├── total_issues
├── critical_count
├── warning_count
├── info_count
├── pages
└── issues
```

Each crawled page is returned as `PageData`:

```text
PageData
│
├── url
├── final_url
├── status_code
├── response_time_ms
├── title
├── title_length
├── text
├── meta_description
├── meta_description_length
├── canonical
├── viewport
├── robots_meta
├── h1_tags ... h6_tags
├── h1_count ... h6_count
├── word_count
├── total_images
├── images_missing_alt
├── images
├── internal_links
├── external_links
├── internal_count
├── external_count
├── schema_found
├── og_title
├── og_description
├── page_score
└── page_issues_count
```

Each detected issue is returned as `SEOIssue`:

```text
SEOIssue
│
├── page_url
├── issue_type
├── severity
├── current_value
└── suggestion
```

---

## Example

```python
from seoextract import SEOExtract

result = SEOExtract.audit("https://example.com", max_pages=3)

print("Site score:", result.site_score)
print("Grade:", result.grade)
print("Total issues:", result.total_issues)

for issue in result.issues:
    print(issue.page_url)
    print(issue.issue_type)
    print(issue.severity)
    print(issue.suggestion)
```

---

## Inspect Page Data

```python
from seoextract import SEOExtract

result = SEOExtract.audit("https://www.python.org", max_pages=3)

for page in result.pages:
    print(page.url)
    print(page.title)
    print(page.word_count)
    print(page.page_score)
    print(page.page_issues_count)
```

---

## Export as JSON

```python
from seoextract import SEOExtract

result = SEOExtract.audit("https://example.com")

json_output = result.model_dump_json(indent=2)
print(json_output)
```

---

## What SEOExtract Evaluates

### Content

- Thin content detection
- Basic page content quality checks using word count

### Metadata

- Missing title
- Title too short
- Title too long
- Duplicate titles
- Missing meta description
- Meta description too short
- Meta description too long
- Duplicate meta descriptions
- Open Graph extraction

### Headings

- Missing H1
- Multiple H1 tags
- Heading extraction for H1–H6

### Images

- Missing ALT text detection
- Image extraction and metadata capture

### Links

- Internal link extraction
- External link extraction
- Poor internal linking detection

### Technical SEO

- Canonical tag detection
- Viewport meta tag detection
- Robots meta tag extraction
- Schema markup detection
- Page accessibility checks

### Overall

- Page SEO score
- Site-wide SEO score
- Severity-based issue summaries
- Structured audit output for automation

---

## Current SEO Checks

- Missing title
- Title too short
- Title too long
- Duplicate title
- Missing meta description
- Meta description too short
- Meta description too long
- Duplicate meta description
- Missing H1
- Multiple H1 tags
- Thin content detection
- Missing image alt text
- Poor internal linking
- Missing canonical tag
- Missing viewport meta tag
- Missing schema markup
- Page inaccessible detection

---

## Example Result

```python
AuditResult(
    site_score=81.0,
    grade="B",
    pages_crawled=3,
    total_issues=14
)
```

---

## Example Output Structure

```json
{
  "url": "https://example.com",
  "audit_date": "2026-07-02 12:00",
  "pages_crawled": 1,
  "site_score": 67.0,
  "grade": "C",
  "total_issues": 6,
  "critical_count": 0,
  "warning_count": 3,
  "info_count": 3,
  "pages": [
    {
      "url": "https://example.com/",
      "status_code": 200,
      "title": "Example Domain",
      "title_length": 14,
      "word_count": 21,
      "internal_count": 0,
      "schema_found": false,
      "page_score": 67.0,
      "page_issues_count": 6
    }
  ],
  "issues": [
    {
      "page_url": "https://example.com/",
      "issue_type": "Missing Meta Description",
      "severity": "WARNING",
      "current_value": "",
      "suggestion": "Add a meta description summarizing the page in roughly 50–160 characters."
    }
  ]
}
```

---

## Scoring

SEOExtract calculates a page score for every crawled page and a site score across all pages.

### Grade Scale

- **A** → 90–100
- **B** → 75–89
- **C** → 60–74
- **D** → 40–59
- **F** → 0–39

### Severity Model

SEOExtract uses issue severity to reduce page scores:

- `CRITICAL` → major SEO or accessibility problem
- `WARNING` → important SEO issue
- `INFO` → lower-priority improvement

The final site score is the average of all crawled page scores.

---

## Project Structure

```text
seoextract/
│
├── __init__.py
├── core.py
├── crawler.py
├── parser.py
├── rules.py
├── scorer.py
├── models.py
└── cli.py
```

---

## How the Package Is Organized

### `crawler.py`

Responsible for:

- Fetching pages
- Respecting robots.txt
- Extracting internal links
- Crawling multiple pages

### `parser.py`

Responsible for:

- Parsing HTML
- Extracting SEO-relevant page data
- Converting raw HTML into structured `PageData`

### `rules.py`

Responsible for:

- Applying SEO rules
- Detecting issues
- Assigning severity

### `scorer.py`

Responsible for:

- Calculating page-level scores
- Calculating site-level scores
- Assigning grades

### `core.py`

Responsible for:

- Orchestrating the full audit flow
- Calling the crawler, parser, rules engine, and scorer
- Returning the final `AuditResult`

### `cli.py`

Responsible for:

- Exposing SEOExtract as a terminal command
- Printing audit summaries and detected issues

---

## Designed For

SEOExtract is ideal for:

- SEO automation
- FastAPI applications
- LangGraph workflows
- LangChain applications
- Streamlit dashboards
- CI/CD quality checks
- Report generators
- AI systems that need deterministic SEO audit data
- Python automation
- Technical SEO pipelines

---

## What SEOExtract Is Not

SEOExtract is a technical and on-page SEO audit engine.

It does not currently perform:

- Keyword research
- Competitor analysis
- Backlink analysis
- Rank tracking
- Content strategy generation
- Business growth strategy

Those can be built on top of SEOExtract in a separate SEO agent, analytics system, or reporting application.

---

## Example Use Cases

- Crawl and audit a client website from Python
- Feed structured SEO issues into a dashboard
- Run technical SEO checks inside a CI workflow
- Use as the deterministic audit layer for an AI SEO agent
- Generate reports from Pydantic output
- Compare SEO health across multiple websites

---

## Dependencies

- beautifulsoup4
- lxml
- requests
- pydantic
- typer
- rich

---

## Roadmap

Potential future additions:

- Broken link validation
- Sitemap parsing
- robots.txt reporting
- JSON export mode for CLI
- CSV / report export
- Configurable scoring thresholds
- Audit comparison mode
- Optional AI recommendation layer built on top of rule output

---

## License

MIT License

---

## Author

**Britto K**

GitHub:  
https://github.com/Britto1221
