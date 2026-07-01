def full_page_audit_prompt(page_data: dict) -> str:
    return f"""
You are an expert SEO auditor.

Analyze the following extracted webpage data and return ONLY valid JSON.

Webpage Data:
{page_data}

Evaluate:
- Title quality
- Meta description quality
- Heading structure
- Content quality
- Search intent match
- Internal linking
- External linking
- Image SEO
- Canonical tag
- Robots meta tag
- Viewport/mobile readiness
- Schema markup
- Open Graph tags
- Overall technical SEO
- Overall user experience

Scoring guide:
- 90–100 = Excellent SEO. Strong metadata, content, structure, links, and technical setup.
- 75–89 = Good SEO. Minor improvements needed.
- 60–74 = Average SEO. Several issues, but page is usable and indexable.
- 40–59 = Weak SEO. Major improvements needed, but page is still accessible.
- 20–39 = Poor SEO. Severe SEO weaknesses.
- 0–19 = Critical failure. Use only if the page is inaccessible, blocked, empty, broken, unsafe, or cannot be analyzed.

If the page is accessible and contains readable HTML content, the page_score should usually be above 20.

Important scoring rule:
Do not assign 0 unless the page cannot be accessed, has no readable content, or the audit fails.

Return JSON in this exact structure:

{{
  "page_score": 0,
  "grade": "A/B/C/D/F",
  "summary": "Short summary of the page SEO quality.",
  "issues": [
    {{
      "category": "Title/Meta/Heading/Content/Links/Images/Technical/UX",
      "title": "Short issue title",
      "severity": "CRITICAL/WARNING/INFO",
      "reason": "Why this is an issue.",
      "recommendation": "How to fix it."
    }}
  ],
  "strengths": [
    "Strength 1",
    "Strength 2"
  ],
  "priority_actions": [
    "Most important action 1",
    "Most important action 2"
  ]
}}

Scoring guide:
- 90–100 = A
- 75–89 = B
- 60–74 = C
- 40–59 = D
- 0–39 = F

Rules:
- Return JSON only.
- Do not include markdown.
- Do not include explanations outside JSON.
- If there are no serious issues, keep issues as an empty list.
"""

def site_context_prompt(homepage_data: dict) -> str:
    return f"""
You are an SEO strategist.

Analyze this homepage data and identify the website's business context.

Homepage Data:
{homepage_data}

Return ONLY valid JSON in this structure:

{{
  "brand_name": "",
  "domain": "",
  "business_type": "",
  "industry": "",
  "target_audience": "",
  "products_or_services": [],
  "geographic_focus": "",
  "main_business_goal": "",
  "seo_opportunities": []
}}

Rules:
- Return JSON only.
- Do not include markdown.
- If something is unknown, use an empty string or empty list.
"""