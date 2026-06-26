import time
import requests
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "SEOExtractHF/1.0 (SEO Audit Bot; +https://github.com/Britto1221/seoextracthf)"
}

TIMEOUT = 10  # seconds per request


# ── Robots.txt Checker ────────────────────────────────────────────────────────

def _load_robots(base_url: str) -> RobotFileParser | None:
    """
    Returns a RobotFileParser if robots.txt is reachable and returns 200.
    Returns None if unreachable or blocked — caller treats None as allow-all.
    """
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        resp = requests.get(robots_url, headers=HEADERS, timeout=5)
        if resp.status_code != 200:
            return None   # can't read robots.txt → allow everything
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp
    except Exception:
        return None


# ── Single Page Fetch ─────────────────────────────────────────────────────────

def fetch_page(url: str, session: requests.Session) -> dict:
    """
    Fetch a single URL.
    Returns: { url, status_code, html, response_time_ms, final_url }
    On failure returns status_code 0 and empty html.
    """
    try:
        start = time.time()
        response = session.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        elapsed = (time.time() - start) * 1000  # ms

        content_type = response.headers.get("Content-Type", "")
        html = response.text if "text/html" in content_type else ""

        return {
            "url"             : url,
            "final_url"       : response.url,
            "status_code"     : response.status_code,
            "html"            : html,
            "response_time_ms": round(elapsed, 2),
        }

    except requests.exceptions.Timeout as e:
        return {
            "url": url,
            "final_url": url,
            "status_code": 408,
            "html": "",
            "response_time_ms": 0.0,
            "error": str(e),
        }
    except requests.exceptions.TooManyRedirects:
        return {"url": url, "final_url": url, "status_code": 310, "html": "", "response_time_ms": 0.0}
    except requests.exceptions.ConnectionError:
        return {"url": url, "final_url": url, "status_code": 0,   "html": "", "response_time_ms": 0.0}
    except Exception:
        return {"url": url, "final_url": url, "status_code": 0,   "html": "", "response_time_ms": 0.0}


# ── Internal Link Extractor ───────────────────────────────────────────────────

def _extract_internal_links(html: str, base_url: str) -> list[str]:
    """Extract all internal hrefs from a page's HTML."""
    soup = BeautifulSoup(html, "lxml")
    base_domain = urlparse(base_url).netloc
    links = []

    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue

        full_url = urljoin(base_url, href)
        parsed   = urlparse(full_url)

        # Keep only http/https same-domain links
        if parsed.scheme in ("http", "https") and parsed.netloc == base_domain:
            # Normalize: remove fragment
            clean = parsed._replace(fragment="").geturl()
            links.append(clean)

    return list(set(links))


# ── BFS Crawler ───────────────────────────────────────────────────────────────

def crawl(seed_url: str, max_pages: int = 20) -> list[dict]:
    """
    BFS crawl starting from seed_url.
    Returns list of fetch results (one dict per page).
    Respects robots.txt and max_pages cap.
    """
    # Normalize seed
    parsed_seed = urlparse(seed_url)

    if not parsed_seed.scheme:
        seed_url = "https://" + seed_url

    parsed_seed = urlparse(seed_url)
    base_url = f"{parsed_seed.scheme}://{parsed_seed.netloc}"

    robots    = _load_robots(base_url)
    session   = requests.Session()
    visited   = set()
    queue     = [seed_url]
    results   = []

    while queue and len(results) < max_pages:
        url = queue.pop(0)

        # Skip already visited
        if url in visited:
            continue
        visited.add(url)

        # Respect robots.txt (None means unreachable → allow all)
        if robots is not None and not robots.can_fetch(HEADERS["User-Agent"], url):
            continue

        # Fetch the page
        result = fetch_page(url, session)
        results.append(result)

        # Only follow links from successful HTML pages
        if result["status_code"] == 200 and result["html"]:
            new_links = _extract_internal_links(result["html"], base_url)
            for link in new_links:
                if link not in visited and link not in queue:
                    queue.append(link)

    session.close()
    return results