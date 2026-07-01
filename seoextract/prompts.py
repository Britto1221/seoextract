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