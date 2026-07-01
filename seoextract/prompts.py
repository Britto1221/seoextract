def title_prompt(title: str, page_text: str) -> str:
    return f"""
You are an SEO audit expert.

Analyze this page title.

Title:
{title}

Page Content:
{page_text[:3000]}

Check:
- Is the title clear?
- Is it relevant to the page?
- Is it SEO-friendly?
- Is it too generic?
- Is it click-worthy without being clickbait?
- Suggest a better title if needed.

Return JSON:
{{
  "issue_found": true/false,
  "severity": "critical/warning/info",
  "reason": "...",
  "recommendation": "...",
  "improved_title": "..."
}}
"""


def meta_description_prompt(meta_description: str, page_text: str) -> str:
    return f"""
You are an SEO audit expert.

Analyze this meta description.

Meta Description:
{meta_description}

Page Content:
{page_text[:3000]}

Check:
- Is it clear?
- Does it summarize the page?
- Is it persuasive?
- Does it match search intent?
- Is it too generic?
- Suggest a better meta description if needed.

Return JSON:
{{
  "issue_found": true/false,
  "severity": "critical/warning/info",
  "reason": "...",
  "recommendation": "...",
  "improved_meta_description": "..."
}}
"""


def heading_prompt(headings: dict, page_text: str) -> str:
    return f"""
You are an SEO audit expert.

Analyze the heading structure.

Headings:
{headings}

Page Content:
{page_text[:3000]}

Check:
- Is the H1 clear and relevant?
- Are H2/H3 headings logical?
- Do headings match page content?
- Are headings useful for users?
- Is the structure SEO-friendly?
- Are there missing or weak headings?

Return JSON:
{{
  "issue_found": true/false,
  "severity": "critical/warning/info",
  "reason": "...",
  "recommendation": "...",
  "improved_headings": {{
    "h1": "...",
    "h2": ["...", "..."]
  }}
}}
"""


def content_prompt(page_text: str) -> str:
    return f"""
You are an SEO audit expert.

Analyze this page content.

Page Content:
{page_text[:5000]}

Check:
- Is the content helpful?
- Is it thin or weak?
- Does it satisfy user intent?
- Is it specific enough?
- Is it keyword-stuffed?
- Is it readable?
- What content should be added?

Return JSON:
{{
  "issue_found": true/false,
  "severity": "critical/warning/info",
  "reason": "...",
  "recommendation": "...",
  "content_gaps": ["...", "..."],
  "improved_summary": "..."
}}
"""


def image_prompt(images: list, page_text: str) -> str:
    return f"""
You are an SEO audit expert.

Analyze image SEO.

Images:
{images}

Page Content:
{page_text[:3000]}

Check:
- Are alt texts useful?
- Are image filenames descriptive?
- Are images relevant to the content?
- Are any images missing alt text?
- Suggest better alt text where needed.

Return JSON:
{{
  "issue_found": true/false,
  "severity": "critical/warning/info",
  "reason": "...",
  "recommendation": "...",
  "image_fixes": [
    {{
      "image": "...",
      "suggested_alt": "..."
    }}
  ]
}}
"""


def links_prompt(internal_links: list, external_links: list, page_text: str) -> str:
    return f"""
You are an SEO audit expert.

Analyze the internal and external linking.

Internal Links:
{internal_links}

External Links:
{external_links}

Page Content:
{page_text[:3000]}

Check:
- Are internal links useful?
- Are anchor texts descriptive?
- Are external links relevant?
- Are there enough useful links?
- Are links helping SEO and user navigation?

Return JSON:
{{
  "issue_found": true/false,
  "severity": "critical/warning/info",
  "reason": "...",
  "recommendation": "...",
  "link_suggestions": ["...", "..."]
}}
"""


def technical_prompt(technical_data: dict) -> str:
    return f"""
You are an SEO technical auditor.

Analyze this technical SEO data.

Technical Data:
{technical_data}

Check:
- Canonical tag
- Viewport tag
- Robots meta tag
- Schema markup
- HTTPS
- Indexability
- Mobile friendliness signals
- Duplicate technical issues

Return JSON:
{{
  "issue_found": true/false,
  "severity": "critical/warning/info",
  "reason": "...",
  "recommendation": "...",
  "technical_fixes": ["...", "..."]
}}
"""


def full_page_audit_prompt(page_data: dict) -> str:
    return f"""
You are an expert SEO auditor.

Analyze this full page SEO data.

Page Data:
{page_data}

Check:
- Title
- Meta description
- Headings
- Content quality
- Image SEO
- Internal links
- External links
- Technical SEO
- Search intent match
- Overall SEO quality

Return JSON:
{{
  "page_score": 0-100,
  "grade": "A/B/C/D/F",
  "top_issues": ["...", "..."],
  "critical_issues": ["...", "..."],
  "warnings": ["...", "..."],
  "recommendations": ["...", "..."],
  "summary": "..."
}}
"""