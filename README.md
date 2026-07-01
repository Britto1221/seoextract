# SEOExtract

<div align="center">

# AI-Powered SEO Audit Engine for Python

Analyze websites using Large Language Models and receive structured, page-level SEO audits with actionable recommendations.

Built for developers, AI agents, automation pipelines, dashboards, and SEO applications.

</div>

---

## Features

- AI-powered SEO auditing
- Website crawler
- Multi-page website analysis
- Technical SEO analysis
- Content quality evaluation
- Heading structure analysis
- Meta title & description analysis
- Internal & external link analysis
- Image SEO analysis
- Schema.org detection
- Open Graph detection
- Canonical tag detection
- Viewport detection
- Structured JSON output
- Pydantic models
- Page-level scoring
- Site-level scoring
- AI-generated recommendations

---

# Installation

```bash
pip install seoextract
```

or

```bash
pip install -e .
```

---

# Requirements

- Python 3.10+
- OpenAI API Key

---

# API Key Setup

Create a `.env` file.

```env
OPENAI_API_KEY=your_api_key
```

SEOExtract automatically loads the API key.

---

# Quick Start

```python
from seoextract import SEOExtract

result = SEOExtract.audit(
    "https://example.com"
)

print(result.site_score)
print(result.grade)
```

---

# Output

SEOExtract returns an `AuditResult`.

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
└── page_audits
```

Each page audit contains:

```text
Page Audit
│
├── page_url
├── page_score
├── grade
├── summary
├── strengths
├── priority_actions
└── issues
```

---

# Example

```python
from seoextract import SEOExtract

result = SEOExtract.audit("https://example.com")

print(result.site_score)

for page in result.page_audits:
    print(page["page_url"])
    print(page["page_score"])
    print(page["summary"])
```

---

# What SEOExtract Evaluates

### Content

- Content quality
- Search intent alignment
- Readability
- Content depth
- Value proposition

### Metadata

- Page title
- Meta description
- Open Graph metadata

### Headings

- Heading hierarchy
- Heading clarity
- Heading relevance

### Images

- Missing ALT text
- Image relevance
- Image optimization suggestions

### Links

- Internal linking
- External linking
- Anchor text quality

### Technical SEO

- Canonical tags
- Viewport meta tag
- Robots meta tag
- Schema markup
- Mobile readiness
- Overall technical quality

### Overall

- Page SEO score
- Overall grade
- AI-generated recommendations
- Priority fixes

---

# Example Result

```python
AuditResult(
    site_score=92.5,
    grade="A",
    pages_crawled=8,
    total_issues=17
)
```

---

# Project Structure

```text
seoextract/
│
├── __init__.py
├── auditor.py
├── crawler.py
├── parser.py
├── prompts.py
├── llm.py
├── models.py
├── utils.py
└── reports/
```

---

# Designed For

SEOExtract is ideal for:

- AI SEO Agents
- SEO automation
- FastAPI applications
- LangGraph workflows
- LangChain applications
- Streamlit dashboards
- CI/CD quality checks
- Report generators
- AI assistants
- Python automation

---

# Dependencies

- beautifulsoup4
- lxml
- requests
- pydantic
- python-dotenv
- langchain-openai

---

# Roadmap

- PDF reports
- Excel reports
- JSON export
- Custom LLM providers
- Local LLM support
- Batch website auditing
- Audit comparison
- Plugin architecture

---

# License

MIT License

---

# Author

**Britto K**

GitHub:
https://github.com/Britto1221