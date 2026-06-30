import json
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from .models import PageData


def _content(soup: BeautifulSoup, selector: dict) -> str | None:
    tag = soup.find("meta", attrs=selector)
    return tag["content"].strip() if tag and tag.get("content") else None


def _meta(name: str) -> dict:
    return {"name": lambda n: n and n.lower() == name}


def _unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def parse(fetch_result: dict) -> PageData:
    url = fetch_result["url"]
    final_url = fetch_result.get("final_url", url)
    page = {
        "url": url,
        "final_url": final_url,
        "status_code": fetch_result["status_code"],
        "response_time_ms": fetch_result["response_time_ms"],
    }
    if not fetch_result.get("html"):
        return PageData(**page)

    soup = BeautifulSoup(fetch_result["html"], "lxml")
    title = soup.title.get_text(strip=True) if soup.title else None
    meta_description = _content(soup, _meta("description"))
    robots_meta = _content(soup, _meta("robots"))
    viewport = _content(soup, _meta("viewport"))
    canonical_tag = soup.find("link", attrs={"rel": lambda r: r and "canonical" in r})
    canonical = canonical_tag["href"].strip() if canonical_tag and canonical_tag.get("href") else None

    h1_tags = [tag.get_text(strip=True) for tag in soup.find_all("h1")]
    h2_tags = [tag.get_text(strip=True) for tag in soup.find_all("h2")]
    h3_tags = [tag.get_text(strip=True) for tag in soup.find_all("h3")]

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    base_domain = urlparse(final_url).netloc
    internal_links, external_links = [], []
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if not href or href.startswith(("#", "mailto:", "tel:")):
            continue
        full_url = urljoin(final_url, href)
        (internal_links if urlparse(full_url).netloc == base_domain else external_links).append(full_url)

    images = soup.find_all("img")
    schema_found = any(
        json.loads(tag.string or "null")
        for tag in soup.find_all("script", attrs={"type": "application/ld+json"})
        if tag.string
    )

    return PageData(
        **page,
        title=title,
        title_length=len(title or ""),
        meta_description=meta_description,
        meta_description_length=len(meta_description or ""),
        robots_meta=robots_meta,
        viewport=viewport,
        canonical=canonical,
        h1_tags=h1_tags,
        h2_tags=h2_tags,
        h3_tags=h3_tags,
        h1_count=len(h1_tags),
        h2_count=len(h2_tags),
        h3_count=len(h3_tags),
        word_count=len(soup.get_text(separator=" ", strip=True).split()),
        total_images=len(images),
        images_missing_alt=sum(not img.get("alt", "").strip() for img in images),
        internal_links=_unique(internal_links),
        external_links=_unique(external_links),
        internal_count=len(_unique(internal_links)),
        external_count=len(_unique(external_links)),
        schema_found=schema_found,
        og_title=_content(soup, {"property": "og:title"}),
        og_description=_content(soup, {"property": "og:description"}),
    )
