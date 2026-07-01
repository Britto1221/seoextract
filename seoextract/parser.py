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
        "status_code": fetch_result.get("status_code", 0),
        "response_time_ms": fetch_result.get("response_time_ms", 0),
    }

    if not fetch_result.get("html"):
        return PageData(**page)

    soup = BeautifulSoup(fetch_result["html"], "lxml")

    title = soup.title.get_text(strip=True) if soup.title else None
    meta_description = _content(soup, _meta("description"))
    robots_meta = _content(soup, _meta("robots"))
    viewport = _content(soup, _meta("viewport"))

    canonical_tag = soup.find("link", attrs={"rel": lambda r: r and "canonical" in r})
    canonical = (
        canonical_tag["href"].strip()
        if canonical_tag and canonical_tag.get("href")
        else None
    )

    h1_tags = [tag.get_text(strip=True) for tag in soup.find_all("h1")]
    h2_tags = [tag.get_text(strip=True) for tag in soup.find_all("h2")]
    h3_tags = [tag.get_text(strip=True) for tag in soup.find_all("h3")]
    h4_tags = [tag.get_text(strip=True) for tag in soup.find_all("h4")]
    h5_tags = [tag.get_text(strip=True) for tag in soup.find_all("h5")]
    h6_tags = [tag.get_text(strip=True) for tag in soup.find_all("h6")]

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    page_text = soup.get_text(separator=" ", strip=True)

    base_domain = urlparse(final_url).netloc
    internal_links, external_links = [], []

    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()

        if not href or href.startswith(("#", "mailto:", "tel:")):
            continue

        full_url = urljoin(final_url, href)

        if urlparse(full_url).netloc == base_domain:
            internal_links.append(full_url)
        else:
            external_links.append(full_url)

    image_tags = soup.find_all("img")

    image_data = [
        {
            "src": urljoin(final_url, img.get("src", "")),
            "alt": img.get("alt", "").strip(),
            "filename": img.get("src", "").split("/")[-1],
        }
        for img in image_tags
        if img.get("src")
    ]

    schema_found = bool(
        soup.find_all("script", attrs={"type": "application/ld+json"})
    )

    return PageData(
        **page,
        title=title,
        title_length=len(title or ""),
        text=page_text,
        meta_description=meta_description,
        meta_description_length=len(meta_description or ""),
        robots_meta=robots_meta,
        viewport=viewport,
        canonical=canonical,
        h1_tags=h1_tags,
        h2_tags=h2_tags,
        h3_tags=h3_tags,
        h4_tags=h4_tags,
        h5_tags=h5_tags,
        h6_tags=h6_tags,
        h1_count=len(h1_tags),
        h2_count=len(h2_tags),
        h3_count=len(h3_tags),
        h4_count=len(h4_tags),
        h5_count=len(h5_tags),
        h6_count=len(h6_tags),
        word_count=len(page_text.split()),
        total_images=len(image_tags),
        images_missing_alt=sum(not img.get("alt", "").strip() for img in image_tags),
        images=image_data,
        internal_links=_unique(internal_links),
        external_links=_unique(external_links),
        internal_count=len(_unique(internal_links)),
        external_count=len(_unique(external_links)),
        schema_found=schema_found,
        og_title=_content(soup, {"property": "og:title"}),
        og_description=_content(soup, {"property": "og:description"}),
    )