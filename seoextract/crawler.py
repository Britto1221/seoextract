import time
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "SEOExtractHF/1.0 (+https://github.com/Britto1221/seoextracthf)"}
TIMEOUT = 10


def _base(url: str) -> str:
    parsed = urlparse(url if urlparse(url).scheme else f"https://{url}")
    return f"{parsed.scheme}://{parsed.netloc}"


def _load_robots(base_url: str) -> RobotFileParser | None:
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        if requests.get(robots_url, headers=HEADERS, timeout=5).status_code != 200:
            return None
        parser = RobotFileParser(robots_url)
        parser.read()
        return parser
    except Exception:
        return None


def fetch_page(url: str, session: requests.Session) -> dict:
    try:
        start = time.time()
        response = session.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        html = response.text if "text/html" in response.headers.get("Content-Type", "") else ""
        return {
            "url": url,
            "final_url": response.url,
            "status_code": response.status_code,
            "html": html,
            "response_time_ms": round((time.time() - start) * 1000, 2),
        }
    except requests.exceptions.Timeout as e:
        return {"url": url, "final_url": url, "status_code": 408, "html": "", "response_time_ms": 0.0, "error": str(e)}
    except requests.exceptions.TooManyRedirects:
        code = 310
    except requests.exceptions.ConnectionError:
        code = 0
    except Exception:
        code = 0
    return {"url": url, "final_url": url, "status_code": code, "html": "", "response_time_ms": 0.0}


def _extract_internal_links(html: str, base_url: str) -> list[str]:
    base_domain = urlparse(base_url).netloc
    links = []
    for tag in BeautifulSoup(html, "lxml").find_all("a", href=True):
        href = tag["href"].strip()
        if not href or href.startswith(("#", "mailto:", "tel:")):
            continue
        parsed = urlparse(urljoin(base_url, href))
        if parsed.scheme in {"http", "https"} and parsed.netloc == base_domain:
            links.append(parsed._replace(fragment="").geturl())
    return list(dict.fromkeys(links))


def crawl(seed_url: str, max_pages: int = 20) -> list[dict]:
    seed_url = seed_url if urlparse(seed_url).scheme else f"https://{seed_url}"
    base_url = _base(seed_url)
    robots = _load_robots(base_url)
    visited, queue, results = set(), [seed_url], []

    with requests.Session() as session:
        while queue and len(results) < max_pages:
            url = queue.pop(0)
            if url in visited:
                continue
            visited.add(url)
            if robots and not robots.can_fetch(HEADERS["User-Agent"], url):
                continue

            result = fetch_page(url, session)
            results.append(result)
            if result["status_code"] == 200 and result["html"]:
                queue.extend(link for link in _extract_internal_links(result["html"], base_url) if link not in visited and link not in queue)
    return results
