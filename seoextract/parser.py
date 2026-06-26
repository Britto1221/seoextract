import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from .models import PageData


def parse(fetch_result: dict) -> PageData:
    """
    Takes one fetch_result dict from crawler.
    Returns a fully populated PageData object.
    """
    url              = fetch_result["url"]
    final_url        = fetch_result.get("final_url", url)
    status_code      = fetch_result["status_code"]
    response_time_ms = fetch_result["response_time_ms"]
    html             = fetch_result.get("html", "")

    # Base for resolving relative URLs
    parsed_base  = urlparse(final_url)
    base_domain  = parsed_base.netloc
    base_url     = f"{parsed_base.scheme}://{base_domain}"

    # If no HTML (error page, non-HTML, timeout) return minimal PageData
    if not html:
        return PageData(
            url=url,
            status_code=status_code,
            response_time_ms=response_time_ms,
        )

    soup = BeautifulSoup(html, "lxml")

    # ── Title ─────────────────────────────────────────────────────────────────
    title_tag    = soup.find("title")
    title        = title_tag.get_text(strip=True) if title_tag else None
    title_length = len(title) if title else 0

    # ── Meta Description ──────────────────────────────────────────────────────
    meta_tag = soup.find("meta", attrs={"name": lambda n: n and n.lower() == "description"})
    meta_description        = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else None
    meta_description_length = len(meta_description) if meta_description else 0

    # ── Robots Meta ───────────────────────────────────────────────────────────
    robots_tag  = soup.find("meta", attrs={"name": lambda n: n and n.lower() == "robots"})
    robots_meta = robots_tag["content"].strip() if robots_tag and robots_tag.get("content") else None

    viewport_tag = soup.find("meta", attrs={"name": lambda n: n and n.lower() == "viewport"})
    viewport = viewport_tag["content"].strip() if viewport_tag and viewport_tag.get("content") else None

    # ── Canonical ─────────────────────────────────────────────────────────────
    canonical_tag = soup.find("link", attrs={"rel": lambda r: r and "canonical" in r})
    canonical     = canonical_tag["href"].strip() if canonical_tag and canonical_tag.get("href") else None

    # ── Headings ──────────────────────────────────────────────────────────────
    h1_tags = [tag.get_text(strip=True) for tag in soup.find_all("h1")]
    h2_tags = [tag.get_text(strip=True) for tag in soup.find_all("h2")]
    h3_tags = [tag.get_text(strip=True) for tag in soup.find_all("h3")]

    # ── Word Count ────────────────────────────────────────────────────────────
    # Remove script and style tags before counting
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    body_text  = soup.get_text(separator=" ", strip=True)
    word_count = len(body_text.split())

    # ── Images ────────────────────────────────────────────────────────────────
    all_images        = soup.find_all("img")
    total_images      = len(all_images)
    images_missing_alt = sum(
        1 for img in all_images
        if not img.get("alt") or img["alt"].strip() == ""
    )

    # ── Links ─────────────────────────────────────────────────────────────────
    internal_links = []
    external_links = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue

        full_url = urljoin(final_url, href)
        link_domain = urlparse(full_url).netloc

        if link_domain == base_domain:
            internal_links.append(full_url)
        else:
            external_links.append(full_url)

    # Deduplicate
    internal_links = list(set(internal_links))
    external_links = list(set(external_links))

    # ── Schema Markup ─────────────────────────────────────────────────────────
    schema_found = False
    for script_tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script_tag.string or "")
            if data:
                schema_found = True
                break
        except (json.JSONDecodeError, TypeError):
            continue

    # ── Open Graph ────────────────────────────────────────────────────────────
    og_title_tag       = soup.find("meta", attrs={"property": "og:title"})
    og_description_tag = soup.find("meta", attrs={"property": "og:description"})
    og_title           = og_title_tag["content"].strip() if og_title_tag and og_title_tag.get("content") else None
    og_description     = og_description_tag["content"].strip() if og_description_tag and og_description_tag.get("content") else None

    return PageData(
        url=url,
        final_url=final_url,
        status_code=status_code,
        response_time_ms=response_time_ms,
        title=title,
        title_length=title_length,
        meta_description=meta_description,
        meta_description_length=meta_description_length,
        robots_meta=robots_meta,
        canonical=canonical,
        h1_tags=h1_tags,
        h2_tags=h2_tags,
        h3_tags=h3_tags,
        h1_count=len(h1_tags),
        h2_count=len(h2_tags),
        h3_count=len(h3_tags),
        word_count=word_count,
        total_images=total_images,
        images_missing_alt=images_missing_alt,
        internal_links=internal_links,
        external_links=external_links,
        internal_count=len(internal_links),
        external_count=len(external_links),
        schema_found=schema_found,
        og_title=og_title,
        og_description=og_description,
    )